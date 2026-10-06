"""Shared visual language and carefully paced teaching-scene helpers.

Base identity belongs to the letter/tile. Strand role belongs to its backbone.
Every molecular strand has explicit polarity; input sequence is spatial order.
"""
import numpy as np
import os
import json
from pathlib import Path
from manim import *

BG = "#F5F5F2"
OLD = "#747B72"
NEW = "#252925"
PRIMER = "#9C6738"
ENZYME = "#6D746A"
SIGNAL = "#527569"
STOP = "#A3513D"
MUTED = "#6C7169"
TEXT = "#242823"
WHITE = TEXT  # Compatibility name: this is the foreground, never literal white.
HAIRLINE = "#D2D5CD"
BASE_COLORS = {"A":"#26745B", "T":"#B46335", "C":"#2E72B8", "G":"#8756AA", "U":"#B46335"}
# Fixed illustrative identity colors; not a claim about instrument dye spectra.
DYE_COLORS = BASE_COLORS.copy()


def label(text, size=22, color=WHITE):
    if not str(text).strip():
        return Text("·", font="Nimbus Sans", font_size=size, color=color).set_opacity(0)
    return Text(str(text), font="Nimbus Sans", font_size=size, color=color,
                disable_ligatures=True)


def caption(text, at, size=20, color=MUTED):
    return label(text, size, color).move_to(at)


def tag(text, color=MUTED):
    name = label(text, 17, color)
    shape = RoundedRectangle(width=name.width + 0.32, height=0.4,
        corner_radius=0.035, stroke_color=HAIRLINE, stroke_width=.8,
        fill_color=BG, fill_opacity=1).move_to(name)
    return VGroup(shape, name)


def base_tile(base, scale=1):
    if base not in BASE_COLORS:
        raise ValueError(f"Unknown base {base}")
    color=BASE_COLORS[base]
    tint=interpolate_color(ManimColor(BG),ManimColor(color),.16)
    tile = RoundedRectangle(width=0.39, height=0.34, corner_radius=0.035,
        stroke_color=color, stroke_width=1.15,
        fill_color=tint, fill_opacity=1)
    return VGroup(tile, label(base, 18, color)).scale(scale)


def enzyme(name="pol", width=1.1):
    text = label(name, 19, WHITE)
    if text.width > width - .18:
        text.scale_to_fit_width(width - .18)
    body = RoundedRectangle(width=width, height=.65, corner_radius=.10,
        stroke_color=ENZYME, stroke_width=1.2, fill_color=ENZYME, fill_opacity=.055)
    return VGroup(body, text)


def arrow(start, end, color=NEW):
    return Arrow(start, end, buff=0, color=color, stroke_width=3,
                 max_tip_length_to_length_ratio=.16)


def block():
    return VGroup(Line(UP * .18, DOWN * .18, color=STOP, stroke_width=5),
                  Line(UP * .18 + LEFT * .08, UP * .18 + RIGHT * .08,
                       color=STOP, stroke_width=4))


def complement(sequence, rna=False):
    table = str.maketrans("ACGTU", "TGCAA")
    if any(b not in "ACGTU" for b in sequence):
        raise ValueError("Use uppercase A/C/G/T/U")
    result = sequence.translate(table)
    return result.replace("T", "U") if rna else result


class Strand(VGroup):
    """Strand with spatially indexed bases and a role-colored backbone.

    direction=+1: 5′ left, 3′ right; direction=-1 reverses polarity labels.
    side controls which side of the backbone its bases face.
    """
    def __init__(self, sequence, x=-3, y=0, step=.58, direction=1,
                 role=OLD, side=-1, labels=True, **kwargs):
        super().__init__(**kwargs)
        if not sequence or direction not in (-1, 1):
            raise ValueError("A strand needs a sequence and direction ±1")
        self.sequence, self.direction, self.role = sequence, direction, role
        self.spacing, self.side = step, side
        self.units = VGroup()
        self.bases = VGroup()
        self._anchors = []
        for i, b in enumerate(sequence):
            pos = np.array([x + i * step, y, 0.])
            # Each base owns the incoming backbone segment; covalent links
            # can therefore be created as incorporation happens.
            if direction == 1:
                start = pos - RIGHT * (step if i else .15)
            else:
                start = pos + RIGHT * (step if i < len(sequence)-1 else .15)
            backbone = Line(start, pos, color=role, stroke_width=2.3 if role==OLD else 3.2)
            stem = Line(pos, pos + UP * side * .12, color=role, stroke_width=2)
            tile = base_tile(b).move_to(pos + UP * side * .30)
            self.units.add(VGroup(backbone, stem, tile))
            self.bases.add(tile)
            self._anchors.append(stem)
        self.ends = VGroup()
        if labels:
            left, right = ("5′", "3′") if direction == 1 else ("3′", "5′")
            self.ends.add(label(left, 18, role).move_to([x - .43, y, 0]),
                          label(right, 18, role).move_to([x + (len(sequence)-1)*step + .43, y, 0]))
        self.add(self.units, self.ends)

    def at(self, index):
        return self.bases[index].get_center()

    def anchor(self, index):
        return self._anchors[index].get_start()

    def pairing(self, other, indices=None):
        indices = range(min(len(self.sequence), len(other.sequence))) if indices is None else indices
        bonds = VGroup()
        for i in indices:
            p, q = self.at(i), other.at(i)
            unit = (q-p) / np.linalg.norm(q-p)
            bonds.add(DashedLine(p+unit*.18, q-unit*.18, dash_length=.06,
                                 color=MUTED, stroke_width=1.2))
        return bonds


