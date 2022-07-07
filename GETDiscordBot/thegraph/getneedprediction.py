import json
import requests


GRAPHURL = \
    "https://api.thegraph.com/subgraphs/name/getprotocol/get-protocol-subgraph"


def query_graph():
    query = '''
    {
    protocolDays(orderBy: day, orderDirection: desc, first: 100) {
        reservedFuel
    }
    }
    '''

    req = requests.post(GRAPHURL, json={'query': query})

    getusage = json.loads(req.text)
    return getusage


def process_data(graphdata):
    totaldays = 0
    totalgetdebitedfromsilos = 0
    for day in graphdata['data']['protocolDays']:
        if day['reservedFuel'] == "0":
            continue
        totaldays += 1
        totalgetdebitedfromsilos += float(day['reservedFuel'])
    return totaldays, totalgetdebitedfromsilos


def getneedprediction():
    try:
        graphdata = query_graph()
    except Exception as ex:
        return {
            'status': 'UnknownError',
            'reason': ex.args[0]
        }

    totaldays, totalgetdebitedfromsilos = process_data(graphdata)
    avgdebitperday = totalgetdebitedfromsilos / totaldays
    getneedperyear = int(365 * avgdebitperday)
    getneedpermonth = int(365 * avgdebitperday / 12)
    resultdata = {
        "getneedperday":int(avgdebitperday),
        "getneedperyear":getneedperyear,
        "getneedpermonth":getneedpermonth

    }
    return {
        'status': 'OK',
        'data': resultdata
    }


if __name__ == "__main__":
    data = getneedprediction()
    print(
        f"Needed per year: {data['data']['getneedperyear']} GET tokens. "
        f"Needed per month: {data['data']['getneedpermonth']} GET tokens."
        )
