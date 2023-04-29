const express = require('express')
var path = require('path');
var bodyParser = require('body-parser');
const app = express();
const port = 3000;
// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');  
//setup public folder
app.use(express.static('./public'));
// parse application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({ extended: false }));
// parse application/json
app.use(bodyParser.json());
    
app.get('/',function (req, res) {
    res.render('pages/login')
});

app.get('/cargo',function (req, res) {
    res.render('pages/cargo')
});

app.get('/captains',function (req, res) {
    res.render('pages/captain')
});

app.get('/ships',function (req, res) {
    res.render('pages/ships')
});

//our alert message midleware
function messages(req,res,next){
    var message;
    res.locals.message = message;
    next();
}

app.get('/login',messages,function (req, res) {
    res.render('pages/login');
});

app.listen(port, () => console.log(`MasterEJS app Started on port ${port}!`));