// tutorial source: https://socket.io/get-started/chat/

var port = 6969;
var http = require('http').createServer();
var server = http.listen(port, function(){
  console.log('listening on *:' + port);
});

var io = require('socket.io')(server);

io.on('connection', function(socket){
  console.log('a user connected');
});


