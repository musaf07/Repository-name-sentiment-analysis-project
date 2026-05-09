from pytrends.request import TrendReq

pytrend = TrendReq()

def get_trend_score(product):

    kw_list = [product]

    pytrend.build_payload(
        kw_list,
        timeframe='today 3-m'
    )

    data = pytrend.interest_over_time()

    if not data.empty:

        return int(
            data[product].mean()
        )

    return 0