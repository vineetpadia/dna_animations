"""Molecular assembly lessons: explicit strands, bonds, junctions and provenance."""
import numpy as np
from manim import *
from dna_animations.core import (
    Lesson, Strand, label, caption, base_tile, enzyme, arrow, complement,
    BG, OLD, NEW, PRIMER, ENZYME, SIGNAL, STOP, MUTED, WHITE,
)


def pt(x,y): return np.array([x,y,0.])


def pair(a,b):
    v=b-a; v=v/np.linalg.norm(v)
    return DashedLine(a+v*.19,b-v*.19,color=MUTED,dash_length=.055,stroke_width=1.0)


def cut_mark(point):
    return VGroup(Line(LEFT*.12+UP*.17,RIGHT*.12+DOWN*.17,color=STOP,stroke_width=2),
                  Line(LEFT*.12+DOWN*.17,RIGHT*.12+UP*.17,color=STOP,stroke_width=2)).move_to(point)


def end_label(words,at,color=OLD):
    return caption(words,at,17,color)


class Duplex(VGroup):
    def __init__(self,seq,x=-3.5,y=0,dx=.7,role=OLD,ends=True):
        self.seq=seq; self.dx=dx
        self.top=Strand(seq,x=x,y=y+.52,step=dx,direction=1,role=role,side=-1,labels=ends)
        self.bottom=Strand(complement(seq),x=x,y=y-.52,step=dx,direction=-1,role=role,side=1,labels=ends)
        self.bonds=self.top.pairing(self.bottom)
        super().__init__(self.bonds,self.top,self.bottom)


class RingDNA(VGroup):
    """A duplex bent into a closed circle, retaining individual nucleotide tiles."""
    def __init__(self,seq,radius=1.48,center=ORIGIN):
        self.seq=seq; self.top=VGroup(); self.bottom=VGroup(); self.bonds=VGroup()
        n=len(seq); delta=TAU/n
        for i,(a,b) in enumerate(zip(seq,complement(seq))):
            theta=PI/2-i*delta
            radial=np.array([np.cos(theta),np.sin(theta),0.])
            # Arcs are real backbone segments. Outer runs clockwise;
            # inner is antiparallel. No terminal labels on a closed circle.
            outer=Arc(radius=radius+.32,start_angle=theta+delta,angle=-delta,
                      color=OLD,stroke_width=2.7).shift(center)
            inner=Arc(radius=radius-.32,start_angle=theta-delta,angle=delta,
                      color=OLD,stroke_width=2.7).shift(center)
            ob=base_tile(a,.60).move_to(center+radial*(radius+.16))
            ib=base_tile(b,.60).move_to(center+radial*(radius-.16))
            os=Line(center+radial*(radius+.32),center+radial*(radius+.27),color=OLD,stroke_width=1.4)
            ins=Line(center+radial*(radius-.32),center+radial*(radius-.27),color=OLD,stroke_width=1.4)
            self.top.add(VGroup(outer,os,ob));self.bottom.add(VGroup(inner,ins,ib))
            self.bonds.add(Line(center+radial*(radius+.025),center+radial*(radius-.025),
                                color=MUTED,stroke_width=1))
        super().__init__(self.bonds,self.top,self.bottom)


def _bend_duplex(scene,top,bottom,bonds,x,dx,center,closing=False,missing=()):
    """Open/close a circular arc without interpolating bases through each other."""
    n=len(top);radius=1.48;delta=TAU/n;span0=delta*(n-1)
    theta0=PI/2-(n-1)*delta/2
    midpoint0=center+radius*pt(np.cos(theta0),np.sin(theta0))
    midpoint1=pt(x+(n-1)*dx/2,0)
    originals=[[u[2].copy() for u in row] for row in (top,bottom)]
    source_scale=.6 if not closing else 1.
    def update(group,alpha):
        f=alpha if closing else 1-alpha
        span=f*span0;length=(1-f)*(n-1)*dx+f*radius*span0
        theta=(1-f)*PI/2+f*theta0
        midpoint=(1-f)*midpoint1+f*midpoint0
        half=(1-f)*.52+f*.32;tile_offset=(1-f)*.22+f*.16
        tile_scale=(1-f)+f*.60
        def raw_position(u,offset=0):
            s=u-(n-1)/2
            angle=theta-s*span/(n-1)
            normal=pt(np.cos(angle),np.sin(angle))
            if span<1e-6: p=midpoint+RIGHT*(s*dx)
            else:p=midpoint+length/span*(normal-pt(np.cos(theta),np.sin(theta)))
            return p+offset*normal
        bounds=np.array([raw_position(u,off) for u in np.linspace(0,n-1,50) for off in (-half,half)])
        lo=bounds.min(axis=0);hi=bounds.max(axis=0)
        extent=hi-lo;fit=min(1.,4.1/max(extent[1],.01),11.4/max(extent[0],.01))
        midpoint_box=(lo+hi)/2
        destination=(1-f)*midpoint1+f*center
        def position(u,offset=0):
            return (raw_position(u,offset)-midpoint_box)*fit+destination
        for j,row in enumerate((top,bottom)):
            sign=1 if j==0 else -1
            for i,u in enumerate(row):
                start=i-1 if j==0 else i+1
                if i==0 and j==0:start=i-.15/dx
                if i==n-1 and j==1:start=i+.15/dx
                curve=ParametricFunction(lambda t:position(t,sign*half),
                    t_range=[min(start,i),max(start,i),max(abs(start-i)/8,.005)],
                    color=OLD,stroke_width=(1-f)*2.3+f*2.7)
                if (j,i) in missing:curve.set_opacity(0)
                stem=Line(position(i,sign*half),position(i,sign*(half-.12+f*.07)),color=OLD,stroke_width=1.6)
                tile=originals[j][i].copy().scale(tile_scale/source_scale*fit).move_to(position(i,sign*tile_offset))
                u.become(VGroup(curve,stem,tile))
        for i,b in enumerate(bonds):
            b.become(Line(position(i,.025),position(i,-.025),color=MUTED,stroke_width=1))
    scene.play(UpdateFromAlphaFunc(VGroup(*top,*bottom,*bonds),update),run_time=2.0)


