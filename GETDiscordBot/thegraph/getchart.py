import json
from datetime import datetime, timedelta
import requests
from quickchart import QuickChart


GRAPH_URL = \
    "https://api.thegraph.com/subgraphs/name/getprotocol/get-protocol-subgraph"


def query_graph(days, skiplastday = False):
    query = (
    "{"
    f"   protocolDays(orderBy: day, orderDirection: desc, first: {days}) {{"
    "       day"
    "       soldCount"
    "       reservedFuel"
    "   }"
    "}"
    )
    request = requests.post(GRAPH_URL, json={'query': query})
    getusage = json.loads(request.text)
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
    quick_chart = QuickChart()
    quick_chart.width = 500
    quick_chart.height = 300
    quick_chart.device_pixel_ratio = 2.0
    quick_chart.config = {
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
    return quick_chart.get_url()


def getchart(days):
    try:
        data = query_graph(days,skiplastday=True)
    except Exception as ex:
        print(f"Error occured: {ex.args[0]}")
        return {
            'status': 'UnknownError',
            'reason': 'Unknown Error'
        }

    try:
        fullgraphurl = create_graphurl(data)
    except Exception as ex:
        print(f"Error occured: {ex.args[0]}")
        return {
            'status': 'UnknownError',
            'reason': 'Unknown Error'
        }

    return {
            'status': 'OK',
            'url': fullgraphurl
        }



if __name__ == '__main__':
    print(getchart(30))
