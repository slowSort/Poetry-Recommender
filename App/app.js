var express = require ('express');
var todoController = require('./controllers/todoController');
var db = require('./db');

var app = express();

db.connect(db.MODE_PRODUCTION, ()=>{});
app.db = db;

//set up template engine
app.set('view engine', 'ejs');

//static files
app.use(express.static('./public'));

//fire controllers
todoController(app);

// Connect to MySQL on start
db.connect(db.MODE_PRODUCTION, function(err) {
  if (err) {
    console.log('Unable to connect to MySQL.')
    process.exit(1)
  } else {
    app.listen(3000, function() {
      console.log('Listening on port 3000...')
    })
  }
})
