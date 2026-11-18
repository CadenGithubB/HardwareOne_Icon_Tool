// Pixel plans for UI drawing. No browser or application state is accessed here.
export const designs = {};
let p;
const start=()=>p=Array.from({length:32},()=>Array(32).fill(0));
function rect(x,y,w,h,v=1){for(let j=y;j<y+h;j++)for(let i=x;i<x+w;i++)if(i>=0&&i<32&&j>=0&&j<32)p[j][i]=v;}
function line(x1,y1,x2,y2,w=2,v=1){for(let y=0;y<32;y++)for(let x=0;x<32;x++){let dx=x2-x1,dy=y2-y1,t=Math.max(0,Math.min(1,((x-x1)*dx+(y-y1)*dy)/(dx*dx+dy*dy||1)));if(Math.hypot(x-x1-t*dx,y-y1-t*dy)<=w/2)p[y][x]=v;}}
function ring(cx,cy,r,w=2){for(let y=0;y<32;y++)for(let x=0;x<32;x++)if(Math.abs(Math.hypot(x-cx,y-cy)-r)<=w/2)p[y][x]=1;}
function disk(cx,cy,r,v=1){for(let y=0;y<32;y++)for(let x=0;x<32;x++)if(Math.hypot(x-cx,y-cy)<=r)p[y][x]=v;}
function path(a,w=2){for(let i=1;i<a.length;i++)line(...a[i-1],...a[i],w);}
function box(x,y,w,h,t=2){rect(x,y,w,h);rect(x+t,y+t,w-2*t,h-2*t,0);}
const save=n=>designs[n]=p.map(r=>r.slice());
const restore=n=>p=designs[n].map(r=>r.slice());
const mirror=a=>a.map(r=>r.slice().reverse());
function file(){start();rect(6,4,2,24);rect(6,26,20,2);rect(24,10,2,18);rect(6,4,14,2);for(let i=0;i<=6;i++)rect(18+i,4+i,2,2);rect(18,5,2,7);rect(18,10,7,2);}
for(let sad of [false,true]){start();ring(15.5,15.5,11.5,2);rect(10,10,3,4);rect(19,10,3,4);path(sad?[[10,21],[12,18],[19,18],[21,21]]:[[10,19],[12,22],[19,22],[21,19]],2);save(sad?'frowny':'smiley');}
start();box(4,10,24,17);rect(4,6,10,6);rect(6,8,6,3,0);save('folder');file();save('file');
for(let n=0;n<4;n++){start();disk(15.5,25.5,1.6);for(let j=1;j<=n;j++){let r=j*6;for(let y=3;y<24;y++)for(let x=3;x<29;x++)if(Math.abs(x-15.5)<=25-y&&Math.abs(Math.hypot(x-15.5,y-25)-r)<1.1)rect(x,y,1,1);}save('wifi_'+n);}
start();rect(5,14,20,4);for(let y=5;y<=26;y++){let edge=27-Math.floor(Math.abs(y-15.5));rect(edge-3,y,4,1);}save('arrow_right');designs.arrow_left=mirror(designs.arrow_right);designs.arrow_up=designs.arrow_left[0].map((_,y)=>designs.arrow_left.map(r=>r[y]));designs.arrow_down=designs.arrow_up.slice().reverse().map(r=>r.slice());
start();path([[20,6],[10,15.5],[20,25]],3);save('chevron_left');designs.chevron_right=mirror(designs.chevron_left);
for(let n of [0,25,50,75,100]){start();box(3,9,24,14);rect(27,13,3,6);for(let j=0;j<n/25;j++)rect(6+j*5,12,3,8);save('battery_'+n);}
start();box(3,9,24,14);rect(27,13,3,6);path([[17,12],[12,16],[18,16],[14,19]],1.8);save('battery_charging');
start();rect(5,14,22,4);rect(14,5,4,22);save('plus');start();rect(5,14,22,4);save('minus');start();path([[6,16],[12,22],[26,8]],3);save('check');start();line(7,7,24,24,3);line(24,7,7,24,3);save('close');
start();for(let y of [7,14,21])rect(5,y,22,3);save('menu');start();ring(13.5,13.5,7.75,2);line(19,19,26,26,3);save('search');start();ring(15.5,15.5,11.5,2);rect(14,9,4,3);rect(14,15,4,8);save('info');
start();path([[15.5,4],[28,26],[3,26],[15.5,4]],2);rect(14,12,4,7);rect(14,22,4,2);save('warning');
start();ring(15.5,15.5,8.5,2);ring(15.5,15.5,3.5,2);for(let a of [[14,3,4,5],[14,24,4,5],[3,14,5,4],[24,14,5,4]])rect(...a);for(let a of [[7,7,10,10],[21,21,24,24],[7,24,10,21],[21,10,24,7]])line(...a,3);save('settings');
start();path([[6,19],[5,16],[5,12],[8,8],[12,6],[23,6]],2);path([[20,3],[23,6],[20,9]],2);{const a=p.map(r=>r.slice());for(let y=0;y<32;y++)for(let x=0;x<32;x++)if(a[31-y][31-x])p[y][x]=1;}save('refresh');
restore('wifi_3');line(4,4,27,27,5,0);line(4,4,27,27,2);save('wifi_off');
start();path([[12,4],[25,4],[25,27],[7,27],[7,9],[12,4]],2);for(let x of [13,17,21])rect(x,7,2,6);box(10,18,12,7);save('sdcard');
start();rect(5,8,22,2);box(11,4,10,5);rect(8,12,2,15);rect(22,12,2,15);rect(8,26,16,2);rect(13,13,2,10);rect(17,13,2,10);save('trash');
for(let down of [false,true]){start();rect(4,23,2,5);rect(26,23,2,5);rect(4,26,24,2);rect(14,6,4,15);path(down?[[8,14],[15.5,21],[23,14]]:[[8,12],[15.5,5],[23,12]],2);save(down?'download':'upload');}
start();path([[7,20],[22,5],[27,10],[12,25],[5,27],[7,20]],2);line(19,8,24,13,2);line(7,20,12,25,2);save('edit');
start();box(5,5,22,22);box(10,5,12,9);rect(17,7,2,5);box(10,18,12,9);save('save');
start();path([[3,15],[15.5,4],[28,15]],2);rect(6,14,2,14);rect(24,14,2,14);rect(6,26,20,2);box(12,18,8,10);rect(14,26,4,2,0);save('home');
start();path([[12,5],[4,13],[12,21]],2);path([[5,13],[21,13],[26,18],[26,26]],2);save('back');
for(let open of [false,true]){start();box(6,14,20,14);path(open?[[11,14],[11,8],[14,5],[20,5],[23,8]]:[[10,14],[10,8],[13,5],[18,5],[21,8],[21,14]],2);disk(15.5,20,2);rect(15,20,2,5);save(open?'unlock':'lock');}
file();for(let y of [14,18,22])rect(10,y,12,2);save('file_text');
file();path([[13,15],[10,18],[13,21]],1.8);path([[19,15],[22,18],[19,21]],1.8);line(17,14,15,22,1.8);save('file_code');
file();disk(11.5,14.5,1.5);disk(21.5,16.5,1.5);path([[10,23],[15,17],[21,23],[10,23]],1.8);save('file_image');
file();for(let y=7;y<=19;y+=3)rect(y%2?12:14,y,2,2);box(12,21,5,4,1);save('file_zip');
file();path([[13,14],[11,14],[11,17],[10,18],[11,19],[11,22],[13,22]],1);path([[19,14],[21,14],[21,17],[22,18],[21,19],[21,22],[19,22]],1);rect(15,16,2,2);rect(15,20,2,2);rect(14,22,2,1);rect(14,23,1,1);save('file_json');
const font={P:['110','101','110','100','100'],D:['110','101','101','101','110'],F:['111','100','110','100','100'],0:['111','101','101','101','111'],1:['010','110','010','010','111']};
function text(s,x,y){for(let c of s){font[c].forEach((r,j)=>[...r].forEach((v,i)=>{if(v==='1')rect(x+i,y+j,1,1);}));x+=4;}}
file();text('PDF',10,16);rect(10,23,12,2);save('file_pdf');file();text('01',12,14);text('10',12,20);save('file_bin');
start();ring(15.5,15.5,6.5,2);for(let a of [[14,2,4,5],[14,25,4,5],[2,14,5,4],[25,14,5,4]])rect(...a);for(let a of [[6,6,8,8],[23,23,25,25],[6,25,8,23],[23,8,25,6]])line(...a,2);save('sun');
start();disk(15,16,11.5);disk(20,11,10.5,0);save('moon');
start();path([[6,23],[9,19],[9,11],[12,7],[19,7],[22,11],[22,19],[25,23],[6,23]],2);rect(14,4,4,3);rect(13,27,6,2);save('notify_bell');
start();box(12,12,8,8);for(let a of [[7,10],[7,21],[24,10],[24,21]]){}path([[8,8],[5,12],[5,19],[8,23]],2);path([[23,8],[26,12],[26,19],[23,23]],2);path([[4,4],[1,10],[1,21],[4,27]],1.8);path([[27,4],[30,10],[30,21],[27,27]],1.8);save('notify_espnow');
start();box(4,4,8,8);box(20,20,8,8);path([[15,8],[24,8],[24,15]],2);path([[20,12],[24,16],[28,12]],2);path([[16,24],[8,24],[8,16]],2);path([[4,20],[8,16],[12,20]],2);save('notify_automation');
start();for(let y of [4,13,22]){box(5,y,22,7);rect(8,y+2,2,3);rect(14,y+2,10,3);}save('notify_server');
start();box(5,6,22,20);path([[8,17],[11,17],[14,11],[18,21],[21,15],[24,15]],1.8);save('notify_sensor');
start();box(7,5,18,23);box(12,3,8,6);for(let y of [12,17,22]){rect(10,y,2,2);rect(15,y,7,2);}save('notify_logging');
start();box(10,8,17,20);path([[6,23],[4,23],[4,3],[20,3],[20,5]],2);rect(14,14,9,2);rect(14,19,9,2);save('notify_files');
function chip(){start();box(8,8,16,16);for(let n of [10,15,20]){rect(n,3,2,5);rect(n,24,2,5);rect(3,n,5,2);rect(24,n,5,2);}}
chip();rect(12,12,8,8);save('notify_system');
function term(){start();box(4,6,24,20);path([[8,12],[12,16],[8,20]],1.8);rect(16,20,7,2);}
term();save('notify_cli');
start();box(6,3,20,26);box(9,6,14,15);rect(10,24,3,2);rect(19,24,3,2);save('device');
start();ring(15.5,15.5,11.5,2);path([[20,10],[12,13],[11,21],[19,18],[20,10]],1.8);line(12,13,19,18,1.8);save('compass');
start();path([[6,24],[16,16],[16,5]],2);path([[16,16],[27,23]],2);path([[12,8],[16,4],[20,8]],2);path([[6,18],[5,25],[12,25]],2);path([[22,24],[28,24],[27,18]],2);save('imu_axes');
start();ring(12.5,23,5,2);path([[9,19],[9,6],[11,4],[14,4],[16,6],[16,19]],1.8);rect(12,10,2,13);disk(12.5,23,2);for(let y of [7,12,17])rect(21,y,6,2);save('thermal');
start();ring(15.5,15.5,11.5,2);ring(15.5,15.5,6,1.7);line(15.5,15.5,23,7,2);disk(15.5,15.5,1.5);disk(10,20,1.5);save('tof_radar');
function bt(){start();path([[14,4],[23,11],[9,23]],2);path([[14,27],[23,20],[9,8]],2);rect(13,4,2,24);}
bt();save('bt_idle');bt();line(4,4,27,27,5,0);line(4,4,27,27,2);save('bt_off');bt();path([[26,10],[29,13],[29,18],[26,21]],1.8);save('bt_advertising');bt();rect(3,14,4,4);rect(26,14,4,4);save('bt_connected');
start();path([[4,12],[10,12],[17,6],[17,25],[10,19],[4,19],[4,12]],2);path([[22,11],[24,14],[24,17],[22,20]],1.8);path([[26,7],[29,12],[29,19],[26,24]],1.8);save('speaker');
start();box(8,3,16,26);rect(14,6,4,2);rect(14,24,4,2);save('smartphone');
start();box(3,11,11,10);box(18,11,11,10);rect(14,13,4,2);path([[3,12],[1,8],[5,6]],1.8);path([[28,12],[30,8],[26,6]],1.8);save('smart_glasses');
start();box(6,5,20,17);path([[6,21],[2,26],[29,26],[25,21]],1.8);rect(12,23,8,2);save('laptop');
start();path([[5,19],[5,12],[8,7],[12,5],[19,5],[23,7],[26,12],[26,19]],2);box(4,16,7,12);box(21,16,7,12);save('headphones');
start();box(8,8,16,16);rect(11,2,10,6);rect(11,24,10,6);path([[15,12],[15,17],[19,17]],1.8);save('watch');
start();path([[4,10],[27,10],[29,24],[25,26],[20,21],[11,21],[6,26],[2,24],[4,10]],2);rect(7,13,2,7);rect(5,15,6,2);rect(21,13,3,3);rect(25,17,3,3);save('gamepad');
start();ring(15.5,16,10.5,2);rect(11,3,10,10,0);rect(14,3,4,14);save('power');
chip();box(12,12,8,8);save('memory');term();rect(4,6,24,3);save('terminal');
start();ring(15.5,10,5.5,2);path([[5,27],[6,23],[10,19],[21,19],[25,23],[26,27],[5,27]],2);save('user');
start();path([[9,20],[9,11],[12,7],[19,7],[22,11],[22,20],[9,20]],2);rect(7,20,18,2);rect(11,22,2,7);rect(19,22,2,7);line(4,4,7,7,1.8);line(27,4,24,7,1.8);rect(15,1,2,3);save('led');
start();box(4,11,24,17);line(7,10,22,3,2);ring(11,19,4,2);rect(19,15,5,2);rect(19,20,5,2);save('radio');
start();path([[10,17],[10,7],[12,5],[14,7],[14,15],[14,4],[16,2],[18,4],[18,15],[18,7],[20,5],[22,7],[22,17],[22,11],[24,9],[26,11],[26,23],[21,28],[13,28],[5,19],[5,16],[7,15],[10,18]],1.8);save('gesture');
start();ring(15.5,15.5,11.5,2);rect(15,8,2,9);rect(15,15,8,2);save('clock');
function bond(){start();path([[14,10],[11,7],[7,7],[4,10],[4,18],[7,21],[11,21],[14,18]],2);path([[17,13],[20,10],[24,10],[27,13],[27,21],[24,24],[20,24],[17,21]],2);line(10,17,21,14,2);}
bond();save('bond');bond();line(4,4,27,27,5,0);line(4,4,27,27,2);save('bond_off');
start();path([[5,12],[8,8],[25,8]],2);path([[22,5],[25,8],[22,11]],2);{const a=p.map(r=>r.slice());for(let y=0;y<32;y++)for(let x=0;x<32;x++)if(a[31-y][31-x])p[y][x]=1;}rect(11,15,10,2);save('bond_sync');
start();path([[12,8],[9,5],[6,5],[3,8],[3,16],[6,19],[9,19],[12,16]],2);ring(20,18,6,2);line(24,23,28,27,2);line(9,13,15,13,2);save('bond_search');

