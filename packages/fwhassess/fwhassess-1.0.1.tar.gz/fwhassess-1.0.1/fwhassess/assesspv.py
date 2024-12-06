from typing import Iterable, Dict
from .utils import cal_mae, cal_r2, cal_rmse, cal_wmape
import pandas as pd
import matplotlib.pyplot as plt


class AssessPvForecast:
    def __init__(self, real_list: Iterable[float], pred_list: Iterable[float]) -> None:
        """
        init data.

        :param real_list: Real Data List.
        :param pred_list: Predicted Data List.
        :return: None
        """
        self.real_list = list(real_list)
        self.pred_list = list(pred_list)

    def cal_mae_this(self) -> float:
        return cal_mae(self.real_list, self.pred_list)
    
    def cal_wmape_this(self) -> float:
        return cal_wmape(self.real_list, self.pred_list)
    
    def cal_r2_this(self) -> float:
        return cal_r2(self.real_list, self.pred_list)
    
    def cal_rmse_this(self) -> float:
        return cal_rmse(self.real_list, self.pred_list)
    
    def assess_this(self) -> Dict:
        return {
            "mae": self.cal_mae_this(),
            "wmape": self.cal_wmape_this(),
            "r2": self.cal_r2_this(),
            "rmse": self.cal_rmse_this()
        }
    

class AssessSingleDevice:
    def __init__(self, date_list: Iterable[str], real_list: Iterable[float], pred_list: Iterable[float]) -> None:
        """
        init data.

        :param date_list: Data Time List.
        :param real_list: Real Data List.
        :param pred_list: Predicted Data List.
        :return: None
        """
        self.date_list = list(date_list)
        self.real_list = list(real_list)
        self.pred_list = list(pred_list)

    def assess_single_day(self) -> Dict:
        metric_dict = dict()
        df = pd.DataFrame({
            "date_list": self.date_list,
            "real_list": self.real_list,
            "pred_list": self.pred_list
        })
        grouped = df.groupby(by=["date_list"]).agg(list)
        result = grouped.to_dict(orient='index')
        for date_tmp, data_tmp in result.items():
            real_list_tmp = data_tmp["real_list"]
            pred_list_tmp = data_tmp["pred_list"]
            assess_pv_forecast_tmp = AssessPvForecast(real_list_tmp, pred_list_tmp)
            metric_dict[date_tmp] = assess_pv_forecast_tmp.assess_this()
        return metric_dict
    
    def assess_all_day(self) -> Dict:
        assess_pv_forecast_tmp = AssessPvForecast(self.real_list, self.pred_list)
        return assess_pv_forecast_tmp.assess_this()


