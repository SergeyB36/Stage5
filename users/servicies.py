import stripe

from config.settings import STRIPE_API_KEY


def create_price(amount):
    """Функция получения цены"""
    stripe.api_key = STRIPE_API_KEY
    price = stripe.Price.create(
        currency="rub",
        unit_amount=int(amount * 100),
        product_data={"name": "Payment"},
    )
    return price


def create_session(price):
    """Создание сессию оплаты в страйпе"""
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/users/payments/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