// Greedy straight UI strokes, including diagonals. The drawing is still entered
// for optional entry with the editor's Line tool.
export function strokes(bitmap){let a=bitmap.map(r=>r.slice()),out=[];while(a.some(r=>r.some(Boolean))){let best=[];for(let y=0;y<32;y++)for(let x=0;x<32;x++)if(a[y][x])for(let [dx,dy] of [[1,0],[0,1],[1,1],[-1,1]]){let run=[],i=x,j=y;while(i>=0&&i<32&&j<32&&a[j][i]){run.push([i,j]);i+=dx;j+=dy;}if(run.length>best.length)best=run;}out.push([best[0],best.at(-1)]);for(let [x,y]of best)a[y][x]=0;}return out;}

// Rebuilt expansion: square 2px strokes, deliberate contours and explicit symmetry.
const symmetry = {};
function dot(x,y,v=1){if(x>=0&&x<32&&y>=0&&y<32)p[y][x]=v;}
function L(x0,y0,x1,y1,w=2){
  // Bresenham with a square brush: no round endcaps or floating point offsets.
  let dx=Math.abs(x1-x0),sx=x0<x1?1:-1,dy=-Math.abs(y1-y0),sy=y0<y1?1:-1,err=dx+dy;
  for(;;){rect(x0,y0,w,w);if(x0===x1&&y0===y1)break;let e=2*err;if(e>=dy){err+=dy;x0+=sx;}if(e<=dx){err+=dx;y0+=sy;}}
}
function P(points,w=2){for(let i=1;i<points.length;i++)L(...points[i-1],...points[i],w);}
function O(points,w=2){P([...points,points[0]],w);}
function B(x,y,w,h,t=2){box(x,y,w,h,t);}
function R(x,y,w,h){
  for(let j=0;j<h;j++){let inset=(j===0||j===h-1)?2:(j===1||j===h-2)?1:0;rect(x+inset,y+j,w-2*inset,1);}
  rect(x+2,y+2,w-4,h-4,0);
}
function C(cx,cy,r,t=2,fill=false){for(let y=0;y<32;y++)for(let x=0;x<32;x++){let d=Math.hypot(x-cx,y-cy);if(d<=r&&(fill||d>r-t))dot(x,y);}}
function mirrorX(){for(let y=0;y<32;y++)for(let x=0;x<16;x++)p[y][31-x]=p[y][x];}
function mirrorY(){for(let y=0;y<16;y++)p[31-y]=p[y].slice();}
function turn(a){return a[0].map((_,y)=>a.map(r=>r[y]).reverse());}
function union(a){for(let y=0;y<32;y++)for(let x=0;x<32;x++)if(a[y][x])p[y][x]=1;}
function S(name,sym=''){if(sym.includes('x'))mirrorX();if(sym.includes('y'))mirrorY();save(name);if(sym)symmetry[name]=sym;}
function fillPolygon(points){for(let y=0;y<32;y++)for(let x=0;x<32;x++){let inside=false;for(let i=0,j=points.length-1;i<points.length;j=i++){let [xi,yi]=points[i],[xj,yj]=points[j];if(((yi>y)!==(yj>y))&&(x<(xj-xi)*(y-yi)/(yj-yi)+xi))inside=!inside;}if(inside)dot(x,y);}}
function chipFrame(){start();B(8,8,16,16);for(let z of [10,15,20]){rect(z,3,2,5);rect(z,24,2,5);rect(3,z,5,2);rect(24,z,5,2);}}
function arrowRight(x,y,len=12){rect(x,y+4,len-4,2);for(let j=0;j<10;j++){let reach=4-Math.floor(Math.abs(j-4.5));rect(x+len-5+reach,y+j,2,1);}}
function speechFrame(){start();O([[4,4],[26,4],[26,22],[14,22],[8,28],[8,22],[4,22]]);}
function badge(){
  rect(21,20,11,12,0);
  rect(25,21,4,2);rect(24,23,6,3);rect(23,26,8,2);rect(26,29,2,2);
}
function notify(name,base){restore(base);badge();S(name);}
function speakerBody(){restore('speaker');rect(19,0,13,32,0);}
function soundWaves(n){for(let i=0;i<n;i++){let x=20+i*3,y=12-i*3;P([[x,y],[x+2,y+2],[x+2,28-y],[x,30-y]]);}}
function shieldFrame(){start();O([[5,4],[15,2],[25,4],[25,17],[22,23],[15,28],[8,23],[5,17]]);mirrorX();}
function node(x,y,size=4){rect(x,y,size,size);}
function masterNetwork(){start();P([[7,7],[23,7],[15,23],[7,7]]);for(let [x,y]of [[5,5],[21,5],[13,21]]){rect(x-1,y-1,8,8,0);B(x,y,6,6);}mirrorX();}

