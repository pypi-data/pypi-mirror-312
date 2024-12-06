# CY3761 | fb764bc@outlook.com | 2024-11-26 17:07:06 | main.py
# ----------------------------------------------------------------------------------------------------
from CY3761 import *

# ----------------------------------------------------------------------------------------------------
js = require('./00_main.js')


# ----------------------------------------------------------------------------------------------------
def main_00():
    cookies = headers = params = data = {}

    cookies = js.call('getCookies', cookies)
    print(dumps(cookies))

    headers = js.call('getHeaders', headers)
    print(dumps(headers))

    params = js.call('getParams', params)
    print(dumps(params))

    data = js.call('getData', data)
    print(dumps(data))

    response = requests.get('')

    res_00(response)

    text = js.call('getResponseBody', response.text)
    # print(text)


# ----------------------------------------------------------------------------------------------------
def main():
    from CY3761.build.res import build_config_js

    build_config_js()
    main_00()
    pass


# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
