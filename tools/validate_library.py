"""Check catalogue/media completeness and retain the render review manifest."""
from pathlib import Path
import hashlib
import json
import sys
import av
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from dna_animations.catalog import LESSONS
from tools.render_lessons import GIF_WIDTH, GIF_HEIGHT, GIF_FPS

OLD={"Replication":"replication","EnzymaticSynthesis":"synthesis",
     "PhosphoramiditeSynthesis":"synthesis","TemplateIndependentSynthesis":"synthesis",
     "PCR":"library","RTqPCR":"library","LAMP":"library","Sanger":"library",
     "Illumina":"library","Nanopore":"sequencing"}


def main():
    records=[]
    for name,module,family,notes in LESSONS:
        movie=ROOT/'media/videos/scenes/720p30'/f'{name}.mp4'
        gif=ROOT/'previews/v5'/f'{name}.gif'
        sheet=ROOT/'previews/review-v5'/f'{name}.jpg'
        audit=(ROOT/'media/v4'/OLD[name]/'layout_audit'/f'{name}.json' if name in OLD
               else ROOT/'media/expansion'/module/'layout_audit'/f'{name}.json')
        for path in [movie,gif,sheet,audit,ROOT/'docs'/f'{notes}.md']:
            assert path.is_file(),f'Missing {path}'
        intersections=json.loads(audit.read_text())
        assert intersections==[],f'Unresolved text intersections in {name}: {intersections}'
        with av.open(str(movie)) as c:
            stream=c.streams.video[0]
            duration=float(stream.duration*stream.time_base)
            assert (stream.width,stream.height)==(1280,720),(name,'movie size')
            # Concatenated Manim clips can differ by milliseconds in container
            # duration; verify the nominal rate and allow that rounding only.
            assert float(stream.base_rate)==30 and abs(float(stream.average_rate)-30)<.1,(name,'movie frame rate')
            assert 30<=duration<120,(name,duration)
        with Image.open(gif) as im:
            assert im.size==(GIF_WIDTH,GIF_HEIGHT),(name,'GIF size')
            assert im.info.get('loop')==0,(name,'GIF looping')
            assert im.n_frames>300,(name,'truncated GIF')
            frames=im.n_frames
            gif_duration=0
            for i in range(frames):
                im.seek(i)
                gif_duration+=im.info.get('duration',0)/1000
            assert abs(gif_duration-duration)<.25,(name,gif_duration,duration)
        records.append(dict(scene=name,family=family,seconds=round(duration,2),
            gif_frames=frames,gif_width=GIF_WIDTH,gif_height=GIF_HEIGHT,gif_fps=GIF_FPS,
            movie=str(movie.relative_to(ROOT)),gif=str(gif.relative_to(ROOT)),
            movie_sha256=hashlib.sha256(movie.read_bytes()).hexdigest(),
            audit=str(audit.relative_to(ROOT)),text_intersections=0,
            review_sheet=str(sheet.relative_to(ROOT)),notes=f'docs/{notes}.md'))
        print(f'{name}: {duration:.2f}s, {frames} GIF frames, audit clear')
    manifest=dict(lesson_count=len(records),new_lessons=len(records)-len(OLD),
        palette={'A':'#26745B','T/U':'#B46335','C':'#2E72B8','G':'#8756AA'},
        verification='Text intersections sampled during rendering; chapter and transition frames reviewed visually.',
        lessons=records)
    destination=ROOT/'previews/v5/manifest.json'
    destination.write_text(json.dumps(manifest,indent=2)+'\n')
    print(f'Verified {len(records)} complete lessons; manifest: {destination}')


if __name__=='__main__':
    main()