// Larger page shared by every file icon: 24x28, still inside 32x32.
function page(){start();rect(4,2,2,28);rect(4,28,24,2);rect(26,9,2,21);rect(4,2,16,2);P([[19,2],[26,9]]);rect(19,3,2,8);rect(19,9,9,2);}
page();S('file');
page();rect(9,14,14,2);rect(9,19,14,2);rect(9,24,10,2);S('file_text');
page();P([[12,14],[8,18],[12,22]]);P([[19,14],[23,18],[19,22]]);L(17,14,14,23);S('file_code');
page();O([[8,25],[15,18],[22,25]]);rect(9,13,3,3);rect(22,16,3,3);S('file_image');
page();B(13,12,6,6);rect(15,18,2,10);rect(12,18,3,2);rect(17,21,3,2);rect(12,24,3,2);S('file_zip');
page();P([[11,13],[9,13],[9,18],[7,20],[9,22],[9,26],[11,26]]);P([[19,13],[21,13],[21,18],[23,20],[21,22],[21,26],[19,26]]);rect(15,16,2,2);rect(15,22,2,3);rect(14,24,2,2);S('file_json');
const letters={P:['111','101','111','100','100'],D:['110','101','101','101','110'],F:['111','100','110','100','100'],'0':['111','101','101','101','111'],'1':['010','110','010','010','111']};
function glyph(c,x,y){letters[c].forEach((row,j)=>[...row].forEach((v,i)=>{if(v==='1')rect(x+i*2,y+j*2,2,2);}));}
page();glyph('P',6,16);glyph('D',13,16);glyph('F',20,16);S('file_pdf');
page();glyph('0',8,15);glyph('1',18,15);S('file_bin');

