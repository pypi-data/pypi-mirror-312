// https://www.npmjs.com/package/curlconverter
// https://github.com/curlconverter/curlconverter
// https://curlconverter.com/
// npm i curlconverter
// ----------------------------------------------------------------------------------------------------

import * as curlconverter from 'curlconverter'
import {read, main_01} from './helper.js'
// ----------------------------------------------------------------------------------------------------
const getCode = (sn) => curlconverter.toPython(read(sn))

// ----------------------------------------------------------------------------------------------------
main_01(import.meta, {getCode})