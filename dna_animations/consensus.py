"""MutS filtering combined with overlap reassembly: consensus shuffling."""
from manim import *
import numpy as np
from dna_animations.core import (Lesson, Strand, complement, caption, enzyme,
    BG, OLD, NEW, ENZYME, SIGNAL, STOP, MUTED)
from dna_animations.foundations import duplex
from dna_animations.editing import bond


class ConsensusShuffling(Lesson):
    title="Consensus shuffling"
    steps=("Copies","Re-pair","Fragment","Filter","Reassemble","Enrich")

    def construct(self):
        sequences=["ATGCCGTA","ATGTCGTA","ATGCCGTA"]
        copies=[duplex(s,[0,y,0],.72) for s,y in zip(sequences,[1.55,0,-1.55])]
        tops=[c[0] for c in copies]
        bottoms=[c[1] for c in copies]
        self.step(0,"Synthetic copies can contain different sequence errors")
        self.play(*[FadeIn(c) for c in copies],run_time=1.5)
        error=SurroundingRectangle(VGroup(tops[1].bases[3],bottoms[1].bases[3]),
            buff=.08,color=STOP,stroke_width=1.2)
        self.play(Create(error),run_time=.6)
        self.pause(2.4)
        self.step(1,"Re-pair strands from different copies to expose errors")
        self.play(FadeOut(error),*[FadeOut(c[2]) for c in copies],
                  *[t.animate.shift(UP*.12) for t in tops],
                  *[b.animate.shift(DOWN*.24) for b in bottoms],run_time=1.4)
        loc0,loc1=bottoms[0].get_center().copy(),bottoms[1].get_center().copy()
        self.play(bottoms[0].animate.shift(RIGHT*3.7),bottoms[1].animate.shift(LEFT*3.7),run_time=1.2)
        self.play(bottoms[0].animate.set_y(loc1[1]),bottoms[1].animate.set_y(loc0[1]),run_time=1.2)
        self.play(bottoms[0].animate.set_x(loc1[0]),bottoms[1].animate.set_x(loc0[0]),run_time=1.2)
        self.play(*[t.animate.shift(DOWN*.12) for t in tops],
                  *[b.animate.shift(UP*.24) for b in bottoms],run_time=1.1)
        row_bottom=[bottoms[1],bottoms[0],bottoms[2]]
        pairs=[]
        for r in range(3):
            pairs.append(VGroup(*[bond(tops[r].at(i),row_bottom[r].at(i),
                STOP if r<2 and i==3 else MUTED) for i in range(8)]))
        self.play(*[Create(v) for v in pairs],run_time=.9)
        mismatch=VGroup(*[SurroundingRectangle(VGroup(tops[r].bases[3],row_bottom[r].bases[3]),
            buff=.09,color=STOP,stroke_width=1.5) for r in range(2)])
        self.play(Create(mismatch),run_time=.6)
        self.pause(2.5)
        self.step(2,"Overlapping fragments preserve usable parts of each copy")
        self.play(FadeOut(mismatch),run_time=.35)
        fragments=[]
        for r,cut in enumerate([4,6,6]):
            top,bot=tops[r],row_bottom[r]
            top.units[cut][0].set_opacity(0)
            bot.units[cut-1][0].set_opacity(0)
            # Remove whole-strand labels; each fragment gets its own ends.
            self.remove(top.ends,bot.ends)
            top.ends.set_opacity(0);bot.ends.set_opacity(0)
            left=VGroup(*top.units[:cut],*bot.units[:cut],*pairs[r][:cut])
            right=VGroup(*top.units[cut:],*bot.units[cut:],*pairs[r][cut:])
            self.play(left.animate.shift(LEFT*.18),right.animate.shift(RIGHT*.18),run_time=.5)
            fragments.append((left,right))
        self.pause(1.5)
        # Track four actual fragments from the displayed pool. The two other
        # short ends leave the zoomed view, not a claim of biochemical removal.
        bad_a,bad_b=fragments[0][0],fragments[1][0]
        good_a,good_b=fragments[2][0],fragments[0][1]
        self.play(FadeOut(fragments[1][1]),FadeOut(fragments[2][1]),
            bad_a.animate.scale(1.16).move_to([-3.45,1.03,0]),
            bad_b.animate.scale(1.16).move_to([-3.45,-1.07,0]),
            good_a.animate.scale(1.16).move_to([2.75,-1.07,0]),
            good_b.animate.scale(1.16).move_to([2.75,1.03,0]),run_time=2)
        mismatch_indices=[(tops[0],row_bottom[0]),(tops[1],row_bottom[1])]
        marks=VGroup(*[SurroundingRectangle(VGroup(t.bases[3],b.bases[3]),buff=.09,
            color=STOP,stroke_width=1.4) for t,b in mismatch_indices])
        self.play(Create(marks),run_time=.7)
        fragment_ends=VGroup()
        for top,bot,start in [(tops[0],row_bottom[0],0),(tops[1],row_bottom[1],0),
                              (tops[2],row_bottom[2],0),(tops[0],row_bottom[0],4)]:
            fragment_ends.add(caption("5′",top.anchor(start)+LEFT*.26,14,OLD),
                              caption("3′",bot.anchor(start)+LEFT*.26,14,OLD))
        self.play(FadeIn(fragment_ends),run_time=.4)
        self.pause(1.5)
        self.step(3,"Immobilized MutS retains mismatch-containing fragments")
        support=Rectangle(width=.25,height=3.5,color=ENZYME,fill_color=ENZYME,
            fill_opacity=.12,stroke_width=1).move_to([-5.75,-.02,0])
        muts=VGroup(*[enzyme("MutS",.9).move_to([mark.get_center()[0],y+.8,0])
                     for mark,y in zip(marks,[1.03,-1.07])])
        tether=VGroup(*[Line([-5.63,m.get_y(),0],m.get_left(),color=ENZYME,
                            stroke_width=1.3) for m in muts])
        self.play(Create(support),FadeIn(muts),Create(tether),run_time=1)
        # Two schematic tethers connect the immobilized recognition proteins
        # to the mismatches; the DNA is captured rather than chemically fixed.
        capture=VGroup(*[Line(m.get_bottom(),mark.get_top(),color=SIGNAL,stroke_width=1.3)
                        for m,mark in zip(muts,marks)])
        self.play(Create(capture),run_time=.8)
        self.pause(2.2)
        retained=caption("unbound fragments",[2.75,2.1,0],18)
        self.play(FadeIn(retained),good_a.animate.shift(RIGHT*.5),good_b.animate.shift(RIGHT*.5),
                  VGroup(*fragment_ends[4:]).animate.shift(RIGHT*.5),run_time=1.3)
        self.pause(1.8)
        self.play(FadeOut(VGroup(support,muts,tether,capture,marks,bad_a,bad_b)),
                  FadeOut(retained),FadeOut(fragment_ends),run_time=.9)
        self.step(4,"Matching overlaps prime reassembly in both directions")
        # Preserve the selected top strand of good_a (positions 0..5) and
        # bottom strand of good_b (positions 4..7) while zooming back to bases.
        a=VGroup(*tops[2].units[:6])
        b=VGroup(*row_bottom[0].units[4:])
        unused_a=VGroup(*row_bottom[2].units[:6],*pairs[2][:6])
        unused_b=VGroup(*tops[0].units[4:],*pairs[0][4:])
        self.play(FadeOut(unused_a),FadeOut(unused_b),run_time=.7)
        x,dx=-2.45,.70
        final_top=Strand("ATGCCGTA",x=x,y=.72,step=dx,side=-1,direction=1,role=NEW)
        final_bot=Strand("TACGGCAT",x=x,y=-.72,step=dx,side=1,direction=-1,role=NEW)
        # Match selected existing fragments to the full-size drawing without
        # altering sequence, then restore their original gray backbone role.
        target_a=VGroup(*final_top.units[:6]).copy()
        target_b=VGroup(*final_bot.units[4:]).copy()
        for g in (target_a,target_b):
            for unit in g: unit[0].set_color(OLD);unit[1].set_color(OLD)
        self.play(Transform(a,target_a),Transform(b,target_b),run_time=2)
        end_names=VGroup(caption("5′",[x-.4,.72,0],18,OLD),
            caption("3′",[x+5*dx+.4,.72,0],18,OLD),
            caption("3′",[x+4*dx-.4,-.72,0],18,OLD),
            caption("5′",[x+7*dx+.4,-.72,0],18,OLD))
        overlap=VGroup(*[bond(final_top.at(i),final_bot.at(i)) for i in [4,5]])
        self.play(Create(overlap),FadeIn(end_names),run_time=.8)
        self.pause(1.4)
        pol_a=enzyme("pol",.8).move_to([x+5*dx,1.85,0])
        pol_b=enzyme("pol",.8).move_to([x+4*dx,-1.9,0])
        self.play(FadeIn(pol_a),FadeIn(pol_b),FadeOut(end_names[1]),FadeOut(end_names[2]),run_time=.7)
        for i in range(6,8):
            self.play(Create(final_top.units[i]),pol_a.animate.set_x(x+i*dx),
                Create(bond(final_top.at(i),final_bot.at(i))),run_time=.7)
        for i in range(3,-1,-1):
            self.play(Create(final_bot.units[i]),pol_b.animate.set_x(x+i*dx),
                Create(bond(final_top.at(i),final_bot.at(i))),run_time=.65)
        self.play(FadeOut(pol_a),FadeOut(pol_b),FadeIn(final_top.ends[1]),FadeIn(final_bot.ends[0]),run_time=.7)
        self.pause(2)
        self.step(5,"Reassembled DNA can now be amplified by PCR")
        arrow=Arrow([-1.4,-2.12,0],[1.4,-2.12,0],buff=0,color=SIGNAL,stroke_width=1.5,tip_length=.13)
        repeat=caption("repeat filtering + reassembly",[0,-2.5,0],18,SIGNAL)
        self.play(Create(arrow),FadeIn(repeat),run_time=.8)
        self.pause(2)
        self.finish("Enrich the consensus; some errors can remain",hold=4)
