module.exports = {
  transpileDependencies: ["vuetify"],
  devServer: {
    port: 3000,
    proxy: {
      "^/api*": {
        target: "http://localhost:5000/"
      }
    }
  },
  outputDir: "dist",
  assetsDir: "static"
};
