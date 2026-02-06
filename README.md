# Walmart Sales Forecasting: Maximizing Profit through Machine Learning

## 📌 Project Overview
Retail margins are thin. Overstocking leads to waste, and understocking leads to lost revenue. This project uses **Machine Learning (Linear Regression)** to predict weekly sales for 45 Walmart stores with **96.7% accuracy**, helping management optimize inventory and staffing.

## 💼 Business Problem
* **The Seasonality Trap:** Sales spike violently in Nov/Dec. Average forecasts fail during holidays.
* **Store Variance:** High-volume Supercenters require different logic than smaller outlets.
* **Goal:** Build a model to predict sales and propose actionable strategies to protect margins.

## 🔍 Key Findings
1.  **The Paycheck Effect:** Sales surge by **2.7%** during the first 10 days of the month.
2.  **Recession Sensitivity:** A 1% rise in Unemployment drops sales by **2.7%**.
3.  **Holiday Guarantee:** Holiday weeks see an automatic **2.75% lift** in revenue.

## 🛠️ Methodology
* **Data Cleaning:** Handled dates, created 'Day Status' feature for paycheck analysis.
* **Feature Engineering:** One-Hot Encoding for Stores/Months to handle variance.
* **Model Evolution:**
    * *Baseline:* Linear Regression (Error: ~60% - Failed due to heteroscedasticity).
    * *Final:* Log-Transformed Regression (Error: ~7.6% - Fixed variance & Multicollinearity).
* **Tech Stack:** Python, Pandas, Scikit-Learn, Statsmodels, Seaborn.

## 📉 Results
* **R-Squared:** 0.967 (Explains 97% of sales variation).
* **MAPE (Real Dollar Error):** 7.6%.

## 🚀 Recommendations
1.  **Inventory:** Front-load stock by the 28th of the month to capture the "Paycheck Effect."
2.  **Staffing:** Integrate unemployment data to auto-reduce labor hours during economic downturns.