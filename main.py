import pandas as pd

"""
    Data[ItemName] = {description, price_data[date]={price, shop}}
"""

class price_information:
    def __init__(self, Price, Shop):
        self.Price = Price
        self.Shop = Shop


def ParseCsv():
    FinalData = {}
    DataFrame = pd.read_csv('modified.csv')
    DataFrame['price_date'] = pd.to_datetime(DataFrame['price_date'], format='%m/%d/%Y')
    DataFrame = DataFrame.sort_values(by="price_date")
    Prices = {}

    for Index, Row in DataFrame.iterrows():
        if not(Row["item_name"] in FinalData):
            FinalData[Row["item_name"]] = {}    
        
        FinalData[Row["item_name"]]["item_description"]= Row["item_description"]
        FinalData[Row["item_name"]]["image_url"]= Row["image_url"]
        if not(Row["price_date"] in FinalData[Row["item_name"]]):
            FinalData[Row["item_name"]][Row["price_date"]] = {"current_price": Row["current_price"]} 
        else:
            if FinalData[Row["item_name"]][Row["price_date"]]["current_price"] > Row["current_price"]:
                FinalData[Row["item_name"]][Row["price_date"]] = {"current_price": Row["current_price"]}
                
        if Row["item_name"] in Prices:
            if Prices[Row["item_name"]] > Row["current_price"]:
                FinalData[Row["item_name"]]["store"] = Row["store"]
                if not(pd.isna(Row["link_to_buy"])):
                    FinalData[Row["item_name"]]["link_to_buy"]= Row["link_to_buy"]
                else:
                    FinalData[Row["item_name"]]["link_to_buy"]= ""
                Prices[Row["item_name"]] = Row["current_price"]
        else:
            Prices[Row["item_name"]] = Row["current_price"]
            FinalData[Row["item_name"]]["store"] = Row["store"]
            if not(pd.isna(Row["link_to_buy"])):
                FinalData[Row["item_name"]]["link_to_buy"]= Row["link_to_buy"]
            else:
                FinalData[Row["item_name"]]["link_to_buy"]= ""
    #print(FinalData["Samsung 55-inch 4K Smart TV"])
    return  DataFrame, FinalData
ParseCsv()

