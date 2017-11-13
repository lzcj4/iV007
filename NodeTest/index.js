function helloWorld() {
    console.log('helloWorld');
}

var app = require('http').createServer(handler)
var io = require('socket.io')(app);
var fs = require('fs');
var WebSocket = require('ws');

//app.listen(80);

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

function threadSleep(sleepDuration) {
    var now = new Date().getTime();
    while (new Date().getTime() < now + sleepDuration) { /* do nothing */ }
}


var i = 0;

function getData() {
    // var lines = fs.readFileSync("d:/log2.txt", 'utf8');
    // //jsonObj = JSON.stringify(data);
    // return lines;

    imgUrl = i % 2 == 0 ? "http://127.0.0.1:8000/static/images/ship.png" : "http://127.0.0.1:8000/static/images/ship2.png";
    var startX = 150,
        startY = 20,
        posStep = 200;
    var startWidth = 50,
        startHeight = 50,
        sizeStep = 2;
    var colors = ["red", "blue", "green", "black", "yellow", "red", "blue", "green", "black", "yellow", ]
    var objects = ["人物", "小汽车", "电脑", "桌子", "椅子"]
    var descriptions = ["男人", "红色丰田", "IBM笔记本", "白色办公桌", "断裂椅子"]
    var layerObjs = [];

    for (i = 0; i < 150; i++) {
        var itemObj = { "frame": i, "objects": [] };
        startX = 100;
        startY = 20 + i * 5;
        startWidth = 50;
        startHeight = 50;
        for (z = 0; z < 3; z++) {
            startX = 100;
            startY += 80;

            for (j = 0; j < 5; j++) {
                itemObj.objects.push({
                    "x": startX,
                    "y": startY,
                    "width": startWidth,
                    "height": startHeight,
                    "objid": "objid" + i + z + j,
                    "objtype": "car",
                    "drawcolor": colors[j],
                    "descs": [{
                            "desckey": "类型",
                            "descvalue": objects[j]
                        },
                        {
                            "desckey": "车辆车型",
                            "descvalue": descriptions[j]
                        }
                    ]
                });
                startX += posStep;
                startWidth += sizeStep;
                startHeight += sizeStep;
            }
        }


        layerObjs.push(itemObj);
    }

    data = {
        'id': i,
        'icon': imgUrl,
        'code': 200,
        'filename': 'test1.mp4',
        'overlays': layerObjs,
    };
    console.log(data);
    return JSON.stringify(data);
}

const wss = new WebSocket.Server({ port: 8080 });

wss.on('connection', function connection(ws) {
    ws.on('message', function incoming(message) {
        console.log('received: %s', message);
        threadSleep(4000);
        if (ws.readyState == WebSocket.OPEN) {
            ws.send(getData());
        }
    });

    ws.send(getData());
});

var isFirst = true;
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

    sendPosData(socket);

    // socket.emit('news', { hello: 'world' });
    socket.on('client', function(data) {
        console.log(data);

        socket.emit('server', getData());
        threadSleep(4000);
    });
});