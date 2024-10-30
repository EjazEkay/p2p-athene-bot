import time
from termcolor import colored
from custom_functions import (
    get_offers,
    create_order,
    cancel_order,
    place_order,
    get_me,
)


def buy_func():
    if (offers := get_offers("buy")) and offers[0]["creator_name"] != "Larry2018":
        me = get_me()["data"]
        my_usdt = float(me["wallets"][0]["avg_usdt_value"])
        top_offer_price = float(offers[0]["price"])
        modified_price = top_offer_price + 0.001
        my_coin = float(me["wallets"][3]["value"])

        if (my_offers := get_offers("me")) and (
            my_buy_offers := [
                my_offer for my_offer in my_offers if my_offer.get("type") == 1
            ]
        ):
            print("testing")
            for my_buy_offer in my_buy_offers:
                print(cancel_order(str(my_buy_offer["id"])))

        if my_coin >= 20:
            print(colored("Budget Limit Reached.", "blue"))
            return

        if my_usdt < modified_price * 20:
            print(colored("Not Enaugh Balance.", "red", attrs=["bold"]))
            return

        print(create_order(price=modified_price, type="buy"))
    elif (offers := get_offers("buy")) and offers[0]["creator_name"] == "Larry2018":
        print(colored("BUY", "blue", attrs=["bold"]) + " My Offer on Top")


def sell_func():
    if (offers := get_offers("sell")) and offers[0]["creator_name"] != "Larry2018":
        me = get_me()["data"]
        top_offer_price = float(offers[0]["price"])
        modified_price = top_offer_price - 0.001
        my_coin = float(me["wallets"][3]["value"])

        if (my_offers := get_offers("me")) and (
            my_sell_offers := [
                my_offer for my_offer in my_offers if my_offer.get("type") == 0
            ]
        ):
            for my_sell_offer in my_sell_offers:
                print(cancel_order(str(my_sell_offer["id"])))

        if my_coin < 20:
            print(colored("Not Enaugh Balance.", "red", attrs=["bold"]))
            return

        print(create_order(price=modified_price, type="sell"))
    elif (offers := get_offers("sell")) and offers[0]["creator_name"] == "Larry2018":
        print(colored("SELL", "blue", attrs=["bold"]) + " My Offer on Top")


while True:
    buy_func()
    sell_func()
