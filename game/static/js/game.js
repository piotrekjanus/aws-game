// test canvas
var canvas = document.getElementById("game-canvas");
var ctx = canvas.getContext("2d");
ctx.fillStyle = "#FF0000";
// ctx.fillRect(0, 0, 150, 75);
ctx.fillRect(0, 0, 300, 150);

// test sockets:
var socket = io('localhost:6969')

// test game loop
var game_loop = function(){
    console.log('game')
}   

var refresh_rate = 1000

var interval = window.setInterval( 
        game_loop, 
        refresh_rate)