class Lesson(Scene):
    title = "DNA processes"
    subtitle = ""
    steps = ()

    def setup(self):
        self.camera.background_color = BG
        self.header = label(self.title, 28).move_to([0,3.35,0])
        self.header.align_to(np.array([-6.05,3.35,0]),LEFT)
        self.counter = label(f"01 / {max(1,len(self.steps)):02d}",14,MUTED).move_to([5.65,3.35,0])
        self.subheading, self.progress, self.rule, self.legend = (VGroup() for _ in range(4))
        self.cue = label(" ",22).move_to([0,-3.22,0])
        self.hud = [self.header,self.counter,self.cue]
        self._audit_enabled = os.environ.get("BIO_LAYOUT_AUDIT") == "1"
        self._audit_clock, self._audit_last = 0., -1.
        self._audit_pairs = {}
        self.add(*self.hud)

    def step(self, i, cue, hold=.4):
        if len(cue) > 60:
            raise ValueError(f"Cue too long: {cue}")
        new = label(cue, 22).move_to([0,-3.22,0])
        if new.width > 11.6:
            raise ValueError(f"Shorten the caption rather than shrinking it: {cue}")
        anims = [FadeOut(self.cue, shift=DOWN*.04)]
        self.play(*anims, run_time=.2)
        self.cue = new
        self.hud[2] = new
        next_counter=label(f"{min(i+1,max(1,len(self.steps))):02d} / {max(1,len(self.steps)):02d}",14,MUTED).move_to(self.counter)
        self.remove(self.counter)
        self.counter=next_counter
        self.hud[1]=next_counter
        self.add(next_counter)
        self.play(FadeIn(new, shift=UP*.04), run_time=.25)
        if hold:
            self.wait(hold)

    def pause(self, t=1):
        self.wait(t)

    def clear_stage(self, run_time=.6):
        stage = [m for m in self.mobjects if all(m is not h for h in self.hud)]
        if stage:
            self.play(*[FadeOut(m) for m in stage], run_time=run_time)

    def finish(self, cue, hold=2.5):
        self.step(len(self.steps)-1, cue, hold=0)
        self.wait(hold)

    def update_mobjects(self, dt):
        super().update_mobjects(dt)
        if not getattr(self,"_audit_enabled",False):
            return
        self._audit_clock = float(self.renderer.time)
        if self._audit_clock-self._audit_last < .22:
            return
        self._audit_last=self._audit_clock
        texts=[]
        seen=set()
        for m in self.get_mobject_family_members():
            if not isinstance(m,Text) or id(m) in seen or not m.text.strip():
                continue
            seen.add(id(m))
            opacity=max((float(g.get_fill_opacity()) for g in m.family_members_with_points()),default=0)
            if opacity<.55 or m.width<.02:
                continue
            texts.append((m,m.get_left()[0],m.get_right()[0],m.get_bottom()[1],m.get_top()[1]))
        for ai,a in enumerate(texts):
            for b in texts[ai+1:]:
                w=min(a[2],b[2])-max(a[1],b[1])
                h=min(a[4],b[4])-max(a[3],b[3])
                if w>.015 and h>.025 and w*h>.12*min((a[2]-a[1])*(a[4]-a[3]),(b[2]-b[1])*(b[4]-b[3])):
                    key=(a[0].text,b[0].text,round((a[1]+a[2])/2,1),round((b[1]+b[2])/2,1))
                    if key not in self._audit_pairs:
                        self._audit_pairs[key]={"time":round(self._audit_clock,2),"a":a[0].text,"b":b[0].text,
                            "a_xy":[round((a[1]+a[2])/2,2),round((a[3]+a[4])/2,2)],
                            "b_xy":[round((b[1]+b[2])/2,2),round((b[3]+b[4])/2,2)]}

    def tear_down(self):
        if getattr(self,"_audit_enabled",False):
            folder=Path(config.media_dir)/"layout_audit"
            folder.mkdir(parents=True,exist_ok=True)
            (folder/f"{type(self).__name__}.json").write_text(json.dumps(list(self._audit_pairs.values()),indent=2))
        super().tear_down()
