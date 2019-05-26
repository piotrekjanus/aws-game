class Game{
    constructor(arg){
        console.log('Initialize Game object');
        this.players = [];
        this.state = [1,2,3];
    }

    add_player(player){
        this.players.push(player)
    }

    game_loop(){

    }

    server_update_loop(){
        for each (var player in this.players){
            player.emit(this.state)
        }
    }
}