def _grow(scene,whole,indices,pace=.62,arrival_side=UP):
    """Add correctly matched nucleotides, then create their owned backbone."""
    for i in indices:
        tile=whole.bases[i].copy().shift(RIGHT*.55+arrival_side*.80)
        scene.play(FadeIn(tile),run_time=.18)
        scene.play(tile.animate.move_to(whole.at(i)),run_time=pace)
        scene.remove(tile)
        scene.play(FadeIn(whole.units[i]),run_time=.25)


def _pairs_for(top,bottom,indices):
    return VGroup(*[pair(top.at(i),bottom.at(i)) for i in indices])


def _outer_pcr(scene,seq,existing,x=-3.85,dx=.70,step_index=4):
    """One explicitly drawn PCR round on an already assembled duplex."""
    scene.step(step_index,"Outer primers amplify the assembled sequence.")
    carried_top=VGroup(*existing[0]); carried_bottom=VGroup(*existing[1])
    # Remove the old base-pair strokes, retaining the very same nucleotide
    # objects as the just-assembled duplex melts for its first PCR round.
    scene.remove(*list(scene.mobjects))
    scene.add(*scene.hud,carried_top,carried_bottom)
    scene.play(carried_top.animate.shift(UP*(1.10-carried_top[0][1].get_start()[1])),
               carried_bottom.animate.shift(UP*(-1.10-carried_bottom[0][1].get_start()[1])),run_time=.8)
    top=Strand(seq,x=x,y=1.10,step=dx,direction=1,side=-1,role=OLD)
    bottom=Strand(complement(seq),x=x,y=-1.10,step=dx,direction=-1,side=1,role=OLD)
    scene.add(top.ends,bottom.ends)
    upper=Strand(complement(seq),x=x,y=.20,step=dx,direction=-1,side=1,role=NEW,labels=False)
    lower=Strand(seq,x=x,y=-.20,step=dx,direction=1,side=-1,role=NEW,labels=False)
    n=len(seq)
    for row,ix in ((upper,[n-2,n-1]),(lower,[0,1])):
        for i in ix:
            row.units[i][0].set_color(PRIMER); row.units[i][1].set_color(PRIMER)
    # Trim the first visible primer's 5′ end to avoid a phantom long bond.
    upper.units[n-1][0].put_start_and_end_on(upper.anchor(n-1)+RIGHT*.15,upper.anchor(n-1))
    scene.play(FadeIn(VGroup(*upper.units[n-2:])),FadeIn(VGroup(*lower.units[:2])),run_time=.8)
    enzymes=VGroup(enzyme("pol",.8).move_to(pt(4.8,.7)),enzyme("pol",.8).move_to(pt(-4.8,-.7)))
    scene.play(FadeIn(enzymes),run_time=.4)
    for a,b in zip(range(n-3,-1,-1),range(2,n)):
        ua=upper.bases[a].copy().shift(LEFT*.38);lb=lower.bases[b].copy().shift(RIGHT*.38)
        scene.play(FadeIn(ua),FadeIn(lb),run_time=.12)
        scene.play(ua.animate.move_to(upper.at(a)),lb.animate.move_to(lower.at(b)),run_time=.24)
        scene.remove(ua,lb)
        scene.play(FadeIn(upper.units[a]),FadeIn(lower.units[b]),run_time=.14)
    scene.play(FadeOut(enzymes),run_time=.4)
    scene.play(Create(top.pairing(upper)),Create(bottom.pairing(lower)),run_time=.5)
    new_ends=VGroup(end_label("3′",upper.anchor(0)+LEFT*.43,NEW),end_label("5′",upper.anchor(n-1)+RIGHT*.43,PRIMER),
                   end_label("5′",lower.anchor(0)+LEFT*.43,PRIMER),end_label("3′",lower.anchor(n-1)+RIGHT*.43,NEW))
    scene.play(FadeIn(new_ends),run_time=.3)
    scene.wait(1.2)
    return VGroup(carried_top,upper),VGroup(carried_bottom,lower)


