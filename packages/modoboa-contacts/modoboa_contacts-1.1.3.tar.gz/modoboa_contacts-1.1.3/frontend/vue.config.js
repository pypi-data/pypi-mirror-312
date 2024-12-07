var path = require('path')
var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
    publicPath: process.env.NODE_ENV === 'production'
              ? '/sitestatic/'
              : 'http://localhost:8080/',
    outputDir: '../modoboa_contacts/static/',
    assetsDir: 'modoboa_contacts',
    chainWebpack: config => {
        config
            .plugin('BundleTracker')
            .use(BundleTracker, [{
                filename: path.join('../modoboa_contacts/static/modoboa_contacts/', 'webpack-stats.json')
            }])

        config.devServer
            .public('http://localhost:8080')
            .port(8080)
            .hotOnly(true)
            .watchOptions({poll: 1000})
            .https(false)
            .headers({
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, PATCH, OPTIONS',
                'Access-Control-Allow-Headers':
                'X-Requested-With, content-type, Authorization',
                'Access-Control-Allow-Credentials': 'true'
            })
    }
}
