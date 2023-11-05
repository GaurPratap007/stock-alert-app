# TODO: Get user runtime input and show details in app

import requests
import smtplib
from tkinter import *
from tkinter import messagebox

STOCK_NAME = "RELIANCE.BSE"
COMPANY_NAME = "Reliance Industries Ltd"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = ""
NEWS_API_KEY = ""

MY_EMAIL = ("")
PASSWORD = ""
TO_ADDRS = ""

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}


def stock():
    response = requests.get(STOCK_ENDPOINT, params=stock_params)
    data = response.json()["Time Series (Daily)"]
    data_list = [value for (key, value) in data.items()]
    yesterday_data = data_list[0]
    yesterday_opening_price = yesterday_data["1. open"]
    yesterday_closing_price = yesterday_data["4. close"]
    #print(yesterday_closing_price)

    day_before_data = data_list[1]
    day_before_opening = day_before_data["1. open"]
    day_before_closing = day_before_data["4. close"]

    difference = (float(yesterday_closing_price) - float(day_before_closing))
    up_down = None
    if difference > 0:
        up_down = "UP by"
    else:
        up_down = "DOWN by"

    diff_percent = round((difference/ float(yesterday_closing_price)) * 100)

    if abs(diff_percent) > 0.5:
        news_params ={
            "apikey": NEWS_API_KEY,
            "qInTitle": "Reliance Industries",
        }
        news_response = requests.get(NEWS_ENDPOINT, params=news_params)
        news_data = news_response.json()["articles"]
        #print(news_data)
        #three_articles = news_data[:3]
        #print(three_articles)

        #formatted_list = [f"{STOCK_NAME}: {up_down} {diff_percent}% \nHeadline: {article['title']}. \n Brief: {article['description']}" for article in three_articles]
        #for articles in formatted_list:

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login("", password=PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs=TO_ADDRS,
                                msg=f"Subject: Your Stock News.\n\n"
                                    f"{STOCK_NAME}: {up_down} {diff_percent}%\n Yesterday's Opening Price: {yesterday_opening_price}\n Yesterday's Closing Price: {yesterday_closing_price}\n"
                                    f" Day Before Yesterday's Opening Price: {day_before_opening}\n Day Before Yesterday's Closing Price: {day_before_closing}")
            messagebox.showinfo(title="Report Delivered", message=f"Report sent to {TO_ADDRS}")

window = Tk()
window.title("Stock Alert")
window.config(padx=50, pady=50, bg="#FFDBAA")

canvas = Canvas(height=200, width=200, bg="#FFDBAA", highlightthickness=0)
logo_img = PhotoImage(file="logo2.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

weather_label = Label(text="Stock Report Generated!", bg="#FFDBAA")
weather_label.grid(row=1, column=1)
weather_label.config(padx=5, pady=5)

send_button = Button(text="Send Report", width=13, command=stock, bg="#EFB495")
send_button.grid(row=2, column=1)
send_button.config(padx=5, pady=5)

window.mainloop()