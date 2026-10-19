from pathlib import Path
p=Path(__file__).parent/'build_chapter.py'
s=p.read_text(encoding='utf-8-sig')
css='''
body{padding:12px}main{width:min(1080px,calc((100dvh - 170px)*1.5),100%)}header{margin-bottom:8px}.brand strong{margin-top:4px}.toolbar{margin-top:8px}.keys{margin-top:8px;line-height:1.5}.note{margin-top:6px;font-size:9px}.actions button{padding:6px 9px}#fullInGame{position:absolute;right:8px;top:30px;z-index:5;padding:5px 8px;background:#101b27d9;color:#bdc8bc;border-color:#485f69;font-size:12px}.stage:fullscreen #fullInGame{top:12px;right:12px}.stage:fullscreen{width:100vw;height:100dvh}.stage:fullscreen canvas{width:min(100vw,150dvh);max-height:100dvh}
@media(max-width:600px),(pointer:coarse){main{width:100%}.touch{margin-top:8px}.touch .pad{grid-template-columns:repeat(3,36px);gap:3px}.touch button{min-width:36px;min-height:36px}.keys{font-size:9px}.note{display:none}.touch .interact{font-size:10px}.overlay .sub{font-size:6px}}
'''
s=s.replace('</style></head>',css+'</style></head>')
s=s.replace('</canvas>', '</canvas><button id="fullInGame" aria-label="Pantalla completa" title="Pantalla completa (P)">⛶</button>')
s=s.replace('F: linterna · C:', 'F: linterna · R: cambiar pila · C:')
s=s.replace('<kbd>C</kbd> Cámara', '<kbd>R</kbd> Pila &nbsp; <kbd>C</kbd> Cámara')
s=s.replace('<kbd>Esc</kbd> Pausa', '<kbd>P</kbd> Pantalla completa &nbsp; <kbd>Esc</kbd> Pausa')
s=s.replace('C · Cámara</button>', 'C · Cámara</button><button class="interact" id="touchBattery">R · Pila</button>')
s=s.replace('Interferencia: normal','Efectos: intensos')
p.write_text(s,encoding='utf-8')
p=Path(__file__).parent/'chapter.js';s=p.read_text(encoding='utf-8')
s=s.replace("if(k==='p'){toggleFullscreen();return}","")
s=s.replace("if(!S.started||S.paused)return;if(['e'", "if(k==='p'){toggleFullscreen();return}if(!S.started||S.paused)return;if(['e'")
s=s.replace("S.reduce?'Interferencia: reducida':'Interferencia: normal'", "S.reduce?'Efectos: suaves':'Efectos: intensos'")
p.write_text(s,encoding='utf-8')
