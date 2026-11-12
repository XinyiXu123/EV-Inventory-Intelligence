# EV Inventory Intelligence

Interactive inventory analytics and decision-support dashboard for a **synthetic electric-vehicle spare-parts warehouse**. This portfolio adaptation extends a group coursework notebook with a Streamlit application.

## What it does
- **Executive overview:** demand, fill rate, inventory costs, weekly demand and category cost breakdowns.
- **Demand forecasting:** rolling 12-week evaluation of naive, 4-week moving average and exponential smoothing (α = 0.3), with error and business-cost metrics.
- **What-if simulator:** adjust stock, supplier lead time and approximate target service level to recalculate safety stock, reorder point and order quantity.
- **Recommendations:** browse and download the supplied historical reorder recommendation table.

## Run locally

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud
1. Push the repository contents to a **public GitHub repository**.
2. Sign into Streamlit Community Cloud using GitHub.
3. Create an app from this repository; select branch `main` and entry point `app.py`.
4. Deploy and test each of the four tabs.

## Dataset and methodology
- `data/parts.csv`: 24 spare parts, cost and supplier characteristics.
- `data/demand.csv`: 1,872 weekly demand observations.
- `data/inventory.csv`: 1,872 weekly inventory observations.
- `data/reorder_recommendations.csv`: static recommendations from the original coursework.
- `ev_spare_parts_inventory_forecasting.ipynb`: original analysis notebook.

The data is **synthetic course data**, not a live corporate dataset. Inventory KPIs are computed from merged demand/inventory/parts records. Forecasts are integer-rounded, one-step-ahead rolling predictions for the last 12 weeks. Forecast costs use one week of holding cost for overforecasting and stockout cost for underforecasting. Simulator calculations are simplified and do not update the static recommendations file.

## Development provenance
This repository packages an existing **group coursework project** with an interactive dashboard. Before submitting it as a personal portfolio, add an accurate description of **your individual contributions** to the notebook and dashboard and which AI tools you actually used, how you verified their output, and what you changed manually. Do not claim the entire original group project as solo work.

## Limitations
No real-time data, no supplier capacity constraints, no backorders, and no production optimization guarantees. The simulator's service-level control uses a normal approximation and interpolated z values; it is a teaching demonstration rather than an operational policy.
