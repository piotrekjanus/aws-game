console.log('start tests');

import {Line, isIntersect} from "./rooms/geometry"

// TEST isIntersect
function shouldIntersect(l1:Line, l2:Line, id : number){
    if( !isIntersect(l1, l2)){
        console.log('TEST ' + id + ' FAILED');
    }
}

function shouldNotIntersect(l1:Line, l2:Line, id : number){
    if( isIntersect(l1, l2)){
        console.log('TEST ' + id + ' FAILED');
    }
}

function testIntersect(){
    let a = new Line(1,1,2,4);
    let b = new Line(1,4, 4,1);
    let c = new Line(3,3,4,6);
    let d = new Line(1,1,4,1);
    let e = new Line(0,2,2,2);
    let f = new Line(-3,5,10,5);
    shouldIntersect(a,b,1);
    shouldIntersect(a,e,2);
    shouldIntersect(a,d,3);
    shouldIntersect(b,d,4);
    shouldNotIntersect(a,c,5);
    shouldNotIntersect(b,c,6);
    shouldNotIntersect(d,c,7);
    shouldNotIntersect(e,c,8);
    shouldNotIntersect(e,b,9);
    shouldNotIntersect(e,d,10);
    shouldIntersect(c,f,11);
    shouldNotIntersect(a,f,12);
    shouldNotIntersect(b,f,13);
    shouldNotIntersect(d,f,14);
    shouldNotIntersect(e,f,15);
}

testIntersect();