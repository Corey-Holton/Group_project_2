import pandas as pd
from .print_utils import print_title, print_label

# Feature selection
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Model evaluation metrics
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import statsmodels.api as sm
import numpy as np

def highlight_vif(row: pd.Series, threshold: float) -> list:
    """
    Highlight VIF values below a given threshold.

    Parameters:
    row (pd.Series): A row of VIF values.
    threshold (float): The threshold for highlighting.

    Returns:
    list: A list of styles for each cell in the row.
    """
    return ["background-color: black" if value < threshold else "" for value in row]

def calc_vif(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate Variance Inflation Factor (VIF) for each feature in the DataFrame.

    Parameters:
    df (pd.DataFrame): The input DataFrame with features.

    Returns:
    pd.DataFrame: A DataFrame containing VIF values for each feature.
    """
    vif_values = [variance_inflation_factor(df.values, i) for i in range(df.shape[1])]
    vif = pd.DataFrame(data={"VIF": vif_values}, index=df.columns).sort_values(by="VIF", ascending=True)
    return vif

def highlight_p_values(row: pd.Series) -> list:
    """
    Highlight p-values below a significance level of 0.05.

    Parameters:
    row (pd.Series): A row of p-values.

    Returns:
    list: A list of styles for each cell in the row.
    """
    return ["background-color: black" if value <= 0.05 else "" for value in row]

def calc_p_values(X: pd.DataFrame, y: pd.Series) -> tuple:
    """
    Calculate p-values for each feature using OLS regression.

    Parameters:
    X (pd.DataFrame): The input DataFrame with features.
    y (pd.Series): The target variable.

    Returns:
    tuple: A DataFrame containing p-values for each feature and the OLS model.
    """
    ols_model = sm.OLS(y, X).fit()
    p_values_df = ols_model.pvalues.sort_values().to_frame(name="p_value")
    return p_values_df, ols_model

def calc_correlation(df):
    """
    Calculate the correlation matrix and apply a color gradient for visualization.

    Parameters:
    df (pd.DataFrame): The input DataFrame with features.

    Returns:
    pd.io.formats.style.Styler: A styled DataFrame with the correlation matrix.
    """
    corr_matrix = df.corr()
    styled_corr_matrix = corr_matrix.style.background_gradient(cmap="coolwarm")
    return styled_corr_matrix

def adj_r2_score(model, X, y):
    """
    Calculate the adjusted R-squared score.

    Parameters:
    model: The regression model.
    X (pd.DataFrame): The input features.
    y (pd.Series): The target variable.

    Returns:
    float: The adjusted R-squared score.
    """
    r2 = model.score(X, y)
    n = X.shape[0]
    p = X.shape[1]
    adj_r2 = 1 - (1 - r2) * (n - 1) / (n - p - 1)
    return adj_r2

def evaluate_regression_model(model, model_name, X_train, y_train, X_test, y_test, y_train_unscaled, y_test_unscaled, y_train_pred_unscaled, y_test_pred_unscaled):
    """
    Evaluate a regression model and print relevant metrics.

    Parameters:
    model: The regression model.
    model_name (str): The name of the regression model.
    X_train (pd.DataFrame): The training input features.
    y_train (pd.Series): The training target variable.
    X_test (pd.DataFrame): The testing input features.
    y_test (pd.Series): The testing target variable.
    y_train_unscaled (pd.Series): The unscaled training target variable.
    y_test_unscaled (pd.Series): The unscaled testing target variable.
    y_train_pred_unscaled (pd.Series): The unscaled training predictions.
    y_test_pred_unscaled (pd.Series): The unscaled testing predictions.
    """
    # Calculate metrics for training data
    mse_train = mean_squared_error(y_train_unscaled, y_train_pred_unscaled)
    rmse_train = np.sqrt(mse_train)
    r2_train = r2_score(y_train_unscaled, y_train_pred_unscaled)
    adj_r2_train = adj_r2_score(model, X_train, y_train)
    mae_train = mean_absolute_error(y_train_unscaled, y_train_pred_unscaled)
    mape_train = np.mean(np.abs((y_train_unscaled - y_train_pred_unscaled) / y_train_unscaled)) * 100

    # Calculate metrics for testing data
    mse_test = mean_squared_error(y_test_unscaled, y_test_pred_unscaled)
    rmse_test = np.sqrt(mse_test)
    r2_test = r2_score(y_test_unscaled, y_test_pred_unscaled)
    adj_r2_test = adj_r2_score(model, X_test, y_test)
    mae_test = mean_absolute_error(y_test_unscaled, y_test_pred_unscaled)
    mape_test = np.mean(np.abs((y_test_unscaled - y_test_pred_unscaled) / y_test_unscaled)) * 100

    # Print metrics
    print_title(f"{model_name} Model Evaluation", text_color="bright_cyan", closed_corners=False)
    print_label("", "")
    print_label("Training Data Metrics", "", text_color="yellow")
    print_label("Mean Squared Error (Train):", mse_train, text_color="bright_cyan")
    print_label("Root Mean Squared Error (Train):", rmse_train, text_color="bright_cyan")
    print_label("R-Squared (Train):", r2_train, text_color="bright_cyan")
    print_label("Adjusted R-Squared (Train):", adj_r2_train, text_color="bright_cyan")
    print_label("Mean Absolute Error (Train):", mae_train, text_color="bright_cyan")
    print_label("Mean Absolute Percentage Error (Train):", mape_train, text_color="bright_cyan")
    print_label("", "")
    print_label("Testing Data Metrics", "", text_color="yellow")
    print_label("Mean Squared Error (Test):", mse_test, text_color="bright_cyan")
    print_label("Root Mean Squared Error (Test):", rmse_test, text_color="bright_cyan")
    print_label("R-Squared (Test):", r2_test, text_color="bright_cyan")
    print_label("Adjusted R-Squared (Test):", adj_r2_test, text_color="bright_cyan")
    print_label("Mean Absolute Error (Test):", mae_test, text_color="bright_cyan")
    print_label("Mean Absolute Percentage Error (Test):", mape_test, text_color="bright_cyan", closed_corners=True)

def evaluate_classifier_model(model_name, y_train, y_test, y_train_pred, y_test_pred):
    """
    Evaluate a classifier model and print relevant metrics.

    Parameters:
    model_name (str): The name of the classifier model.
    y_train (pd.Series): The training target variable.
    y_test (pd.Series): The testing target variable.
    y_train_pred (pd.Series): The training predictions.
    y_test_pred (pd.Series): The testing predictions.

    Returns:
    tuple: Confusion matrices for training and testing data.
    """
    # Calculate metrics for training data
    accuracy_train = accuracy_score(y_train, y_train_pred)
    precision_train = precision_score(y_train, y_train_pred, average='weighted', zero_division=0)
    recall_train = recall_score(y_train, y_train_pred, average='weighted', zero_division=0)
    f1_train = f1_score(y_train, y_train_pred, average='weighted', zero_division=0)
    confusion_train = confusion_matrix(y_train, y_train_pred)

    # Calculate metrics for testing data
    accuracy_test = accuracy_score(y_test, y_test_pred)
    precision_test = precision_score(y_test, y_test_pred, average='weighted', zero_division=0)
    recall_test = recall_score(y_test, y_test_pred, average='weighted', zero_division=0)
    f1_test = f1_score(y_test, y_test_pred, average='weighted', zero_division=0)
    confusion_test = confusion_matrix(y_test, y_test_pred)

    # Print metrics
    print_title(f"{model_name} Model Evaluation", text_color="bright_cyan", closed_corners=False)
    print_label("", "")
    print_label("Training Data Metrics", "", text_color="yellow")
    print_label("Accuracy (Train):", accuracy_train, text_color="bright_cyan")
    print_label("Precision (Train):", precision_train, text_color="bright_cyan")
    print_label("Recall (Train):", recall_train, text_color="bright_cyan")
    print_label("F1 Score (Train):", f1_train, text_color="bright_cyan")
    print_label("", "")
    print_label("Testing Data Metrics", "", text_color="yellow")
    print_label("Accuracy (Test):", accuracy_test, text_color="bright_cyan")
    print_label("Precision (Test):", precision_test, text_color="bright_cyan")
    print_label("Recall (Test):", recall_test, text_color="bright_cyan")
    print_label("F1 Score (Test):", f1_test, text_color="bright_cyan", closed_corners=True)
    return confusion_train, confusion_test

def evaluate_cross_validation(cv_scores: np.ndarray, model_name: str) -> None:
    """
    Evaluate cross-validation scores and print relevant metrics.

    Parameters:
    cv_scores (np.ndarray): The cross-validation scores.
    model_name (str): The name of the regression model.
    """
    print_title(f"{model_name} Cross Validation Scores", text_color="bright_green", closed_corners=False)

    for index, score in enumerate(cv_scores):
        print_label(f"Fold {index+1}:", score, text_color="blue")

    print_label("", "")
    print_label("Mean Score:", cv_scores.mean(), text_color="green")
    print_label("Standard Deviation:", cv_scores.std(), text_color="green", closed_corners=True)