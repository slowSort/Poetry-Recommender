var bodyParser = require('body-parser');
var {PythonShell} = require('python-shell')
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

  app.get('/recommendations', function(req,res){
    PythonShell.run('./controllers/poemRec.py', null, function (err, results) {
      if (err) throw err;
      res.send(JSON.parse(results))
    });
  });

  app.post('/newpoem', urlencodedParser, function(req,res){
    //Add recommendation data to the server
    var poem_id = req.body.poem_id;
    var user_id = 1; //hardcoded user for now, as only 1 user
    var opinion;

    if (req.body.buttonName === "like-button") {
      opinion = 1;
    } else {
      opinion = -1;
    }

    //app.db.storeOpinion(poem_id, user_id, opinion);

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
