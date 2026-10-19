const {chromium}=require('C:/Users/axlta/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const path=require('path');
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true});
 const page=await browser.newPage({viewport:{width:1200,height:1000}}),errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto('file:///C:/Users/axlta/Documents/Codex/2026-10-07/qui/outputs/La-busqueda-de-Vale.html');
 await page.locator('#start').click();
 await page.screenshot({path:'C:/Users/axlta/Documents/Codex/2026-10-07/qui/work/room.png'});
 const move=async(key,ms)=>{await page.keyboard.down(key);await page.waitForTimeout(ms);await page.keyboard.up(key)};
 const assert=async(expr,msg)=>{if(!await page.evaluate(expr))throw new Error(msg);console.log('PASS '+msg)};
 await move('ArrowUp',1500);
 await assert('S.y>=140 && S.y<160','Desk collision prevents walking through furniture');
 await move('ArrowLeft',530);await page.keyboard.press('e');
 await assert('S.dialog?.id==="molo"','Molo reachable from spawn using keyboard');
 await page.waitForTimeout(1800);await page.screenshot({path:'C:/Users/axlta/Documents/Codex/2026-10-07/qui/work/dialog-molo.png'});
 for(let i=0;i<8 && await page.evaluate('S.dialog!==null');i++)await page.keyboard.press('e');
 await assert('S.dialog===null','Dialogue finishes');
 await page.keyboard.press('e');await assert('S.dialog?.id==="molo"','Dialogue repeatable');await page.keyboard.press('Escape');
 await move('ArrowDown',850);await move('ArrowRight',3600);await move('ArrowDown',400);await page.keyboard.press('e');await page.waitForTimeout(800);
 await assert('S.map===1','Exit door takes player to street');
 await page.screenshot({path:'C:/Users/axlta/Documents/Codex/2026-10-07/qui/work/street.png'});
 await move('ArrowDown',200);await move('ArrowRight',3020);await page.keyboard.press('e');
 await assert('S.dialog?.id==="neighbor"','Street NPC reachable using keyboard');
 await page.waitForTimeout(1800);await page.screenshot({path:'C:/Users/axlta/Documents/Codex/2026-10-07/qui/work/dialog-neighbor.png'});
 await page.keyboard.press('Escape');await move('ArrowLeft',3040);await page.keyboard.press('e');await page.waitForTimeout(800);
 await assert('S.map===0','Return door takes player back to room');
 await page.keyboard.press('Escape');await assert('S.paused','Pause works');await page.locator('#resume').click();
 await page.locator('#sound').click();await assert('S.sound && audio.state==="running"','Sound toggle works');await page.locator('#sound').click();
 await assert('!S.sound','Sound can be muted');
 console.log('Errors:',errors);if(errors.length)throw new Error(errors.join('\n'));
 await page.setViewportSize({width:390,height:844});await page.screenshot({path:'C:/Users/axlta/Documents/Codex/2026-10-07/qui/work/mobile.png'});
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});


