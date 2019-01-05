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

  app.post('/todo', urlencodedParser, function(req,res){
    //could replace this with a new poem refresh
    data.push(req.body);
    res.json(data);
  });

};
