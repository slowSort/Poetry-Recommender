var bodyParser = require('body-parser');
var urlencodedParser = bodyParser.urlencoded({extended: false});

module.exports = function(app){
  app.get('/home', function(req,res){
    app.db.getRandomPoem(function(err, poem){
      if (err) {
        console.log("poem not returned")
      } else {
        res.render('home', {poems: poem});
      }
    })
  });

  app.post('/newpoem', urlencodedParser, function(req,res){
    app.db.getRandomPoem(function(err, poem){
      if (err) {
        console.log("poem not returned")
      } else {
        res.render('poem.ejs', {poems: poem});
      }
    })
  });

};