class RestrictionLigation(Lesson):
    title="Restriction digestion and ligation"
    steps=("Recognize","Cut","Separate","Anneal","Seal")

    def construct(self):
        seq="CGGAATTCTG"; x=-3.6; dx=.8
        dna=Duplex(seq,x=x,dx=dx)
        self.step(0,"EcoRI recognizes GAATTC.")
        self.play(FadeIn(dna),run_time=1.1)
        region=SurroundingRectangle(VGroup(*dna.top.bases[2:8],*dna.bottom.bases[2:8]),
                                     color=SIGNAL,buff=.16,corner_radius=.04)
        eco=enzyme("EcoRI",1.2).move_to(pt(0,1.85))
        self.play(Create(region),FadeIn(eco),run_time=.8); self.wait(2.0)
        self.step(1,"Cut both backbones at staggered positions.")
        m1=cut_mark((dna.top.anchor(2)+dna.top.anchor(3))/2)
        m2=cut_mark((dna.bottom.anchor(6)+dna.bottom.anchor(7))/2)
        self.play(FadeIn(m1),FadeIn(m2),run_time=.7);self.wait(1.3)
        self.play(FadeOut(dna.top.units[3][0]),FadeOut(dna.bottom.units[6][0]),
                  FadeOut(region),FadeOut(eco),run_time=.7)
        dna.top.units[3][0].set_opacity(0); dna.bottom.units[6][0].set_opacity(0)
        self.play(FadeOut(m1),FadeOut(m2),*[FadeOut(dna.bonds[i]) for i in range(3,7)],run_time=.6)
        self.remove(dna.top.ends,dna.bottom.ends)
        left=VGroup(*dna.top.units[:3],*dna.bottom.units[:7],*dna.bonds[:3])
        right=VGroup(*dna.top.units[3:],*dna.bottom.units[7:],*dna.bonds[7:])
        self.step(2,"The cuts expose complementary 5′ overhangs.")
        self.play(left.animate.shift(LEFT*1.45),right.animate.shift(RIGHT*1.45),run_time=1.5)
        ends=VGroup(end_label("5′",dna.top.anchor(0)+LEFT*.4),
                    end_label("3′–OH",dna.top.anchor(2)+UP*.62),
                    end_label("5′–P",dna.top.anchor(3)+UP*.62),
                    end_label("3′",dna.top.anchor(9)+RIGHT*.4),
                    end_label("3′",dna.bottom.anchor(0)+LEFT*.4),
                    end_label("5′–P",dna.bottom.anchor(6)+DOWN*.62),
                    end_label("3′–OH",dna.bottom.anchor(7)+DOWN*.62),
                    end_label("5′",dna.bottom.anchor(9)+RIGHT*.4))
        self.play(FadeIn(ends),run_time=.6);self.wait(3.2)
        self.step(3,"Matching overhangs anneal by base pairing.")
        self.play(FadeOut(ends),run_time=.4)
        self.play(left.animate.shift(RIGHT*1.45),right.animate.shift(LEFT*1.45),run_time=1.7)
        pairing=VGroup(*[pair(dna.top.at(i),dna.bottom.at(i)) for i in range(3,7)])
        self.play(Create(pairing),run_time=1.1);self.wait(2.2)
        self.step(4,"Ligase connects each 3′–OH to its 5′ phosphate.")
        lig=enzyme("DNA ligase",1.7).move_to(pt(0,-2.05))
        nicks=VGroup(cut_mark((dna.top.anchor(2)+dna.top.anchor(3))/2),
                     cut_mark((dna.bottom.anchor(6)+dna.bottom.anchor(7))/2))
        self.play(FadeIn(lig),FadeIn(nicks),run_time=.6);self.wait(1)
        seals=VGroup(Line(dna.top.anchor(2),dna.top.anchor(3),color=OLD,stroke_width=3),
                      Line(dna.bottom.anchor(6),dna.bottom.anchor(7),color=OLD,stroke_width=3))
        self.play(FadeOut(nicks),Create(seals),run_time=1.4);self.wait(1.5)
        self.play(FadeOut(lig),FadeIn(dna.top.ends),FadeIn(dna.bottom.ends),run_time=.6)
        self.finish("Base pairing aligns the ends; ligase seals them.",hold=4.0)
        self.wait(4)


class GibsonAssembly(Lesson):
    title="Gibson assembly"
    steps=("Overlap","Resect","Anneal","Fill","Seal")

    def construct(self):
        a=Duplex("ATGCCGTA",x=-5.0,dx=.63)
        b=Duplex("CGTATCGA",x=.65,dx=.63)
        self.step(0,"Design matching sequence at adjacent ends.")
        self.play(FadeIn(a),FadeIn(b),run_time=1.1)
        marks=VGroup(SurroundingRectangle(VGroup(*a.top.bases[4:],*a.bottom.bases[4:]),color=SIGNAL,buff=.13),
                     SurroundingRectangle(VGroup(*b.top.bases[:4],*b.bottom.bases[:4]),color=SIGNAL,buff=.13))
        self.play(Create(marks),run_time=.8);self.wait(2.4)
        self.step(1,"A 5′ exonuclease exposes 3′ single-stranded ends.")
        exo=enzyme("5′ exonuclease",2.0).move_to(pt(0,-2.05))
        self.play(FadeIn(exo),FadeOut(marks),FadeOut(a.bottom.ends),FadeOut(b.top.ends),run_time=.6)
        for ia,ib in zip(range(7,2,-1),range(5)):
            self.play(FadeOut(a.bottom.units[ia],shift=DOWN*.45),
                      FadeOut(b.top.units[ib],shift=UP*.45),
                      FadeOut(a.bonds[ia]),FadeOut(b.bonds[ib]),run_time=.6)
        a.bottom.units[2][0].put_start_and_end_on(a.bottom.anchor(2)+RIGHT*.15,a.bottom.anchor(2))
        b.top.units[5][0].put_start_and_end_on(b.top.anchor(5)-RIGHT*.15,b.top.anchor(5))
        tails=VGroup(end_label("3′",a.top.anchor(7)+UP*.53),end_label("3′",b.bottom.anchor(0)+DOWN*.53))
        self.play(FadeIn(tails),run_time=.4);self.wait(2.0)
        self.step(2,"The complementary 3′ overlaps anneal.")
        self.play(FadeOut(exo),FadeOut(tails),FadeOut(a.top.ends),FadeOut(b.bottom.ends),run_time=.4)
        left=VGroup(*a.top.units,*a.bottom.units[:3],*a.bonds[:3])
        right=VGroup(*b.top.units[5:],*b.bottom.units,*b.bonds[5:])
        ax=-3.465;dx=.63
        self.play(left.animate.shift(RIGHT*(ax+5.0)),right.animate.shift(LEFT*(.65-(ax+4*dx))),run_time=1.4)
        top=Strand("ATGCCGTATCGA",x=ax,y=.52,step=dx,side=-1,role=NEW,labels=False)
        bottom=Strand(complement(top.sequence),x=ax,y=-.52,step=dx,direction=-1,side=1,role=NEW,labels=False)
        annealed=VGroup(*[pair(a.top.at(i),b.bottom.at(i-4)) for i in range(4,8)])
        ends=VGroup(end_label("5′",a.top.anchor(0)+LEFT*.42),end_label("3′",b.top.anchor(7)+RIGHT*.42),
                    end_label("3′",a.bottom.anchor(0)+LEFT*.42),end_label("5′",b.bottom.anchor(7)+RIGHT*.42))
        self.play(Create(annealed),FadeIn(ends),run_time=.9);self.wait(2.3)
        self.step(3,"Polymerase extends each 3′ end across its gap.")
        pol=enzyme("DNA polymerase",2.0).move_to(pt(0,-2.05))
        self.play(FadeIn(pol),run_time=.5)
        _grow(self,top,[8],pace=1.1,arrival_side=UP)
        _grow(self,bottom,[3],pace=1.1,arrival_side=DOWN)
        self.play(Create(pair(top.at(8),b.bottom.at(4))),Create(pair(a.top.at(3),bottom.at(3))),run_time=.5)
        self.wait(2)
        self.step(4,"Ligase seals the two remaining nicks.")
        self.play(FadeOut(pol),run_time=.3)
        lig=enzyme("DNA ligase",1.7).move_to(pt(0,-2.05))
        nicks=VGroup(cut_mark((top.anchor(8)+b.top.anchor(5))/2),cut_mark((bottom.anchor(3)+a.bottom.anchor(2))/2))
        self.play(FadeIn(lig),FadeIn(nicks),run_time=.6);self.wait(1.6)
        seals=VGroup(Line(top.anchor(8),b.top.anchor(5),color=NEW,stroke_width=3),
                     Line(bottom.anchor(3),a.bottom.anchor(2),color=NEW,stroke_width=3))
        self.play(FadeOut(nicks),Create(seals),run_time=1.1)
        self.play(FadeOut(lig),run_time=.5)
        self.finish("One continuous duplex, joined through its overlap.",hold=4.0)
        self.wait(3)


