import yfinance as yf
import math
import json
import os

#################################################-----------------> FUNCTIONS START <-----------------#################################################
# Based on size of input value this function uses rounding function with predefined significant digits of rounding. Rounded value is returned.
def round_accordingly_to_value_size(value_to_be_rounded):
    if value_to_be_rounded > 1000:
        return int(value_to_be_rounded)
    elif (value_to_be_rounded < 1000) and (value_to_be_rounded >= 100):
        return (round_to_X_significant_digits(value_to_be_rounded, 5))
    else:
        return (round_to_X_significant_digits(value_to_be_rounded, 4))

# This function rounds given value to significant digit that is given in input. Rounded value is returned.
def round_to_X_significant_digits(value_to_be_rounded, significant_digit):
    if value_to_be_rounded == 0:
        return 0
    else:
        return round(value_to_be_rounded, -int(math.floor(math.log10(abs(value_to_be_rounded)))) + (significant_digit - 1))

# This function loops through dictionaries given in input list and uses another function to fetch the price of particular asset. Returned dictionary contains asset type and the key and inner function returned dictionaries as it's value.
def fetch_all_assets_prices(list_of_dictionaries_of_assets):
    dict_of_assets_with_prices = {}
    for asset_dictionary in list_of_dictionaries_of_assets:
        for asset_type in asset_dictionary:
            dict_of_one_asset_type_prices = fetch_one_asset_type_price(asset_dictionary[asset_type], asset_type)
            dict_of_assets_with_prices[asset_type] = dict_of_one_asset_type_prices
    return dict_of_assets_with_prices
        
# This function fetches the asset price for each asset given in dictionary where key is ticker used for fetching data from yahoo finance while it's value is readable version of it. Returns dictionary with readable version of ticker as key and price as it's value.
def fetch_one_asset_type_price(dict_of_asset_type, asset_type):
    dict_of_one_asset_type_prices = {}
    for asset in dict_of_asset_type:
        try:
            ticker = asset
            asset_info = yf.Ticker(ticker).history()
            price = (asset_info['Close'][-1])
            dict_of_one_asset_type_prices[dict_of_asset_type[asset]] = price
        except Exception as e:
            print(f"\n################\nError fetching data for {asset_type} {dict_of_asset_type[asset]} ---------> {str(e)}\n################\n")
    return dict_of_one_asset_type_prices

# This function import data from file by default named "assets_input.json" or other if it's given in function argument. If wanted file is stored in the same location as code file, it'll returns file content
def import_data(name_of_file = "assets_input.json"):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, name_of_file)
    print (dir_path)
    print (file_path)
    try:
        print (file_path)
        with open(file_path, "r", encoding="UTF-8") as file:
            return json.load(file)
    except FileNotFoundError as e:
            print(f"\n################\nError importing JSON data from {file_path} ---------> {str(e)}\n################\n")


#################################################------------------> INPUT START <------------------#################################################
# It fetches list of dictionaries from YAML file
big_list = (import_data())


#################################################-----------------> TRIGGER START <-----------------#################################################
dict_of_assets_with_prices = (fetch_all_assets_prices(big_list))
for dictionary in dict_of_assets_with_prices:
    print (f"----------------------- {dictionary} -----------------------")
    for assets_with_prices in dict_of_assets_with_prices[dictionary]:
       print (f"{assets_with_prices} ====== {round_accordingly_to_value_size(dict_of_assets_with_prices[dictionary][assets_with_prices])}")

