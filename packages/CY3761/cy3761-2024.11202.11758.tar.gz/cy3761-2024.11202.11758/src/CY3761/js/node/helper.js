import fs from 'fs'
// ----------------------------------------------------------------------------------------------------
const encoding = 'utf8'
// ----------------------------------------------------------------------------------------------------
// 同步读文件
const read = src => fs.readFileSync(src, encoding)
// 同步写文件
const save = (src, data) => fs.writeFileSync(src, data, encoding)
// ----------------------------------------------------------------------------------------------------
const main_00 = (imm, cb) => {
    if (typeof cb !== 'function') return

    const u00 = decodeURIComponent(imm.url.slice('file:///'.length))
    const u01 = process.argv[1].replaceAll('\\', '/')

    // console.log(u00)
    // console.log(u01)

    u00 === u01 && cb()
}
// ----------------------------------------------------------------------------------------------------
const main_01 = (imm, win = {}) => {
    return main_00(imm, () => {
        const [func, ...args] = process.argv.slice(2)

        // console.log(func, args)

        if (!func || func.trim().length === 0) return

        let method = undefined

        try {
            method = eval(func)
        } catch (e) {
            method = win[func]
        }

        if (typeof method !== 'function') return

        try {
            console.log(method(...args))
        } catch (e) {
            const data = [e.toString(), method.toString(), args]

            save('main-01--error.log', data.join(' | ')) || console.error(data)
        }
    })
}
// ----------------------------------------------------------------------------------------------------
const sum = (a, b) => {
    [a, b] = [a, b].map(v => Number(v)).map(v => isNaN(v) ? 0 : v)

    return a + b
}
// ----------------------------------------------------------------------------------------------------
export {read, save, main_00, main_01, sum}
// 导出一个函数时需要在 export 后面增加 default

// ----------------------------------------------------------------------------------------------------
main_00(import.meta, () => {
    // console.log('sum(5, 7)', '=', sum(5, 7))
})
// ----------------------------------------------------------------------------------------------------
// node I:\33008\项目\CY3761\src\CY3761\js\node\helper.js sum 7 9
// 执行的错误文件写在 运行脚本的目录下
main_01(import.meta)