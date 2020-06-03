import requests

token = '6FpCIZY0btmSe4NjtbVpROlhFXk3E6Ix2kLUUzLP'
query = 'goose'

params = {
    'token': token,
    'query': query,
}

url_address = f'https://freesound.org/apiv2/search/text/'
response = requests.get(url_address, params=params)

with open(f'goose_sounds.json', 'w') as f:
    f.write(response.text)
