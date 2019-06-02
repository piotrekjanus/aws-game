// connect to colyseus
var host = window.document.location.host.replace(/:.*/, '');
var port = 6969
// var client = new Colyseus.Client(location.protocol.replace("http", "ws") + host + ':' + port);
console.log('connecting to host: ' + config.game_host);
var client = new Colyseus.Client("ws://" + config.game_host);

var room;

function addHandlers(room){

  room.onJoin.add(function() {

  // listen to patches coming from the server
    room.state.players.onAdd = function(player, sessionId) {
      // listen to patches coming from the server
      console.log('new player!' + player);
      PLAYERS[sessionId] = player;
      updatePlayerInfo();
    }

    room.state.players.onRemove = function(player, sessionId) {
      delete PLAYERS[sessionId];
      updatePlayerInfo();
    }

    room.state.players.onChange = function (player, sessionId) {
      PLAYERS[sessionId] = player;
    }

    room.onMessage.add( function (message){
      if(message.isCountdown){
        let current = message.countdown;
        
        console.log('countdown: ' +  (current==1));
        CountDown(current);
        
      } else if(message.gameResults){
        // TODO, display results
        // message.gameResults == loser id (client.id is a thing or something like that)
        GameOver(message.gameResults);
      }
      else{
        CountDown('');
      }
    })

  });
  
}

function CountDown(number){
  let counter = document.getElementById("counter");
  if(number == 0){
    counter.innerText = '';
  } else{
    counter.innerText = number;
  }
}

function GameOver(results){
  console.log('GAME OVER!');
  usernames = Object.values(room.state.players).map(function(x){return x.username;});
  console.log(usernames);
  console.log(room.state.players)
  // getScore(results, usernames);
}

function getScore(message, players){
  $(document).ready(function () {
  $.ajax({
    url: "/results/",
    type: "POST",
    data: {info: message, users: JSON.stringify(players)},
    success:function(response){},
    complete:window.location.href = '/game/',
    error:function (xhr, textStatus, thrownError){
        alert("Error while saving match results");
    }
  });
});
}

function joinRoomInTable(roomId){
  if(!room){
    // let roomId = document.getElementById("join_room_name_input").value;
    room = client.join(roomId, {username: logged_user});
    addHandlers(room);
  }
}

function joinSpecificRoom(){
  if(!room){
    let roomId = document.getElementById("join_room_name_input").value;
    room = client.join(roomId, {username: logged_user});
    addHandlers(room);
  }
}

function createNewRoom(){
  if(!room){
    room = client.join("game-room", { create: true, username: logged_user});
    addHandlers(room);
  }
}

function quitGame(){
  if(room){
    room.leave();
    room = null;
    PLAYERS = {};
    updatePlayerInfo();
  }
}


function updateRooms(){

  if(client){
    let oldTbody = document.getElementsByTagName('tbody')[0];
    // console.log(oldTbody);
    let newTbody = document.createElement('tbody');
    client.getAvailableRooms('game-room', function(rooms, err) {
      rooms.forEach(function(room){
        // Insert a row at the end of the table
        let newRow = newTbody.insertRow(-1);
        // Insert a cell in the row at index 0
        let newCell = newRow.insertCell(0);
        // Append a text node to the cell
        let newText = document.createTextNode(room.roomId);

        newCell.appendChild(newText);
        newCell = newRow.insertCell(1);
        newText = document.createTextNode(room.clients);
        newCell.appendChild(newText);
        newCell = newRow.insertCell(2);
        newText = document.createElement("button");
        newText.innerHTML = "Join";
        newText.className += "btn btn-primary";
        newText.addEventListener ("click", function() {
          joinRoomInTable(newRow.getElementsByTagName("td")[0].innerText);
        });
        newCell.appendChild(newText);
      });
    });

    oldTbody.parentNode.replaceChild(newTbody, oldTbody);
  }
}

function updatePlayerInfo()
{
  let oldTbody = document.getElementsByClassName('player_table')[0];
  let newTbody = document.createElement('tbody');
  newTbody.className += "player_table";
  for (var key in PLAYERS) {
    player = PLAYERS[key];
    let newRow = newTbody.insertRow(-1);
    let newCell = newRow.insertCell(0);
    let newText = document.createTextNode(player.username);
    newCell.appendChild(newText);
    newCell = newRow.insertCell(1);
    // td.style.backgroundColor='#FF8000'
    newCell.style.backgroundColor = PLAYER_COLORS[player.color]
    // newText = document.createTextNode(PLAYER_COLORS[player.color]);      
    // newCell.appendChild(newText);
  
    player = PLAYERS[key];
    console.log(player);
  };
  oldTbody.parentNode.replaceChild(newTbody, oldTbody);
}

window.setInterval(updateRooms, 1000);

var steeringInterval;
var steeringIntervalTime = 60;
var isSteering = false;

// controls
window.addEventListener("keydown", function (e) {
  if( e.repeat ){
    return;
  }
  if (e.which === 39) {
    startSteering(1);
  } else if (e.which === 37) {
    startSteering(-1);
  }
});

// controls
window.addEventListener("keyup", function (e) {
  if( e.repeat ){
    return;
  }
  if (e.which === 39 || e.which === 37) {
    stopSteering();
  }
});

function startSteering(direction){
  if( isSteering ){
    stopSteering(); 
  }
  isSteering = true;
  steeringInterval = window.setInterval(function(){
    if( room ){
      room.send({ direction: direction });
      console.log('turn turn');
    }
  }, steeringIntervalTime);
}

function stopSteering(){
  clearInterval(steeringInterval);
  isSteering = false;
}