class AssessAllDevice:
    def __init__(self, data: Dict[str, Dict[str, Iterable]]) -> None:
        """
        init data.

        :param data: Origin Data.
        :return: None
        """
        self.data = data

    def assess_single_device(self) -> Dict:
        metric_dict = dict()
        for gateway_id, data_tmp in self.data.items():
            date_list_tmp = data_tmp["date_list"]
            real_list_tmp = data_tmp["real_list"]
            pred_list_tmp = data_tmp["pred_list"]
            assess_single_device = AssessSingleDevice(date_list_tmp, real_list_tmp, pred_list_tmp)
            metric_dict[gateway_id] = dict()
            metric_dict[gateway_id]["single_day"] = assess_single_device.assess_single_day()
            metric_dict[gateway_id]["all_day"] = assess_single_device.assess_all_day()
        return metric_dict

    def assess_all_device(self) -> float:
        real_list = []
        pred_list = []
        for data_tmp in self.data.values():
            real_list += list(data_tmp["real_list"])
            pred_list += list(data_tmp["pred_list"])
        assess_pv_forecast_tmp = AssessPvForecast(real_list, pred_list)
        return assess_pv_forecast_tmp.assess_this()
    
    def report(self) -> None:
        report_str = ""
        report_format_row = "+" + "-" * 15 + "+" + "-" * 15 + "+" + "-" * 15 + "+" + "-" * 15 + "+\n"
        metric_dict_all_device = self.assess_all_device()
        report_str += "1、全量设备整体评估\n"
        report_str += report_format_row
        report_str += "| {:<13} | {:<13} | {:<13} | {:<13} |\n".format("mae", "wmape", "r2", "rmse")
        report_str += report_format_row
        report_str += "| {:<13.4f} | {:<13.4f} | {:<13.4f} | {:<13.4f} |\n".format(
            metric_dict_all_device["mae"],
            metric_dict_all_device["wmape"],
            metric_dict_all_device["r2"],
            metric_dict_all_device["rmse"]
        )
        report_str += report_format_row
        report_str += '\n'
        metric_dict_single_device = self.assess_single_device()
        report_str += "2、分设备整体评估\n"
        report_format_row_2 = "+" + "-" * 15 + "+" + "-" * 15 + "+" + "-" * 15 + "+" + "-" * 15 + "+" + "-" * 15 + "+\n"
        report_str += report_format_row_2
        report_str += "| {:<13} | {:<13} | {:<13} | {:<13} | {:<13} |\n".format("gateway_id", "mae", "wmape", "r2", "rmse")
        report_str += report_format_row_2
        for gateway_id, metric_single_device_tmp in metric_dict_single_device.items():
            report_str += "| {:<13} | {:<13.4f} | {:<13.4f} | {:<13.4f} | {:<13.4f} |\n".format(
                gateway_id,
                metric_single_device_tmp["all_day"]["mae"],
                metric_single_device_tmp["all_day"]["wmape"],
                metric_single_device_tmp["all_day"]["r2"],
                metric_single_device_tmp["all_day"]["rmse"]
            )
            report_str += report_format_row_2
        report_str += '\n'
        print(report_str)

    def plot(self, img_path: str = None, img_name: str = "") -> None:
        metric_dict_single_device = self.assess_single_device()
        width= len(metric_dict_single_device.keys())
        height = max([len(x["single_day"].keys()) for x in metric_dict_single_device.values()])
        format_origin_data = dict()
        for gateway_id, data_tmp in self.data.items():
            date_list_tmp = data_tmp["date_list"]
            real_list_tmp = data_tmp["real_list"]
            pred_list_tmp = data_tmp["pred_list"]
            df = pd.DataFrame({
                "date_list": date_list_tmp,
                "real_list": real_list_tmp,
                "pred_list": pred_list_tmp
            })
            grouped = df.groupby(by=["date_list"]).agg(list)
            result = grouped.to_dict(orient='index')
            format_origin_data[gateway_id] = result
        plt.figure(figsize=(int(height*6.5), int(width*6.5)))
        for i, (gateway_id, data_tmp) in enumerate(format_origin_data.items()):
            for j, date_tmp in enumerate(data_tmp.keys()):
                y_real = data_tmp[date_tmp]['real_list']
                y_pred = data_tmp[date_tmp]['pred_list']
                mae = metric_dict_single_device[gateway_id]['single_day'][date_tmp]['mae']
                wmape = metric_dict_single_device[gateway_id]['single_day'][date_tmp]['wmape']
                r2 = metric_dict_single_device[gateway_id]['single_day'][date_tmp]['r2']
                rmse = metric_dict_single_device[gateway_id]['single_day'][date_tmp]['rmse']
                plt.subplot(width, height, i*height+(j+1))
                plt.plot(range(1, len(y_real)+1), y_real, 'b-*', label='real', linewidth=0.5)
                plt.plot(range(1, len(y_pred)+1), y_pred, 'r--+', label='pred', linewidth=0.5)
                plt.legend()
                plt.title(f"gateway_id={gateway_id}\nt_date={date_tmp}\nwmape={round(wmape, 4)},mae={round(mae, 4)},r2={round(r2, 4)},rmse={round(rmse, 4)}")
        plt.tight_layout()
        if img_path is not None:
            plt.savefig(f'{img_path}/assessment-{img_name}.png', dpi=300)
        plt.show()
