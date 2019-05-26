export class Point {
   constructor(x : number, y : number){
       this.x = x;
       this.y = y;
   }
}

export class Line {
   constructor(x1 : number, y1 : number, x2 : number, y2 : number){
       this.p1 = new Point(x1, y1);
       this.p2 = new Point(x2, y2);
   }
}

function onLine(line : Line, p : Point) {   //check whether p is on the line or not
   if(p.x <= Math.max(l1.p1.x, l1.p2.x) && p.x <= Math.min(l1.p1.x, l1.p2.x) &&
      (p.y <= Math.max(l1.p1.y, l1.p2.y) && p.y <= Math.min(l1.p1.y, l1.p2.y))){
      return true;
   }
   return false;
}

function direction(a : Point, b: Point, c: Point) {
   let val = (b.y-a.y)*(c.x-b.x)-(b.x-a.x)*(c.y-b.y);
   // originally was == 0 
   if (Math.abs(val) < 1e-7)
      return 0;     //colinear
   else if(val < 0)
      return 2;    //anti-clockwise direction
   return 1;    //clockwise direction
}

export function isIntersect(l1 : Line, l2 : Line) {
   //four direction for two lines and points of other line
   let dir1 = direction(l1.p1, l1.p2, l2.p1);
   let dir2 = direction(l1.p1, l1.p2, l2.p2);
   let dir3 = direction(l2.p1, l2.p2, l1.p1);
   let dir4 = direction(l2.p1, l2.p2, l1.p2);
   
   if(dir1 != dir2 && dir3 != dir4)
      return true; //they are intersecting

   if(dir1 == 0 && onLine(l1, l2.p1)) //when p2 of line2 are on the line1
      return true;

   if(dir2 == 0 && onLine(l1, l2.p2)) //when p1 of line2 are on the line1
      return true;

   if(dir3 == 0 && onLine(l2, l1.p1)) //when p2 of line1 are on the line2
      return true;

   if(dir4 == 0 && onLine(l2, l1.p2)) //when p1 of line1 are on the line2
      return true;
         
   return false;
}