// Firmware symbols previously missed by the original set.
start();R(3,9,26,18);P([[8,9],[11,6],[19,6],[22,9]]);C(15.5,18.5,6.5,2);S('camera','x');
start();R(10,8,12,19);B(12,5,8,5);rect(15,11,2,14);P([[12,5],[10,3]]);for(let y of [12,18,24])P([[10,y],[6,y-2],[4,y-2]]);S('debug','x');
chipFrame();for(let y of [11,15,19])for(let x of [11,15,19])rect(x,y,2,2);S('edgeimpulse','xy');
speechFrame();for(let [x,h]of [[7,4],[11,8],[15,12],[19,8],[23,4]])rect(x,14-h/2,2,h);S('espsr');
start();C(15.5,15.5,12.5,2);P([[11,10],[11,8],[13,6],[17,6],[19,8],[19,12],[15,16],[15,19]]);rect(15,23,2,2);S('help');
start();R(11,3,10,17);P([[7,12],[7,18],[10,21],[20,21],[23,18],[23,12]]);rect(15,23,2,4);rect(10,27,12,2);S('mic','x');
start();R(10,3,12,18);rect(13,8,6,2);rect(13,13,6,2);P([[6,13],[6,19],[10,23],[20,23],[24,19],[24,13]]);rect(15,24,2,3);rect(8,27,16,2);S('microphone','x');
start();C(15.5,15.5,4.5,2);rect(15,6,2,6);B(13,2,6,5);arrowRight(2,11,10);arrowRight(20,11,10);S('mqtt');
start();B(8,8,16,16);for(let x of [10,15,20])rect(x,13,2,6);rect(15,2,2,4);rect(15,26,2,4);rect(2,15,4,2);rect(26,15,4,2);P([[5,5],[7,7]]);P([[24,24],[26,26]]);P([[5,26],[7,24]]);P([[24,7],[26,5]]);S('neopixel','xy');
start();R(3,4,26,19);rect(15,23,2,4);rect(10,27,12,2);S('notify_display','x');
start();C(15.5,10.5,3.5,2);P([[9,26],[9,23],[12,20],[18,20],[21,23],[21,26]]);P([[6,7],[3,10],[3,15],[6,18]]);S('presence','x');
chipFrame();C(15.5,15.5,6,2);rect(15,11,2,6);rect(15,15,5,2);S('rtc');
start();B(5,14,22,14);rect(2,19,3,4);rect(27,19,3,4);rect(14,7,4,8);R(8,3,16,5);C(15.5,15.5,3.5,2);rect(10,23,12,2);S('servo','x');
speakerBody();P([[20,11],[28,19]]);P([[28,11],[20,19]]);S('vol_mute');
speakerBody();soundWaves(1);S('vol_min');
speakerBody();soundWaves(3);S('vol_max');
start();C(15.5,15.5,12.5,2);P([[14,4],[11,7],[9,12],[9,18],[11,23],[14,26]]);mirrorX();rect(5,10,22,2);rect(5,20,22,2);S('web','xy');
start();B(3,8,26,16);for(let x of [7,14,21])rect(x,12,4,6);for(let x of [5,9,13,17,21,25])rect(x,24,2,4);rect(7,20,18,2);S('memory','x');
start();R(3,5,26,22);P([[7,11],[11,15],[7,19]]);rect(15,12,9,2);rect(15,18,6,2);badge();S('notify_cli');

