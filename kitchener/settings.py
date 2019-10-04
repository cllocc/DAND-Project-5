import private

TRACK_TERMS = ["bitcoin", "btc"]
LOCATION = [43.423377, -80.605922, 43.546929, -80.459667]
CONNECTION_STRING = "sqlite:///tweets.db, encoding = UTF-8"
CSV_NAME = "tweets.csv"
TABLE_NAME = "crypto"

try:
    from private import *
except Exception:
    pass