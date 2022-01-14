import requests
import shutil
import os

def saveimage(url,filename):
    r = requests.get(url, stream = True)

    if os.path.isfile(filename):
        try:
            os.remove(filename)
        except:
            raise Exception('CantRemoveFile')
    if r.status_code == 200:
        r.raw.decode_content = True
        with open(filename,'wb') as f:
            shutil.copyfileobj(r.raw, f)
    else:
        raise Exception('ImageDownloadError')

    return True


if __name__ == '__main__':
    url = 'https://quickchart.io/chart?c=%7B%22type%22%3A%22line%22%2C%22data%22%3A%7B%22labels%22%3A%5B%2214-10-21%22%2C%2215-10-21%22%2C%2216-10-21%22%2C%2217-10-21%22%2C%2218-10-21%22%2C%2219-10-21%22%2C%2220-10-21%22%2C%2221-10-21%22%2C%2222-10-21%22%2C%2223-10-21%22%2C%2224-10-21%22%2C%2225-10-21%22%2C%2226-10-21%22%2C%2227-10-21%22%2C%2228-10-21%22%2C%2229-10-21%22%2C%2230-10-21%22%2C%2231-10-21%22%2C%2201-11-21%22%2C%2202-11-21%22%2C%2203-11-21%22%2C%2204-11-21%22%2C%2205-11-21%22%2C%2206-11-21%22%2C%2207-11-21%22%2C%2208-11-21%22%2C%2209-11-21%22%2C%2210-11-21%22%2C%2211-11-21%22%2C%2212-11-21%22%5D%2C%22datasets%22%3A%5B%7B%22label%22%3A%22GET+debited+from+silos%22%2C%22data%22%3A%5B%220%22%2C%220%22%2C%220%22%2C%220%22%2C%220%22%2C%220%22%2C%220%22%2C%220%22%2C%220%22%2C%220%22%2C%220%22%2C%220%22%2C%2219.3549766%22%2C%2237.3888088%22%2C%22251.9404443%22%2C%22280.3821723%22%2C%221115.7835462%22%2C%2272.6279381%22%2C%2243.7067464%22%2C%2235.4175483%22%2C%22432.51235%22%2C%22202.5482758%22%2C%22126.5141612%22%2C%2271.9455846%22%2C%2264.5235542%22%2C%222730.0249499%22%2C%22666.9916496%22%2C%221035.6716018%22%2C%221119.0915911%22%2C%22711.8271591%22%5D%2C%22yAxisID%22%3A%22y-axis-1%22%7D%2C%7B%22label%22%3A%22Tickets+sold%22%2C%22data%22%3A%5B%222688%22%2C%223178%22%2C%222689%22%2C%221866%22%2C%221880%22%2C%222417%22%2C%222859%22%2C%222689%22%2C%223057%22%2C%222482%22%2C%222043%22%2C%226600%22%2C%222368%22%2C%221704%22%2C%227199%22%2C%228451%22%2C%2212549%22%2C%222310%22%2C%222019%22%2C%223094%22%2C%226939%22%2C%224127%22%2C%225284%22%2C%223397%22%2C%222625%22%2C%2222276%22%2C%226803%22%2C%228458%22%2C%229066%22%2C%225367%22%5D%2C%22yAxisID%22%3A%22y-axis-2%22%2C%22type%22%3A%22bar%22%7D%5D%7D%2C%22options%22%3A%7B%22scales%22%3A%7B%22yAxes%22%3A%5B%7B%22id%22%3A%22y-axis-1%22%2C%22scaleLabel%22%3A%7B%22display%22%3Atrue%2C%22labelString%22%3A%22GET+debited%22%7D%2C%22type%22%3A%22linear%22%2C%22display%22%3Atrue%2C%22position%22%3A%22left%22%7D%2C%7B%22id%22%3A%22y-axis-2%22%2C%22scaleLabel%22%3A%7B%22display%22%3Atrue%2C%22labelString%22%3A%22Tickets+sold%22%7D%2C%22type%22%3A%22linear%22%2C%22display%22%3Atrue%2C%22position%22%3A%22right%22%2C%22gridLines%22%3A%7B%22drawOnChartArea%22%3Afalse%7D%7D%5D%7D%7D%7D&w=500&h=300&bkg=%23ffffff&devicePixelRatio=2.0&f=png&v=2.9.4'
    saveimage(url)