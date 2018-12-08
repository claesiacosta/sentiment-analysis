const app = require('./config/express')();
const config = require('./config/config')();
const fs = require('fs');
const https = require('https');
const logger = require('./app/utils/logger');
require('./config/database')(config.MONGODB_URI);

// Initialize the app
https.createServer({
  key: fs.readFileSync('server.key'),
  cert: fs.readFileSync('server.cert')
}, app).listen(config.PORT_HTTPS, () => {
  logger.success('Sentiment Analysis Server Running on Port ' + config.PORT_HTTPS);
});

// set up a route to redirect http to https
app.get('*', function(req, res) {
    res.redirect('https://' + req.headers.host + req.url);
    // Or, if you don't want to automatically detect the domain name from the request header, you can hard code it:
    // res.redirect('https://example.com' + req.url);
})

// have it listen on 8080
app.listen(config.PORT_HTTP);
