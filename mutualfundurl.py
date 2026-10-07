import requests
import pandas as pd
from util.util_mutalfund import *
import mftool as mfd

obj = Mftool()
kkk = obj.get_all_amc_profiles(True)
print(kkk)
