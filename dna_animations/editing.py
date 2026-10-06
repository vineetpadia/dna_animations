"""Targeted editing and a complete example of cellular DNA repair.

Sequences and recognition domains are shortened teaching models. See notes.
"""
from manim import *
import numpy as np
from dna_animations.core import (Lesson, Strand, complement, base_tile, caption,
    label, enzyme, tag, BG, OLD, NEW, PRIMER, ENZYME, SIGNAL, STOP, MUTED)


def p(x,y):
    return np.array([x,y,0.])


def bond(a,b,color=MUTED):
    d=b-a
    d=d/np.linalg.norm(d)
    return DashedLine(a+d*.19,b-d*.19,color=color,dash_length=.06,stroke_width=1.1)


def dna(seq,x=-3.8,step=.70,ty=.72,by=-.72):
    a=Strand(seq,x=x,y=ty,step=step,side=-1,direction=1,role=OLD)
    b=Strand(complement(seq),x=x,y=by,step=step,side=1,direction=-1,role=OLD)
    return a,b,a.pairing(b)


def gap_mark(at):
    return VGroup(Line(at+UP*.16+LEFT*.07,at+DOWN*.16+LEFT*.07,color=STOP,stroke_width=2),
                  Line(at+UP*.16+RIGHT*.07,at+DOWN*.16+RIGHT*.07,color=STOP,stroke_width=2))


class CRISPRCas9(Lesson):
    title="CRISPR–Cas9 editing"
    steps=("Recognize","Pair","Cut","Release","Repair")

    def construct(self):
        seq="ACGTACGAAGG"
        top,bottom,pairs=dna(seq)
        self.step(0,"Cas9 checks a PAM beside the target")
        self.play(Create(top),Create(bottom),Create(pairs),run_time=1.8)
        pam=SurroundingRectangle(VGroup(*top.bases[8:]),buff=.12,color=SIGNAL,stroke_width=1.5)
        pam_name=caption("PAM",[2.5,1.45,0],18,SIGNAL)
        cas=enzyme("Cas9",1.1).move_to([4.9,1.7,0])
        self.play(Create(pam),FadeIn(pam_name),FadeIn(cas),run_time=.9)
        self.pause(2.5)
        guide=Strand(seq[:8].replace("T","U"),x=-3.8,y=-1.95,step=.7,
                     side=-1,direction=1,role=PRIMER)
        guide_name=caption("guide RNA",[-.9,-2.58,0],18,PRIMER)
        self.play(FadeIn(guide),FadeIn(guide_name),run_time=1)
        self.pause(1.5)
        self.step(1,"The guide pairs with a complementary DNA strand")
        self.play(FadeOut(guide),FadeOut(guide_name),run_time=.45)
        prefix=VGroup(*top.units[:8])
        self.play(FadeOut(VGroup(*pairs[:8])),FadeOut(top.units[8][0]),
                  prefix.animate.shift(UP*.92),FadeOut(top.ends[0]),
                  run_time=1.5)
        guide.shift(UP*2.60)
        bridge=Line(top.anchor(7),top.anchor(8),color=OLD,stroke_width=2.3)
        gpair=VGroup(*[bond(guide.at(i),bottom.at(i)) for i in range(8)])
        self.play(Create(bridge),FadeIn(guide,shift=RIGHT*.55),run_time=.9)
        self.play(Create(gpair),run_time=.8)
        self.pause(3)
        self.step(2,"Cas9 cuts both backbones near the PAM")
        cutx=(-3.8+4*.7)+.35
        cut_t=gap_mark(p(cutx,1.64))
        cut_b=gap_mark(p(cutx,-.72))
        self.play(FadeIn(cut_t),FadeIn(cut_b),run_time=.6)
        self.play(FadeOut(top.units[5][0]),FadeOut(bottom.units[4][0]),run_time=1)
        self.pause(2.5)
        self.step(3,"The guide and Cas9 leave the broken DNA")
        self.play(FadeOut(guide),FadeOut(gpair),FadeOut(cas),FadeOut(pam),FadeOut(pam_name),
                  FadeOut(cut_t),FadeOut(cut_b),FadeOut(bridge),run_time=1)
        self.play(prefix.animate.shift(DOWN*.92),run_time=1)
        self.add(top.ends[0],top.units[8][0])
        for i in range(8): pairs[i]=bond(top.at(i),bottom.at(i))
        self.play(Create(VGroup(*pairs[:8])),run_time=.8)
        left=VGroup(*top.units[:5],*bottom.units[:5],*pairs[:5],top.ends[0],bottom.ends[0])
        right=VGroup(*top.units[5:],*bottom.units[5:],*pairs[5:],top.ends[1],bottom.ends[1])
        self.play(left.animate.shift(LEFT*.3),right.animate.shift(RIGHT*.3),run_time=1.6)
        self.pause(2)
        self.step(4,"End joining can remove bases at the break")
        # One illustrative one-base-pair deletion, not every NHEJ outcome.
        lost=VGroup(top.units[4],bottom.units[4],pairs[4])
        repair=enzyme("end repair",1.7).move_to([-.8,-2.03,0])
        self.play(FadeIn(repair),run_time=.6)
        self.play(lost.animate.shift(DOWN*.45).set_opacity(0),run_time=1.3)
        self.remove(lost)
        self.play(right.animate.shift(LEFT*1.3),run_time=1.6)
        top_link=Line(top.anchor(3),top.anchor(5),color=NEW,stroke_width=3.2)
        bot_link=Line(bottom.anchor(3),bottom.anchor(5),color=NEW,stroke_width=3.2)
        self.play(Create(top_link),Create(bot_link),FadeOut(repair),run_time=1.3)
        self.pause(3)
        self.finish("Repair determines the edit; outcomes can differ",hold=4)


