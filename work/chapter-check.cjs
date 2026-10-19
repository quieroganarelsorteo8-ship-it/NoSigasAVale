const {chromium}=require('C:/Users/axlta/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs');
const ROOT='C:/Users/axlta/Documents/Codex/2026-10-07/qui';
(async()=>{
const browser=await chromium.launch({channel:'msedge',headless:true});
const page=await browser.newPage({viewport:{width:1280,height:1040}}), errors=[];
page.on('pageerror',e=>errors.push(e.message));
await page.goto('file:///'+ROOT+'/outputs/La-busqueda-de-Vale.html');
const check=async(expr,msg)=>{if(!await page.evaluate(expr))throw Error(msg+' '+await page.evaluate('JSON.stringify({map:S.map,x:S.x,y:S.y,mode:S.mode,flags:S.flags})'));console.log('PASS '+msg)};
const shot=async(name)=>page.screenshot({path:ROOT+'/work/v2-'+name+'.png'});
const dialog=async()=>{for(let i=0;i<50&&await page.evaluate('S.mode==="dialog"');i++)await page.keyboard.press('e');await check('S.mode!=="dialog"','Dialogue completed')};
const walk=async(id)=>{
 await page.evaluate((id)=>{
 const t=typeof id==='string'?layouts[S.map].objects.find(o=>o.id===id).target:id;
 if(S.mode!=='play')throw Error('Cannot walk while '+S.mode);
 const dirs=[[4,0,'ArrowRight'],[-4,0,'ArrowLeft'],[0,4,'ArrowDown'],[0,-4,'ArrowUp']],q=[{x:S.x,y:S.y,p:-1,k:null}],seen=new Set(['0,0']);let end=-1;
 for(let i=0;i<q.length&&q.length<20000;i++){
 let n=q[i];if(Math.hypot(n.x-t.x,n.y-t.y)<7){end=i;break}
 for(let [dx,dy,k] of dirs){let x=n.x+dx,y=n.y+dy,h=Math.round((x-S.x)/4)+','+Math.round((y-S.y)/4);if(!seen.has(h)&&canMove(x,y)&&canMove(n.x+dx/2,n.y+dy/2)){seen.add(h);q.push({x,y,p:i,k})}}
 }
 if(end<0)throw Error('No walkable route to '+JSON.stringify(t));
 let path=[];for(let i=end;q[i].p!==-1;i=q[i].p)path.push(q[i].k);path.reverse();keys.clear();for(let key of path){keys.add(key);update(4/57);keys.delete(key)}draw();
 },id);
 if(typeof id==='string')await check('target()?.id==='+JSON.stringify(id),'Walkable target '+id);
};
await page.locator('#start').click();await check('S.mode==="calls"','Chapter begins with calls');
for(let i=0;i<5;i++){await page.waitForTimeout(360);await page.keyboard.press('e')}
await check('S.mode==="play"&&S.map==="hall"','All three calls, voicemail and silence lead to house');
await shot('hall');
await page.keyboard.down('ArrowLeft');await page.waitForTimeout(180);await page.keyboard.up('ArrowLeft');await check('S.x<219','Physical keyboard moves Mateo');
await walk('valeDoor');await page.keyboard.press('e');await check('S.mode==="dialog"&&!S.flags.unlocked','Door requires key');await dialog();
await walk('frontDoor');await page.keyboard.press('e');await check('S.map==="hall"','Cannot skip chapter through front door');await dialog();
await walk('torch');await page.keyboard.press('e');await dialog();await check('S.flags.flashlight&&S.flash','Flashlight collectible');await page.keyboard.press('f');await check('!S.flash','F switches flashlight off');await page.keyboard.press('f');
await walk('keys');await page.keyboard.press('e');await dialog();await check('S.flags.key','Key collected');
await walk('valeDoor');await page.keyboard.press('e');await page.waitForTimeout(800);await check('S.map==="room"&&S.flags.unlocked','Key opens Vale room');
await shot('room');
await check('layouts.room.objects.filter(o=>!["map","exit"].includes(o.id)).every(o=>!canMove(o.x+o.w/2,o.y+o.h/2))','All furniture footprints block the character');
await walk({x:190,y:224});await shot('behind-books');
await walk({x:190,y:257});await shot('front-books');
await walk('radio');await page.keyboard.press('e');await dialog();await check('!S.flags.radio','Radio narrative is gated by photo reveal');
await walk('photos');await page.keyboard.press('e');await check('S.mode==="photo"&&S.photo===0','Four photograph viewer starts at street');
for(let i=0;i<3;i++)await page.keyboard.press('e');await check('S.photo===3','Mirror photograph is fourth');await page.keyboard.press('c');await check('S.analysis===0','Cannot analyze without camera');await page.keyboard.press('e');await check('S.flags.photos&&S.mode==="play"','Player asked to collect camera');
await page.keyboard.press('e');await dialog();await check('S.flags.camera','Camera collected');await page.keyboard.press('e');await page.keyboard.press('c');await page.waitForTimeout(1800);await shot('reveal');
await page.waitForTimeout(2200);await dialog();await page.waitForTimeout(2700);await shot('apparition');await page.waitForTimeout(3500);await check('S.flags.photo','Photo reveal and doorway apparition finish');
await walk('radio');await page.keyboard.press('e');await page.keyboard.press('e');await page.keyboard.press('e');await page.waitForTimeout(900);await shot('radio');await dialog();await check('S.flags.radio','Original Molo conversation unlocks marked map');
await walk('map');await page.keyboard.press('e');await shot('map');await page.keyboard.press('e');await check('S.flags.marked','Map location registered');
await walk('photos');await page.keyboard.press('e');await dialog();await check('S.flags.packed&&S.inventory.length===5','All four tools and key collected');await page.keyboard.press('i');await shot('inventory');await page.keyboard.press('i');
await walk('exit');await page.keyboard.press('e');await page.waitForTimeout(6000);await shot('ending');await page.waitForTimeout(4000);await check('S.flags.completed&&S.mode==="complete"','Knock, closing door and black liquid end chapter');await shot('complete');
await page.locator('#explore').click();await page.waitForTimeout(800);await check('S.map==="street"','Second chapter map remains available as preview');
await walk('home');await page.keyboard.press('e');await page.waitForTimeout(800);await check('S.map==="hall"','Return from street works');
await page.reload();await page.locator('#continue').click();await check('S.flags.completed&&S.inventory.length===5','Reload restores completed chapter and inventory');
await page.keyboard.press('Escape');await check('S.paused','Pause works');await page.locator('#resume').click();await page.locator('#sound').click();await check('S.sound&&audio.state==="running"','Ambient audio works');await page.locator('#sound').click();await page.locator('#effects').click();await check('S.reduce','Reduced interference works');
console.log('PAGE ERRORS',errors);if(errors.length)throw Error(errors.join('\n'));
await page.setViewportSize({width:390,height:844});await shot('mobile');
await browser.close();console.log('COMPLETE');
})().catch(e=>{console.error(e);process.exit(1)});

