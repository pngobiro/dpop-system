// webpack.config.js
const path = require('path');

module.exports = {
  entry: {
    main: './static/js/src/index.js',
    memos: './static/js/src/memos/index.js',
  },
  output: {
    path: path.resolve(__dirname, './static/js/dist'),
    filename: '[name].bundle.js',
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
        },
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
    ],
  },
  resolve: {
    extensions: ['.js', '.jsx'],
  },
};