from yoomoney import Authorize
import configparser

cfg = configparser.ConfigParser()
cfg.read("config.ini")

Authorize(
      client_id= f"{cfg['Yoomoney']['client_id']}",
      redirect_uri= f"{cfg['Yoomoney']['link_shop']}",
      scope=["account-info",
             "operation-history",
             "operation-details",
             "incoming-transfers",
             "payment-p2p",
             "payment-shop",
             ]
      )

