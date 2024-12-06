# CY3761 | fb764bc@outlook.com | 2024-11-26 12:05:21 | build.py
# ----------------------------------------------------------------------------------------------------
from CY3761 import *

# ----------------------------------------------------------------------------------------------------
root_10 = Path(__file__)
template_dir = root_10.parent / 'template' / root_10.name.replace(root_10.suffix, '')


# ----------------------------------------------------------------------------------------------------
def build_base64(rows):
    a_00 = []

    for i, v in enumerate(rows):
        z = str(i).zfill(2)
        a_00.extend([
            # a_032.join([a_035, z, v]),
            a_032.join([a_035, z, atob(v)])
        ])

        # print(a_00[-2:])

    storage('./base.py', a_00)


# data 在另一个函数内进行优化代码, 然后再传给 save
def build_file(sn: str, name: str, suffix: str):
    name = name + '.' + suffix
    data = storage(template_dir / name)

    # print(template_dir / name)
    # print(data)

    def save(rows, code):
        src = switch(sn == '', sn + a_095 + name, name)

        for k, v in rows:
            code = code.replace('{%s}' % k, '%s' % v)

        storage(src, code)

    return data, save


# ----------------------------------------------------------------------------------------------------
def build_main(sn: str, suffix: str):
    return build_file(sn, 'main', suffix)


# ----------------------------------------------------------------------------------------------------
def build_main_py(sn: str):
    data, save = build_main(sn, 'py')

    return save([
        ('sn', sn),
    ], data)


# ----------------------------------------------------------------------------------------------------
def build_main_js(sn: str):
    data, save = build_main(sn, 'js')

    # print(data)

    return save([
        ('sn', sn),
    ], data)


# 包的配置脚本, 复制到项目使用, 当调用了包的脚本时所需
def build_config_js():
    data, save = build_file('', 'config', 'js')

    return save([
        # 运行时需要更新这个路径, 因为未知运行时的包路径是在哪里
        ('pakPath', str((root_00 / 'js' / 'node').absolute()).replace('\\', '/')),
    ], data)


def build_test_py(sn: str, code: str):
    from random import randint
    from CY3761.js.cmd_npm import install

    cmd_cwd(root_02)

    install('curlconverter')

    cmd_cwd('')

    src = Path('./{0}'.format(randint(int(1e3), int(9e3))))

    storage(src, code.strip())

    # I:\33008\项目\CY3761\src\CY3761\js\node\curlconverter.js
    code = node(root_00 / 'js' / 'node' / 'curlconverter.js', 'getCode', src)

    print(code)

    ret = storage('./' + sn + '_test.py', code)

    src.unlink(missing_ok=True)

    return ret


# ----------------------------------------------------------------------------------------------------
def main_00():
    pass
    build_base64([
        'aHR0cHM6Ly93d3cuZGlnaWtleS5jb20vZW4vcHJvZHVjdHMvZmlsdGVyL2NvYXhpYWwtY2FibGVzLzQ1Ng==',
        'aHR0cHM6Ly93d3cuZGlnaWtleS5jb20vcHJvZHVjdHMvYXBpL3Y1L2ZpbHRlcnMvNDU2P3M9TjRJZ2pDQmNvTFFkSURHVUJtQkRBTmdad0tZQm9RQjdLQWJYQUU0UUJkQVh6cUE=',
        'aHR0cHM6Ly93d3cuZGlnaWtleS5jb20vcHJvZHVjdHMvYXBpL3Y1L2ZpbHRlci1wYWdlLzQ1Nj9zPU40SWdyQ0Jjb0E1UWpBR2hET2w0QVlNRjl0QQ=='
    ])


def main_01():
    build_main_js('00')


# ----------------------------------------------------------------------------------------------------
def main():
    pass
    # main_00()
    main_01()


# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
