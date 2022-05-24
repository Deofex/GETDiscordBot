import requests
import json
import re
from datetime import datetime, timedelta

graphurl = \
    "https://api.thegraph.com/subgraphs/name/getprotocol/get-protocol-subgraph-deprecated"


def queryGraph(day):
    q = '''
    {
        protocolDays(where:{day:%s}) {
            day
            mintCount
            getDebitedFromSilos
            getCreditedToDepot
            averageGetPerMint
        }
    }
    ''' % day

    r = requests.post(graphurl, json={'query': q})

    getusage = json.loads(r.text)
    return getusage


def getdatenumber(day):
    epochdate = datetime(1970, 1, 1)
    if day.lower() == 'today':
        date = datetime.now()
    elif day.lower() == 'yesterday':
        date = datetime.now() - timedelta(days=1)
    else:
        dateregex = '^[0-3][0-9]-[0-1][0-9]-[0-9][0-9][0-9][0-9]$'
        if re.match(dateregex, day):
            d = day.split('-')
            date = datetime(int(d[2]), int(d[1]), int(d[0]))
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
    except Exception as e:
        if (e.args[0] == 'InvalidDay'):
            return {
                'status': 'InvalidDay',
                'reason': ("The day is specified in an unknow format. Use "
                           "'Today', 'Yesterday' or 'dd-mm-yyyy'.")
            }
        elif (e.args[0] == 'FutureDate'):
            return {
                'status': 'FutureDate',
                'reason': ("My crystal ball is damaged, future predictions "
                "are temporary disabled.")
            }
        else:
            return {
                'status': 'UnknownError',
                'reason': e.args[0]
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
        data = (queryGraph(datenumber))['data']['protocolDays'][0]
    except Exception as e:
        print('Error occured: {}'.format(e.args[0]))
        return {
            'status': 'UnknownError',
            'reason': 'Unknown Error'
        }
    return {
        'status': 'OK',
        'data': {
            'date': date,
            'averageGetPerMint': data['averageGetPerMint'],
            'getDebitedFromSilos':data['getDebitedFromSilos'],
            'getCreditedToDepot': data['getCreditedToDepot'],
            'mintCount': data['mintCount'],
            'mintCount': data['mintCount']
        }
    }


if __name__ == '__main__':
    getusage = getusageday("26-12-2021")
    if getusage['status'] == 'OK':
        print(getusage)
    else:
        print('Status not okay')
        print('Reason: {}'.format(getusage['reason']))