class BaseEditing(Lesson):
    title="Base editing · C → T"
    steps=("Expose","Deaminate","Protect","Repair","Copy")

    def construct(self):
        seq="ACGTCCGAAGG"
        top,bottom,pairs=dna(seq)
        guide=Strand(seq[:8].replace("T","U"),x=-3.8,y=.56,step=.7,
            side=-1,direction=1,role=PRIMER)
        cas=enzyme("Cas9 nickase",1.95).move_to([4.85,-1.75,0])
        deaminase=enzyme("deaminase",1.8).move_to([4.85,1.82,0])
        self.step(0,"A guide exposes the DNA strand to be edited")
        self.play(Create(top),Create(bottom),Create(pairs),FadeIn(cas),FadeIn(deaminase),run_time=1.7)
        self.pause(1.8)
        exposed=VGroup(*top.units[:8])
        self.play(FadeOut(VGroup(*pairs[:8])),FadeOut(top.units[8][0]),
                  FadeOut(top.ends[0]),exposed.animate.shift(UP*.95),run_time=1.5)
        bridge=Line(top.anchor(7),top.anchor(8),color=OLD,stroke_width=2.3)
        guide_pairs=VGroup(*[bond(guide.at(i),bottom.at(i)) for i in range(8)])
        self.play(Create(bridge),FadeIn(guide),Create(guide_pairs),run_time=1)
        target=SurroundingRectangle(top.bases[4],buff=.12,color=SIGNAL,stroke_width=1.5)
        self.play(Create(target),run_time=.6)
        self.pause(2)
        self.step(1,"The deaminase converts the exposed C into U")
        self.play(deaminase.animate.move_to([-.65,2.2,0]),run_time=1.6)
        u=base_tile("U").move_to(top.at(4))
        self.play(Transform(top.bases[4],u),run_time=1.2)
        self.pause(2.5)
        self.step(2,"UGI helps prevent removal of the new U")
        ugi=enzyme("UGI",.9).move_to([1.2,2.2,0])
        self.play(FadeIn(ugi),run_time=.7)
        self.pause(2.5)
        self.play(FadeOut(deaminase),FadeOut(ugi),FadeOut(target),run_time=.8)
        self.step(3,"A nick biases repair of the opposite strand")
        cutx=(-3.8+4*.7)+.35
        nick=gap_mark(p(cutx,-.72))
        self.play(FadeIn(nick),FadeOut(bottom.units[4][0]),run_time=.75)
        self.pause(1.8)
        self.play(FadeOut(cas),FadeOut(guide),FadeOut(guide_pairs),FadeOut(nick),FadeOut(bridge),run_time=.8)
        self.play(exposed.animate.shift(DOWN*.95),run_time=1.2)
        self.add(top.ends[0],top.units[8][0])
        repair=enzyme("repair",1.1).move_to([-.8,-1.95,0])
        self.play(FadeIn(repair),run_time=.5)
        old=bottom.bases[4]
        incoming=base_tile("A").move_to([.65,-1.25,0])
        self.play(old.animate.shift(LEFT*.55+DOWN*.3).set_opacity(0),FadeIn(incoming),run_time=.8)
        targetpos=bottom.anchor(4)+UP*.30
        self.play(incoming.animate.move_to(targetpos),run_time=1)
        self.remove(old,incoming)
        bottom.units[4].remove(old)
        bottom.bases[4]=base_tile("A").move_to(targetpos)
        bottom.units[4].add(bottom.bases[4])
        self.add(bottom.bases[4])
        self.play(Create(bottom.units[4][0]),FadeOut(repair),run_time=.6)
        restored=VGroup(*[bond(top.at(i),bottom.at(i)) for i in range(8)])
        self.play(Create(restored),run_time=.7)
        self.pause(2)
        self.step(4,"Copying the A-containing strand fixes a T·A pair")
        self.play(FadeOut(restored),FadeOut(VGroup(*pairs[8:])),
                  top.animate.shift(UP*.8),run_time=1.2)
        self.play(FadeOut(top),run_time=.7)
        final_seq=seq[:4]+"T"+seq[5:]
        copied=Strand(final_seq,x=-3.8,y=.72,step=.7,side=-1,direction=1,role=NEW)
        for unit in copied.units[:2]:
            unit[0].set_color(PRIMER);unit[1].set_color(PRIMER)
        copied.ends[0].set_color(PRIMER)
        primer_name=caption("primer",[-3.45,1.48,0],17,PRIMER)
        terminus=caption("3′",[-3.1+.43,.92,0],17,PRIMER)
        self.play(FadeIn(copied.ends[0]),Create(VGroup(*copied.units[:2])),
                  FadeIn(primer_name),FadeIn(terminus),
                  *[Create(bond(copied.at(i),bottom.at(i))) for i in range(2)],run_time=1)
        self.pause(1.4)
        self.play(FadeOut(primer_name),run_time=.3)
        # The lower A-containing strand templates primer extension.
        for i in range(2,len(seq)):
            self.play(Create(copied.units[i]),Create(bond(copied.at(i),bottom.at(i))),
                      terminus.animate.set_x(-3.8+i*.7+.43).set_color(NEW),run_time=.32)
        self.play(Transform(terminus,copied.ends[1]),run_time=.25)
        highlight=SurroundingRectangle(VGroup(copied.bases[4],bottom.bases[4]),buff=.13,color=SIGNAL,stroke_width=1.5)
        self.play(Create(highlight),run_time=.6)
        self.finish("A C·G pair becomes T·A at the chosen window",hold=4)


