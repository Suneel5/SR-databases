
# url='https://www.google.com/search?q=RealEstate+reddit&tbs=cdr:1,cd_min:04/19/2024,cd_max:04/21/2024&as_sitesearch=reddit.com/r/RealEstate/&start=0'

import requests
def zen_api(url):
    apikey = '8b64fdb1a15e6a4fef59aa154aa1ca9b95938f56'
    params = {
        'url': url,
        'apikey': apikey,
        'premium_proxy': 'true',
    }
    response = requests.get('https://api.zenrows.com/v1/', params=params)
    return response
    # print(response.text)