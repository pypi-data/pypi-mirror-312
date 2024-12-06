# CY3761 | fb764bc@outlook.com | 2024-11-28 10:38:59 | setup.py
# ----------------------------------------------------------------------------------------------------
from CY3761.build.res import *


# ----------------------------------------------------------------------------------------------------
def main_00():
    build_base64([
        'aHR0cHM6Ly93d3cuZGlnaWtleS5jb20vZW4vcHJvZHVjdHMvZmlsdGVyL2NvYXhpYWwtY2FibGVzLzQ1Ng==',
        'aHR0cHM6Ly93d3cuZGlnaWtleS5jb20vcHJvZHVjdHMvYXBpL3Y1L2ZpbHRlcnMvNDU2P3M9TjRJZ2pDQmNvTFFkSURHVUJtQkRBTmdad0tZQm9RQjdLQWJYQUU0UUJkQVh6cUE=',
        'aHR0cHM6Ly93d3cuZGlnaWtleS5jb20vcHJvZHVjdHMvYXBpL3Y1L2ZpbHRlci1wYWdlLzQ1Nj9zPU40SWdyQ0Jjb0E1UWpBR2hET2w0QVlNRjl0QQ=='
    ])

    # 这个需要放在 main.py
    build_config_js()

    [v('00') for v in (build_main_js, build_main_py)]
# ----------------------------------------------------------------------------------------------------
def main_01():
    build_test_py('00', """
curl 'https://www.digikey.com/products/api/v5/filters/456?s=N4IgjCBcoLQdIDGUBmBDANgZwKYBoQB7KAbXAE4QBdAXzqA' \
  -H 'accept: */*' \
  -H 'accept-language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6' \
  -H 'authorization: Bearer' \
  -H 'cookie: _pxhd=cf8a293676402ad0b876a9e62457bb2b4455b6f98e8736ccbb9e83ad746a9f93:75dc9504-aae1-11ef-ae4d-05478e2a84f6; _pxvid=75dc9504-aae1-11ef-ae4d-05478e2a84f6; pf-accept-language=en-US; ping-accept-language=en-US; digikey_theme=dklt; search=%7B%22id%22%3A%228f205383-4837-4c13-9170-76f4540df153%22%2C%22usage%22%3A%7B%22dailyCount%22%3A2%2C%22lastRequest%22%3A%222024-12-01T09%3A29%3A43.808Z%22%7D%2C%22version%22%3A1.1%7D; TS01173021=01f9ef228d2db0c97ef3a6e82b3292c034b301bd2315c4f0876bbf9e228ddd653c2a8e3f6d61409d4715acc0735325ec0c87ee2f1c; TScaafd3c3027=08205709cbab2000e71fa5777d7d33a537d85c8f96902ad9c508bfadbbfbc6837074ded51dbce2f40897e4b837113000b6919b58fb72ff3653019a152d095f2e53582e065c828c389b248a23ed529dc5ea943aadff5d77456433968617077250; pxcts=cee29e0d-afc6-11ef-b1be-cd0fa866978d; dkc_tracker=3664857667361; _px2=eyJ1IjoiZjNiOWNjMDAtYWZjNi0xMWVmLWFlMzAtYzMxM2Q3ZTYxNTEyIiwidiI6Ijc1ZGM5NTA0LWFhZTEtMTFlZi1hZTRkLTA1NDc4ZTJhODRmNiIsInQiOjE3MzMwNDU3NTU1MzgsImgiOiJkYmJmNTY2MTFmYmQ0OWE0OWY5OTZjNmI4MjM3YWEyYzYyYWRjNTY5MmY5Mzk4NDM2MTZlNTM2YmEwMTc3ZTdmIn0=; _pxde=660f345e165501b2c39bc9158293fdcf1f9b9daa1a1e8557b6b5619c5e42b4a7:eyJ0aW1lc3RhbXAiOjE3MzMwNDU0NjQ0OTIsImZfa2IiOjAsImlwY19pZCI6W10sImNncCI6MX0=' \
  -H 'dnt: 1' \
  -H 'lang: en' \
  -H 'priority: u=1, i' \
  -H 'referer: https://www.digikey.com/en/products/filter/coaxial-cables/456' \
  -H 'sec-ch-ua: "Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'site: us' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0' \
  -H 'x-currency: USD' \
  -H 'x-request-id: b8c11b9f-f0f4-4877-a2b0-ddbdce6d3822'
    """)

# ----------------------------------------------------------------------------------------------------
def main():
    main_00()
    main_01()


# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
