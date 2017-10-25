function helloWorld() {
    console.log('helloWorld');
}

var app = require('http').createServer(handler)
var io = require('socket.io')(app);
var fs = require('fs');

app.listen(80);

function handler(req, res) {
    fs.readFile(__dirname + '/index.js',
        function(err, data) {
            if (err) {
                res.writeHead(500);
                return res.end('Error loading index.html');
            }

            res.writeHead(200);
            res.end(data);
        });
}

function sleepFor(sleepDuration) {
    var now = new Date().getTime();
    while (new Date().getTime() < now + sleepDuration) { /* do nothing */ }
}

var x1 = 0;
var y1 = 0;
var x2 = 100;
var y2 = 100;
var i = 0;

function move(socket) {
    imgUrl = i % 2 == 0 ? "http://127.0.0.1:8000/static/images/ship.png" : "http://127.0.0.1:8000/static/images/ship2.png";
    p_name = i % 2 == 0 ? "张三" : "李四";
    p_sex = i % 2 == 0 ? "男" : "女";
    p_age = i % 2 == 0 ? 20 : 80;
    p_width = i % 2 == 0 ? 200 : 300;
    p_height = i % 2 == 0 ? 100 : 200;
    x = i % 2 == 0 ? x1 : x2;
    y = i++ % 2 == 0 ? y1 : y2;
    data = {
        'id': i,
        'name': p_name,
        'sex': p_sex,
        'age': p_age,
        'icon': imgUrl,
        'x': x,
        'y': y,
        'width': p_width,
        'height': p_height
    }
    console.log(data);
    socket.emit('server', data);
    x1 += 5;
    y1 += 5;
    x2 += 5;
    y2 += 5;
}

io.on('connection', function(socket) {
    x1 = y1 = 0;
    x2 = y2 = 100;
    i = 0;

    // while (true) {
    //     socket.emit('news', { 'x': x, 'y': y });
    //     x += 10;
    //     y += 10;
    //     sleepFor(1000);
    // }
    // var timer = setInterval(function() {
    //     move(socket);
    // }, 1 * 1000);

    move(socket);

    // socket.emit('news', { hello: 'world' });
    socket.on('client', function(data) {
        console.log(data);
        sleepFor(1000);
        move(socket);
    });
});