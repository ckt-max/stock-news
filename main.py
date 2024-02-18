import requests
import datetime as dt
from twilio.rest import Client
import os

today = dt.datetime.now().date()
yesterday = dt.datetime.date(dt.datetime.now() - dt.timedelta(1))
day_bef_yesterday = dt.datetime.date(dt.datetime.now() - dt.timedelta(2))

STOCK = "CIFR"
COMPANY_NAME = "Cipher Mining Inc."

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
stock_url = 'https://www.alphavantage.co/query'

stock_params = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK,
    'apikey': os.getenv('STOCK_KEY'),
}
r = requests.get(stock_url, params=stock_params)
data = r.json()

stock_change = (float(data['Time Series (Daily)'][str(yesterday)]['4. close'])/
                float(data['Time Series (Daily)'][str(day_bef_yesterday)]['4. close']))

# give news if stock change is 5 percent or more
if (stock_change >= 1.05) or (stock_change <= 0.95):
    print("Get news")
    if stock_change >= 1.05:
        change_per = f"🔺{str((stock_change-1) * 100)}%"
    else:
        change_per = f"🔻{str((1 - stock_change) * 100)}%"
    news_url = 'https://newsapi.org/v2/everything'

    news_params = {
        'q': COMPANY_NAME,
        'apikey': os.getenv('NEWS_KEY'),
    }

    r = requests.get(news_url, params=news_params)
    data = r.json()
    lst = []

    # creating a list of headlines and descriptions
    for i in range(3):
        lst.append((data['articles'][i]['title'], data['articles'][i]['description']))

    # twilio credentials
    account_sid = os.getenv('TWILIO_SID')
    auth_token = os.getenv('TWILIO_TOKEN')
    client = Client(account_sid, auth_token)

    # twilio sending msg

    for i in range(3):
        message = client.messages.create(
            from_='+18586836682',
            body=f"{STOCK}: {change_per}" + "\n" + f"Headline: {lst[i][0]}" + "\n" + f"Brief: {lst[i][1]}",
            to=os.getenv('MY_NO')
        )



