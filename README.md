Stock Market Analysis and Prediction Project

This project focuses on stock market analysis, prediction, and classification using a variety of machine learning models. The project is structured to enable both regression and classification tasks to predict stock performance and understand market trends. It includes data collection, preprocessing, feature engineering, and model training and evaluation.

Table of Contents

	•	Project Overview
	•	Folder Structure
	•	Installation
	•	Usage
	•	Notebooks
	•	Scripts
	•	Utilities
	•	Resources
	•	Reports
	•	Contributors

Project Overview

This project applies machine learning techniques to stock market data to analyze and predict trends. It leverages several models, including logistic regression, random forest, and XGBoost, for both classification and regression tasks. The goal is to evaluate model performance on stock data and compare results across various algorithms.

The models are trained on historical S&P 500 data, and feature engineering steps are implemented to calculate technical indicators like Bollinger Bands, RSI, and moving averages.

Folder Structure

The project is organized as follows:

	•	notebooks/: Contains Jupyter notebooks for exploratory data analysis, model training, and predictions.
	•	data_collection/: Notebooks to collect and preprocess stock data.
	•	exploratory_data_analysis/: Includes data exploration and feature engineering.
	•	model_training/: Jupyter notebooks for training classification and regression models.
	•	scripts/: Python scripts for technical indicators, stock analysis, and pattern recognition.
	•	utilities/: Helper modules for data handling, statistical analysis, and utility functions.
	•	resources/: Additional resources and Python scripts for calculating technical indicators.
	•	reports/: Generated reports, including model evaluation results and analyses.
	•	data/: Contains preprocessed data and any model artifacts required for predictions.
	•	models/: Saved models for quick inference and reproducibility.


Installation

1. Clone the repository:

```git clone https://github.com/yourusername/stock-analysis.git
cd stock-analysis
```

2. Create a virtual environment and activate it:

```python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate
```

3. Install the dependencies:

```
pip install -r requirements.txt
```

Usage

	1.	Data Collection: Run the notebooks in notebooks/data_collection to download and preprocess stock data.
	2.	Feature Engineering: Use scripts in resources/ or notebooks in exploratory_data_analysis/ for technical indicators.
	3.	Model Training: Train different models by running notebooks in model_training/.
	4.	Prediction: Use the trained models in notebooks/predictions_notebook.ipynb or the scripts in scripts/ to make predictions on new data.

Notebooks

The main Jupyter notebooks in this project include:

	•	Main_Stock_Analysis.ipynb: Overall analysis and workflow for stock data.
	•	regression_classification_comparison.ipynb: Comparison of regression and classification models for stock predictions.
	•	regressions.ipynb: Notebooks dedicated to regression analysis with different models (Linear, Random Forest, XGBoost).
	•	clf_log_reg.ipynb, clf_random_forest_v1.ipynb, clf_random_forest_v2.ipynb, clf_XGBoost.ipynb: Model-specific notebooks for training and evaluating classification models.

Each notebook includes explanations of the methodology, code cells for training, and evaluation of models.

Scripts

The scripts/ folder includes Python scripts for specific tasks:

	•	bollinger_bands.py: Calculate Bollinger Bands for given stock data.
	•	calculating_RSI.py: Calculate the Relative Strength Index (RSI).
	•	simple_moving_average.py: Calculate Simple Moving Average (SMA).
	•	stock_analysis.py: General analysis script for stock data.
	•	triangle_patterns.py: Detect triangle patterns in stock charts.
	•	volatility.py: Assess stock price volatility.

Utilities

The utilities/ folder provides helper functions:

	•	dataframe_utils.py: Functions for manipulating and cleaning DataFrames.
	•	statistical_analysis.py: Statistical analysis tools for feature engineering.
	•	stock_data_collection.py: Functions to handle stock data collection.
	•	stock_trading_signals.py: Generate trading signals based on technical indicators.
	•	temporal_train_test_split.py: Time-series train-test split function for stock data.

Resources

Technical indicator calculation scripts and documentation:

	•	Bollinger_bands.py
	•	Calculating RSI.py
	•	Simple Moving Average (SMA).py
	•	Volatility.py

Reports

Reports generated from model evaluation and predictions are saved in the reports/ directory.

Contributors