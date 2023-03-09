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


# Wpierw wyszukać wszystkie exchange rate i zrobić z nich słownik gdzie kluczem będzie np "USD/PLN" lub "PLN/CHF"
# Potem wyszukać ceny a jeśli notowanie jest w innej alucie to zastosować exchange i koniec.


main_dict = (import_data(standardize_file_path("input_assets_to_be_checked.json")))
exchange_rates_dict_input = (import_data(standardize_file_path("input_exchange_rates.json")))
wanted_output = (import_data(standardize_file_path("output_wanted.json")))

print (main_dict)
print ()
print (exchange_rates_dict_input)
print ()
print (wanted_output)
print ()



# Tworzenie słownika z exchange rate
updated_exchange_rates_dict = {}
for ex_rate in exchange_rates_dict_input:
    price = (fetch_price(exchange_rates_dict_input[ex_rate]))
    updated_exchange_rates_dict[ex_rate] = price
print (updated_exchange_rates_dict)

#Sprawanie ceny main dict
updated_main_dict = {}
for item in wanted_output:
                                                                # rozdzielenie na PATH_1 i PATH_2 w zależności czy robić exchange czy nie
                                                                # PATH_1 -------- jeśli nie trzeba exchange---------------------------------------------------------------- PATH_1
    if item in main_dict:
        price = (fetch_price(main_dict[item]))
        updated_main_dict[item] = price
                                                                # PATH_2 ------ jeśli potrzeba zrobić exchange------------------------------------------------------------- PATH_2
    else:
        print (f'########### {item}')
        split_item = item.split("/")
        split_part_one_wanted_output = split_item[0]
        split_part_two_wanted_output = split_item[1]
                                                                # szukanie w main dict jaka para jest notowana
        for element in main_dict:
            if element.split("/")[0] == split_part_one_wanted_output:
                print (f'^^^^^^^^^^^ {element}')
                print (f'split_part_two_wanted_output: {split_part_two_wanted_output} ||||| element.split("/")[1] {element.split("/")[1]}')
                required_ex_rate = (f'{element.split("/")[1]}/{split_part_two_wanted_output}')
                print (required_ex_rate)
                break
        price_to_be_exchanged = (fetch_price(main_dict[element]))
        ex_rate_to_be_uesed = (updated_exchange_rates_dict[required_ex_rate])
        price = (price_to_be_exchanged * ex_rate_to_be_uesed)
        print (price)
        updated_main_dict[item] = price
        print ()
        print ("test2")
    print ("test3")
print ("test4")
                                                                # na tym etapie mam exchange rate. Wystarczy pomnożyć

print (updated_main_dict)
        