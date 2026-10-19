from pathlib import Path
p=Path('work/chapter.js')
s=p.read_text(encoding='utf-8')
s=s.replace('S.photo=f.photos?3:0;S.mode=\'photo\';S.analysis=0;', "S.photo=f.photos?3:0;S.mode='photo';S.analysis=0;resetPhotoLens();")
a=s.index("else{sound('radio');say([");b=s.index("}break;",a)
radio=s[a:b]
lines=radio[radio.index('say(['):]
s=s[:a]+"else{openTuner()}"+s[b+1:]
s=s.replace("else notify('Pulsa C para analizar la fotografía del espejo.')", "else notify('Acerca la imagen con la rueda y observa junto a Vale.')")
a=s.index('function useCamera()');b=s.index('const photoCaptions',a)
s=s[:a]+'''function resetPhotoLens(){S.lens={zoom:1,clue:false,reveal:0};}
function useCamera(){if(S.mode==='photo')notify('Rueda del mouse: acercar o alejar. También + y −.');else if(S.mode==='play')notify(S.flags.camera?'Revisa la fotografía del espejo en el escritorio.':'Todavía no tienes la cámara.')}
function zoomPhoto(delta){if(!S.started||S.paused||S.mode!=='photo'||S.photo!==3||!S.flags.camera||S.flags.photo)return;
 const l=S.lens;if(l.reveal)return;l.zoom=Math.max(1,Math.min(2.8,l.zoom+delta));
 if(l.zoom>=2.15&&!l.clue){l.clue=true;sound('static');$('live').textContent='Una mano oscura junto a Vale. Aleja la imagen.'}
 if(l.clue&&l.zoom<=1.08){l.reveal=.001;keys.clear();sound('dread');$('live').textContent='Hay alguien detrás de Vale.'}
}
function openTuner(){S.mode='tuning';S.tuner={value:18,target:63+Math.random()*18,hold:0,pulse:0};keys.clear();sound('radio');$('live').textContent='Sintoniza la radio con A y D. Mantén la señal estable.'}
function radioConversation(){''' + lines + '''}
function tuningUpdate(dt){const t=S.tuner,dir=+(keys.has('d')||keys.has('ArrowRight'))-+(keys.has('a')||keys.has('ArrowLeft'));t.value=Math.max(0,Math.min(100,t.value+dir*22*dt));const quality=Math.max(0,1-Math.abs(t.value-t.target)/17);t.hold=Math.abs(t.value-t.target)<3?t.hold+dt:0;t.pulse-=dt;
 if(t.pulse<=0){t.pulse=.16;hiss(.15,.012+(1-quality)*.06,800+(1-quality)*1500);if(quality>.7)beep(180+quality*90,.12,.012,'triangle')}
 if(t.hold>=1.2){sound('confirm');keys.clear();radioConversation()}
}
function tuningView(){const t=S.tuner,q=Math.max(0,1-Math.abs(t.value-t.target)/17);rect(0,25,480,276,'#08121e');text('RADIO / BUSCAR LA SEÑAL',240,40,'#b4bdb0',10,'center');frame(65,66,350,199,'#70847e');rect(72,73,336,185,'#243a43');rect(88,84,304,55,'#101e29');
 for(let i=0;i<74;i++){const amp=(1-q)*noise(i,Math.floor(S.time*14))*18+q*(3+Math.sin(i*.36+S.time*5)*3);rect(93+i*4,110-amp,2,amp*2+1,q>.82?'#b4c6a0':'#738d90')}
 for(let i=0;i<=20;i++)rect(94+i*14,147,1,i%5===0?12:6,'#839a95');rect(94+t.value*2.8,144,2,18,'#d9b27c');text((87+t.value*.21).toFixed(1)+' MHz',240,170,'#d0ceb1',10,'center');
 ellipse(240,218,27,27,'#101e28');ellipse(240,218,22,22,'#657e7b');ellipse(240,218,17,17,'#344d53');const ang=(-140+t.value*2.8)*Math.PI/180;line(240,218,240+Math.sin(ang)*19,218-Math.cos(ang)*19,'#ddcaa1',3);
 text('A  ◀',155,213,'#c3c6b2',10,'center');text('▶  D',325,213,'#c3c6b2',10,'center');text(t.hold>0?'SEÑAL ENCONTRADA · MANTÉN LA SINTONÍA':q>.7?'La voz está cerca...':'Busca una voz entre la interferencia.',240,277,'#abbcb0',8,'center');rect(179,253,122,2,'#172c36');rect(179,253,Math.min(1,t.hold/1.2)*122,2,'#cad4a7');
}
''' +s[b:]
# Captured callback formerly closes against inspect-local f.
s=s.replace("()=>{f.radio=true;notify('Una ubicación aparece marcada en el mapa.');save()})", "()=>{S.flags.radio=true;notify('Una ubicación aparece marcada en el mapa.');save()})")
a=s.index(" if(S.mode==='photo'&&S.analysis)");b=s.index(" if(S.mode!=='play')return;",a)
s=s[:a]+''' if(S.mode==='tuning'){tuningUpdate(dt);return}
 if(S.mode==='photo'){
  if(S.photo===3&&S.flags.camera&&!S.flags.photo){const l=S.lens;if(l.reveal){l.reveal+=dt;if(l.reveal>=.65&&!l.hit){l.hit=true;if(!S.reduce)sound('dread')}if(l.reveal>1.35){S.analysis=0;say([['Mateo','¿Qué...?']],()=>{beginScene('apparition');S.scene.jump=false})}}}
  return;
 }
'''+s[b:]
s=s.replace('function photoArt(index,x,y,scale=1,reveal=false)', 'function photoArt(index,x,y,scale=1,reveal=false,redEyes=true)')
s=s.replace('entity(88,107,1.35,true)', 'entity(88,107,1.35,redEyes)')
a=s.index('function photoView()');b=s.index('function mapView()',a)
s=s[:a]+'''function photoView(){rect(0,25,480,276,'#0b1420');
 if(S.photo===3&&S.flags.camera){const l=S.lens||{zoom:1,clue:false,reveal:0},revealed=!!l.reveal||S.flags.photo;
  frame(12,43,456,234,'#7a8c88');c.save();c.beginPath();c.rect(16,47,448,226);c.clip();rect(16,47,448,226,'#121e29');c.translate(240,160);c.scale(2.65*l.zoom,2.65*l.zoom);photoArt(3,-73,-71,1,revealed,l.reveal>.35||S.flags.photo);
  if(!revealed&&l.zoom>1.45){rect(7,0,2,12,'#1a202b');rect(9,3,1,8,'#1a202b');rect(11,4,1,6,'#202632');rect(6,-1,4,3,'#292b36')}
  c.restore();rect(16,47,448,14,'#0b1420c9');text('CÁMARA / ARCHIVO 04',26,50,'#a3b7b0',7);text(l.zoom.toFixed(1)+'×',454,50,'#cbd0bc',7,'right');
  text(revealed?'Hay alguien detrás de Vale.':l.clue?'Hay algo a su lado. Aleja la imagen.':'Examina el reflejo junto a Vale.',240,283,'#d1d2bc',8,'center');
  text(S.flags.photo?'E / ESC  VOLVER':'RUEDA  ZOOM · + / −  ALTERNATIVA · ESC  VOLVER',240,31,'#a8b7b2',7,'center');
  if(l.reveal>=.65&&l.reveal<1.05&&!S.reduce){rect(0,25,480,276,'#080e18ee');glow(240,162,120,'#7b3c452a');entity(240,318,4.7,true)}
  return;
 }
 text('FOTOGRAFÍAS / '+String(S.photo+1).padStart(2,'0')+' DE 04',24,38,'#9daeb1',8);photoArt(S.photo,170,60,1,S.flags.photo&&S.photo===3);text(photoCaptions[S.photo],240,245,'#d2d1c0',9,'center');text(S.photo<3?'E  SIGUIENTE FOTOGRAFÍA':'E  VOLVER Y RECOGER LA CÁMARA',240,272,'#aab5a6',8,'center');text('ESC  VOLVER',25,287,'#6d8996',7)
}
'''+s[b:]
s=s.replace("if(S.mode==='item')itemView();", "if(S.mode==='item')itemView();if(S.mode==='tuning')tuningView();")
s=s.replace("if(S.mode==='photo'&&S.analysis)return;", "if(S.mode==='photo'&&S.lens?.reveal&&!S.flags.photo)return;if(S.mode==='tuning'){S.mode='play';keys.clear();return;}")
s=s.replace("if(S.analysis>0)return;", "if(S.lens?.reveal&&!S.flags.photo)return;")
s=s.replace("if(k==='c'){useCamera();return}", "if(['+','=','-','_'].includes(k)){zoomPhoto(k==='+'||k==='='?.18:-.18);return}")
s=s.replace("canvas.onclick=()=>canvas.focus();", "canvas.addEventListener('wheel',e=>{if(S.mode==='photo'&&S.photo===3&&S.flags.camera){e.preventDefault();zoomPhoto(-Math.sign(e.deltaY)*Math.min(.22,Math.abs(e.deltaY)*.003))}},{passive:false});\ncanvas.onclick=()=>canvas.focus();")
s=s.replace("S.started=true;$('intro').hidden=true;", "resetPhotoLens();S.started=true;$('intro').hidden=true;")
s=s.replace("'Usa la cámara para analizar la fotografía del espejo.'", "'Examina con zoom la fotografía del espejo.'")
p.write_text(s,encoding='utf-8')
p=Path('work/build_chapter.py');s=p.read_text(encoding='utf-8');s=s.replace('C cámara;', 'rueda zoom; A/D sintonizar;').replace('C: analizar fotografía','Rueda: zoom · A/D: radio').replace('<kbd>C</kbd> Cámara','<kbd>Rueda</kbd> Zoom · <kbd>A / D</kbd> Radio').replace('C · Cámara','Ayuda cámara');p.write_text(s,encoding='utf-8')
