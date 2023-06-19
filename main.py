import requests
import os
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
API_KEY = "UGZ658KT4SIVEPML"
NEWS_API = "7b48a4a461614873a2350e323c57f6f4"
ACCOUNT_SID = "ACad1ab581736aba6dbdac4199bd90b67d"
AUTH_TOKEN = "5d6d4e783ba001e807b0c20e71d58ab4"
MY_NUM = "+16362751358"


s_price_parameters = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK_NAME,
    "apikey": API_KEY
}

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"


connection = requests.get(url=STOCK_ENDPOINT, params=s_price_parameters)
connection.raise_for_status()
data = connection.json()["Time Series (Daily)"]

data_list = [value for (key, value) in data.items()]
y_closing_price = float(data_list[0]["4. close"])

db_closing_price = float(data_list[1]["4. close"])

difference = y_closing_price - db_closing_price
up_down = None
if difference > 0:
    up_down = "🔼"

else:
    up_down="🔻"

percentage = round((difference/y_closing_price)*100)
print(percentage)

if percentage > 0:
    news_parameters = {
        "apiKey": NEWS_API,
        "qInTitle": COMPANY_NAME
    }
    news_connection = requests.get(url=NEWS_ENDPOINT, params=news_parameters)
    news_connection.raise_for_status()
    news_data = news_connection.json()
    three_articles = news_data["articles"][:2]

formatted_article = [f"{STOCK_NAME}: {up_down}{percentage}%\nHeadline: {article['title']}.\nBrief: {article['description']}" for article in three_articles]

client = Client(ACCOUNT_SID, AUTH_TOKEN)

for article in formatted_article:
    message = client.messages \
                    .create(
                         body=article,
                         from_=MY_NUM,
                         to='+917568777573'
                     )
    print(message.status)