// Menus: consistent live area and square-ended strokes.
start();for(let x of [4,18])for(let y of [4,18])R(x,y,10,10);S('apps','xy');
start();rect(15,12,2,16);C(15.5,9.5,2.5,2,true);P([[10,5],[7,8],[7,12],[10,15]]);P([[6,2],[2,6],[2,14],[6,18]]);S('signal','x');
start();B(5,15,22,13);B(9,19,6,5);rect(20,19,3,3);P([[10,11],[13,8],[17,8],[20,11]]);P([[6,7],[10,3],[20,3],[24,7]]);mirrorX();rect(18,18,6,7,0);rect(20,20,2,2);S('sensor');
start();B(11,7,14,18);rect(3,4,2,24);rect(7,4,2,24);for(let y of [10,20]){rect(3,y,8,2);rect(25,y,4,2);}B(15,12,6,8);S('i2c');
start();rect(4,4,2,24);rect(4,26,24,2);P([[9,22],[14,17],[18,21],[26,13]]);S('chart');
start();for(let y of [6,14,22]){rect(4,y,4,4);rect(12,y+1,16,2);}S('list');
start();C(15.5,15.5,8.5,2);C(15.5,15.5,2.5,2);rect(15,2,2,8);rect(15,22,2,8);rect(2,15,8,2);rect(22,15,8,2);S('gps','xy');
start();C(15.5,16.5,12.5,2);rect(0,24,32,8,0);rect(4,19,2,7);rect(26,19,2,7);rect(4,24,24,2);for(let a of [[7,17,9,17],[9,10,11,12],[15,6,15,9],[19,12,21,10],[21,17,23,17]])L(...a);L(15,20,22,13);C(15.5,20.5,2.5,2,true);S('perf');
start();R(2,7,28,19);for(let y of [11,16])for(let x of [6,11,16,21,26])rect(x-1,y,2,2);rect(8,21,16,2);S('keyboard','x');
start();P([[17,4],[26,4],[26,26],[17,26]]);arrowRight(3,11,13);rect(22,14,2,2);S('login');
start();P([[13,4],[4,4],[4,26],[13,26]]);arrowRight(16,11,13);rect(8,14,2,2);S('logout');
start();C(8.5,9.5,3.5,2);P([[3,26],[3,22],[6,19],[10,19],[13,22],[13,26]]);S('users','x');
start();B(2,8,28,16);for(let x of [7.5,15.5,23.5])C(x,15.5,2.5,2,true);S('password','xy');
start();R(4,4,8,15);P([[2,13],[2,19],[5,22],[9,22],[12,19],[12,13]]);rect(7,23,2,5);for(let y of [6,12,18,24])rect(17,y,12,2);S('transcript');
start();O([[4,7],[11,4],[19,8],[26,4],[26,24],[19,28],[11,24],[4,28]]);rect(11,5,2,20);rect(19,8,2,20);S('map');
speechFrame();rect(8,10,7,2);rect(8,16,12,2);rect(21,8,2,8);rect(18,11,8,2);S('llm');
start();O([[15,27],[4,16],[4,9],[8,5],[11,5],[15,9],[19,5],[22,5],[26,9],[26,16]]);mirrorX();P([[4,16],[10,16],[13,13],[17,21],[20,16],[26,16]]);S('health');

