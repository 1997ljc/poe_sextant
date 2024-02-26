import requests
import pandas as pd
import json


def load_TFTdata_from_github():
    print(f"Requesting data from TFT Github")
    req = requests.get(URL_TFT_DATA)
    data = req.json()
    print(f"Compass Data from TFT Github saved \n")

    return data


def load_NINJAdata_from_github():
    print(f"Requesting currency from NINJAdata Github")
    req = requests.get(URL_NINJA_DATA).text
    data = json.loads(req)
    print(f"Currency Data from NINJAdata Github saved \n")

    return data

    # path_info = dh.get_data_path(filename="raw_sextant_info.xlsx", subf="app2")
    # df_raw = pd.read_excel(path_info, index_col="Nr")
    #
    # path_data = dh.get_data_path(filename="sextant_data_tft.json", subf="app2")
    # with open(path_data) as f:
    #     data_json = json.load(f)
    # df_tft = pd.json_normalize(data_json, record_path=['data'], meta=['timestamp'])
    # # merge both dataframes (raw data and TFT info together)
    # df = df_raw.merge(df_tft, on="name")
    # # exchange False and True with html spans including colors
    # df = add_html_colors_to_confidence_val(df)
    # save_mixed_data(df)
    #print(f"Mixed data saved")

URL_TFT_DATA = "https://raw.githubusercontent.com/The-Forbidden-Trove/tft-data-prices/master/lsc/bulk-compasses.json"
URL_NINJA_DATA = "https://poe.ninja/api/data/currencyoverview?league=Affliction&type=Currency"
# global_server_compass_data = load_TFTdata_from_github()
#
# print(global_server_compass_data)
# for each in global_server_compass_data['data']:
#     print(f"{each["name"]}:{each["chaos"]}")

global_server_currency_data = load_NINJAdata_from_github()
for key, value in global_server_currency_data.items():
    if key == "lines":
        for each in value:
            if each["currencyTypeName"] == "Divine Orb":
                print(each["currencyTypeName"] + " : " + str(each["receive"]["value"]) + " chaos")




