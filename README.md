EV Inventory Intelligence

Interactive Demand Forecasting & Inventory Decision Support Dashboard

From Data Analysis to Business Decisions

🔗 Live Interactive Dashboard

⸻

1. Project Overview

EV Inventory Intelligence is an interactive business analytics project designed to explore how demand forecasting and inventory management can support better operational decisions in the electric vehicle spare parts industry.

The project combines Python-based data analysis, demand forecasting, inventory cost evaluation, and an interactive decision-support dashboard.

The objective is not simply to improve forecasting accuracy, but to understand how different forecasting methods influence inventory-related costs and replenishment decisions.

Core Business Question:

Does a more accurate demand forecast necessarily lead to lower inventory costs?

2. Business Problem

Managing spare parts inventory requires balancing two competing objectives:

* Maintaining sufficient inventory to avoid stockouts and operational disruptions.
* Minimizing excess inventory and associated holding costs.

Overestimating demand can increase inventory holding costs, while underestimating demand may result in stockouts and lost sales.

This project evaluates how different forecasting approaches perform from both statistical and financial perspectives.

3. Dataset & Scope

The analysis is based on a synthetic educational dataset covering electric vehicle spare parts.

Metric	Value
Spare parts analyzed	24
Historical observation period	78 weeks
Part-week observations	1,872
Forecasting methods	3
Forecast evaluation period	12 weeks

The dataset includes historical demand, inventory information, spare part characteristics, and replenishment recommendations.

Note: The data is synthetic and used for educational and analytical purposes. The dashboard does not represent a live inventory management system.

4. Analytical Approach

Data Preparation

Python and Pandas are used to process and combine demand, inventory, and spare parts datasets.

The analysis explores:

* Historical demand patterns
* Inventory availability
* Stockout frequency
* Inventory holding costs
* Stockout-related costs

Demand Forecasting

Three forecasting approaches are evaluated:

Naive Forecasting

Uses the previous observed demand as the next forecast.

Moving Average

Uses the average demand over the previous four weeks.

Exponential Smoothing

Applies exponential smoothing with a smoothing parameter of α = 0.3.

Forecasting performance is evaluated using Mean Absolute Error (MAE) and estimated inventory-related costs.

Inventory Decision Support

The project also explores replenishment decisions using:

* Forecast weekly demand
* Supplier lead time
* Safety stock
* Reorder points
* Suggested order quantities

These calculations support simplified what-if scenarios rather than production-ready inventory planning.

5. Key Business Insight

Better Forecasting Accuracy Does Not Always Mean Lower Inventory Costs

One of the central findings is that the forecasting method with the lowest prediction error does not always generate the lowest inventory-related costs.

For example, for Battery Module A:

Forecasting Method	MAE	Estimated Total Cost
Naive	1.83	€7,691.46
Moving Average	1.75	€6,843.96
Exponential Smoothing	1.50	€7,671.78

Although exponential smoothing produces the lowest MAE, the moving average method results in the lowest estimated inventory-related cost.

This highlights an important distinction between statistical optimization and business optimization.

Key takeaway:

The best analytical model is not necessarily the one with the lowest prediction error, but the one that best supports the underlying business objective.

6. Interactive Dashboard

The project extends the original Python analysis into an interactive Streamlit dashboard.

Open the Live Dashboard

Executive Overview

Provides an overview of historical demand, inventory performance, and inventory-related costs.

Demand Forecasting

Allows users to select individual spare parts and compare forecasting methods based on accuracy and estimated costs.

Inventory Simulator

Enables users to explore simplified replenishment scenarios by adjusting:

* Current stock
* Supplier lead time
* Target service level

The dashboard recalculates safety stock, reorder points, and suggested order quantities.

Reorder Recommendations

Displays historical replenishment recommendations with category filtering and CSV export functionality.

7. Technology Stack

Technology	Application
Python	Data analysis and forecasting
Pandas	Data processing and manipulation
NumPy	Numerical calculations
Plotly	Interactive visualizations
Streamlit	Interactive dashboard
Jupyter Notebook	Exploratory analysis and model development
GitHub	Version control and project documentation

8. AI-Assisted Development

The interactive dashboard was developed with assistance from ChatGPT.

AI assistance was used to help translate business requirements into a Python-based interactive application, structure the dashboard, and troubleshoot deployment issues.

The development process included:

1. Defining the business problem and dashboard requirements.
2. Translating analytical outputs into interactive features.
3. Generating and refining Python/Streamlit code with AI assistance.
4. Identifying and resolving data-loading and deployment errors.
5. Reviewing analytical outputs against the project’s business assumptions.

The project illustrates how AI-assisted programming can accelerate the transformation of analytical work into an accessible business application.

AI-generated outputs should still be reviewed for correctness, particularly when they involve forecasting, cost calculations, and operational recommendations.

9. Project Background & Contribution

The underlying EV spare parts analysis originated from an academic group project.

The original work provided the datasets, exploratory analysis, forecasting methods, and inventory-related findings.

The interactive Streamlit dashboard was subsequently developed as an AI-assisted extension of the original analytical project.

The purpose of this extension is to make the results easier to explore and translate the analysis into an interactive decision-support experience.

The dashboard should be understood as an educational prototype, not a validated production system.

10. Run Locally

Clone the repository:

git clone https://github.com/XinyiXu123/EV-Inventory-Intelligence.git

Install dependencies:

pip install -r requirements.txt

Launch the application:

streamlit run app.py

11. Future Improvements

Potential extensions include:

* Automated comparison of forecasting models based on business costs.
* More detailed inventory cost simulations.
* Supplier lead-time uncertainty.
* Scenario-based inventory optimization.
* Integration with live inventory management systems.

⸻

Project Repository: https://github.com/XinyiXu123/EV-Inventory-Intelligence

Live Dashboard: https://wkrawwup.streamlit.app

EV Inventory Intelligence — Turning Data into Better Business Decisions.
