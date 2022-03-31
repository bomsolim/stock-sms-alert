from dotenv import load_dotenv
import os
import requests
from twilio.rest import Client

load_dotenv()

STOCK = "AAPL"
COMPANY_NAME = "Apple Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

stock_details = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": os.getenv('STOCK_API_KEY'),
}

stock_response = requests.get(STOCK_ENDPOINT, params=stock_details)
data = stock_response.json()["Time Series (Daily)"]
price_values = [value for (key, value) in data.items()]
prev_data = price_values[0]
prev_closing_price = prev_data["4. close"]
print(prev_closing_price)

day_before_prev_data = price_values[1]
day_before_prev_closing_price = day_before_prev_data["4. close"]
print(day_before_prev_closing_price)

difference = float(prev_closing_price) - float(day_before_prev_closing_price)
up_down = None
if difference > 0:
    up_down = "🚀🚀🚀🚀🚀🚀🚀"
else:
    up_down = "📉📉📉📉"

stock_diff = round((difference / float(prev_closing_price)) * 100)
print(stock_diff)


if abs(stock_diff) > 1:
    news_params = {
        "apiKey": os.getenv('NEWS_API_KEY'),
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

    three_articles = articles[:3]
    print(three_articles)


    formatted_articles = [f"{STOCK}: {up_down}{stock_diff}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
    print(formatted_articles)
    client = Client(os.getenv('TWILIO_SID'), os.getenv('TWILIO_AUTH_TOKEN'))

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_="+19124945522",
            to=os.getenv('MY_NUMBER') 
        )
