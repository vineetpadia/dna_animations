"""From a biological sample to purified and size-separated DNA."""
from manim import *
import numpy as np
from dna_animations.core import (Lesson, Strand, complement, caption, label, enzyme,
    BG, OLD, NEW, PRIMER, ENZYME, SIGNAL, STOP, MUTED, HAIRLINE)


def duplex(sequence, center=(0, 0, 0), scale=1):
    x = -(len(sequence)-1)*.58/2
    top = Strand(sequence, x=x, y=.55, side=-1, direction=1)
    bottom = Strand(complement(sequence), x=x, y=-.55, side=1, direction=-1)
    bonds = top.pairing(bottom)
    return VGroup(top, bottom, bonds).scale(scale).move_to(center)


class DNAExtraction(Lesson):
    title = "DNA extraction & purification"
    steps = ("Release", "Digest", "Bind", "Wash", "Elute", "Recover")

    def construct(self):
        cell = Ellipse(width=4.3, height=2.8, color=OLD, stroke_width=2).move_to([-3.3,.1,0])
        dna = duplex("ATGCCGTA", [-3.3,.25,0], .67)
        proteins = VGroup(*[RoundedRectangle(width=.3,height=.18,corner_radius=.07,
            color=ENZYME,fill_color=ENZYME,fill_opacity=.3,stroke_width=1).move_to(p)
            for p in [(-4.6,-.65,0),(-3.7,-.8,0),(-2.5,-.55,0),(-2.1,.85,0),(-4.1,1.05,0)]])
        cell_name = caption("cell",[-3.3,1.9,0],19)
        self.step(0,"Open the cell to release its DNA")
        self.play(Create(cell),FadeIn(cell_name),FadeIn(dna),FadeIn(proteins),run_time=1.5)
        self.pause(2)
        detergent = enzyme("lysis",1.0).move_to([-5.4,1.9,0])
        self.play(FadeIn(detergent),run_time=.6)
        self.play(cell.animate.scale(1.16).set_opacity(0),
                  *[m.animate.shift((m.get_center()-cell.get_center())*.32)
                    for m in proteins],FadeOut(cell_name),run_time=2)
        self.remove(cell)
        self.pause(1.4)
        self.step(1,"Break down proteins around the DNA")
        protease=enzyme("protease",1.5).move_to([-3.4,-1.95,0])
        self.play(FadeOut(detergent),FadeIn(protease),run_time=.65)
        fragments=VGroup(*[VGroup(*[Dot(radius=.035,color=ENZYME).move_to(
            p.get_center()+np.array([.14*(k-1),-.15*(k%2),0])) for k in range(3)]) for p in proteins])
        self.play(*[ReplacementTransform(p,f) for p,f in zip(proteins,fragments)],run_time=1.4)
        self.pause(2)
        self.play(FadeOut(protease),run_time=.5)
        column=VMobject(color=OLD,stroke_width=2).set_points_as_corners([
            [1.05,1.8,0],[1.05,.25,0],[1.48,-.58,0],[3.02,-.58,0],[3.45,.25,0],[3.45,1.8,0]])
        membrane=Rectangle(width=1.92,height=.18,color=MUTED,fill_color=OLD,
            fill_opacity=.2,stroke_width=1.1).move_to([2.25,-.08,0])
        column_name=caption("silica",[4.35,-.08,0],18)
        pointer=Line([3.3,-.08,0],[3.87,-.08,0],color=MUTED,stroke_width=1)
        salt=caption("binding buffer",[2.25,2.2,0],18)
        self.step(2,"Binding conditions hold DNA on silica")
        self.play(Create(column),Create(membrane),FadeIn(column_name),Create(pointer),FadeIn(salt),run_time=1.2)
        self.play(dna.animate.scale(.62).move_to([2.25,.42,0]),
                  fragments.animate.move_to([2.25,1.25,0]).scale(.65),run_time=2.5)
        self.pause(1.8)
        waste=RoundedRectangle(width=2.25,height=.78,corner_radius=.16,color=OLD,
            stroke_width=1.4).move_to([2.25,-1.7,0])
        waste_name=caption("waste",[4.17,-1.7,0],18)
        self.play(Create(waste),FadeIn(waste_name),run_time=.6)
        self.play(fragments.animate.move_to([2.25,-1.7,0]),run_time=1.8)
        self.pause(1.4)
        self.step(3,"Wash away contaminants while DNA stays bound")
        self.play(FadeOut(salt),run_time=.3)
        wash=caption("wash",[2.25,2.2,0],18)
        flow=VGroup(*[Arrow([xx,1.65,0],[xx,.95,0],buff=0,color=SIGNAL,
            stroke_width=1.5,tip_length=.1) for xx in (1.65,2.25,2.85)])
        self.play(FadeIn(wash),Create(flow),run_time=.9)
        for _ in range(2):
            self.play(flow.animate.shift(DOWN*.65).set_opacity(.2),run_time=1)
            self.remove(flow)
            flow.shift(UP*.65).set_opacity(1)
            self.add(flow)
            self.pause(.6)
        self.play(FadeOut(flow),FadeOut(wash),FadeOut(fragments),run_time=.6)
        self.play(VGroup(waste,waste_name).animate.shift(RIGHT*2).set_opacity(0),run_time=1)
        self.pause(1)
        collection=RoundedRectangle(width=2.25,height=1.0,corner_radius=.2,color=OLD,
            stroke_width=1.6).move_to([2.25,-1.75,0])
        water=caption("elution buffer",[2.25,2.2,0],18)
        self.step(4,"Low-salt buffer releases DNA into a clean tube")
        self.play(Create(collection),FadeIn(water),run_time=.9)
        self.pause(1.5)
        self.play(dna.animate.move_to([2.25,-1.75,0]),run_time=2.5)
        self.pause(2.2)
        self.play(FadeOut(column),FadeOut(membrane),FadeOut(column_name),
                  FadeOut(pointer),FadeOut(water),FadeOut(collection),run_time=.8)
        self.step(5,"Purified DNA is ready for the next method")
        self.play(dna.animate.scale(2.4).move_to([0,.1,0]),run_time=2)
        self.pause(3.5)


