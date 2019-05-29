import { Room } from "colyseus";
import { Schema, type, MapSchema, ArraySchema } from "@colyseus/schema";
import {Line, isIntersect} from "./geometry"

export class Position extends Schema{
    @type("int32")
    x = 0;
    @type("int32")
    y = 0;

    constructor(x : number, y : number){
        super();
        this.x = x;
        this.y = y;
    }
}

export class Player extends Schema {
    @type("number")
    x = 100 + Math.floor(Math.random() * 400);

    @type("number")
    y = 100 + Math.floor(Math.random() * 400);

    @type("number")
    color = Math.floor(Math.random() * 6);

    @type("number")
    direction_x = 0;

    @type("number")
    direction_y = -1;

    @type([Position])
    trail = new ArraySchema<Position>();

    @type("string")
    username = "unknown";

    constructor(username : string){
        super();
        console.log('creating player : ', username);
        this.username = username;
    }

    increaseTrail(){
        this.trail.push( new Position(this.x, this.y) );
    }

    changeDirection(direction : number){
        let angle = Math.PI / 72 * direction;
        let sin = Math.sin(angle);
        let cos = Math.cos(angle);
        this.direction_x = this.direction_x * cos - this.direction_y * sin;
        this.direction_y = this.direction_x * sin + this.direction_y * cos;

        // normalize, because it slows down after some time
        let length = Math.sqrt(this.direction_x * this.direction_x + this.direction_y * this.direction_y);
        this.direction_x /= length;
        this.direction_y /= length;
    }
}

export class State extends Schema {
    @type({ map: Player })
    players = new MapSchema<Player>();

    createPlayer (id: string, username) {
        this.players[ id ] = new Player(username);
    }

    removePlayer (id: string) {
        delete this.players[ id ];
    }

    changeDirection (id: string, direction: number) {
        this.players[id].changeDirection(direction);
    }
}

enum GameState{
    WaitingForPlayers,
    Countdown,
    Game,
    GameOver,
}

export class GameRoom extends Room<State> {

    maxClients = 2;
    increaseTrailIter = 0;
    trailIncreaseInterval = 20;
    gameState = GameState.WaitingForPlayers;
    countdown = 3;
    countdownInterval = 100;
    countdownIter = 0;

    onInit (options) {
        console.log("StateHandlerRoom created!", options);
        this.setSimulationInterval((deltaTime) => this.update(deltaTime));
        this.setState(new State());
    }

    update (deltaTime) {
        if( this.gameState == GameState.Countdown){
            if( this.countdownIter % this.countdownInterval  == 0){
                if( this.countdown < 0){
                    this.gameState = GameState.Game;
                } else {
                    console.log('countdown : ' + this.countdown);
                    this.broadcast({isCountdown : true, countdown : this.countdown});
                    this.countdown -= 1;
                }
            }
            this.countdownIter += 1;
        } else if( this.gameState == GameState.Game){
            Object.keys(this.state.players).forEach(function (key){
                let player = this.state.players[key];
                if(this.increaseTrailIter % this.trailIncreaseInterval == 0){
                    player.increaseTrail();
                }
                let newX = player.x + player.direction_x;
                let newY = player.y + player.direction_y;
                let intersectionsExist = this.checkIntersections(newX, newY, player.x, player.y, key);
                // let intersectionsExist = false;
                player.x = newX;
                player.y = newY;
                let outOfBounds = this.checkIfOutOfBounds(player.x, player.y);
                if(intersectionsExist || outOfBounds){
                    console.log("GAME OVER!!")
                    this.gameState = GameState.GameOver;
                    this.sendResults(key);
                }
            }.bind(this));
            if(this.increaseTrailIter >= this.trailIncreaseInterval){
                this.increaseTrailIter = 0;
            } else{
                this.increaseTrailIter += 1;
            }
        }
    }    

    checkIntersections(x1 : number, y1: number, x2 : number, y2: number, playerId : string){
        let newLine = new Line(x1, y1, x2, y2);
        let intersects = false;
        Object.keys(this.state.players).forEach(function (key){
            // some previous line already intersected
            if( intersects || playerId == key){
                return;
            }

            let player = this.state.players[key];

            if( player.trail.length > 0 ){
                let start = player.trail[player.trail.length - 1];
                let trailLine = new Line(start.x, start.y , player.x, player.y);
                intersects = intersects || isIntersect(trailLine, newLine);
                if( intersects){
                    return;
                }
            }

            for(let i = 0; i < player.trail.length - 1; i++ ){
                let start = player.trail[i];
                let stop = player.trail[i + 1];
                let trailLine = new Line(start.x, start.y , stop.x, stop.y);
                intersects = intersects || isIntersect(trailLine, newLine);
                if( intersects ){
                    console.log('intersects debug')
                    console.log(key)
                    console.log(playerId)
                    console.log(newLine.p1.x + ' ' + newLine.p1.y + ' ' + newLine.p2.x + ' ' + newLine.p2.y)
                    console.log(trailLine.p1.x + ' ' + trailLine.p1.y + ' ' + trailLine.p2.x + ' ' + trailLine.p2.y)
                    console.log('intersects debug - end')
                }
            }
            
        }.bind(this));
        return intersects;
    }

    checkIfOutOfBounds(x : number, y: number){
        return ( x < 0 || x > 600 || y < 0 || y > 600)
    }

    sendResults(looser){
        for(let i = 0; i < this.clients.length; i ++){
            if( this.clients[i].sessionId == looser){
                this.send(this.clients[i], {gameResults : 'looser' })
            } else{
                this.send(this.clients[i], {gameResults : 'winner' })
            }
        }
    }

    requestJoin (options, isNewRoom: boolean) {
        return (options.create)
            ? (options.create && isNewRoom)
            : this.clients.length > 0;
    }

    onJoin (client, options) {
        this.state.createPlayer(client.sessionId, options.username);
        if(this.clients.length == 2){
            this.gameState = GameState.Countdown
        }
    }

    onLeave (client) {
        this.state.removePlayer(client.sessionId);
    }

    onMessage (client, data) {
        console.log("GameRoom received message from", client.sessionId, ":", data);
        this.state.changeDirection(client.sessionId, data.direction);
    }

    onDispose () {
        console.log("Dispose GameRoom");
    }
}