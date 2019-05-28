// tutorial source: https://socket.io/get-started/chat/

var port = 6969;
var http = require('http').createServer();
var server = http.listen(port, function(){
  console.log('listening on *:' + port);
});

var io = require('socket.io')(server);

// define player id generator
function * generator_func(){
    var id = 0;
    while(true){
        yield id;
        id++;
    }
}
var id_generator = generator_func()

io.on('connection', function(socket){
  console.log('a user connected');
  var id = id_generator.next().value
  

});

