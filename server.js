var express = require('express');
var app = express();
const path = require('path');
var _ = require('./common/lodash.min.js')
const fs = require('fs');

app.get('/index.html',function (req, res) {
  res.sendFile(path.join(__dirname, 'local.html'));
})

app.get('*',function (req, res) {
  console.log('GET * path=' + decodeURIComponent(req.path));
  res.sendFile(path.join(__dirname, decodeURIComponent(req.path)));
  
})

var port = 3001

app.listen(port);

console.log('Listening on http://localhost:' + port)

/*app.get('/common/*',function (req, res) {
  res.sendFile(path.join(__dirname, req.path));
})

app.get('/icon/*',function (req, res) {
  res.sendFile(path.join(__dirname, req.path));
})

app.get('/images/*',function (req, res) {
  res.sendFile(path.join(__dirname, req.path));
})

app.get('/index.js',function (req, res) {
  res.sendFile(path.join(__dirname, req.path));
})

app.get('/index.html',function (req, res) {
  res.sendFile(path.join(__dirname, req.path));
})*/

  /*var filePath = path.join(__dirname, req.path);
  if (filePath == './')
    filePath = './index.html';

  filePath = decodeURIComponent(filePath)
  console.log('GET * path=' + filePath);

  var extname = path.extname(filePath);

  const map = {
    '.ico': 'image/x-icon',
    '.html': 'text/html',
    '.js': 'text/javascript',
    '.json': 'application/json',
    '.css': 'text/css',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.wav': 'audio/wav',
    '.mp3': 'audio/mpeg',
    '.svg': 'image/svg+xml',
    '.pdf': 'application/pdf',
    '.doc': 'application/msword'
  };
  var contentType = map[extname] || 'text/html'

  res.set({ 'content-type': 'text/html; charset=utf-8' });
  //res.set({ 'content-type': contentType });

  //const stream = fs.createReadStream(filePath, {encoding: 'utf-8'});

  //stream.on('error', function(error) {
  //  res.writeHead(404, 'Not Found');
  //  res.end();
  //});

  //stream.pipe(new HtmlSpacer()).pipe(res)
  //stream.pipe(res)

  fs.readFile(filePath, function(error, content) {
    if (error) {
      if(error.code == 'ENOENT'){
        console.log('error ENOENT... filepath: ' + filePath);
        fs.readFile('./404.html', function(error, content) {
          res.writeHead(200, { 'Content-Type': 'text/html' });
          res.end(content, 'utf-8');
        });
      } else {
        console.log('error...');
        res.writeHead(500);
        res.end('Sorry, check with the site admin for error: '+error.code+' ..\n');
        res.end();
      }
    } else {
      console.log('should be working no error...');
      res.writeHead(200, { 'Content-Type': 'text/plain' });
      res.end(content, 'utf-8');
    }
  })*/