class GoldenGateAssembly(Lesson):
    title="Golden Gate assembly"
    steps=("Recognize","Cut outside","Match","Ligate","Accumulate")

    def construct(self):
        seq="GGTCTCAAGGTCGAT";dx=.60;x=-4.2
        dna=Duplex(seq,x=x,dx=dx)
        self.step(0,"BsaI recognizes GGTCTC.")
        self.play(FadeIn(dna),run_time=1)
        site=SurroundingRectangle(VGroup(*dna.top.bases[:6],*dna.bottom.bases[:6]),color=SIGNAL,buff=.13)
        enz=enzyme("BsaI",1.1).move_to(pt(-2.7,1.9))
        self.play(Create(site),FadeIn(enz),run_time=.7);self.wait(2)
        self.step(1,"The enzyme cuts outside its recognition site.")
        cuts=VGroup(cut_mark((dna.top.anchor(6)+dna.top.anchor(7))/2),
                    cut_mark((dna.bottom.anchor(10)+dna.bottom.anchor(11))/2))
        self.play(FadeIn(cuts),run_time=.6);self.wait(1.5)
        self.play(FadeOut(dna.top.units[7][0]),FadeOut(dna.bottom.units[10][0]),
                  *[FadeOut(dna.bonds[i]) for i in range(7,11)],run_time=.7)
        dna.top.units[7][0].set_opacity(0); dna.bottom.units[10][0].set_opacity(0)
        self.play(FadeOut(cuts),FadeOut(enz),FadeOut(dna.top.ends),FadeOut(dna.bottom.ends),run_time=.4)
        discarded=VGroup(*dna.top.units[:7],*dna.bottom.units[:11],*dna.bonds[:7],site)
        self.play(FadeOut(discarded,shift=LEFT*1.0),run_time=1.3)
        kept=VGroup(*dna.top.units[7:],*dna.bottom.units[11:],*dna.bonds[11:])
        self.wait(1.0)
        self.step(2,"Designed overhangs select the neighboring fragment.")
        full="TACCAGGTCGAT";xx=-3.85; dd=.7
        target=Duplex(full,x=xx,dx=dd,ends=False)
        # Carry every retained nucleotide into the enlarged junction view.
        target.top.units[4][0].set_opacity(0)
        self.play(*[Transform(dna.top.units[7+i],target.top.units[4+i]) for i in range(8)],
                  *[Transform(dna.bottom.units[11+i],target.bottom.units[8+i]) for i in range(4)],
                  *[Transform(dna.bonds[11+i],target.bonds[8+i]) for i in range(4)],run_time=1.2)
        # Neither incoming terminal bond exists until ligation.
        dna.top.units[7][0].set_opacity(0)
        target.bottom.units[7][0].set_opacity(0)
        incoming=VGroup(*target.top.units[:4],*target.bottom.units[:8],*target.bonds[:4])
        incoming.shift(LEFT*1.45)
        self.play(FadeIn(incoming,shift=RIGHT*.2),run_time=.9)
        target.bottom.units[7][0].set_opacity(0)
        self.wait(1.5)
        self.play(incoming.animate.shift(RIGHT*1.45),run_time=1.3)
        anneal=VGroup(*[pair(target.top.at(i),target.bottom.at(i)) for i in range(4,8)])
        ends=VGroup(end_label("5′",target.top.anchor(0)+LEFT*.42),end_label("3′",target.top.anchor(11)+RIGHT*.42),
                    end_label("3′",target.bottom.anchor(0)+LEFT*.42),end_label("5′",target.bottom.anchor(11)+RIGHT*.42))
        self.play(Create(anneal),FadeIn(ends),run_time=.8);self.wait(2)
        self.step(3,"Ligase seals both backbones.")
        lig=enzyme("DNA ligase",1.7).move_to(pt(0,-2.0))
        self.play(FadeIn(lig),run_time=.6)
        seals=VGroup(Line(target.top.anchor(3),target.top.anchor(4),color=OLD,stroke_width=3),
                    Line(target.bottom.anchor(7),target.bottom.anchor(8),color=OLD,stroke_width=3))
        self.play(Create(seals),run_time=1.2);self.wait(1.8)
        self.play(FadeOut(lig),run_time=.5)
        self.wait(.5)
        self.step(4,"The assembled junction has lost the BsaI site.")
        enz.move_to(pt(-3.1,1.8))
        self.play(FadeIn(enz),run_time=.4)
        self.play(enz.animate.move_to(pt(3.1,1.8)),run_time=2.6)
        self.play(FadeOut(enz),run_time=.6)
        self.finish("Correct products accumulate during cut-and-join cycles.",hold=4)
        self.wait(4)


