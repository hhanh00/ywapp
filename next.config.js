const withNextra = require('nextra')({
    theme: 'nextra-theme-docs',
    themeConfig: './theme.config.jsx'
})
   
module.exports = {
    ...withNextra(),
    async redirects() {
      return [
        // {
        //   source: '/',
        //   destination: '/about',
        //   permanent: true,
        // },
      ]
    },
}
