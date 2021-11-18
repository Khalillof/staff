const path = require('path');
const fs = require('fs')
const webpack = require('webpack');

const CopyPlugin = require('copy-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
//const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
//const HtmlWebpackPlugin = require('html-webpack-plugin');
const MinifyHtmlWebpackPlugin = require('minify-html-webpack-plugin');
const ImageMinimizerPlugin  = require("image-minimizer-webpack-plugin");


//joining path of directory 

function get__dir_not_empty(startPath,filter,callback){

  //console.log('Starting from dir '+startPath+'/');

  if (!fs.existsSync(startPath)){
      console.log("no dir ",startPath);
      return;
  }

  var files=fs.readdirSync(startPath);
  for(var i=0;i<files.length;i++){
      var filename=path.join(startPath,files[i]);
      var stat = fs.lstatSync(filename);
      if (stat.isDirectory()){
          get__dir_not_empty(filename,filter,callback); //recurse
      }
      else if (filter.test(filename)) callback(filename);
  };
};

function get_asests_dirs(dir_name,ext_reg, callback){
let _dirs =[];
let uniques = [];
let files = [];
get__dir_not_empty(dir_name,ext_reg,function(filename){
  //dist_path= path.resolve(__dirname,path.join('dist/',path.dirname(filename)));
  dist_path= path.join('dist/',path.dirname(filename));
  files.push(filename)

  if (uniques.indexOf(dist_path) == -1){
    uniques.push(dist_path);
    console.log('-- found: ',dist_path);
    if(callback){
      _dirs.push(callback(dist_path));
  }else{
      _dirs.push(dist_path);
  }
}
});
return {
  dirs:_dirs,
  files:files
}
};
/*
const html_dirs = (()=> get_asests_dirs('./capstone/agency/templates',/\.html$/, function(dist_path){ 
//console.log('from withen callback dir is :' + dist_path)
return new MinifyHtmlWebpackPlugin({
src: dist_path,
dest: dist_path,
afterBuild:true,
rules: {
    collapseBooleanAttributes: true,
    collapseWhitespace: true,
    removeAttributeQuotes: true,
    removeComments: true,
    minifyJS: true,
}
})}
))();
*/
html_dirs = ['./dist/capstone/agency/templates', './dist/capstone/accounts/templates', './dist/capstone/mail/templates',
'./dist/capstone/news/templates'].map((dir)=> new MinifyHtmlWebpackPlugin({  
  src: dir,
  dest: dir,
  afterBuild:true,
  rules: {
      collapseBooleanAttributes: true,
      collapseWhitespace: true,
      removeAttributeQuotes: true,
      removeComments: true,
      minifyJS: true,
  }
  }));

const images_dirs = (()=> get_asests_dirs('./capstone/agency/static/images',/\.(jpe?g|png|gif|svg)$/i))();

const webpackConfig = {
  // mode: "production", // "production" | "development" | "none"

  entry: {
    app: {import:['./capstone/agency/static/js/idleTimer.js',
      './capstone/agency/static/js/site.js',
    ]}, // string | object | array
    
    'plugins':{ import:[
      './node_modules/jquery/dist/jquery.min.js',
      './node_modules/jquery-easing/dist/jquery.easing.1.3.umd.min.js',
      './node_modules/bootstrap/dist/js/bootstrap.min.js',
      './node_modules/admin-lte/dist/js/adminlte.min.js',
      './node_modules/moment/dist/moment.js', 
      './node_modules/inputmask/dist/inputmask.min.js',
      './node_modules/bs-custom-file-input/dist/bs-custom-file-input.min.js', 
      './node_modules//select2/dist/js/select2.min.js'
    ],
    filename:'./capstone/agency/static/js/[name].bundle.js'
  },
  styles:[
    "./node_modules/animate.css/animate.css",
    "./capstone/agency/static/test/site.css",
    "./capstone/agency/static/css/site.css"
  ],
  
}, 
  output: {
    path: path.resolve(__dirname, "dist"), // string
    // the target directory for all output files
    // must be an absolute path (use the Node.js path module)
    filename: './capstone/agency/static/js/[name].js',
    assetModuleFilename: 'images/[name][ext]',
    assetModuleFilename: 'images/[hash][ext]',
    assetModuleFilename: 'images/[hash][ext][query]',
    clean: true,
    
  },
  target: 'web', // in order to ignore built-in modules like path, fs, etc. 
  module: {

    rules: [
      {
        test: /\.js$/,
        use: 'babel-loader',
        //exclude: /node_modules/
      },
      {
        test: /.s?css$/,
        //exclude: /node_modules/,
        use: [
          MiniCssExtractPlugin.loader, 
          { loader: "css-loader", options: { sourceMap: true } },
          { loader: "sass-loader", options: { sourceMap: true } },
        ],
      },
      {
        test: /\.ts(x)?$/,
        loader: 'ts-loader',
        exclude: /node_modules/
      },
      {
        test: /\.(png|svg|jpg|jpeg|gif)$/i,
        type: 'asset',
        generator: {
          filename: 'images/[name][ext]'
        },
        use: [
          {
            loader: 'file-loader', // Or `url-loader` or your other loader   
            options: {
              cache: true,
              outputPath: 'assets/images',
              esModule: false,
        }  
            }
              ]
        //use: [
        //  ImageMinimizerPlugin.loader
        //]
      },
      {
        test: /\.(woff|woff2|eot|ttf|otf)$/i,
        type: 'asset/resource',
        use: [
          {
            loader: 'file.loader',
            options: {
              cache: true,
              outputPath: 'assets/fonts',
              esModule: false,
        }
      }
    ]
  },
    ]
  },
  plugins: [
    new CopyPlugin({
      patterns: [
        //{ from: "./tsc-output/", to: "./capstone/" },
        { from: "./capstone/news", to: "./capstone/news" },
        { from: "./capstone/mail", to: "./capstone/mail" },
        { from: "./capstone/capstone", to: "./capstone/capstone" },
        { from: "./capstone/agency", to: "./capstone/agency" },
        { from: "./capstone/accounts", to: "./capstone/accounts" },

        { from: "./entrypoint.sh", to: "./capstone/" },
        { from: "./Dockerfile", to: "./capstone/" },
        { from: "./capstone/requirements.txt", to: "./capstone/" },
        { from: "./capstone/manage.py", to: "./capstone/" },
        { from: "./capstone/.env", to: "./capstone/" },
        {from:'node_modules/jquery-easing/dist/', to:'./capstone/agency/static/venders/jquery-easing/'},
        {from:'node_modules/jquery/dist/', to:'./capstone/agency/static/venders/jquery/'},
        {from:'node_modules/bootstrap/dist/', to:'./capstone/agency/static/venders/bootstrap/'},
        {from:'node_modules/@fortawesome/fontawesome-free/css/all.min.css', to:'./capstone/agency/static/venders/fontawesome/'},
        {from:'node_modules/@fortawesome/fontawesome-free/webfonts', to:'./capstone/agency/static/venders/fontawesome/webfonts'},
        {from:'node_modules/admin-lte/dist/', to:'./capstone/agency/static/venders/admin-lte/'},
        {from:"node_modules/icheck-bootstrap",to:'./capstone/agency/static/venders/icheck-bootstrap'},
        {from:"node_modules/select2/dist/",to:'./capstone/agency/static/venders/select2/'},
        {from:"node_modules/select2-bootstrap-5-theme/dist/",to:'./capstone/agency/static/venders/select2-bootstrap-5-theme/'},
        {from:'node_modules/moment/dist/', to:'./capstone/agency/static/venders/moment/'},
      ]
    }),
    
    new CleanWebpackPlugin(),
    new MiniCssExtractPlugin({filename:"./capstone/agency/static/css/[name].css"}),

    new webpack.ProgressPlugin({
      activeModules: false,
      entries: true,
      handler(percentage, message, ...args) {
        // custom logic
        console.log(`${(percentage * 100).toFixed()}% ${message} ${args}`);
      },
      modules: true,
      modulesCount: 5000,
      profile: false,
      dependencies: true,
      dependenciesCount: 10000,
      percentBy: null,
    }),
    /*
    new HtmlWebpackPlugin({  // Also generate a test.html
      filename: './dist/capstone/agency/templates/shared/layout.html',
      template: './capstone/agency/templates/shared/layout.html',
      minify: true
    }),
    */
    ...html_dirs,

      new ImageMinimizerPlugin({
        test: /\.(jpe?g|png|gif|svg)$/i,
        include: images_dirs.files,
        
        filter: (source, sourcePath) => {
          console.log('from image filter :'+sourcePath)
          // The `source` argument is a `Buffer` of source file
          // The `sourcePath` argument is an absolute path to source
          if (source.byteLength < 8192) {
            return false;
          }
  
          return true;
        },
        minimizerOptions: {
          // Lossless optimization with custom option
          // Feel free to experiment with options for better result for you
          plugins: [
            ['gifsicle', { interlaced: true }],
            ['jpegtran', { progressive: true }],
            ['optipng', { optimizationLevel: 5 }],
            [
              'svgo',
              {
                plugins: [
                  {
                    removeViewBox: false,
                  },
                ],
              },
            ],
          ],
        },
      }),
  ],
  optimization:{
    minimize: true,
    minimizer:[
      //new CssMinimizerPlugin(),
    ],
    splitChunks: {
      // include all types of chunks
      chunks: 'all',
    },
    
  },
  resolve: {
    extensions: [
      '.tsx',
      '.ts',
      '.js',
      '.css', 
      '.scss',
      '.json',
      '.html'
    ]
  }
};

module.exports = webpackConfig;
