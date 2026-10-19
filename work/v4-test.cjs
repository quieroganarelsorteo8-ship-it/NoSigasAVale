const fs=require('fs'),vm=require('vm');
const {createCanvas}=require('C:/Users/axlta/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@napi-rs/canvas');
const root='C:/Users/axlta/Documents/Codex/2026-10-07/qui';
const game=createCanvas(480,320);game.focus=()=>{};
const els=new Map([['game',game]]),local=new Map(),events=[];
const el=id=>{if(!els.has(id))els.set(id,{hidden:false,textContent:'',setAttribute(){},focus(){}});return els.get(id)};
const param=()=>({value:0,setValueAtTime(v,t){events.push(['value',v,t])},exponentialRampToValueAtTime(v,t){events.push(['ramp',v,t])},setTargetAtTime(){}});
class AC{constructor(){this.currentTime=0;this.sampleRate=16000;this.state='running';this.destination={}}resume(){return Promise.resolve()}createGain(){return{gain:param(),connect(){}}}createOscillator(){return{frequency:param(),connect(){},start(){events.push(['tone'])},stop(){}}}createBufferSource(){return{connect(){},start(){events.push(['noise'])}}}createBiquadFilter(){return{frequency:param(),connect(){}}}createBuffer(ch,n){return{getChannelData(){return new Float32Array(n)}}}}
const ctx=vm.createContext({console,Math,document:{getElementById:el,createElement:()=>createCanvas(480,320),querySelectorAll:()=>[],addEventListener(){}},window:{addEventListener(){},AudioContext:AC},localStorage:{setItem:(k,v)=>local.set(k,v),getItem:k=>local.get(k)},requestAnimationFrame(){}});
const html=fs.readFileSync(root+'/outputs/La-busqueda-de-Vale.html','utf8');vm.runInContext(html.match(/<script>([\s\S]*)<\/script>/)[1],ctx);
const run=s=>vm.runInContext(s,ctx),check=(s,msg)=>{if(!run(s))throw Error(msg);console.log('PASS '+msg)};
const shot=name=>{run('draw()');fs.writeFileSync(root+'/work/v4-'+name+'.png',game.toBuffer('image/png'))};
const dismiss=()=>{for(let i=0;i<100&&run("['dialog','item'].includes(S.mode)");i++)run('act()');check("S.mode==='play'||S.mode==='scene'",'Modal flow advances with E')};
run('fresh()');check('S.battery===75&&S.sound','75 second battery and gesture-start audio');for(let i=0;i<5;i++)run('S.scene.t=1;act()');
check('S.mode==="play"','Opening finishes');
for(const [seconds,segments,color] of [[75,6,'#68c87b'],[62.5,5,'#68c87b'],[50,4,'#e1bc55'],[37.5,3,'#e1bc55'],[25,2,'#e06960'],[12.5,1,'#e06960'],[0,0,'#e06960']]){run('S.battery='+seconds);check(`batterySegments()===${segments}&&batteryColor()==='${color}'`,'Battery '+seconds+' seconds: '+segments+' segments')}
run('S.battery=75;S.flash=true;update(74.9)');check('S.battery>0&&S.battery<.11','Battery lasts until 75 seconds');run('update(.1)');check('S.battery===0&&!S.flash','Battery expires at 75 seconds');run('recharge()');check('S.battery===75&&S.spares===0','Replacement cell restores 75 seconds');
run("inspect({id:'keys'})");check("S.mode==='item'&&S.item.id==='key'&&!S.flags.key",'Key has full-screen acquisition before grant');shot('key');run('update(10)');check('S.battery===75','Item presentation does not drain battery');run('act()');check('S.flags.key&&S.mode==="play"','Key confirmed with E');
run("inspect({id:'cabinet'})");check('S.mode==="dialog"&&S.item===null','Batteries do not open important-item interface');dismiss();check('S.spares===2','Battery reward still works');
run("inspect({id:'valeDoor'});update(.7)");check('S.map==="room"','Door transition after key works');
run("inspect({id:'photos'});act();act()");check('S.photo===2','Third photo is antennas');shot('antennas');run('act();act()');
run("inspect({id:'photos'})");check('S.mode==="item"&&S.item.id==="camera"','Camera has dedicated acquisition screen');shot('camera');run('act()');check('S.flags.camera','Camera granted');
run("inspect({id:'photos'});useCamera();update(3.8)");dismiss();check('S.mode==="scene"','Photo reaction still leads to apparition');run('S.scene.t=2.5');shot('eyes');run('update(6)');check('S.flags.photo','Apparition ends');
run("inspect({id:'radio'})");dismiss();check('S.flags.radio','Radio dialogue completes');run("inspect({id:'map'});act();inspect({id:'photos'})");check('S.mode==="item"&&S.item.id==="radio"','Radio acquisition begins equipment sequence');run('act()');check('S.mode==="item"&&S.item.id==="photos"&&!S.flags.packed','Photos have dedicated screen before final equipment grant');shot('photos');run('act()');check('S.flags.packed&&S.inventory.length===5','Equipment granted exactly once');
run("inspect({id:'exit'});update(.7);update(9)");check('S.flags.completed','Chapter still completes');
run("S.mode='play';S.scene=null;S.battery=50;S.flash=false;S.toastTime=0;S.map='room';S.x=270;S.y=202;S.dir='up'");shot('yellow');run('S.battery=25');shot('red');run('S.battery=75;S.flash=true');shot('light');
run('S.weatherWait=.1;weatherUpdate(.1)');check('S.lightning===.24&&S.weatherWait>=60&&S.weatherWait<=120&&S.thunderWait===.65','Lightning schedules next storm at 60–120 seconds');shot('lightning');const before=events.length;run('weatherUpdate(.7)');if(events.length<=before)throw Error('Thunder sound missing');
run('S.paused=true;const interval=S.weatherWait;update(60)');check('S.weatherWait===interval','Weather pauses with gameplay');run('S.paused=false');
for(const kind of ['door','radio','paper','pickup','confirm','locked','battery','thunder','dread']){let n=events.length;run(`sound('${kind}')`);if(events.length===n)throw Error('Missing retro sound '+kind);console.log('PASS sound route '+kind)}
run('S.sound=false');let n=events.length;run("sound('door');sound('thunder')");if(events.length!==n)throw Error('Mute failed');console.log('PASS mute');
run('S.battery=44;S.spares=2;save();S.battery=0;resumeSave()');check('S.battery===44&&S.spares===2','Charge and spare count survive saved game');
console.log('ALL CHECKS PASSED');