class GelElectrophoresis(Lesson):
    title = "Gel electrophoresis"
    steps = ("Load", "Field", "Separate", "Ladder", "Read")

    def construct(self):
        gx, top, bottom = 1.65,1.85,-2.12
        lane_x=[.1,1.65,3.2]
        gel=RoundedRectangle(width=4.8,height=top-bottom,corner_radius=.12,
            color=OLD,stroke_width=1.3,fill_color=OLD,fill_opacity=.035).move_to([gx,(top+bottom)/2,0])
        wells=VGroup(*[Rectangle(width=.78,height=.21,color=OLD,stroke_width=1.2,
            fill_color=BG,fill_opacity=1).move_to([xx,1.5,0]) for xx in lane_x])
        names=VGroup(*[caption(n,[xx,2.18,0],17) for xx,n in zip(lane_x,["ladder","sample","check"])])
        molecules=VGroup()
        sizes=[1200,600,300]
        for i,n in enumerate(sizes):
            length=n/500
            yy=1.15-i*1.12
            molecule=VGroup(Line([-5.4,yy+.08,0],[-5.4+length,yy+.08,0],color=NEW,stroke_width=2),
                Line([-5.4,yy-.08,0],[-5.4+length,yy-.08,0],color=OLD,stroke_width=2))
            molecule.add(*[Line([-5.4+j*length/8,yy-.08,0],[-5.4+j*length/8,yy+.08,0],
                color=OLD,stroke_width=1) for j in range(9)])
            molecules.add(molecule)
        sizes_text=VGroup(*[caption(f"{n} bp",[-4.3,1.58-i*1.12,0],17) for i,n in enumerate(sizes)])
        self.step(0,"Load DNA fragments into wells")
        self.play(Create(gel),Create(wells),FadeIn(names),Create(molecules),FadeIn(sizes_text),run_time=1.6)
        self.pause(2)
        sample=VGroup(*[Line([1.32,1.5-i*.035,0],[1.98,1.5-i*.035,0],color=NEW,stroke_width=3) for i in range(3)])
        self.play(*[ReplacementTransform(molecules[i],sample[i]) for i in range(3)],
                  FadeOut(sizes_text),run_time=2.3)
        ladder=VGroup(*[Line([-.24,1.5-i*.025,0],[.44,1.5-i*.025,0],color=OLD,stroke_width=3) for i in range(5)])
        check=Line([2.87,1.5,0],[3.53,1.5,0],color=NEW,stroke_width=3)
        self.play(FadeIn(ladder),FadeIn(check),run_time=.8)
        self.pause(1.7)
        self.step(1,"Negatively charged DNA moves toward the + electrode")
        polarity=VGroup(caption("−",[4.85,1.72,0],26),caption("+",[4.85,-2.05,0],26),
            Arrow([4.85,1.27,0],[4.85,-1.57,0],color=SIGNAL,buff=0,stroke_width=2,tip_length=.15))
        self.play(FadeIn(polarity),run_time=1)
        self.pause(3)
        self.step(2,"Shorter linear fragments travel farther")
        # Same length -> same destination; migration is schematic, not a fit.
        ys={1500:1.0,1200:.61,900:.18,600:-.49,300:-1.48}
        self.play(*[b.animate.set_y(ys[n]) for b,n in zip(sample,sizes)],
            *[b.animate.set_y(ys[n]) for b,n in zip(ladder,[1500,1200,900,600,300])],
            check.animate.set_y(ys[600]),run_time=7,rate_func=linear)
        self.pause(3)
        self.step(3,"Known ladder bands provide a size reference")
        ticks=VGroup(*[caption(str(n),[-1.21,ys[n],0],16) for n in [1500,1200,900,600,300]])
        bp=caption("bp",[-1.21,1.55,0],17)
        self.play(FadeIn(ticks),FadeIn(bp),run_time=1.2)
        line=DashedLine([-.26,ys[600],0],[3.61,ys[600],0],color=SIGNAL,stroke_width=1,dash_length=.07)
        self.play(Create(line),run_time=1)
        self.pause(3)
        self.step(4,"Matching migration suggests matching fragment length")
        self.play(Indicate(sample[1],color=SIGNAL),Indicate(check,color=SIGNAL),run_time=1.5)
        self.pause(2)
        self.play(FadeOut(line),run_time=.5)
        self.finish("A band contains many fragments of similar length",hold=4)
