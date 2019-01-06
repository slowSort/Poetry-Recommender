var bodyParser = require('body-parser');
var urlencodedParser = bodyParser.urlencoded({extended: false});

module.exports = function(app){
  app.use(bodyParser.json());  //bodyParser

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
    //Add recommendation data to the server
    console.log("buttonName: " + req.body.buttonName)
    console.log("poem_id: " + req.body.poem_id)

    //Return a new poem
    app.db.getRandomPoem(function(err, poem){
      if (err) {
        console.log("poem not returned")
      } else {
        res.render('poem.ejs', {poems: poem});
      }
    })
  });

};
