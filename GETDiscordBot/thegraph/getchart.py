import requests
import json
from quickchart import QuickChart
from datetime import datetime, timedelta


graphurl = \
    "https://api.thegraph.com/subgraphs/name/getprotocol/get-protocol-subgraph"


def queryGraph(days, skiplastday = False):
    q = ('''
    {
    protocolDays(orderBy: day, orderDirection: desc, first: %s) {
        day
        soldCount
        reservedFuel
    }
    }
    ''' % days )
    r = requests.post(graphurl, json={'query': q})
    getusage = json.loads(r.text)
    if skiplastday:
        getusage['data']['protocolDays'] = getusage['data']['protocolDays'][1:]
    return getusage


def create_graphurl(data):
    epochdate = datetime(1970, 1, 1)
    days = data['data']['protocolDays']
    days.reverse()
    labels = []
    values1 = []
    values2 = []
    for day in days:
        lday = (epochdate + timedelta(days=day['day'])).strftime('%d-%m-%y')
        labels.append(lday)
        values1.append(day['reservedFuel'])
        values2.append(day['soldCount'])
    qc = QuickChart()
    qc.width = 500
    qc.height = 300
    qc.device_pixel_ratio = 2.0
    qc.config = {
        "type": "line",
        "data": {
            "labels": labels,
            "datasets": [{
                "label": "GET reserved",
                "data": values1,
                "yAxisID": "y-axis-1",
            },
                {
                "label": "NFT Tickets sold",
                "data": values2,
                "yAxisID": "y-axis-2",
                "type": "bar"
            }]
        },
        "options": {
            "scales": {
                "yAxes": [{
                    "id": "y-axis-1",
                    "scaleLabel": {
                        "display": True,
                        "labelString": "GET reserved"
                    },
                    "type": "linear",
                    "display": True,
                    "position": 'left'
                },
                    {
                    "id": "y-axis-2",
                    "scaleLabel": {
                        "display": True,
                        "labelString": "NFT Tickets created"
                    },
                    "type": "linear",
                    "display": True,
                    "position": 'right',
                    "gridLines": {
                        "drawOnChartArea": False
                    }
                }]
            }
        }
    }

    # Print the chart URL
    return(qc.get_url())


def getchart(days):
    try:
        data = queryGraph(days,skiplastday=True)
    except Exception as e:
        print('Error occured: {}'.format(e.args[0]))
        return {
            'status': 'UnknownError',
            'reason': 'Unknown Error'
        }

    try:
        graphurl = create_graphurl(data)
    except Exception as e:
        print('Error occured: {}'.format(e.args[0]))
        return {
            'status': 'UnknownError',
            'reason': 'Unknown Error'
        }

    return {
            'status': 'OK',
            'url': graphurl
        }



if __name__ == '__main__':
    print(getchart(30))
