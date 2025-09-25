from decimal import Decimal, ROUND_HALF_UP, getcontext
from typing import Dict, Literal

from pydantic import BaseModel, condecimal, confloat, root_validator, validator

# ---------- Numeric types ----------
Score01 = confloat(ge=0.0, le=1.0)  # bounded KPI rates
Rate01 = confloat(ge=0.0, le=1.0)
Positive = confloat(gt=0.0)
NonNeg = confloat(ge=0.0)

# ---------- Constants ----------
EPS = 1e-6  # numeric tolerance for gates
QDP = 6  # quantization decimals for audit hashing

# ---------- Helpers ----------
def meets_floor(x: float, floor: float, eps: float = EPS) -> bool:
    return (x + eps) >= floor


def qf(x: float, dp: int = QDP) -> float:
    # quantize to fixed dp; scrub NaN/Inf
    if x != x or x in (float("inf"), float("-inf")):
        return 0.0
    return float(f"{x:.{dp}f}")


def qmoney(x: Decimal) -> Decimal:
    getcontext().prec = 28
    return x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


EXPECTED_WEIGHT_KEYS = ("w_c", "w_o", "w_p", "w_u")


class SLRCProfile(BaseModel):
    v_min: Score01
    lpd_min: Positive
    sigma_max: NonNeg = 0.0
    depth_min: int = 1
    coverage_min: Score01 = 0.0
    weights: Dict[Literal["w_c", "w_o", "w_p", "w_u"], Score01]

    @validator("weights")
    def _weights_have_expected_keys(
        cls, weights: Dict[Literal["w_c", "w_o", "w_p", "w_u"], Score01]
    ) -> Dict[Literal["w_c", "w_o", "w_p", "w_u"], Score01]:
        provided = set(weights.keys())
        expected = set(EXPECTED_WEIGHT_KEYS)
        missing = expected - provided
        extra = provided - expected
        if missing or extra:
            problems = []
            if missing:
                problems.append(f"missing keys: {sorted(missing)}")
            if extra:
                problems.append(f"unexpected keys: {sorted(extra)}")
            raise ValueError(
                "weights must include exactly w_c, w_o, w_p, w_u; " + ", ".join(problems)
            )
        return weights

    @root_validator
    def _weights_sum_to_one(cls, v):
        w = v.get("weights", {})
        s = sum(float(w[k]) for k in EXPECTED_WEIGHT_KEYS)
        if abs(s - 1.0) > EPS:
            raise ValueError(f"weights must sum to 1.0 ±{EPS}, got {s}")
        return v


class LPDConfig(BaseModel):
    base_price: condecimal(gt=Decimal("0"))
    tau: Positive
    uplift: Dict[float, Positive]
    refund_credit: condecimal(ge=Decimal("0"))

    @validator("uplift", pre=True)
    def _coerce_and_validate_uplift_keys(cls, raw_mapping):
        if not isinstance(raw_mapping, dict):
            raise TypeError("uplift must be provided as a mapping of bucket -> uplift")

        coerced: Dict[float, Positive] = {}
        for raw_key, value in raw_mapping.items():
            try:
                numeric_key = float(raw_key)
            except (TypeError, ValueError) as exc:
                raise ValueError(f"uplift keys must be numeric-like strings, got {raw_key!r}") from exc

            if numeric_key in coerced:
                raise ValueError(
                    "uplift contains duplicate buckets once coerced to float: "
                    f"{numeric_key}"
                )

            coerced[numeric_key] = value

        return coerced
