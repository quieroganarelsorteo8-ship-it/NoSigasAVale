from pathlib import Path
p=Path(__file__).parent/'chapter.js'
s=p.read_text(encoding='utf-8-sig')
s=s.replace("const S=", "const BATTERY_SECONDS=75;\nconst S=")
s=s.replace('battery:30','battery:BATTERY_SECONDS').replace('S.battery=30','S.battery=BATTERY_SECONDS').replace('S.battery>29.95','S.battery>BATTERY_SECONDS-.05')
s=s.replace('Math.min(30,data.battery)):30','Math.min(BATTERY_SECONDS,data.battery)):BATTERY_SECONDS')
s=s.replace('30 segundos','75 segundos').replace('30 SEGUNDOS','75 SEGUNDOS').replace('(30 s)','(75 s)')
s=s.replace('saveTick:0}', 'saveTick:0,item:null,weatherWait:60+Math.random()*60,lightning:0,thunderWait:0}')
s=s.replace("if(eyes){rect(-3,-45,2,2,'#9f4648');rect(2,-45,2,2,'#9f4648')}", "if(eyes){rect(-4,-46,4,4,'#601923');rect(1,-46,4,4,'#601923');rect(-3,-45,2,2,'#ee4a46');rect(2,-45,2,2,'#ee4a46');rect(-3,-45,1,1,'#ffc1a0');rect(2,-45,1,1,'#ffc1a0')}")
s=s.replace('entity(277,281,1.15)', 'entity(277,281,1.15,true)').replace('entity(88,107,1.35,S.analysis>1.25&&S.analysis<1.65)', 'entity(88,107,1.35,true)')
# Important items have a dedicated modal, with grants committed on E.
a=s.index(" case 'keys':");b=s.index(" case 'torch':",a)
s=s[:a]+" case 'keys':if(!f.key)showItem('key','LLAVE DE VALE','La llave de la habitación de Vale.',()=>{f.key=true;addItem('key','Llave de Vale');notify('Llave de Vale recogida');save()});else say(['El cuenco está vacío.']);break;\n"+s[b:]
s=s.replace("say(['Mateo recoge la cámara, la linterna, la radio y las fotografías.'],()=>{", "showItem('radio','RADIO PORTÁTIL','La voz sigue al otro lado de la estática.',()=>showItem('photos','FOTOGRAFÍAS DE VALE','Mateo recoge la cámara, la linterna, la radio y las fotografías.',()=>{")
s=s.replace("notify('Equipo preparado. Sal al corredor.');save()})}","notify('Equipo preparado. Sal al corredor.');save()}))}")
s=s.replace("say(['Una cámara descansa junto a las fotografías.'],()=>{", "showItem('camera','CÁMARA','Una cámara descansa junto a las fotografías.',()=>{")
s=s.replace("function inspect(o){const f=S.flags;", "function inspect(o){const f=S.flags;sound(['photos','books','map'].includes(o.id)?'paper':'interact');")
s=s.replace("if(!f.key)say([['Mateo'", "if(!f.key){sound('locked');say([['Mateo'")
s=s.replace("Necesito encontrar la llave.']]);else", "Necesito encontrar la llave.']]);}else")
s=s.replace("if(f.completed)transition('street',92,163);", "if(f.completed){sound('door');transition('street',92,163);}")
s=s.replace("case 'home':transition", "case 'home':sound('door');transition")
s=s.replace("else{sound('static');say([", "else{sound('radio');say([")
s=s.replace("S.spares+=count;notify", "S.spares+=count;sound('battery');notify")
s=s.replace("function act(){if(!S.started)return;if(S.paused||S.transition)return;", "function act(){if(!S.started)return;if(S.paused||S.transition)return;if(S.mode==='item'){const done=S.item.done;S.item=null;S.mode='play';sound('confirm');if(done)done();return;}")
# Battery casing and six blocks.
a=s.index("text('LUZ',237");b=s.index("text(Math.ceil(S.battery)",a)
s=s[:a]+"text('LUZ',231,8,'#879b9c',7);batteryIcon(253,5);"+s[b:]
insert='''
function batterySegments(seconds=S.battery){return Math.max(0,Math.min(6,Math.ceil(seconds/(BATTERY_SECONDS/6))))}
function batteryColor(n=batterySegments()){return n>=5?'#68c87b':n>=3?'#e1bc55':'#e06960'}
function batteryIcon(x,y){const n=batterySegments(),col=batteryColor(n);rect(x,y,55,15,'#a6b2ab');rect(x+2,y+2,51,11,'#0b1720');rect(x+55,y+5,3,5,'#a6b2ab');for(let i=0;i<6;i++){rect(x+4+i*8,y+4,6,7,i<n?col:'#26333c');if(i<n)rect(x+5+i*8,y+4,1,6,n>=5?'#a7ed9e':n>=3?'#f7db83':'#f4a08b')}}
function showItem(id,title,description,done){S.mode='item';S.item={id,title,description,done};keys.clear();sound('pickup');$('live').textContent=title+'. '+description+'. E para continuar.'}
function itemView(){const item=S.item;rect(0,25,W,276,'#090f19f5');glow(240,146,103,'#5e7d7a24');text('OBJETO ENCONTRADO',240,45,'#839c9c',8,'center');
 c.save();c.translate(240,145);c.scale(3,3);
 if(item.id==='key'){rect(-22,-9,15,17,'#5e5545');rect(-21,-10,15,16,'#c4b589');rect(-18,-7,9,10,'#131e27');rect(-16,-6,5,8,'#29343b');rect(-7,-4,27,5,'#b3a279');rect(-7,-4,26,1,'#e1d0a0');rect(10,0,4,6,'#c0ab7d');rect(17,0,4,6,'#c0ab7d')}
 if(item.id==='camera'){rect(-22,-12,44,28,'#33434c');rect(-20,-14,11,3,'#b0ae95');rect(-16,-16,14,5,'#1c2c35');rect(-20,-9,40,4,'#718383');rect(12,-8,6,4,'#c6bfa1');rect(-19,-2,8,16,'#1c2c36');rect(-7,-7,22,22,'#14232e');rect(-5,-5,18,18,'#8b9c96');rect(-3,-3,14,14,'#354d5b');rect(0,-1,8,9,'#112630');rect(1,0,3,2,'#a1c6bb')}
 if(item.id==='radio'){rect(-24,-15,48,32,'#435457');rect(-22,-13,44,4,'#8d9e90');rect(-20,-7,25,18,'#1c323d');for(let i=0;i<7;i++)rect(-18+i*3,-5,1,14,'#6b807a');rect(11,-6,8,8,'#a5aa88');rect(13,-4,4,4,'#3b5557');rect(10,6,10,3,'#7c9688');line(17,-15,23,-35,'#b0b5a5',1);rect(-19,13,36,2,'#1e303a')}
 c.restore();
 if(item.id==='photos'){c.save();c.translate(211,83);c.rotate(-.10);photoArt(0,-37,0,.62);c.restore();c.save();c.translate(243,82);c.rotate(.10);photoArt(3,-24,0,.62,false);c.restore()}
 text(item.title,240,224,'#e1d9bc',12,'center');wrap(item.description,62).forEach((l,i)=>text(l,240,248+i*12,'#b9c3ba',8,'center'));text('E  CONTINUAR',240,283,'#d6c49b',8,'center');}
function weatherUpdate(dt){S.lightning=Math.max(0,S.lightning-dt);if(S.thunderWait>0){S.thunderWait-=dt;if(S.thunderWait<=0)sound('thunder')}S.weatherWait-=dt;if(S.weatherWait<=0){S.lightning=.24;S.thunderWait=.65;S.weatherWait=60+Math.random()*60}}
'''
s=s.replace('function hud(){',insert+'\nfunction hud(){')
s=s.replace("if(S.mode==='dialog')dialogView();", "if(S.mode==='item')itemView();if(S.mode==='dialog')dialogView();")
s=s.replace(" if(S.mode!=='play')return;\n if(S.flash", " if(S.mode!=='play')return;\n weatherUpdate(dt);\n if(S.flash")
s=s.replace(" light();", " light();\n if(S.lightning>0&&!S.reduce&&!blackout()){c.globalAlpha=S.lightning/.24*.32;c.drawImage(detail,0,0);c.globalAlpha=1}")
s=s.replace("function fresh(){S.flags", "function fresh(){startAudio();S.item=null;S.weatherWait=60+Math.random()*60;S.lightning=0;S.thunderWait=0;S.flags")
s=s.replace("function resumeSave(){try", "function resumeSave(){startAudio();S.item=null;try")
# Recognizable steel tower, cross braces, sector panels and a parabolic antenna.
a=s.index(' if(index===2)');b=s.index(' if(index===3)',a)
s=s[:a]+''' if(index===2){rect(5,5,130,128,'#263642');for(let i=0;i<5;i++)rect(10+i*26,19+(i%2)*7,21,3,'#53616a30');rect(5,112,130,21,'#3e4c51');rect(13,94,33,26,'#5e6367');rect(11,91,37,4,'#92948a');rect(19,101,8,13,'#283d46');rect(32,100,9,6,'#253e49');
  const tx=64;line(tx,16,tx-16,116,'#b7b6a2',2);line(tx,16,tx+16,116,'#a1aa9f',2);line(tx,12,tx,117,'#748c91');
  for(let i=0;i<6;i++){const yy=32+i*14,ww=(yy-16)*.16;line(tx-ww,yy,tx+ww,yy,'#bdbeab');line(tx-ww,yy,tx+(yy+14-16)*.16,yy+14,'#8fa3a4');line(tx+ww,yy,tx-(yy+14-16)*.16,yy+14,'#637e88')}
  rect(tx-2,11,4,3,'#c47a70');rect(tx-15,29,30,2,'#9eafa6');rect(tx-18,23,5,18,'#c7c8b2');rect(tx+13,23,5,18,'#aabbb1');rect(tx-2,21,5,17,'#d0cbb8');
  ellipse(78,57,7,9,'#afbbb0');ellipse(76,56,4,6,'#627e87');line(76,56,68,53,'#c2c6b3');
  rect(106,97,4,22,'#919f98');poly([[94,78],[119,65],[116,87],[109,96],[102,94]],'#a9b7ad');line(94,78,109,88,'#dee0c7');line(109,88,120,78,'#d3d4ba');rect(119,76,3,4,'#d5d3b8');
  for(let x=8;x<134;x+=9)line(x,118,x,130,'#667c7d');line(6,120,134,120,'#93a297');line(6,126,134,126,'#728883');}
''' +s[b:]
# Richer restrained, chiptune-style sound palette.
a=s.index('function sound(type)');b=s.index('\nfunction initAudio()',a)
s=s[:a]+'''function sweep(from,to,d,v,type='triangle'){if(!S.sound||!audio)return;const o=audio.createOscillator(),g=audio.createGain();o.type=type;for(let i=0;i<12;i++)o.frequency.setValueAtTime(from*Math.pow(to/from,i/11),audio.currentTime+i*d/12);g.gain.setValueAtTime(.0001,audio.currentTime);g.gain.exponentialRampToValueAtTime(v,audio.currentTime+.012);g.gain.exponentialRampToValueAtTime(.0001,audio.currentTime+d);o.connect(g);g.connect(master);o.start();o.stop(audio.currentTime+d)}
function sound(type){
 if(type==='step')hiss(.09,.035,500);
 if(type==='interact'){beep(170,.045,.012,'square')}
 if(type==='door'){sweep(170,43,.42,.045,'sawtooth');hiss(.13,.045,450);beep(58,.26,.045,'triangle')}
 if(type==='locked'){beep(110,.08,.025,'square');sweep(120,70,.13,.025)}
 if(type==='phone'){beep(440,.8,.035,'triangle');beep(480,.8,.018)}
 if(type==='switch'||type==='battery'){sweep(300,130,.07,.025,'square');hiss(.04,.025,1400)}
 if(type==='focus'){sweep(460,720,.13,.022,'square')}
 if(type==='paper'){hiss(.14,.045,2100);beep(190,.04,.009,'triangle')}
 if(type==='static'||type==='radio'){hiss(.65,.10,2200);sweep(980,95,.44,.018,'square')}
 if(type==='pickup'){sweep(220,440,.32,.025,'triangle');beep(329.6,.42,.018,'square')}
 if(type==='confirm')beep(220,.06,.015,'triangle');
 if(type==='dread'){sweep(150,34,.75,.065,'sawtooth');beep(43,1.4,.065);beep(47,1.2,.035)}
 if(type==='knock'){beep(85,.22,.09,'triangle');hiss(.16,.08,600)}
 if(type==='thunder'){hiss(2.7,.22,220);sweep(67,28,2.1,.055,'triangle');beep(37,2.4,.035)}
}
function startAudio(){if(audio)return;try{initAudio();S.sound=true;audio.resume().catch(()=>{});master.gain.setTargetAtTime(.5,audio.currentTime,.15);$('sound').textContent='Sonido: encendido';$('sound').setAttribute('aria-pressed','true')}catch{S.sound=false}}
''' +s[b:]
p.write_text(s,encoding='utf-8')
p=Path(__file__).parent/'build_chapter.py';s=p.read_text(encoding='utf-8-sig').replace('ACTIVA EL SONIDO PARA ESCUCHAR EL AMBIENTE','SONIDO RETRO · PUEDES SILENCIARLO CON EL BOTÓN');p.write_text(s,encoding='utf-8')