// File-format symbols use the full enlarged interior.
page();B(7,14,18,12);rect(12,14,2,12);rect(18,14,2,12);rect(7,19,18,2);S('file_csv');
page();rect(12,13,10,3);rect(12,14,2,11);rect(20,14,2,9);C(10.5,24.5,2.5,2,true);C(18.5,22.5,2.5,2,true);S('file_audio');
page();B(7,15,12,10);O([[18,17],[23,12],[23,26],[18,21]]);rect(10,18,3,3);S('file_video');
page();O([[7,15],[13,13],[19,16],[24,14],[24,24],[19,26],[13,23],[7,25]]);rect(13,14,2,10);rect(19,17,2,9);S('file_map');
start();P([[9,15],[21,15],[15,23],[9,15]]);for(let [x,y]of [[7,13],[19,13],[13,21]]){rect(x-1,y-1,8,8,0);B(x,y,6,6);}mirrorX();{const glyph=p.map(r=>r.slice());page();union(glyph);}S('file_model');
page();C(11.5,17.5,3.5,2);L(14,20,20,26);L(18,24,20,22);L(20,26,22,24);S('file_key');

// Hardware and future feature symbols.
start();C(15.5,17.5,11.5,2);C(15.5,17.5,7.5,2);B(11,3,10,5);S('ring','x');
start();O([[4,4],[26,4],[26,20],[20,26],[4,26]]);P([[20,26],[20,20],[26,20]]);rect(9,10,13,2);rect(9,15,9,2);S('note');
start();B(3,5,18,22);B(7,10,10,10);rect(7,24,10,3);arrowRight(21,11,8);S('coprocessor');
start();fillPolygon([[14,13],[10,11],[10,9],[12,7],[15,7],[17,9],[17,11],[16,13]]);{let a=p.map(r=>r.slice());for(let i=0;i<3;i++){a=turn(a);union(a);}}C(15.5,15.5,12.5,2);C(15.5,15.5,2.5,2,true);S('fan');symmetry.fan='rot90';
start();C(15.5,16.5,8.5,2);L(15,16,20,11);rect(15,2,2,4);L(5,5,7,7);L(24,7,26,5);rect(2,15,4,2);rect(26,15,4,2);P([[9,28],[5,24],[9,24]]);S('rotary_encoder');
start();B(3,3,26,26);for(let y of [7,14,21])for(let x of [7,14,21])rect(x,y,4,4);S('led_matrix','xy');
start();R(3,8,18,17);O([[20,13],[27,6],[27,26],[20,19]]);rect(7,12,4,4);S('video');
masterNetwork();S('mesh_nodes','x');
shieldFrame();S('shield','x');
chipFrame();rect(10,10,12,12,0);P([[11,14],[14,11],[19,11],[21,13],[21,18],[18,21],[13,21],[11,19]]);P([[10,15],[10,19],[14,19]]);S('firmware_update');
start();B(4,11,24,18);O([[4,11],[9,6],[21,6],[26,11]]);rect(14,11,4,5);P([[10,18],[13,15],[18,15],[21,18],[21,23],[18,26],[13,26],[10,23]]);P([[10,26],[10,23],[13,23]]);S('backup');
start();C(15.5,15.5,12.5,2);L(10,10,20,20);L(20,10,10,20);S('error','xy');

