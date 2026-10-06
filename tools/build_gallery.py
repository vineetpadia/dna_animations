"""Build the offline teaching gallery from the verified lesson catalogue."""
from pathlib import Path
import html
import json
import sys
import av

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from dna_animations.catalog import LESSONS
from dna_animations.scenes import SCENES


def main():
    folder=ROOT/'previews'
    posters=folder/'posters'
    posters.mkdir(parents=True,exist_ok=True)
    cards=[]
    families=list(dict.fromkeys(row[2] for row in LESSONS))
    for name,module,family,notes in LESSONS:
        movie=ROOT/'media/videos/scenes/720p30'/f'{name}.mp4'
        gif=folder/'v5'/f'{name}.gif'
        if not movie.exists() or not gif.exists():
            raise FileNotFoundError(f'Export the movie and GIF for {name} first')
        with av.open(str(movie)) as container:
            stream=container.streams.video[0]
            duration=float(stream.duration*stream.time_base)
            time=duration*.74
            container.seek(int(time/stream.time_base),stream=stream)
            for frame in container.decode(stream):
                if frame.time>=time:
                    poster=frame.to_image().convert('RGB')
                    poster.thumbnail((1280,720))
                    poster.save(posters/f'{name}.jpg',quality=88)
                    break
        title=SCENES[name].title
        esc=html.escape
        # Refresh browser caches when higher-resolution exports replace files.
        poster_src=f'posters/{name}.jpg?v={(posters/f"{name}.jpg").stat().st_mtime_ns}'
        gif_src=f'v5/{name}.gif?v={gif.stat().st_mtime_ns}'
        cards.append(f'''<article class="card" data-family="{esc(family)}" data-search="{esc(title.lower()+' '+name.lower()+' '+family.lower())}">
<div class="card-heading"><h2>{esc(title)}</h2><span>{duration:.0f}s</span></div>
<button class="screen" aria-label="Play {esc(title)}" type="button"><img src="{poster_src}" data-poster="{poster_src}" data-gif="{gif_src}" alt="{esc(title)} animation" loading="lazy" width="1280" height="720"></button>
<div class="card-controls"><button class="toggle" type="button" aria-pressed="false">Play GIF</button><button class="enlarge" type="button" aria-haspopup="dialog" aria-controls="viewer" aria-label="Enlarge {esc(title)}">Enlarge</button><a href="{gif_src}">GIF file</a><a class="video-link" href="../media/videos/scenes/720p30/{name}.mp4">Video</a><a href="../docs/{notes}.md">Teaching notes</a></div>
</article>''')
    options=''.join(f'<option>{html.escape(f)}</option>' for f in families)
    page='''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>DNA methods · Animation library</title>
<style>
:root{color-scheme:light;--paper:#f5f5f2;--ink:#242823;--muted:#6c7169;--line:#d2d5cd;--sage:#527569}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
main{max-width:1488px;margin:auto;padding:32px 24px}
header{max-width:900px;margin-bottom:30px}
h1{font-size:clamp(32px,4vw,52px);font-weight:560;letter-spacing:-.045em;margin:0 0 12px}
header p{color:var(--muted);font-size:18px;max-width:720px;margin:0 0 18px}
.palette{display:flex;gap:10px;flex-wrap:wrap}.nt{font-size:14px;border:1px solid currentColor;padding:3px 10px;border-radius:5px}
.a{color:#26745b;background:#d3e0d9}.t{color:#b46335;background:#eaddd3}.c{color:#2e72b8;background:#d5e0e8}.g{color:#8756aa;background:#e3dbe6}
.toolbar{display:flex;align-items:end;gap:14px;flex-wrap:wrap;margin:32px 0 12px}
.field{display:grid;gap:6px;flex:1;min-width:230px}.field label{font-size:13px;color:var(--muted)}
input,select,button{font:inherit}input,select{background:transparent;color:var(--ink);border:1px solid var(--line);border-radius:7px;padding:11px 12px;width:100%}
button,a{touch-action:manipulation}button{cursor:pointer;color:var(--ink);background:transparent;border:1px solid var(--line);border-radius:6px;padding:10px 14px}
button:hover,a:hover{color:var(--sage);border-color:var(--sage)}
button:focus-visible,a:focus-visible,input:focus-visible,select:focus-visible{outline:2px solid var(--sage);outline-offset:4px}
a{color:var(--muted);text-underline-offset:4px}#count{font-size:13px;color:var(--muted);margin:12px 0 25px}
.grid{display:grid;grid-template-columns:minmax(0,1fr);gap:32px}
.card{border:1px solid var(--line);border-radius:10px;overflow:hidden;min-width:0}.card[hidden]{display:none}
.card-heading{display:flex;justify-content:space-between;gap:12px;padding:18px 20px 8px;align-items:baseline}
.card-heading h2{font-size:21px;font-weight:550;letter-spacing:-.025em;margin:0}.card-heading span{font-size:13px;color:var(--muted);white-space:nowrap}
.screen{display:block;padding:0;border:0;width:100%;border-radius:0;line-height:0;background:var(--paper)}
.screen img{display:block;width:100%;height:auto;aspect-ratio:16/9;object-fit:contain}
.card-controls{padding:12px 20px 18px;display:flex;align-items:center;gap:18px;flex-wrap:wrap;font-size:14px}
.toggle,.enlarge{font-weight:550;padding:7px 12px;min-width:90px}
footer{margin-top:40px;color:var(--muted);font-size:13px;max-width:760px}#empty{color:var(--muted);padding:20px 0}
body.viewer-open{overflow:hidden}
#viewer{margin:auto;padding:0;border:1px solid var(--line);border-radius:10px;background:var(--paper);color:var(--ink);width:calc(100vw - 24px);max-width:none;height:calc(100vh - 24px);height:calc(100dvh - 24px);max-height:none;overflow:hidden}
#viewer[open]{display:flex;flex-direction:column}
#viewer::backdrop{background:rgba(17,20,17,.72)}
.viewer-bar{display:flex;align-items:center;gap:16px;padding:12px 18px;flex:0 0 auto}
.viewer-bar h2{font-size:clamp(17px,2vw,23px);font-weight:550;line-height:1.25;margin:0;flex:1;min-width:0}
#viewer-close{flex:0 0 auto}
.viewer-stage{display:flex;align-items:center;justify-content:center;flex:1 1 auto;min-height:0;min-width:0;padding:0 12px}
.viewer-stage img{display:block;width:100%;height:100%;object-fit:contain}
.viewer-controls{display:flex;align-items:center;gap:18px;flex-wrap:wrap;padding:12px 18px;flex:0 0 auto;font-size:14px}
#viewer-hint{color:var(--muted);margin-left:auto;font-size:13px}
@media(max-width:650px){main{padding:24px 12px}.grid{gap:24px}.card-controls{gap:12px;padding:12px 14px 16px}.card-heading{padding:14px 14px 6px}.card-heading h2{font-size:18px}.viewer-bar,.viewer-controls{padding:10px 12px}.viewer-stage{padding:0 4px}#viewer-hint{display:none}}
</style></head><body><main>
<header><h1>DNA methods, in motion.</h1><p>Follow the molecules from sample preparation to synthesis, assembly, amplification and sequencing. Select a lesson to play its full animation.</p>
<div class="palette" aria-label="Consistent nucleotide colors"><span class="nt a">A · adenine</span><span class="nt t">T / U · thymine / uracil</span><span class="nt c">C · cytosine</span><span class="nt g">G · guanine</span></div></header>
<div class="toolbar"><div class="field"><label for="search">Find a technique</label><input id="search" type="search" placeholder="e.g. MutS, PCR, editing"></div><div class="field"><label for="family">Browse a family</label><select id="family"><option value="">All families</option>'''+options+'''</select></div><button id="pause" type="button">Stop all</button></div>
<p id="count" role="status" aria-live="polite"></p><div class="grid">'''+''.join(cards)+'''</div><p id="empty" hidden>No matching lessons.</p>
<footer>Conceptual teaching diagrams. Sequences and molecular dimensions are simplified; teaching notes retain the mechanism, sources and scope. Video files offer smoother motion and a scrubber for classroom discussion.</footer>
</main>
<dialog id="viewer" aria-labelledby="viewer-title" aria-describedby="viewer-hint">
<div class="viewer-bar"><h2 id="viewer-title"></h2><button id="viewer-close" type="button" aria-label="Close enlarged lesson" autofocus>Close ×</button></div>
<div class="viewer-stage"><img id="viewer-image" alt="" width="1280" height="720"></div>
<div class="viewer-controls"><button id="viewer-toggle" type="button" aria-pressed="false">Play GIF</button><button id="viewer-fullscreen" type="button">Full screen</button><a id="viewer-video">Video</a><span id="viewer-hint">Escape to close</span></div>
</dialog><script>
const cards=[...document.querySelectorAll('.card')],search=document.querySelector('#search'),family=document.querySelector('#family');
const viewer=document.querySelector('#viewer'),viewerImage=document.querySelector('#viewer-image'),viewerToggle=document.querySelector('#viewer-toggle');
const fullscreenButton=document.querySelector('#viewer-fullscreen');
let viewerCard=null,viewerPlaying=false,viewerReturnFocus=null,viewerOwnsFullscreen=false;
function stop(card){const img=card.querySelector('img');if(card.dataset.playing==='true')img.src=img.dataset.poster;card.dataset.playing='false';const button=card.querySelector('.toggle');button.textContent='Play GIF';button.setAttribute('aria-pressed','false');card.querySelector('.screen').setAttribute('aria-label','Play '+card.querySelector('h2').textContent)}
function toggle(card){if(card.dataset.playing==='true'){stop(card);return}const img=card.querySelector('img');img.src=img.dataset.gif;card.dataset.playing='true';const button=card.querySelector('.toggle');button.textContent='Stop';button.setAttribute('aria-pressed','true');card.querySelector('.screen').setAttribute('aria-label','Stop '+card.querySelector('h2').textContent)}
function setViewerPlaying(playing){if(!viewerCard)return;const img=viewerCard.querySelector('img');viewerPlaying=playing;viewerImage.src=playing?img.dataset.gif:img.dataset.poster;viewerToggle.textContent=playing?'Stop':'Play GIF';viewerToggle.setAttribute('aria-pressed',String(playing))}
function openViewer(card,trigger){cards.forEach(stop);viewerCard=card;viewerReturnFocus=trigger;const title=card.querySelector('h2').textContent;document.querySelector('#viewer-title').textContent=title;viewerImage.alt=title+' animation';document.querySelector('#viewer-video').href=card.querySelector('.video-link').href;document.body.classList.add('viewer-open');viewer.showModal();setViewerPlaying(true);document.querySelector('#viewer-close').focus()}
cards.forEach(card=>{card.querySelector('.screen').addEventListener('click',()=>toggle(card));card.querySelector('.toggle').addEventListener('click',()=>toggle(card));const enlarge=card.querySelector('.enlarge');enlarge.addEventListener('click',()=>openViewer(card,enlarge))});
viewerToggle.addEventListener('click',()=>setViewerPlaying(!viewerPlaying));
document.querySelector('#viewer-close').addEventListener('click',()=>viewer.close());
// A native modal dialog traps focus and closes on Escape. Only an actual
// backdrop click closes it; clicks on the image and its letterbox remain safe.
viewer.addEventListener('click',event=>{if(event.target!==viewer)return;const r=viewer.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)viewer.close()});
viewer.addEventListener('close',()=>{viewerImage.removeAttribute('src');viewerCard=null;viewerPlaying=false;viewerToggle.textContent='Play GIF';viewerToggle.setAttribute('aria-pressed','false');document.body.classList.remove('viewer-open');if(viewerOwnsFullscreen&&document.fullscreenElement)document.exitFullscreen().catch(()=>{});viewerOwnsFullscreen=false;const trigger=viewerReturnFocus;viewerReturnFocus=null;if(trigger&&trigger.isConnected)trigger.focus({preventScroll:true})});
fullscreenButton.hidden=!document.fullscreenEnabled;
fullscreenButton.addEventListener('click',async()=>{try{if(document.fullscreenElement){await document.exitFullscreen();viewerOwnsFullscreen=false}else{await document.documentElement.requestFullscreen();viewerOwnsFullscreen=true}}catch{fullscreenButton.hidden=true}});
document.addEventListener('fullscreenchange',()=>{fullscreenButton.textContent=document.fullscreenElement?'Exit full screen':'Full screen';if(!document.fullscreenElement)viewerOwnsFullscreen=false});
function filter(){const q=search.value.trim().toLowerCase();let shown=0;cards.forEach(card=>{const match=(!family.value||card.dataset.family===family.value)&&q.split(/\\s+/).every(word=>card.dataset.search.includes(word));card.hidden=!match;if(match)shown++;else stop(card)});document.querySelector('#count').textContent=shown+' of '+cards.length+' lessons';document.querySelector('#empty').hidden=shown>0}
search.addEventListener('input',filter);family.addEventListener('change',filter);document.querySelector('#pause').addEventListener('click',()=>cards.forEach(stop));filter();
</script></body></html>'''
    (folder/'index.html').write_text(page)
    print(f'Built {len(cards)} lesson cards: {folder/"index.html"}')


if __name__=='__main__':
    main()
