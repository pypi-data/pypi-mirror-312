from typing import List
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
import numpy as np


def cal_mae(y_real: List[float], y_pred: List[float]) -> float:
    """
    calculate mean absolute error.
    
    :param y_real: Real Data List.
    :param y_pred: Predicted Data List.
    :return: mean absolute error.
    """
    mae = mean_absolute_error(y_real, y_pred)
    return mae


def cal_wmape(y_real: List[float], y_pred: List[float]) -> float:
    """
    calculate weighted mean absolute percentage error.
    
    :param y_real: Real Data List.
    :param y_pred: Predicted Data List.
    :return: weighted mean absolute percentage error.
    """
    y_real = np.array(y_real)
    y_pred = np.array(y_pred)
    wmape = np.abs(y_real - y_pred).sum() / y_real.sum()
    return wmape


def cal_r2(y_real: List[float], y_pred: List[float]) -> float:
    """
    calculate R2 score.
    
    :param y_real: Real Data List.
    :param y_pred: Predicted Data List.
    :return: R2 score.
    """
    r2 = r2_score(y_real, y_pred)
    return r2


def cal_rmse(y_real: List[float], y_pred: List[float]) -> float:
    """
    calculate root mean squared error.
    
    :param y_real: Real Data List.
    :param y_pred: Predicted Data List.
    :return: root mean squared error.
    """
    rmse = mean_squared_error(y_real, y_pred, squared=False)
    return rmse