// Retained planned names.
start();B(3,3,26,26);rect(8,8,3,16);rect(21,8,3,16);rect(11,14,10,3);S('logo','x');
start();rect(5,5,22,3);rect(14,8,4,19);rect(9,26,14,2);S('text','x');
start();O([[13,5],[26,15],[13,25]]);rect(3,7,6,2);rect(1,15,8,2);rect(3,23,6,2);S('animation');
restore('signal');rect(10,27,12,2);S('pair_beacon','x');
start();C(9.5,9.5,6.5,2);L(13,13,26,26);L(21,21,24,18);L(24,24,27,21);S('key');
restore('bond');rect(17,1,15,12,0);O([[19,5],[21,7],[23,3],[25,7],[27,5],[27,11],[19,11]]);S('bond_master');
restore('bond');rect(17,1,15,13,0);C(23.5,7.5,4.5,2);rect(23,1,2,3);rect(23,12,2,3);rect(17,7,3,2);rect(28,7,3,2);S('bond_worker');
masterNetwork();rect(5,5,6,6);S('mesh_master');
start();O([[15,28],[6,17],[5,11],[8,5],[12,3],[18,3],[22,5],[25,11],[24,17]]);mirrorX();C(15.5,11.5,4.5,2);S('map_pin','x');
start();C(6.5,24.5,3.5,2);C(24.5,6.5,3.5,2);P([[11,24],[21,24],[24,21],[24,17],[21,14],[10,14],[6,10],[6,7],[9,4],[17,4]]);S('route');
start();O([[3,10],[15,4],[27,10],[15,16]]);P([[3,16],[15,22],[27,16]]);P([[3,22],[15,28],[27,22]]);S('layers','x');
restore('search');rect(9,12,8,2);rect(12,9,2,8);S('zoom_in');
restore('search');rect(9,12,8,2);S('zoom_out');
start();for(let a of [[[3,10],[3,3],[10,3]],[[20,3],[27,3],[27,10]],[[3,20],[3,27],[10,27]],[[20,27],[27,27],[27,20]]])P(a);C(15.5,15.5,5.5,2);rect(15,15,2,2);S('recenter','xy');
notify('notify_auth','shield');notify('notify_power','power');notify('notify_voice','mic');notify('notify_camera','camera');notify('notify_bluetooth','bt_idle');notify('notify_network','signal');notify('notify_mqtt','mqtt');notify('notify_storage','sdcard');notify('notify_time','clock');
export { symmetry };
