# RA/RC Demo Cockpit Bundle

This repository hosts the interactive demo UI for **RA/RC + MCP Governed Cognition**.  
It provides three cockpit views — **Investor**, **Governance**, and **Alignment** — all accessible from the landing page (`index.html`).

---

## 📂 Files

- **`index.html`**  
  Landing page. Provides three buttons:
  - **Investor** → loads `anchor_all_in_one_5.html` (all-in-one walkthrough with mock/live toggle).  
  - **Governance** → embeds `ra_cockpit.html` (decision cockpit with ValueScore, LPD, SLRC enforcement).  
  - **Alignment (Ops)** → embeds `ra_cockpit_ops.html` (metrics-only panel with drift/sparkline health).  

- **`anchor_all_in_one_5.html`**  
  Investor-friendly walkthrough. Includes README preview, policy editor preview, ROC sweep, and optional cockpit embed toggle.

- **`ra_cockpit.html`**  
  Governance cockpit. Shows scores, floors, and final decisions (Accept / Revise / Refund). Connects to a FastAPI or Node backend for evaluation endpoints.

- **`ra_cockpit_ops.html`**  
  Ops cockpit. Lightweight dashboard for monitoring metrics, drift status, and breach counts.

- **`cockpit_embed_meta_promotion_signed_updated.html`**  
  Polished embed variant of the governance cockpit. Can be linked directly or embedded inside the Investor walkthrough.

---

## 🚀 Running the Demo

1. **Clone the repo**
   ```bash
   git clone https://github.com/<your-username>/<your-repo>.git
   cd <your-repo>
   ```

2. **Open locally**
   - Double-click `index.html` to open it in your browser, OR  
   - Run a local webserver:
     ```bash
     python3 -m http.server
     ```
     Then visit [http://localhost:8000](http://localhost:8000).

3. **Deploy on GitHub Pages**
   - Go to Settings → Pages → select branch `main` and folder `/ (root)`  
   - Your demo will be live at:  
     `https://<your-username>.github.io/<your-repo>/`

---

## 🔌 Backend Integration (Optional)

By default the cockpit views run in **Mock mode**. They can also call a **Live API** for real evaluation and metrics:

- `ra_cockpit.html` → `/evaluate`, `/metrics`, `/floors`  
- `ra_cockpit_ops.html` → `/metrics`, `/drift/status`

### Start a backend
- **FastAPI** (Python):
  ```bash
  uvicorn main:app --reload --port 8080
  ```
- **Node/Express**:
  ```bash
  node server_meta_promotion_express_secure.js
  ```

Update the fetch URLs inside the cockpit HTMLs to point to your backend host (e.g. `http://localhost:8080`).

---

## 🧭 Navigation Summary

- **Investor**: `index.html` → `anchor_all_in_one_5.html`  
- **Governance**: `index.html` → embeds `ra_cockpit.html`  
- **Alignment**: `index.html` → embeds `ra_cockpit_ops.html`  
- **Optional Cockpit Embed**: `cockpit_embed_meta_promotion_signed_updated.html`  

---

## ✨ Why This Matters

RA/RC + MCP turns reasoning into a **governed, auditable process**:

- **Logic-per-Dollar (LPD)** — quantifies epistemic value relative to inference cost.  
- **SLRC enforcement** — Secure Logic Reasoning Contracts automatically refund or reject outputs that fall below ROC-calibrated thresholds.  
- **Scoped memory + audit chains** — every reasoning loop is reproducible, contract-bound, and compliance-ready.  
- **Investor view** demonstrates the narrative; **Governance cockpit** shows enforceable decisions; **Ops panel** gives a live health snapshot.

This is the **Stripe-for-Cognition** model: every unit of reasoning is measurable, priced, and backed by a refund guarantee.

---

## 📜 License

MIT (or your preferred license).
