from pathlib import Path
p=Path(__file__).parent/'chapter.js'
s=p.read_text(encoding='utf-8-sig')
s=s.replace("toastTime:0}","toastTime:0,battery:30,spares:1,saveTick:0}")
s=s.replace("()=>cabinetDraw(365,228,41))", "()=>cabinetDraw(365,228,41),{target:{x:385,y:258},label:'Buscar en el armario'})")
s=s.replace("()=>cabinetDraw(329,135,37))", "()=>cabinetDraw(329,135,37),{target:{x:348,y:166},label:'Buscar en el armario'})")
s=s.replace("label:'Revisar la linterna'", "label:'Revisar los repuestos'")
s=s.replace("object('bench',320,253,65,15,()=>tableDraw(320,253,65,'books'))", "object('bench',320,281,56,11,()=>streetBench(320,281)),object('lamp',402,153,8,9,()=>lampPost(406,160))")
s=s.replace("lampPost(405,238);rain", "rain")
s=s.replace("function lampPost(x,y)", "function streetBench(x,y){ellipse(x+28,y+12,31,3,'#09121c66');rect(x+3,y-14,3,27,'#27323e');rect(x+49,y-14,3,27,'#27323e');for(let i=0;i<3;i++)rect(x,y-14+i*4,56,3,'#877160');rect(x,y+1,56,5,'#a18b72');rect(x+4,y+5,3,9,'#202c38');rect(x+48,y+5,3,9,'#202c38')}\nfunction lampPost(x,y)")
start=s.index('function light(){');end=s.index('\nfunction target()',start)
s=s[:start]+'''const detail=document.createElement('canvas'),lit=document.createElement('canvas'),coarse=document.createElement('canvas');
detail.width=lit.width=W;detail.height=lit.height=H;coarse.width=W/3;coarse.height=Math.ceil(H/3);
const dc=detail.getContext('2d'),litc=lit.getContext('2d'),cc=coarse.getContext('2d');cc.imageSmoothingEnabled=false;
function blackout(){return S.scene?.type==='apparition'&&S.scene.t>=2.1&&S.scene.t<3.1}
function light(){
 dc.clearRect(0,0,W,H);dc.drawImage(canvas,0,0);cc.clearRect(0,0,coarse.width,coarse.height);cc.drawImage(detail,0,0,coarse.width,coarse.height);
 c.drawImage(coarse,0,0,W,H);rect(0,25,W,276,blackout()?'#020610f0':'#030916da');
 lc.clearRect(0,0,W,H);lc.globalCompositeOperation='source-over';
 // A permanent soft halo: navigation never becomes a completely black screen.
 hole(S.x,S.y-12,49,blackout()?.23:.88);
 if(!blackout()){
  if(S.map==='street')hole(406,154,58,.70);
  else if(S.map==='hall')hole(174,92,38,.18);else hole(137,94,34,.16);
  if(S.flash&&S.battery>0){const ang={up:-Math.PI/2,down:Math.PI/2,left:Math.PI,right:0}[S.dir];
   lc.save();lc.beginPath();lc.moveTo(S.x,S.y-17);lc.arc(S.x,S.y-17,168,ang-.45,ang+.45);lc.closePath();lc.clip();
   const g=lc.createRadialGradient(S.x,S.y-17,12,S.x,S.y-17,168);g.addColorStop(0,'rgba(0,0,0,.98)');g.addColorStop(.55,'rgba(0,0,0,.91)');g.addColorStop(1,'rgba(0,0,0,0)');lc.fillStyle=g;lc.fillRect(0,0,W,H);lc.restore();
  }
 }else{hole(277,253,43,.20)}
 litc.globalCompositeOperation='source-over';litc.clearRect(0,0,W,H);litc.drawImage(detail,0,0);litc.globalCompositeOperation='destination-in';litc.drawImage(lighting,0,0);litc.globalCompositeOperation='source-over';c.drawImage(lit,0,0);
}
''' +s[end:]
s=s.replace('flash:S.flash}', 'flash:S.flash,battery:S.battery,spares:S.spares}')
s=s.replace("S.scene={type,t:0,beat:-1}","S.scene={type,t:0,beat:-1,jump:Math.random()<.55}")
start=s.index(" case 'torch':");end=s.index(" case 'valeDoor':",start)
s=s[:start]+''' case 'torch':findBatteries('batteryTorch',1);break;
 case 'cabinet':findBatteries('batteryHall',2);break;
 case 'wardrobe':findBatteries('batteryRoom',2);break;
''' +s[end:]
start=s.index('function inspect(o)')
s=s[:start]+'''function findBatteries(flag,count){if(S.flags[flag]){say(['Ya revisaste este mueble. No quedan pilas.']);return}say([count===1?'Una pila de repuesto en el cajón.':'Dos pilas escondidas al fondo del armario.'],()=>{S.flags[flag]=true;S.spares+=count;notify('+'+count+' pilas · R para colocar una pila de 30 segundos');save()})}
function recharge(){if(S.paused||!['play','inventory'].includes(S.mode))return;if(S.battery>29.95){notify('La pila está llena.');return}if(S.spares<1){notify('Sin repuestos. Busca en cajones y armarios.');return}S.spares--;S.battery=30;S.flash=true;sound('switch');notify('Pila nueva · 30 segundos de luz');save()}
''' +s[start:]
s=s.replace(" if(s.t>5.8)"," if(s.t>3.15&&s.jump&&!s.hit&&!S.reduce){s.hit=true;sound('dread')}\n if(s.t>5.8)")
s=s.replace(" if(S.mode!=='play')return;\n let dx", " if(S.mode!=='play')return;\n if(S.flash&&S.battery>0){const before=S.battery;S.battery=Math.max(0,S.battery-dt);if(before>5&&S.battery<=5)notify('Quedan 5 segundos · R para cambiar la pila');if(S.battery===0){S.flash=false;notify(S.spares?'Pila agotada · Pulsa R para cambiarla':'Pila agotada · Busca repuestos en los armarios');save()}}\n S.saveTick+=dt;if(S.saveTick>=5){S.saveTick=0;save()}\n let dx")
s=s.replace(" light();", " light();\n if(S.scene?.type==='apparition'&&S.scene.jump&&!S.reduce&&S.scene.t>=3.15&&S.scene.t<3.5){rect(0,25,W,276,'#0b1426c9');glow(240,162,125,'#65728230');entity(240,302,4.25,true)}")
s=s.replace("text(S.map==='street'?'VISTA PREVIA / 02':'CAPÍTULO 01',465,8,'#7d969f',8,'right');", "text('LUZ',237,8,'#879b9c',7);rect(258,7,49,9,'#58686c');rect(260,9,45,5,'#101a25');rect(260,9,Math.round(45*S.battery/30),5,S.battery<=5?'#b78568':'#a9b89a');text(Math.ceil(S.battery)+'s',315,8,'#c3c8b6',7);text('R · PILAS '+S.spares,463,8,'#b2bcac',7,'right');")
s=s.replace("CAPÍTULO 01 / SIN CONSUMO DE BATERÍA", "30 SEGUNDOS POR PILA · R PARA RECARGAR")
s=s.replace("text('I / ESC  VOLVER',35,283", "text('Pila: '+Math.ceil(S.battery)+' s · Repuestos: '+S.spares,35,245,'#d1c3a0',9);text('I / ESC  VOLVER',35,283")
s=s.replace("function fresh(){S.flags={};S.inventory=[];", "function fresh(){S.flags={flashlight:true};S.inventory=[{id:'flashlight',label:'Linterna'}];S.battery=30;S.spares=1;S.saveTick=0;")
s=s.replace("S.dir='up';S.flash=false;S.dialog=null", "S.dir='up';S.flash=true;S.dialog=null")
s=s.replace("S.flash=data.flash;S.started", "S.battery=Number.isFinite(data.battery)?Math.max(0,Math.min(30,data.battery)):30;S.spares=Number.isFinite(data.spares)?Math.max(0,Math.floor(data.spares)):1;S.flags.flashlight=true;addItem('flashlight','Linterna');S.flash=!!data.flash&&S.battery>0;S.started")
s=s.replace("notify('Flechas / WASD · Caminar     Mayús · Correr')", "notify('Ya tienes linterna · F apagar · R cambiar pila (30 s)')")
s=s.replace("'f','c','i'].includes", "'f','c','i','r','p'].includes")
s=s.replace("if(k==='f'){toggleFlash();return}", "if(k==='p'){toggleFullscreen();return}if(k==='r'){recharge();return}if(k==='f'){toggleFlash();return}")
s=s.replace("S.flash=!S.flash;sound('switch');save()", "if(!S.flash&&S.battery<=0){notify('Pila agotada · R para recargar');return}S.flash=!S.flash;sound('switch');save()")
s=s.replace("$('touchCamera').onclick=useCamera;", "$('touchCamera').onclick=useCamera;$('touchBattery').onclick=recharge;")
s=s.replace("$('fullscreen').onclick=async()=>", "async function toggleFullscreen()")
s=s.replace("document.addEventListener('fullscreenchange'", "$('fullscreen').onclick=toggleFullscreen;$('fullInGame').onclick=toggleFullscreen;\ndocument.addEventListener('fullscreenchange'")
p.write_text(s,encoding='utf-8')