class OverlapExtensionPCR(Lesson):
    title="Overlap-extension PCR"
    steps=("Overlap","Melt","Anneal","Extend","Amplify")

    def construct(self):
        dx=.63
        a=Duplex("ATGCCGTA",x=-4.0,y=1.05,dx=dx,role=NEW)
        b=Duplex("CGTATCGA",x=-.4,y=-1.05,dx=dx,role=NEW)
        # End-primer segments remain copper after their PCR amplification.
        for dna in (a,b):
            for row,indices in ((dna.top,[0,1]),(dna.bottom,[6,7])):
                for i in indices: row.units[i][0].set_color(PRIMER);row.units[i][1].set_color(PRIMER)
        self.step(0,"PCR primers give the products a shared overlap.")
        self.play(FadeIn(a),FadeIn(b),run_time=1.1)
        overlap=VGroup(SurroundingRectangle(VGroup(*a.top.bases[4:],*a.bottom.bases[4:]),color=SIGNAL,buff=.12),
                       SurroundingRectangle(VGroup(*b.top.bases[:4],*b.bottom.bases[:4]),color=SIGNAL,buff=.12))
        self.play(Create(overlap),run_time=.8);self.wait(2.0)
        self.step(1,"Heat separates the strands.")
        self.play(FadeOut(overlap),FadeOut(a.bonds),FadeOut(b.bonds),run_time=.6)
        self.play(a.top.animate.shift(UP*.32),a.bottom.animate.shift(DOWN*.32),
                  b.top.animate.shift(UP*.32),b.bottom.animate.shift(DOWN*.32),run_time=1.0)
        self.wait(1.3)
        self.step(2,"Complementary 3′ ends meet across the overlap.")
        self.play(FadeOut(a.bottom,shift=LEFT*.4),FadeOut(b.top,shift=RIGHT*.4),
                  FadeOut(a.top.ends),FadeOut(b.bottom.ends),run_time=.6)
        a.top.remove(a.top.ends)
        b.bottom.remove(b.bottom.ends)
        xx=-3.465
        self.play(a.top.animate.shift(pt(xx-a.top.anchor(0)[0],.52-a.top.anchor(0)[1])),
                  b.bottom.animate.shift(pt(xx+4*dx-b.bottom.anchor(0)[0],-.52-b.bottom.anchor(0)[1])),run_time=1.4)
        pairs=VGroup(*[pair(a.top.at(i),b.bottom.at(i-4)) for i in range(4,8)])
        self.play(Create(pairs),run_time=.8)
        ends=VGroup(end_label("5′",a.top.anchor(0)+LEFT*.42),end_label("3′",a.top.anchor(7)+UP*.52),
                    end_label("3′",b.bottom.anchor(0)+DOWN*.52),end_label("5′",b.bottom.anchor(7)+RIGHT*.42))
        self.play(FadeIn(ends),run_time=.5);self.wait(2)
        self.step(3,"Each fragment primes extension of the other.")
        self.play(FadeOut(ends[1]),FadeOut(ends[2]),run_time=.3)
        pol=enzyme("DNA polymerase",2.0).move_to(pt(0,-2.15))
        self.play(FadeIn(pol),run_time=.5)
        seq="ATGCCGTATCGA"
        top=Strand(seq,x=xx,y=.52,step=dx,side=-1,role=NEW,labels=False)
        bottom=Strand(complement(seq),x=xx,y=-.52,step=dx,direction=-1,side=1,role=NEW,labels=False)
        for ti,bi in zip(range(8,12),range(3,-1,-1)):
            u=top.bases[ti].copy().shift(RIGHT*.40);v=bottom.bases[bi].copy().shift(LEFT*.40)
            self.play(FadeIn(u),FadeIn(v),run_time=.18)
            self.play(u.animate.move_to(top.at(ti)),v.animate.move_to(bottom.at(bi)),run_time=.5)
            self.remove(u,v)
            self.play(FadeIn(top.units[ti]),FadeIn(bottom.units[bi]),run_time=.22)
        self.play(FadeOut(pol),run_time=.4)
        self.wait(2.0)
        _outer_pcr(self,seq,(list(a.top.units)+list(top.units[8:]),list(bottom.units[:4])+list(b.bottom.units)),x=xx,dx=dx)
        self.finish("The overlap becomes one continuous DNA sequence.",hold=3.5)
        self.wait(2.5)


