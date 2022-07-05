import requests
import json


graphurl = \
    "https://api.thegraph.com/subgraphs/name/getprotocol/get-protocol-subgraph"


def queryGraph():
    q = '''
    {
    protocolDays(orderBy: day, orderDirection: desc, first: 100) {
        reservedFuel
    }
    }
    '''

    r = requests.post(graphurl, json={'query': q})

    getusage = json.loads(r.text)
    return getusage


def process_data(data):
    totaldays = 0
    totalgetdebitedfromsilos = 0
    for day in data['data']['protocolDays']:
        if day['reservedFuel'] == "0":
            continue
        totaldays += 1
        totalgetdebitedfromsilos += float(day['reservedFuel'])
    return totaldays, totalgetdebitedfromsilos


def getneedprediction():
    try:
        data = queryGraph()
    except Exception as e:
        return {
            'status': 'UnknownError',
            'reason': e.args[0]
        }

    totaldays, totalgetdebitedfromsilos = process_data(data)
    avgdebitperday = totalgetdebitedfromsilos / totaldays
    getneedperyear = int(365 * avgdebitperday)
    getneedpermonth = int(365 * avgdebitperday / 12)
    data = {
        "getneedperday":int(avgdebitperday),
        "getneedperyear":getneedperyear,
        "getneedpermonth":getneedpermonth

    }
    return {
        'status': 'OK',
        'data': data
    }


if __name__ == "__main__":
    data = getneedprediction()
    print("Needed per year: {} GET tokens. "
    "Needed per month: {} GET tokens.".format(
        data['data']['getneedperyear'],
        data['data']['getneedpermonth']
        ))
