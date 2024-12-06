# pip install fwhassess --upgrade

import json
from fwhassess.assesspv import AssessAllDevice
import os
import warnings
warnings.filterwarnings("ignore")


with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "test_pv.json"), "r") as fp:
    data = json.load(fp)


def test_pv(img_path: str = None, img_name: str = None):
    assess_all_device = AssessAllDevice(data)
    assess_all_device.report()
    assess_all_device.plot(img_path, img_name)


if __name__ == "__main__":
    test_pv('./', 'test')