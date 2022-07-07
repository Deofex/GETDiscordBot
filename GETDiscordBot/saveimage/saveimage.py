import shutil
import os
import requests

def saveimage(url,filename):
    req = requests.get(url, stream = True)

    if os.path.isfile(filename):
        try:
            os.remove(filename)
        except Exception as ex:
            raise Exception('CantRemoveFile') from ex
    if req.status_code == 200:
        req.raw.decode_content = True
        with open(filename,'wb') as file:
            shutil.copyfileobj(req.raw, file)
    else:
        raise Exception('ImageDownloadError')

    return True
    