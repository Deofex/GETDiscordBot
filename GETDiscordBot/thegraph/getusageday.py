import json
import re
from datetime import datetime, timedelta
import requests

GRAPH_URL = \
    "https://api.thegraph.com/subgraphs/name/getprotocol/get-protocol-subgraph"


def query_graph(day):
    query = '''
    {
        protocolDays(where:{day:%s}) {
            day
            eventCount
            soldCount
            spentFuel
            reservedFuel
            averageReservedPerTicket
            totalSalesVolume
        }
    }
    ''' % day

    request = requests.post(GRAPH_URL, json={'query': query})

    get_usage= json.loads(request.text)
    return get_usage


def getdatenumber(day):
    epochdate = datetime(1970, 1, 1)
    if day.lower() == 'today':
        date = datetime.now()
    elif day.lower() == 'yesterday':
        date = datetime.now() - timedelta(days=1)
    elif day == "":
        raise Exception('InvalidDay')
    else:
        dateregex = '^[0-3][0-9]-[0-1][0-9]-[0-9][0-9][0-9][0-9]$'
        if re.match(dateregex, day):
            d_splitted = day.split('-')
            date = datetime(int(d_splitted[2]), int(d_splitted[1]), int(d_splitted[0]))
        else:
            raise Exception('InvalidDay')
    if date > datetime.now():
        raise Exception('FutureDate')
    datenumber = (date - epochdate).days
    datestr = date.strftime('%d-%m-%y')
    return datestr, datenumber


def getusageday(day):
    # Convert given date to datenumber
    try:
        date, datenumber = getdatenumber(day)
    except Exception as ex:
        if ex.args[0] == 'InvalidDay':
            return {
                'status': 'InvalidDay',
                'reason': ("The day is specified in an unknow format. Use "
                           "'Today', 'Yesterday' or 'dd-mm-yyyy'.")
            }
        elif ex.args[0] == 'FutureDate':
            return {
                'status': 'FutureDate',
                'reason': ("My crystal ball is damaged, future predictions "
                "are temporary disabled.")
            }
        else:
            return {
                'status': 'UnknownError',
                'reason': ex.args[0]
            }
    # If datenumber is below the release of mainnet, return DateToOld
    if datenumber < 18926:
        return {
            'status': 'DateToOld',
            'reason': ("The given day was before the mainnet launch. Specify "
                       "a data after 25-10-2021")
        }
    # Query the data
    try:
        data = (query_graph(datenumber))['data']['protocolDays'][0]
    except Exception as ex:
        print(f"Error occured: {ex.args[0]}")
        return {
            'status': 'UnknownError',
            'reason': 'Unknown Error'
        }
    return {
        'status': 'OK',
        'data': {
            'date': date,
            'eventCount': data['eventCount'],
            'soldCount': data['soldCount'],
            'spentFuel':data['spentFuel'],
            'reservedFuel': data['reservedFuel'],
            'averageReservedPerTicket': data['averageReservedPerTicket'],
            'totalSalesVolume': data['totalSalesVolume'],
        }
    }


if __name__ == '__main__':
    getusage = getusageday("26-12-2021")
    if getusage['status'] == 'OK':
        print(getusage)
    else:
        print('Status not okay')
        print(f"Reason: {getusage['reason']}")
