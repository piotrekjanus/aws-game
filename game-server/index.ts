import path from 'path';
import express from 'express';
import serveIndex from 'serve-index';
import { createServer } from 'http';
import { Server } from 'colyseus';

// Import demo room handlers
import { GameRoom } from "./rooms/game-room";

const port = Number(process.env.PORT || 6969);
const app = express();

// Attach WebSocket Server on HTTP Server.
const gameServer = new Server({
  server: createServer(app)
});

// Register StateHandlerRoom as "state_handler"
gameServer.register("game-room", GameRoom);

gameServer.onShutdown(function(){
  console.log(`game server is going down.`);
});

gameServer.listen(port);

process.on("uncaughtException", (e) => {
    console.log(e.stack);
    process.exit(1);
});

console.log(`Listening on http://localhost:${ port }`);
