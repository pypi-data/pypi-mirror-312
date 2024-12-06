import requests

cookies = {
    '_pxhd': 'cf8a293676402ad0b876a9e62457bb2b4455b6f98e8736ccbb9e83ad746a9f93:75dc9504-aae1-11ef-ae4d-05478e2a84f6',
    '_pxvid': '75dc9504-aae1-11ef-ae4d-05478e2a84f6',
    'pf-accept-language': 'en-US',
    'ping-accept-language': 'en-US',
    'digikey_theme': 'dklt',
    'search': '%7B%22id%22%3A%228f205383-4837-4c13-9170-76f4540df153%22%2C%22usage%22%3A%7B%22dailyCount%22%3A2%2C%22lastRequest%22%3A%222024-12-01T09%3A29%3A43.808Z%22%7D%2C%22version%22%3A1.1%7D',
    'TS01173021': '01f9ef228d2db0c97ef3a6e82b3292c034b301bd2315c4f0876bbf9e228ddd653c2a8e3f6d61409d4715acc0735325ec0c87ee2f1c',
    'TScaafd3c3027': '08205709cbab2000e71fa5777d7d33a537d85c8f96902ad9c508bfadbbfbc6837074ded51dbce2f40897e4b837113000b6919b58fb72ff3653019a152d095f2e53582e065c828c389b248a23ed529dc5ea943aadff5d77456433968617077250',
    'pxcts': 'cee29e0d-afc6-11ef-b1be-cd0fa866978d',
    'dkc_tracker': '3664857667361',
    '_px2': 'eyJ1IjoiZjNiOWNjMDAtYWZjNi0xMWVmLWFlMzAtYzMxM2Q3ZTYxNTEyIiwidiI6Ijc1ZGM5NTA0LWFhZTEtMTFlZi1hZTRkLTA1NDc4ZTJhODRmNiIsInQiOjE3MzMwNDU3NTU1MzgsImgiOiJkYmJmNTY2MTFmYmQ0OWE0OWY5OTZjNmI4MjM3YWEyYzYyYWRjNTY5MmY5Mzk4NDM2MTZlNTM2YmEwMTc3ZTdmIn0=',
    '_pxde': '660f345e165501b2c39bc9158293fdcf1f9b9daa1a1e8557b6b5619c5e42b4a7:eyJ0aW1lc3RhbXAiOjE3MzMwNDU0NjQ0OTIsImZfa2IiOjAsImlwY19pZCI6W10sImNncCI6MX0=',
}

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'authorization': 'Bearer',
    # 'cookie': '_pxhd=cf8a293676402ad0b876a9e62457bb2b4455b6f98e8736ccbb9e83ad746a9f93:75dc9504-aae1-11ef-ae4d-05478e2a84f6; _pxvid=75dc9504-aae1-11ef-ae4d-05478e2a84f6; pf-accept-language=en-US; ping-accept-language=en-US; digikey_theme=dklt; search=%7B%22id%22%3A%228f205383-4837-4c13-9170-76f4540df153%22%2C%22usage%22%3A%7B%22dailyCount%22%3A2%2C%22lastRequest%22%3A%222024-12-01T09%3A29%3A43.808Z%22%7D%2C%22version%22%3A1.1%7D; TS01173021=01f9ef228d2db0c97ef3a6e82b3292c034b301bd2315c4f0876bbf9e228ddd653c2a8e3f6d61409d4715acc0735325ec0c87ee2f1c; TScaafd3c3027=08205709cbab2000e71fa5777d7d33a537d85c8f96902ad9c508bfadbbfbc6837074ded51dbce2f40897e4b837113000b6919b58fb72ff3653019a152d095f2e53582e065c828c389b248a23ed529dc5ea943aadff5d77456433968617077250; pxcts=cee29e0d-afc6-11ef-b1be-cd0fa866978d; dkc_tracker=3664857667361; _px2=eyJ1IjoiZjNiOWNjMDAtYWZjNi0xMWVmLWFlMzAtYzMxM2Q3ZTYxNTEyIiwidiI6Ijc1ZGM5NTA0LWFhZTEtMTFlZi1hZTRkLTA1NDc4ZTJhODRmNiIsInQiOjE3MzMwNDU3NTU1MzgsImgiOiJkYmJmNTY2MTFmYmQ0OWE0OWY5OTZjNmI4MjM3YWEyYzYyYWRjNTY5MmY5Mzk4NDM2MTZlNTM2YmEwMTc3ZTdmIn0=; _pxde=660f345e165501b2c39bc9158293fdcf1f9b9daa1a1e8557b6b5619c5e42b4a7:eyJ0aW1lc3RhbXAiOjE3MzMwNDU0NjQ0OTIsImZfa2IiOjAsImlwY19pZCI6W10sImNncCI6MX0=',
    'dnt': '1',
    'lang': 'en',
    'priority': 'u=1, i',
    'referer': 'https://www.digikey.com/en/products/filter/coaxial-cables/456',
    'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'site': 'us',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
    'x-currency': 'USD',
    'x-request-id': 'b8c11b9f-f0f4-4877-a2b0-ddbdce6d3822',
}

params = {
    's': 'N4IgjCBcoLQdIDGUBmBDANgZwKYBoQB7KAbXAE4QBdAXzqA',
}

response = requests.get('https://www.digikey.com/products/api/v5/filters/456', params=params, cookies=cookies, headers=headers)