class SiteDirectedMutagenesis(Lesson):
    title="Site-directed mutagenesis"
    steps=("Design","Anneal","Extend","Copy","Verify")

    def construct(self):
        x=-3.4;dx=.92; wild="ATGCCATG"; mutant="ACGCCATG"
        template=Strand(complement(wild),x=x,y=.65,step=dx,direction=-1,role=OLD,side=-1)
        self.step(0,"Put the intended substitution inside a primer.")
        self.play(FadeIn(template),run_time=1)
        primer=Strand(mutant[:4],x=x,y=-1.35,step=dx,role=PRIMER,side=1)
        self.play(FadeIn(primer),run_time=1.0)
        changed=SurroundingRectangle(primer.bases[1],color=SIGNAL,buff=.14)
        self.play(Create(changed),run_time=.7);self.wait(2)
        self.step(1,"Matched bases at the 3′ end anchor the primer.")
        self.play(primer.animate.shift(UP*.9),changed.animate.shift(UP*.9),run_time=1.3)
        bonds=VGroup(*[pair(template.at(i),primer.at(i)) for i in (0,2,3)])
        self.play(Create(bonds),run_time=.8);self.wait(1.8)
        self.step(2,"Polymerase extends the primer carrying the change.")
        self.play(FadeOut(changed),FadeOut(primer.ends[1]),run_time=.4)
        pol=enzyme("DNA polymerase",2).move_to(pt(.25,-2.0))
        self.play(FadeIn(pol),run_time=.5)
        new=Strand(mutant,x=x,y=-.45,step=dx,role=NEW,side=1,labels=False)
        _grow(self,new,range(4,8),pace=.72,arrival_side=DOWN)
        for i in range(4,8):self.add(pair(template.at(i),new.at(i)))
        self.play(FadeOut(pol),run_time=.4);self.wait(1.8)
        self.step(3,"The new strand becomes a template next cycle.")
        carried=VGroup(*primer.units,*new.units[4:],primer.ends[0])
        self.play(FadeOut(template,shift=UP*.5),FadeOut(bonds),
                  *[FadeOut(m) for m in self.mobjects if isinstance(m,DashedLine)],run_time=.8)
        self.play(carried.animate.shift(DOWN*.30),run_time=.6)
        reverse=Strand(complement(mutant),x=x,y=.35,step=dx,direction=-1,role=NEW,side=-1,labels=False)
        for i in (6,7):reverse.units[i][0].set_color(PRIMER);reverse.units[i][1].set_color(PRIMER)
        self.play(FadeIn(VGroup(*reverse.units[6:]),shift=DOWN*.4),run_time=.8)
        self.play(FadeIn(pol.move_to(pt(-.4,1.8))),run_time=.5)
        _grow(self,reverse,range(5,-1,-1),pace=.55,arrival_side=UP)
        self.play(FadeOut(pol),run_time=.4)
        bottom_positions=[primer.at(i) for i in range(4)]+[new.at(i) for i in range(4,8)]
        finalpairs=VGroup(*[pair(reverse.at(i),bottom_positions[i]) for i in range(8)])
        self.play(Create(finalpairs),run_time=.8)
        check=SurroundingRectangle(VGroup(reverse.bases[1],primer.bases[1]),color=SIGNAL,buff=.13)
        self.play(Create(check),run_time=.8)
        self.step(4,"The substitution is now copied into both strands.")
        ends=VGroup(end_label("3′",reverse.anchor(0)+LEFT*.42),end_label("5′",reverse.anchor(7)+RIGHT*.42),
                    end_label("3′",new.anchor(7)+RIGHT*.42))
        self.play(FadeIn(ends),run_time=.5);self.wait(2.2)
        self.finish("Sequence the product to verify the intended change.",hold=3.5)


class PlasmidCloning(Lesson):
    title="Plasmid cloning"
    steps=("Open","Insert","Ligate","Transform","Select","Verify")

    def construct(self):
        vectorseq="GCTACGTATC";insertseq="AGGT";allseq=vectorseq+insertseq
        ring=RingDNA(vectorseq,center=DOWN*.15)
        self.step(0,"Open the vector at a chosen cloning site.")
        self.play(FadeIn(ring),run_time=1.1)
        cut=VGroup(cut_mark(ring.top[0][0].point_from_proportion(.5)),cut_mark(ring.bottom[-1][0].point_from_proportion(.5)))
        self.play(FadeIn(cut),run_time=.6);self.wait(1.5)
        self.play(FadeOut(ring.top[0][0]),FadeOut(ring.bottom[-1][0]),FadeOut(cut),run_time=.6)
        linear=Duplex(vectorseq,x=-4.7,dx=.57,ends=False)
        _bend_duplex(self,list(ring.top),list(ring.bottom),list(ring.bonds),
                     x=-4.7,dx=.57,center=DOWN*.15)
        name=caption("vector",pt(-2.15,1.5),18,MUTED)
        vector_ends=VGroup(linear.top.ends,linear.bottom.ends)
        # The construction above suppresses default labels while bending.
        vector_ends=VGroup(end_label("5′",linear.top.anchor(0)+LEFT*.43),end_label("3′",linear.top.anchor(9)+RIGHT*.43),
                           end_label("3′",linear.bottom.anchor(0)+LEFT*.43),end_label("5′",linear.bottom.anchor(9)+RIGHT*.43))
        self.play(FadeIn(name),FadeIn(vector_ends),run_time=.4);self.wait(1)
        self.step(1,"Bring an insert with compatible ends.")
        insert=Duplex(insertseq,x=2.0,dx=.57,role=OLD,ends=False)
        insertname=caption("insert",pt(2.85,1.5),18,MUTED)
        insert_ends=VGroup(end_label("5′",insert.top.anchor(0)+LEFT*.43),end_label("3′",insert.top.anchor(3)+RIGHT*.43),
                           end_label("3′",insert.bottom.anchor(0)+LEFT*.43),end_label("5′",insert.bottom.anchor(3)+RIGHT*.43))
        self.play(FadeIn(insert),FadeIn(insertname),FadeIn(insert_ends),run_time=.9);self.wait(1.3)
        self.play(FadeOut(vector_ends),FadeOut(insert_ends),run_time=.4)
        self.play(insert.animate.shift(LEFT*1.0),run_time=1.2)
        target=RingDNA(allseq,center=DOWN*.15)
        # Four nicks: both strands at both vector–insert junctions.
        missing=[target.top[0][0],target.top[10][0],target.bottom[9][0],target.bottom[13][0]]
        for bond in missing:bond.set_opacity(0)
        self.play(FadeOut(name),FadeOut(insertname),run_time=.4)
        _bend_duplex(self,list(ring.top)+list(insert.top.units),list(ring.bottom)+list(insert.bottom.units),
                     list(ring.bonds)+list(insert.bonds),x=-4.7,dx=.57,center=DOWN*.15,closing=True,
                     missing=((0,0),(0,10),(1,9),(1,13)))
        self.step(2,"Ligase closes both vector–insert junctions.")
        lig=enzyme("ligase",1.25).move_to(DOWN*.15)
        self.play(FadeIn(lig),run_time=.5)
        seals=VGroup(*[bond.copy().set_opacity(1) for bond in missing])
        self.play(Create(seals),run_time=1.2);self.wait(1.7)
        self.play(FadeOut(lig),run_time=.4)
        assembled=VGroup(ring,insert,seals)
        self.step(3,"A competent bacterium takes up the plasmid.")
        self.play(assembled.animate.scale(.37).move_to(pt(-3.9,.15)),run_time=1.0)
        cell=RoundedRectangle(width=3.6,height=2.3,corner_radius=1.05,color=MUTED,
                               fill_color=MUTED,fill_opacity=.035).move_to(pt(1.7,.15))
        cellname=caption("bacterium",pt(1.7,-1.48),18,MUTED)
        self.play(Create(cell),FadeIn(cellname),run_time=.7)
        self.play(assembled.animate.move_to(pt(1.7,.15)),run_time=1.6);self.wait(1.4)
        self.step(4,"Selection enriches cells carrying the plasmid.")
        empty=cell.copy().move_to(pt(-3.0,.15))
        self.play(FadeIn(empty),run_time=.6)
        drug=caption("antibiotic selection",pt(0,1.95),18,MUTED)
        self.play(FadeIn(drug),run_time=.5);self.wait(1.2)
        self.play(FadeOut(empty),run_time=1.1);self.wait(1.2)
        self.play(FadeOut(drug),FadeOut(cellname),run_time=.4)
        # Clonal growth, shown as two descendants carrying copied plasmids.
        daughter=cell.copy().scale(.72).move_to(pt(-2.0,.2))
        self.play(cell.animate.scale(.72).move_to(pt(2.0,.2)),
                  assembled.animate.scale(.72).move_to(pt(2.0,.2)),FadeIn(daughter),run_time=1.0)
        clone=assembled.copy().move_to(pt(-2.0,.2))
        self.play(TransformFromCopy(assembled,clone),run_time=1.0);self.wait(1.2)
        self.step(5,"Check the insert and both joining sequences.")
        self.play(FadeOut(cell),FadeOut(daughter),FadeOut(clone),run_time=.5)
        self.play(assembled.animate.scale(3.75).move_to(DOWN*.1),run_time=1.0)
        checks=VGroup(*[SurroundingRectangle(insert.top.units[i][2],color=SIGNAL,buff=.08) for i in range(4)])
        self.play(Create(checks),run_time=.8)
        self.finish("A resistant colony still needs sequence verification.",hold=4.0)


