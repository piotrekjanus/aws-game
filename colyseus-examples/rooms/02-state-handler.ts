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

    @type("boolean")
    isRunning = false;

    createPlayer (id: string) {
        this.players[ id ] = new Player();
    }

    removePlayer (id: string) {
        delete this.players[ id ];
    }

    changeDirection (id: string, direction: number) {
        this.players[id].changeDirection(direction);
    }
}

export class StateHandlerRoom extends Room<State> {

    numberOfPlayers = 0;
    frame = 0;
    trailIncreaseInterval = 20;

    onInit (options) {
        console.log("StateHandlerRoom created!", options);
        this.setSimulationInterval((deltaTime) => this.update(deltaTime));
        this.setState(new State());
    }

    update (deltaTime) {
        if( this.state.isRunning){
            Object.keys(this.state.players).forEach(function (key){
                let player = this.state.players[key];
                if(this.frame % 20 == 0){
                    player.increaseTrail();
                    this.frame = 0;
                }
                let newX = player.x + player.direction_x;
                let newY = player.y + player.direction_y;
                // let intersectionsExits = this.checkIntersections(newX, newY, player.x, player.y);
                player.x = newX;
                player.y = newY;
                /*
                let outOfBounts = this.checkIfOutOfBounds(player);
                if(intersecionsExists || outOfBounds){
                    this.state.isRunning = false;
                }
                */
            }.bind(this));
            this.frame += 1;
        }
    }    

    checkIntersections(x1 : number, y1: number, x2 : number, y2: number, playerId : string){
        let newLine = new Line(x1, y1, x2, y2);
        let intersects = false;
        Object.keys(this.state.players).forEach(function (key){
            console.log('keyy ' + key);
            // some previous line already intersected
            let player = this.state.players[key];
            if( intersects  || player.trail == null){
                return;
            }
            // check for latest collision
            /*
            if( key != playerId && player.trail.length > 0){
                let lastPos = player.trail[player.trail.length - 1];
                currLine = new Line(player.x, player.y, lastPos.x, lastPos.y);
                if(isIntersect(newLine, currLine)){
                    intersects = true;
                    return;
                }
            }
            */

            // check for collision with rest of the trail
            for(let i = 0; i < player.trail.length - 1; ++i){
                let lineBegin = player.trail[i];
                let lineEnd = player.trail[i + 1];
                currLine = new Line(lineBegin.x, lineBegin.y, lineEnd.x, lineEnd.y);
                if(isIntersect(newLine, currLine)){
                    intersects = true;
                    return;
                }
            }
        }.bind(this, newLine, playerId, intersects));
        return intersects;
    }

    checkIfOutOfBounds(x : number, y: number){
        return ( x < 0 || x > 600 || y < 0 || y > 600)
    }

    onJoin (client) {
        // TODO Matchmaking
        this.state.createPlayer(client.sessionId);
        this.numberOfPlayers += 1;
        if(this.numberOfPlayers == 2){
            this.state.isRunning = true;
        }
    }
 
    onLeave (client) {
        this.state.removePlayer(client.sessionId);
    }

    onMessage (client, data) {
        console.log("StateHandlerRoom received message from", client.sessionId, ":", data);
        this.state.changeDirection(client.sessionId, data.direction);
    }

    onDispose () {
        console.log("Dispose StateHandlerRoom");
    }

}