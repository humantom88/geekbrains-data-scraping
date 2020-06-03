import requests

test_token = '2e70d2261f73ab84186c74fc2c854443f8153716'

usernames = ['iGhibli']

params = {
    'type': 'owner'
}

headers = {
    'Authorization': f'token {test_token}',
}

for username in usernames:
    url_address = f'https://api.github.com/users/{username}/repos'
    response = requests.get(url_address, params=params, headers=headers)

    with open(f'{username}.json', 'w') as f:
        f.write(response.text)
