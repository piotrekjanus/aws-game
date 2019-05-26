// connect to colyseus
var host = window.document.location.host.replace(/:.*/, '');
var port = 6969
// var client = new Colyseus.Client(location.protocol.replace("http", "ws") + host + ':' + port);
var client = new Colyseus.Client("ws://localhost:6969");
var room = client.join("state_handler");

room.onJoin.add(function() {
console.log('chociaż tutaj');

// listen to patches coming from the server
  room.state.players.onAdd = function(player, sessionId) {
    console.log("boi, I'm in");
    // listen to patches coming from the server
    console.log('new player!' + player);
    PLAYERS[sessionId] = player;
  }

  room.state.players.onRemove = function(player, sessionId) {
    delete PLAYERS[sessionId];
  }

  room.state.players.onChange = function (player, sessionId) {
    PLAYERS[sessionId] = player;
  }
});


// controls
window.addEventListener("keydown", function (e) {
console.log(e.which);

if (e.which === 39) {
  right();
} else if (e.which === 37) {
  left();
}

});

function right () {
  room.send({ direction: 1 });
}

function left () {
  room.send({ direction: -1 })
}
