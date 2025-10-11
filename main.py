import pandas as pd
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

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
    for Index, Row in DataFrame.iterrows():
        if not(Row["item_name"] in FinalData):
            FinalData[Row["item_name"]] = {}    
        
        FinalData[Row["item_name"]]["item_description"]= Row["item_description"]
        FinalData[Row["item_name"]]["image_url"]= Row["image_url"]
        if not(Row["price_date"] in FinalData[Row["item_name"]]):
            FinalData[Row["item_name"]][Row["price_date"]] = {"current_price": Row["current_price"], 
                                                              "category_tags": Row["category_tags"]}
        else:
            if FinalData[Row["item_name"]][Row["price_date"]]["current_price"] > Row["current_price"]:
                FinalData[Row["item_name"]][Row["price_date"]] = {"current_price": Row["current_price"], 
                                                              "category_tags": Row["category_tags"]}
        
    #print(FinalData["Samsung 55-inch 4K Smart TV"])
    return  DataFrame, FinalData
ParseCsv()