class PrimeEditing(Lesson):
    title="Prime editing"
    steps=("Target","Nick","Prime","Write","Replace","Seal","Resolve")

    def construct(self):
        seq,newseq="ATGCCATGAC","ATGCGATGAC"
        x,dx=-3.6,.72
        top,bottom,pairs=dna(seq,x=x,step=dx,ty=.8,by=-.6)
        complex_=enzyme("Cas9n–RT",1.8).move_to([4.75,1.6,0])
        guide_mark=VMobject(color=PRIMER,stroke_width=2).set_points_smoothly([
            p(3.95,1.7),p(3.65,2.1),p(3.28,1.8),p(3.5,1.35),p(3.25,1.05)])
        guide_name=caption("pegRNA",[4.7,.91,0],17,PRIMER)
        self.step(0,"A pegRNA guides a nickase fused to reverse transcriptase")
        self.play(Create(top),Create(bottom),Create(pairs),FadeIn(complex_),Create(guide_mark),FadeIn(guide_name),run_time=1.8)
        self.pause(2.8)
        nickx=x+3.5*dx
        nick=gap_mark(p(nickx,.8))
        self.step(1,"Nick one strand to expose a DNA 3′ end")
        self.play(FadeIn(nick),FadeOut(top.units[4][0]),run_time=.9)
        self.pause(1.7)
        self.play(FadeOut(pairs),bottom.animate.shift(DOWN*1.6),
                  VGroup(*top.units[4:],top.ends[1]).animate.shift(UP*.9),
                  FadeOut(nick),run_time=1.8)
        self.pause(1.2)
        self.step(2,"The DNA end pairs with the pegRNA primer-binding site")
        rna=Strand("ACGCUACU",x=x+dx,y=-.8,step=dx,direction=-1,side=1,role=PRIMER,labels=False)
        pbs=caption("primer-binding site",[-2.12,-1.4,0],16,PRIMER)
        rtname=caption("RNA template",[1.13,-1.4,0],16,PRIMER)
        rna3=caption("3′",[x+dx-.4,-.8,0],17,PRIMER)
        attach=VMobject(color=PRIMER,stroke_width=1.5).set_points_smoothly([
            rna.anchor(7),p(3.2,-.8),p(3.7,.35),p(3.85,1.3)])
        self.play(FadeIn(rna),FadeIn(pbs),FadeIn(rtname),FadeIn(rna3),Create(attach),run_time=1.2)
        initial_pairs=VGroup(*[bond(top.at(i),rna.at(i-1)) for i in range(1,4)])
        self.play(Create(initial_pairs),run_time=.8)
        oh=tag("3′–OH",NEW).scale(.8).move_to([x+3*dx,1.19,0])
        self.play(FadeIn(oh),run_time=.5)
        self.pause(2.2)
        self.step(3,"Reverse transcriptase copies the encoded edit into DNA")
        extension=Strand(newseq,x=x,y=.8,step=dx,side=-1,direction=1,role=NEW,labels=False)
        pol=enzyme("RT",.75).move_to([x+3*dx,2.2,0])
        self.play(FadeOut(oh),FadeIn(pol),run_time=.6)
        fresh_pairs=VGroup()
        for i in range(4,9):
            incoming=base_tile(newseq[i]).move_to([x+i*dx+.5,.02,0])
            self.play(FadeIn(incoming),run_time=.25)
            self.play(incoming.animate.move_to(extension.at(i)),pol.animate.set_x(x+i*dx),run_time=.65)
            self.remove(incoming)
            pair=bond(extension.at(i),rna.at(i-1))
            fresh_pairs.add(pair)
            self.play(Create(extension.units[i]),Create(pair),run_time=.45)
        self.pause(2)
        self.step(4,"The edited 3′ flap replaces the old 5′ flap")
        self.play(FadeOut(pol),FadeOut(initial_pairs),FadeOut(fresh_pairs),
                  FadeOut(rna),FadeOut(rna3),FadeOut(pbs),FadeOut(rtname),
                  FadeOut(attach),FadeOut(complex_),FadeOut(guide_mark),FadeOut(guide_name),run_time=1)
        old_flap=VGroup(*top.units[4:9])
        self.play(FadeOut(top.units[9][0]),run_time=.4)
        top.units[9][0].set_opacity(0)
        self.play(old_flap.animate.shift(UP*.45).set_opacity(0),run_time=1.5)
        self.remove(old_flap)
        self.play(VGroup(top.units[9],top.ends[1]).animate.shift(DOWN*.9),
                  bottom.animate.shift(UP*1.6),run_time=1.5)
        assembled=VGroup(*top.units[:4],*extension.units[4:9],top.units[9])
        matched=VGroup()
        for i in range(10):
            at=top.at(i) if i<4 or i==9 else extension.at(i)
            matched.add(bond(at,bottom.at(i),STOP if i==4 else MUTED))
        self.play(Create(matched),run_time=.8)
        self.pause(2.2)
        self.step(5,"Ligase seals the edited strand at the remaining nick")
        lig=enzyme("ligase",1.1).move_to([x+8.5*dx,1.8,0])
        final_nick=gap_mark(p(x+8.5*dx,.8))
        self.play(FadeIn(lig),FadeIn(final_nick),run_time=.6)
        self.pause(1.2)
        sealed=Line(extension.anchor(8),top.anchor(9),color=NEW,stroke_width=3.2)
        self.play(Create(sealed),FadeOut(final_nick),run_time=1.1)
        self.play(FadeOut(lig),run_time=.5)
        self.step(6,"Repair resolves the remaining mismatch")
        mismatch=SurroundingRectangle(VGroup(extension.bases[4],bottom.bases[4]),buff=.12,color=SIGNAL,stroke_width=1.4)
        self.play(Create(mismatch),run_time=.6)
        newbase=base_tile("C").move_to(bottom.at(4))
        self.play(Transform(bottom.bases[4],newbase),matched[4].animate.set_color(MUTED),run_time=1.2)
        self.pause(2)
        self.finish("The pegRNA specifies the sequence to be written",hold=4)


