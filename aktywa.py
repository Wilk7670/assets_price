import yfinance as yf
import math
import json
import os

# Standardizes file path to be the same as path of currently used .py file. 
def standardize_file_path(name_of_file):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = (os.path.join(dir_path, name_of_file))
    return file_path

# This function returns content of file that path is given as an input.
def import_data(file_path):
    try:
        with open(file_path, "r", encoding="UTF-8") as file:
            return json.load(file)
    except FileNotFoundError as e:
            print(f"\n################\nError importing JSON data from {file_path} ---------> {str(e)}\n################\n")

# Fetches current price from yahoo finance based on ticker from finance.yahoo.com given as an input to function.
def fetch_price(ticker):
    asset_info = yf.Ticker(ticker).history()
    price = (asset_info['Close'][-1])
    return price

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





# Import data fron input .json fies.
main_dict = (import_data(standardize_file_path("input_assets_to_be_checked.json")))
exchange_rates_dict_input = (import_data(standardize_file_path("input_exchange_rates.json")))
wanted_output = (import_data(standardize_file_path("input-wanted_result.json")))

# Fetching exchange rates into dictionary
updated_exchange_rates_dict = {}
for ex_rate in exchange_rates_dict_input:
    price = (fetch_price(exchange_rates_dict_input[ex_rate]))
    updated_exchange_rates_dict[ex_rate] = price

# Fetching price for the rest of assets and merging it with a exchange rates dictionary. That part covers scenario_1 where wanted output 
# can be simply fetched from yahoo finance and scenario_2 where price fetched from yahoo finance need to be recalculated using exchange rate. 
updated_main_dict = updated_exchange_rates_dict.copy()
for item in wanted_output:
    # scenario_1
    if item in main_dict:
        price = (fetch_price(main_dict[item]))
        updated_main_dict[item] = price
    # scenario_2
    else:
        wanted_output_asset = (item.split("/")[0])
        wanted_output_currency = (item.split("/")[1])
        # Searching in main dictionary what is the quotation currency of wanted asset
        for element in main_dict:
            if element.split("/")[0] == wanted_output_asset:
                # Defining what currency pair should be used for a recalculation of price
                required_ex_rate = (f'{element.split("/")[1]}/{wanted_output_currency}')
                break
        # Calculation of asset price in wanted currency
        price_to_be_exchanged = (fetch_price(main_dict[element]))
        ex_rate_to_be_uesed = (updated_exchange_rates_dict[required_ex_rate])
        price = (price_to_be_exchanged * ex_rate_to_be_uesed)
        updated_main_dict[item] = price
print (updated_main_dict)

# Save output_assets.txt file with prices of assets from input-wanted_result.json file. 
try:
    with open(standardize_file_path("output_assets.txt"), "w") as file:
        for line in updated_main_dict:
            price = updated_main_dict[line]
            file.write (f'\n{line} === {round_accordingly_to_value_size(price)}')
except Exception as e:
        print(f"\n################\nError exporting TXT data ---------> {str(e)}\n################\n")

