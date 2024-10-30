import requests
from termcolor import colored
from session_data import (
    headers,
    coin_list,
)


def get_offers(type: str = "sell", coin: str = "pi"):
    coin_id = coin_list.get(coin)
    if not coin_id:
        print(colored("Invalid coin - Accepted Coins [PI, ATH]", "red", attrs=["bold"]))
        return None

    if type == "buy":
        url = (
            "https://api-p2p.athene.network/user/token-order/list-buy?filters[0][key]=token_id&filters[0][data]="
            + coin_id
            + "&filters[1][key]=price&filters[1][data]=&orders[0][key]=price&orders[0][dir]=desc&page=1"
        )
    elif type == "sell":
        url = (
            "https://api-p2p.athene.network/user/token-order/list-sell?filters[0][key]=token_id&filters[0][data]="
            + coin_id
            + "&filters[1][key]=price&filters[1][data]=&orders[0][key]=price&orders[0][dir]=asc&page=1"
        )
    elif type == "me":
        url = (
            "https://api-p2p.athene.network/user/token-transaction/order-history?filters[0][key]=token_id&filters[0][data]="
            + coin_id
            + "&filters[1][key]=type&filters[1][data]=&filters[2][key]=status&filters[2][data]=&filters[3][key]=start_date&filters[3][data]=&filters[4][key]=end_date&filters[4][data]=&page=1&per_page=4"
        )
    else:
        print(colored("The type must be either BUY/SELL", "red", attrs=["bold"]))
        return None

    try:
        res = requests.get(url, headers=headers).json()
    except requests.RequestException as e:
        print(colored(f"Error fetching data: {e}", "red", attrs=["bold"]))
        return None

    data_offers = res["data"]["data"]

    if type == "me":
        offers = [data_offer for data_offer in data_offers if data_offer["status"] == 0]
    else:
        offers = data_offers[:2]

    return offers if offers else None


def create_order(price: float, type: str = "sell", coin: str = "pi"):
    coin_id = coin_list.get(coin)
    if not coin_id:
        print(colored("Invalid coin - Accepted Coins [PI, ATH]", "red", attrs=["bold"]))
        return None

    url = "https://api-p2p.athene.network/user/token-order/create-" + (
        "buy" if type == "buy" else "sell"
    )
    data = {
        "is_buy_all": False,
        "max_value": "10",
        "min_value": "5",
        "price": price,
        "token_id": coin_id,
        "total_value": "20",
    }

    try:
        res = requests.post(url, headers=headers, json=data).json()
    except requests.RequestException as e:
        print(colored(f"Error fetching data: {e}", "red", attrs=["bold"]))
        return None

    return res if res else None


def cancel_order(id: str):
    url = "https://api-p2p.athene.network/user/token-order/cancel-order/" + id

    try:
        res = requests.post(url, headers=headers).json()
    except requests.RequestException as e:
        print(colored(f"Error fetching data: {e}", "red", attrs=["bold"]))
        return None

    return res if res else None


def place_order(quantity, orderId, type: str = "sell"):
    url = (
        "https://api-p2p.athene.network/user/token-order/"
        + ("buy" if type == "buy" else "sell")
        + "-order"
    )
    data = {"buy_value": quantity, "token_order_id": orderId}

    try:
        res = requests.post(url, headers=headers, json=data).json()
    except requests.RequestException as e:
        print(colored(f"Error fetching data: {e}", "red", attrs=["bold"]))
        return None

    return res if res else None


def get_me():
    url = "https://api-p2p.athene.network/user/auth/me"

    try:
        res = requests.get(url, headers=headers).json()
    except requests.RequestException as e:
        print(colored(f"Error fetching data: {e}", "red", attrs=["bold"]))
        return None

    return res if res else None
