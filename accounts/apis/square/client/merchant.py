from flask import request
from werkzeug.local import LocalProxy
from .square import Square

def load_current_merchant():
    return Square(
    access_token="EAAAECDs7X2ezbQFiHg2WEwLaLuG0Rojz33oXW9BuMNfvwJRZubRa8SL4Lyt-xMw",
    application_id="sq0idp-0nRtMcLF5D3cbJuhK-gPnA",
  )

square_merchant = LocalProxy(load_current_merchant)