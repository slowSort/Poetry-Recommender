var bodyParser = require('body-parser');
var {PythonShell} = require('python-shell')
var urlencodedParser = bodyParser.urlencoded({extended: false});

var poetryList = [146, 147]

module.exports = function(app){
  app.use(bodyParser.json());  //bodyParser

  app.get('/home', function (req, res) {
    getPoem(function(poem){
      res.render('home', {poems: poem});
    });
  });

  app.get('/poemrec', function(req,res){
    PythonShell.run('./controllers/poemRec.py', null, function (err, results) {
      if (err) throw err;
      res.send(JSON.parse(results))
    });
  });

  app.post('/newpoem', urlencodedParser, function(req,res){
    //Add recommendation data to the server
    var poem_id = req.body.poem_id;
    var user_id = 1; //hardcoded user for now, as only 1 user
    var opinion = (req.body.buttonName === "like-button") ? 1 : 0;
    app.db.storeOpinion(poem_id, user_id, opinion);
    getPoem(function(poem){
      res.render('poem', {poems: poem});
    });
  });

  app.delete('/clear', function(req, res){
    app.db.clearRecommender();
    console.log('Cleared the recommender');
  });

  function getPoem(callback){
    let returnPoem = null
    if (poetryList.length !== 0) {
      app.db.getPoemByID(poetryList.shift(), function(err, poem){
        if (err) console.log("home getPoemByID: error");
        returnPoem = poem
        callback(returnPoem)
      })
    } else {
      app.db.getRandomPoem(function(err, poem){
        if (err) console.log("home getRandomPoem: error");
        returnPoem = poem
        callback(returnPoem)
      })
    }
    if (poetryList.length < 5) {
      PythonShell.run('./controllers/poemRec.py', null, function (err, results) {
        if (err) throw err;
        poetryList = JSON.parse(results)
      });
    }
    console.log(poetryList)
  }

};
