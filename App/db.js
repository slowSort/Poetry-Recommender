//https://www.terlici.com/2015/08/13/mysql-node-express.html

var mysql = require('mysql')
  , async = require('async')

var PRODUCTION_DB = 'sys'
  , TEST_DB = 'sys'

exports.MODE_TEST = 'mode_test'
exports.MODE_PRODUCTION = 'mode_production'

var state = {
  pool: null,
  mode: null,
}

exports.connect = function(mode, done) {
  state.pool = mysql.createPool({
    host: 'localhost',
    user: 'root',
    password: 'cKeecl00',
    database: mode === exports.MODE_PRODUCTION ? PRODUCTION_DB : TEST_DB
  })

  state.mode = mode
  done()
}

exports.getPoemByID = function(poem_id, callback) {
  var pool = state.pool
  if(!pool) return done(new Error('Missing database connection.'))

  var sql = 'SELECT * FROM poems WHERE poem_id = ?';
  pool.query('SELECT * FROM poems WHERE poem_id = ?', poem_id, function(err, results) {
    if (err) callback(error, null)
    var poem = {
      poem_id: results[0].poem_id,
      title: results[0].title,
      author: results[0].author,
      lines: JSON.parse(results[0].lines),
      wordcount: results[0].wordcount,
    }
    callback(null, poem);
  })
}

exports.getRandomPoem = function(callback) {
  var pool = state.pool
  if (!pool) return done(new Error('Missing database connection.'))

  pool.query('SELECT * FROM poems ORDER BY RAND() LIMIT 1', function(err, results) {
    if (err) callback(error, null)
    var poem = {
      poem_id: results[0].poem_id,
      title: results[0].title,
      author: results[0].author,
      lines: JSON.parse(results[0].lines),
      wordcount: results[0].wordcount,
    }
    callback(null, poem);
  })
}

exports.storeOpinion = function(poem_id, user_id, opinion) {
  var pool = state.pool
  if (!pool) return done(new Error('Missing database connection.'))
  var sql = 'INSERT INTO poems_users (poem_id, user_id, opinion) VALUES (?, ?, ?)' +
            'ON DUPLICATE KEY UPDATE opinion = opinion';
  var value = [poem_id, user_id, opinion];

  pool.query(sql, value, function(err, results) {
    if (err) throw err;
  })
}

exports.get = function() {
  return state.pool
}

exports.fixtures = function(data) {
  var pool = state.pool
  if (!pool) return done(new Error('Missing database connection.'))

  var names = Object.keys(data.tables)
  async.each(names, function(name, cb) {
    async.each(data.tables[name], function(row, cb) {
      var keys = Object.keys(row)
        , values = keys.map(function(key) { return "'" + row[key] + "'" })

      pool.query('INSERT INTO ' + name + ' (' + keys.join(',') + ') VALUES (' + values.join(',') + ')', cb)
    }, cb)
  }, done)
}

exports.drop = function(tables, done) {
  var pool = state.pool
  if (!pool) return done(new Error('Missing database connection.'))

  async.each(tables, function(name, cb) {
    pool.query('DELETE * FROM ' + name, cb)
  }, done)
}
