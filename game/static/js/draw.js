var CANVAS_WIDTH = 600;
var CANVAS_HEIGHT = 600;
var PLAYERS = [];
var PLAYER_COLORS = ['red', 'green', 'yellow', 'blue', 'cyan', 'magenta'];
var PLAYER_SIZE = 30;
function init() {
  window.requestAnimationFrame(draw);
}

function draw() {
  var ctx = document.getElementById('canvas').getContext('2d');

  ctx.globalCompositeOperation = 'destination-over';
  ctx.clearRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT); // clear canvas

  // config
  ctx.lineWidth = 5;

  // background
  ctx.strokeStyle = 'rgba(0, 0, 0, 1)';
  ctx.strokeRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);


  // Draw players
  for (var key in PLAYERS) {
    player = PLAYERS[key];
    ctx.fillStyle = PLAYER_COLORS[player.color]
    ctx.strokeStyle = PLAYER_COLORS[player.color]

    // draw trail
    ctx.beginPath();
    ctx.moveTo(player.x, player.y);

    for(i = player.trail.length - 1; 0 <= i; --i){
      let position = player.trail[i];
      ctx.lineTo(position.x, position.y);
    }
    ctx.stroke();

    // draw player
    x = player.x - PLAYER_SIZE/2;
    y = player.y - PLAYER_SIZE/2;
    ctx.fillRect(x, y, PLAYER_SIZE, PLAYER_SIZE);
  }

  window.requestAnimationFrame(draw);
}

init();