class DNARepair(Lesson):
    title="DNA repair · base excision"
    steps=("Damage","Recognize","Excise","Process","Fill","Seal")

    def construct(self):
        seq="ATGCCGTA"
        top,bottom,pairs=dna(seq,x=-3.5,step=1.0,ty=.72,by=-.72)
        i=3
        self.step(0,"Spontaneous deamination can turn C into U")
        self.play(Create(top),Create(bottom),Create(pairs),run_time=1.5)
        self.pause(1.6)
        self.play(Transform(top.bases[i],base_tile("U").move_to(top.at(i))),
                  pairs[i].animate.set_color(STOP),run_time=1.3)
        self.pause(2.2)
        gly=enzyme("glycosylase",1.8).move_to([-3.5,1.95,0])
        self.step(1,"A glycosylase recognizes the abnormal base")
        self.play(FadeIn(gly),run_time=.6)
        self.play(gly.animate.set_x(top.anchor(i)[0]),run_time=2.5)
        mark=SurroundingRectangle(top.bases[i],buff=.13,color=SIGNAL,stroke_width=1.3)
        self.play(Create(mark),run_time=.6)
        self.pause(2)
        self.step(2,"Remove the base; leave the backbone intact")
        self.play(FadeOut(mark),FadeOut(pairs[i]),top.bases[i].animate.shift(UP*.78+RIGHT*.85),run_time=1.4)
        self.play(FadeOut(top.bases[i]),FadeOut(gly),run_time=.8)
        ap=caption("abasic site",[-.5,1.6,0],19)
        ap_line=Line([-.5,1.32,0],[-.5,.88,0],color=MUTED,stroke_width=1)
        self.play(FadeIn(ap),Create(ap_line),run_time=.8)
        self.pause(2.4)
        self.step(3,"Cut beside the site and remove the sugar remnant")
        endo=enzyme("AP endonuclease",2.25).move_to([-2.7,2.05,0])
        cut=gap_mark(p(-1.0,.72))
        self.play(FadeIn(endo),FadeIn(cut),run_time=.7)
        self.play(FadeOut(top.units[i][0]),run_time=.7)
        self.pause(1.3)
        self.play(FadeOut(endo),FadeOut(cut),FadeOut(ap),FadeOut(ap_line),
                  FadeOut(top.units[i][1]),FadeOut(top.units[i+1][0]),run_time=.8)
        self.pause(1.5)
        self.step(4,"DNA polymerase fills the gap using the intact strand")
        pol=enzyme("polymerase β",1.9).move_to([-.5,1.9,0])
        incoming=base_tile("C").move_to([1.7,1.35,0])
        site=top.anchor(i)+DOWN*.3
        self.play(FadeIn(pol),FadeIn(incoming),run_time=.8)
        self.play(incoming.animate.move_to(site),run_time=1.5)
        newlink=Line(top.anchor(i-1),top.anchor(i),color=NEW,stroke_width=3.2)
        stem=Line(top.anchor(i),top.anchor(i)+DOWN*.12,color=NEW,stroke_width=2)
        pair=bond(site,bottom.at(i))
        self.play(Create(newlink),Create(stem),Create(pair),run_time=1)
        self.pause(2)
        self.play(FadeOut(pol),run_time=.5)
        self.step(5,"Ligase seals the final nick")
        lig=enzyme("ligase",1.1).move_to([.4,1.9,0])
        self.play(FadeIn(lig),run_time=.6)
        sealed=Line(top.anchor(i),top.anchor(i+1),color=NEW,stroke_width=3.2)
        self.play(Create(sealed),run_time=1.5)
        self.pause(1.8)
        self.play(FadeOut(lig),run_time=.6)
        self.finish("Restore the base pair and a continuous backbone",hold=4)
