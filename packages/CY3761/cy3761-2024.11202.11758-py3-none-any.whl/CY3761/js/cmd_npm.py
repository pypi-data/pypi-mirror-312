# CY3761 | fb764bc@outlook.com | 2024-12-02 12:23:27 | npm.py
# ----------------------------------------------------------------------------------------------------
from CY3761 import *


# ----------------------------------------------------------------------------------------------------
def install(pkg: str, check=True):
    installed = False

    if check:
        installed = has(pkg)

    return installed or npm('install', pkg)


# ----------------------------------------------------------------------------------------------------
def remove(pkg: str):
    return npm('remove', pkg)


# 运行这个 npm list 可能会报错
def has(kpg: str):
    try:
        return npm('list').count(kpg) > 0
    except (Exception,) as e:
        pass

    return False


# ----------------------------------------------------------------------------------------------------
def version():
    return npm('-v')


# ----------------------------------------------------------------------------------------------------
def main():
    cmd_cwd(root_02)
    # print(version())

    print(has('curlconverter') or install('curlconverter'))

    # print(remove('curlconverter'))


# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