class MutSErrorCorrection(Lesson):
    title="MutS error filtering"
    steps=("Mix","Reanneal","Recognize","Capture","Enrich")

    def construct(self):
        correct="ATGCATCG";variant="ATGTATCG";x=-4.55;dx=.53
        rows=[Duplex(correct,x=x,y=1.32,dx=dx),Duplex(variant,x=x,y=-.05,dx=dx),
              Duplex(correct,x=x,y=-1.42,dx=dx)]
        self.step(0,"A synthesized DNA pool can contain sequence errors.")
        self.play(*[FadeIn(d) for d in rows],run_time=1.2)
        marker=SurroundingRectangle(VGroup(rows[1].top.bases[3],rows[1].bottom.bases[3]),color=SIGNAL,buff=.12)
        self.play(Create(marker),run_time=.7);self.wait(2.2)
        self.step(1,"Separate strands, then allow new partners to pair.")
        moving_ends=VGroup(*[row.ends for d in rows[:2] for row in (d.top,d.bottom)])
        self.play(FadeOut(marker),FadeOut(rows[0].bonds),FadeOut(rows[1].bonds),FadeOut(moving_ends),run_time=.6)
        for d in rows[:2]:
            for row in (d.top,d.bottom):row.remove(row.ends)
        # Route the exchanged strands through the open right-hand lane.
        # A direct diagonal swap sends their tiles through the fixed top strand.
        self.play(rows[0].bottom.animate.shift(RIGHT*5.3),run_time=.9)
        self.play(rows[0].bottom.animate.shift(UP*.8),run_time=.5)
        self.play(rows[1].bottom.animate.shift(RIGHT*5.3),run_time=.9)
        self.play(rows[1].bottom.animate.shift(UP*1.37),run_time=.6)
        self.play(rows[1].bottom.animate.shift(LEFT*5.3),run_time=.9)
        self.play(rows[0].bottom.animate.shift(DOWN*2.17),run_time=.8)
        self.play(rows[0].bottom.animate.shift(LEFT*5.3),run_time=.9)
        rows[0].bottom.ends.shift(DOWN*1.37)
        rows[1].bottom.ends.shift(UP*1.37)
        self.play(FadeIn(moving_ends),run_time=.4)
        for d in rows[:2]:
            for row in (d.top,d.bottom):row.add(row.ends)
        mismatchgroups=[]
        for i,j in ((0,1),(1,0)):
            bonds=VGroup(*[pair(rows[i].top.at(k),rows[j].bottom.at(k)) for k in range(8) if k!=3])
            self.play(Create(bonds),run_time=.5)
            mismatchgroups.append(VGroup(rows[i].top,rows[j].bottom,bonds))
        self.wait(2)
        self.step(2,"MutS recognizes the exposed mismatched pairs.")
        clamps=VGroup()
        names=VGroup()
        for y in (1.32,-.05):
            clamps.add(RoundedRectangle(width=.76,height=1.20,corner_radius=.18,
                color=ENZYME,stroke_width=2,fill_opacity=0).move_to(pt(x+3*dx,y)))
            names.add(caption("MutS",pt(.55,y),17,ENZYME))
        self.play(Create(clamps),FadeIn(names),run_time=1.0);self.wait(2.5)
        self.step(3,"Immobilized MutS retains mismatch-bearing DNA.")
        self.play(FadeOut(names),run_time=.4)
        support=Line(pt(5.45,-.9),pt(5.45,2.10),color=MUTED,stroke_width=6)
        self.play(Create(support),run_time=.6)
        self.play(*[g.animate.shift(RIGHT*4.1) for g in mismatchgroups],clamps.animate.shift(RIGHT*4.1),run_time=1.5)
        links=VGroup(*[Line(clamps[k].get_right(),pt(5.45,yy),color=ENZYME,stroke_width=1.4) for k,yy in enumerate((1.32,-.05))])
        self.play(Create(links),run_time=.7);self.wait(2.4)
        self.step(4,"Collect the unbound DNA, enriched for matched pairs.")
        self.play(rows[2].animate.shift(RIGHT*2.7),run_time=1.4)
        self.play(*[g.animate.set_opacity(.24) for g in mismatchgroups],clamps.animate.set_opacity(.24),
                  links.animate.set_opacity(.24),support.animate.set_opacity(.24),run_time=.8)
        self.wait(2.2)
        self.finish("MutS selects molecules; it does not rewrite bases.",hold=4.0)
        self.wait(4)


