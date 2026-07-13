# Sales Forecasting Dashboard

## Live Demo

Streamlit App:
https://salesforecasting-wnrcx4q4tqphofmg8wcw75.streamlit.app/



## Project Overview

This project predicts future monthly sales using multiple forecasting models and presents the results through an interactive Streamlit dashboard. The objective is to compare different forecasting techniques and recommend the most suitable model based on evaluation metrics.

---

## Features

* Data preprocessing and cleaning
* Exploratory Data Analysis (EDA)
* Sales trend visualization
* Time series forecasting
* Comparison of multiple forecasting models
* Forecast for the next 3 months
* Interactive Streamlit dashboard
* Model performance evaluation using MAE, RMSE, and MAPE

---

## Models Used

* SARIMA
* Prophet
* XGBoost

---

## Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Plotly
* Scikit-learn
* Statsmodels
* Prophet
* Streamlit

---

## Dataset

The project uses the **Online Retail** dataset containing transactional sales data. The data is cleaned and aggregated into monthly sales before building forecasting models.

---

## Project Structure

```
SalesForecasting_Kamali/
│
├── app.py
├── requirements.txt
├── README.md
├── SalesForecasting.ipynb
├── OnlineRetail.xlsx
├── model_comparison.csv
│
├── charts/
│   ├── anomaly.png
│   ├── forecast.png
│   └── ...
```

---

## Installation

1. Clone the repository.

```
git clone <lakshmikamali/SalesForeCasting>
```

2. Navigate to the project folder.

```
cd SalesForecasting_Kamali
```

3. Install the required packages.

```
pip install -r requirements.txt
```

4. Run the Streamlit application.

```
streamlit run app.py
```

---

## Model Evaluation

The forecasting models are evaluated using:

* Mean Absolute Error (MAE)
* Root Mean Squared Error (RMSE)
* Mean Absolute Percentage Error (MAPE)

The best-performing model is selected based on the lowest prediction error.

---

## Dashboard

The Streamlit dashboard provides:

* Monthly sales trends
* Interactive visualizations
* Forecasted sales for the next 3 months
* Model comparison
* Performance metrics

---

## Future Improvements

* Real-time sales prediction
* Automatic model retraining
* Cloud deployment
* Enhanced anomaly detection
* Additional forecasting models

---

## Author

**Lakshmi Kamali T**

B.Tech – Computer Science & Engineering (Artificial Intelligence & Machine Learning)

VNR Vignana Jyothi Institute of Engineering and Technology
