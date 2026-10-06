"""Render teaching movies, looping GIFs, and frame contact sheets.

Run from project root with .venv/bin/python tools/render_lessons.py --help.
"""
import argparse
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from dna_animations.catalog import SCENE_NAMES as SCENES

GIF_WIDTH = 1280
GIF_HEIGHT = 720
GIF_FPS = 12

def run(cmd):
    subprocess.run(cmd, cwd=ROOT, check=True)


def export_gif(movie, destination, width=GIF_WIDTH, fps=GIF_FPS):
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(f".{destination.stem}.exporting.gif")
    try:
        run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(movie),
             "-filter_complex_threads", "1",
             "-filter_complex", f"[0:v]fps={fps},scale={width}:-1:flags=lanczos,split[a][b];"
             "[a]palettegen=max_colors=128:stats_mode=full[p];"
             "[b][p]paletteuse=dither=none:diff_mode=rectangle",
             "-loop", "0", str(temporary)])
        temporary.replace(destination)
    finally:
        temporary.unlink(missing_ok=True)


def contact_sheet(movie, destination, count=12):
    # Video frames are evidence for visual review, rather than passing a render
    # being treated as evidence of an accurate, legible lesson.
    import av
    from PIL import Image, ImageDraw
    with av.open(str(movie)) as container:
        stream = container.streams.video[0]
        duration = float(stream.duration * stream.time_base)
        times = [(i+.45)*duration/count for i in range(count)]
        images = []
        for i,t in enumerate(times):
            container.seek(int(t / stream.time_base),stream=stream)
            for frame in container.decode(stream):
                if float(frame.time or 0) >= t:
                    image = frame.to_image().convert("RGB")
                    image.thumbnail((480,270))
                    images.append((image,t))
                    break
    result = Image.new("RGB",(1440, 4*300),(245,245,242))
    draw = ImageDraw.Draw(result)
    for i,(image,t) in enumerate(images):
        xx, yy = (i%3)*480, (i//3)*300
        result.paste(image,(xx,yy+22))
        draw.text((xx+8,yy+4),f"{movie.stem}  |  {t:.1f}s",fill=(36,40,35))
    destination.parent.mkdir(parents=True,exist_ok=True)
    result.save(destination)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenes",nargs="*",metavar="SCENE",help="Lesson names; omit to render the full catalogue")
    parser.add_argument("--quality",choices=("draft","lesson"),default="lesson")
    parser.add_argument("--exports-only",action="store_true")
    parser.add_argument("--gif",action="store_true")
    parser.add_argument("--contact-sheet",action="store_true")
    args = parser.parse_args()
    unknown = set(args.scenes)-set(SCENES)
    if unknown:
        parser.error("Unknown scenes: " + ", ".join(sorted(unknown)))
    names = args.scenes or list(SCENES)
    resolution,fps = (("854,480",15) if args.quality=="draft" else ("1280,720",30))
    directory = "480p15" if args.quality=="draft" else "720p30"
    for name in names:
        if not args.exports_only:
            run([sys.executable,"-m","manim","--resolution",resolution,"--fps",str(fps),
                 "--progress_bar","none","dna_animations/scenes.py",name])
        movie = ROOT/"media/videos/scenes"/directory/f"{name}.mp4"
        if args.gif:
            export_gif(movie,ROOT/"previews/v5"/f"{name}.gif")
        if args.contact_sheet:
            contact_sheet(movie,ROOT/"previews/review-v5"/f"{name}.jpg")
        print(f"Ready: {movie}",flush=True)


if __name__=="__main__":
    main()