class DNAShuffling(Lesson):
    title="DNA shuffling"
    steps=("Parents","Fragment","Reanneal","Extend","Amplify")

    def construct(self):
        dx=.61;x=-3.35
        one="ATGCCGTATCGA";two="ATGTCGTATAGA";chimera="ATGCCGTATAGA"
        a=Duplex(one,x=x,y=1.05,dx=dx);b=Duplex(two,x=x,y=-1.05,dx=dx)
        self.step(0,"Start with related genes carrying different variants.")
        self.play(FadeIn(a),FadeIn(b),run_time=1.1)
        labels=VGroup(caption("parent 1",pt(-5.0,1.05),17,MUTED),caption("parent 2",pt(-5.0,-1.05),17,MUTED))
        self.play(FadeIn(labels),run_time=.6)
        variants=VGroup(SurroundingRectangle(VGroup(a.top.bases[3],a.bottom.bases[3]),color=SIGNAL,buff=.1),
                        SurroundingRectangle(VGroup(b.top.bases[9],b.bottom.bases[9]),color=SIGNAL,buff=.1))
        self.play(Create(variants),run_time=.7);self.wait(2)
        self.step(1,"Fragment the parental DNA at varied positions.")
        dnase=enzyme("DNase I",1.5).move_to(pt(5.0,1.40))
        self.play(FadeIn(dnase),FadeOut(variants),run_time=.5)
        cuts=VGroup(cut_mark((a.top.anchor(7)+a.top.anchor(8))/2),cut_mark((a.bottom.anchor(7)+a.bottom.anchor(8))/2),
                    cut_mark((b.top.anchor(3)+b.top.anchor(4))/2),cut_mark((b.bottom.anchor(3)+b.bottom.anchor(4))/2))
        self.play(FadeIn(cuts),run_time=.6);self.wait(.8)
        self.play(FadeOut(a.top.units[8][0]),FadeOut(a.bottom.units[7][0]),
                  FadeOut(b.top.units[4][0]),FadeOut(b.bottom.units[3][0]),FadeOut(cuts),run_time=.6)
        a.top.units[8][0].set_opacity(0); a.bottom.units[7][0].set_opacity(0)
        b.top.units[4][0].set_opacity(0); b.bottom.units[3][0].set_opacity(0)
        offa=VGroup(*a.top.units[8:],*a.bottom.units[8:],*a.bonds[8:])
        offb=VGroup(*b.top.units[:4],*b.bottom.units[:4],*b.bonds[:4])
        self.play(FadeOut(offa,shift=RIGHT*.8),FadeOut(offb,shift=LEFT*.8),
                  FadeOut(dnase),FadeOut(labels),FadeOut(a.top.ends),FadeOut(a.bottom.ends),
                  FadeOut(b.top.ends),FadeOut(b.bottom.ends),run_time=1.0)
        self.wait(1.2)
        self.step(2,"Fragments reanneal wherever their sequences match.")
        self.play(*[FadeOut(a.bonds[i]) for i in range(8)],*[FadeOut(b.bonds[i]) for i in range(4,12)],run_time=.5)
        self.play(FadeOut(VGroup(*a.bottom.units[:8]),shift=DOWN*.35),
                  FadeOut(VGroup(*b.top.units[4:]),shift=UP*.35),run_time=.7)
        chosen_a=VGroup(*a.top.units[:8]);chosen_b=VGroup(*b.bottom.units[4:])
        self.play(chosen_a.animate.shift(DOWN*1.05),chosen_b.animate.shift(UP*1.05),run_time=1.1)
        ends=VGroup(end_label("5′",a.top.anchor(0)+LEFT*.42),end_label("3′",a.top.anchor(7)+UP*.52),
                    end_label("3′",b.bottom.anchor(4)+DOWN*.52),end_label("5′",b.bottom.anchor(11)+RIGHT*.42))
        self.play(Create(VGroup(*[pair(a.top.at(i),b.bottom.at(i)) for i in range(4,8)])),FadeIn(ends),run_time=.8)
        self.wait(2.0)
        self.step(3,"Extension combines variants from both parents.")
        self.play(FadeOut(ends[1]),FadeOut(ends[2]),run_time=.3)
        pol=enzyme("DNA polymerase",2).move_to(pt(0,-2.05))
        self.play(FadeIn(pol),run_time=.5)
        top=Strand(chimera,x=x,y=.52,step=dx,side=-1,role=NEW,labels=False)
        bottom=Strand(complement(chimera),x=x,y=-.52,step=dx,direction=-1,side=1,role=NEW,labels=False)
        for ti,bi in zip(range(8,12),range(3,-1,-1)):
            u=top.bases[ti].copy().shift(RIGHT*.4);v=bottom.bases[bi].copy().shift(LEFT*.4)
            self.play(FadeIn(u),FadeIn(v),run_time=.18)
            self.play(u.animate.move_to(top.at(ti)),v.animate.move_to(bottom.at(bi)),run_time=.5)
            self.remove(u,v)
            self.play(FadeIn(top.units[ti]),FadeIn(bottom.units[bi]),run_time=.22)
        self.play(FadeOut(pol),run_time=.4)
        sources=VGroup(SurroundingRectangle(VGroup(a.top.bases[3],bottom.bases[3]),color=SIGNAL,buff=.12),
                       SurroundingRectangle(VGroup(top.bases[9],b.bottom.bases[9]),color=SIGNAL,buff=.12))
        self.play(Create(sources),run_time=.7);self.wait(2.2)
        _outer_pcr(self,chimera,(list(a.top.units[:8])+list(top.units[8:]),list(bottom.units[:4])+list(b.bottom.units[4:])),x=x,dx=dx)
        self.finish("Reassembly combines variants from different parents.",hold=3.5)
