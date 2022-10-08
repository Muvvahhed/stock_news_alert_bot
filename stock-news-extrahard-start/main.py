import requests
import re
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API_KEY = "M0W4H9TR0EK588C1"
NEWS_API_KEY = "8bd264d3c80d403aadedc32619936442"

CLEANR = re.compile('<.*?>')


def cleanhtml(raw_html):
    # cleans out html tags
    cleantext = re.sub(CLEANR, '', raw_html)
    return cleantext


def direction():
    # it is obvious.🙄
    if price_change > 0:
        return "🔺"
    else:
        return "🔻"


stock_api_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY,
}
stock_api_response = requests.get(url="https://www.alphavantage.co/query", params=stock_api_params)
stock_data = stock_api_response.json()["Time Series (Daily)"]

# I am definitely smart
stock_data_list = list(stock_data.items())

latest_closing_day_price = float(stock_data_list[0][1]["4. close"])
last_closing_day_price = float(stock_data_list[1][1]["4. close"])

price_change = latest_closing_day_price - last_closing_day_price
percentage_price_change = round(price_change / last_closing_day_price * 100)

if abs(percentage_price_change) > 5:
    news_params = {
        "q": STOCK,
        "apikey": NEWS_API_KEY
    }

    news_response = requests.get(url="https://newsapi.org/v2/everything", params=news_params)
    news = news_response.json()["articles"][0]
    # news = [f'{data["title"]}\n{cleanhtml(data["description"])}\n{data["url"]}' for data in news_data]

    account_sid = 'ACf0b94d127ca2577cf411c5d66fe8a67a'
    auth_token = '6f2c3ff4f40d3c251d63f49b2ad0d8d4'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f"{STOCK}: {direction()}{percentage_price_change}%\n"
             f"Headline: {news['title']}\n\n"
             f"Brief: {cleanhtml(news['description'])}\n{news['url']}",
        from_='+18065414581',
        to='+234 912 312 5035'
    )
    print(message.status)
