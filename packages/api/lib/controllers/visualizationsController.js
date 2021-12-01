const getWebMap = async function getWebMap (req, res, next) {
    console.log("GetWebMap endpoint triggered!")
}

const getPDF = async function getPDF (req, res, next) {
    console.log("GetPDF endpoint triggered!")
}

const getGIF = async function getGIF (req, res, next) {
    console.log("GetGIF endpoint triggered!")
}

module.exports = {
    getWebMap,
    getPDF,
    getGIF
}