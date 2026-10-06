"""Additional amplification mechanisms in the shared teaching language.

Every basewise extension reuses the incoming tile as the incorporated base.
Overview transitions change scale; they do not substitute for synthesis.
"""
import math
import numpy as np
from manim import *
from dna_animations.core import (
    Lesson, Strand, label, caption, base_tile, enzyme, arrow, complement,
    BG, OLD, NEW, PRIMER, SIGNAL, STOP, MUTED, HAIRLINE, ENZYME,
)


def P(x,y):
    return np.array([x,y,0.])


def pair(a,b):
    v=b-a; v=v/np.linalg.norm(v)
    return DashedLine(a+.18*v,b-.18*v,color=MUTED,stroke_width=1,dash_length=.045)


def termini(x0,x1,y,direction=1,color=NEW):
    a,b=("5′","3′") if direction==1 else ("3′","5′")
    return VGroup(caption(a,P(x0-.4,y),16,color),caption(b,P(x1+.4,y),16,color))


def grow(scene,strand,indices,pol=None,end=None,template=None,map_index=None,
         seconds=.55,enzyme_y=-1.5,incoming_y=-2.05,hide_end=False,incoming_dx=.55):
    """Move the actual future base from the reagent lane into the strand."""
    bonds=VGroup()
    for i in indices:
        unit=strand.units[i]; target=strand.at(i).copy()
        if hide_end and end is not None:
            scene.play(FadeOut(end),run_time=.08)
        unit[2].move_to(P(target[0]+incoming_dx*strand.direction,incoming_y))
        scene.play(FadeIn(unit[2]),run_time=.12)
        acts=[unit[2].animate.move_to(target),Create(unit[0]),Create(unit[1])]
        if pol is not None:
            acts.append(pol.animate.move_to(P(target[0],enzyme_y)))
        if end is not None and not hide_end:
            acts.append(end.animate.move_to(strand.anchor(i)+RIGHT*.40*strand.direction).set_color(NEW))
        scene.play(*acts,run_time=seconds)
        if hide_end and end is not None:
            end.move_to(strand.anchor(i)+RIGHT*.40*strand.direction).set_color(NEW)
            scene.play(FadeIn(end),run_time=.08)
        if template is not None:
            j=map_index(i) if map_index else i
            b=pair(template.at(j),strand.at(i));bonds.add(b)
            scene.play(Create(b),run_time=.10)
    return bonds


def molecule(width=.72,color=OLD):
    """Small duplex at sample scale, with antiparallel arrows."""
    return VGroup(arrow(P(-width/2,.07),P(width/2,.07),color),
        arrow(P(width/2,-.07),P(-width/2,-.07),color),
        *[Line(P(x,-.05),P(x,.05),color=HAIRLINE,stroke_width=.8)
          for x in np.linspace(-width*.32,width*.32,4)])


def bent_strand(strand, offsets):
    """Bend a strand without leaving gaps between nucleotide-owned links."""
    target=strand.copy()
    pts=[strand.anchor(i)+UP*offsets[i] for i in range(len(offsets))]
    for i,unit in enumerate(target.units):
        neighbor=i-1 if strand.direction==1 else i+1
        start=pts[neighbor] if 0<=neighbor<len(pts) else pts[i]-RIGHT*.15*strand.direction
        unit[0].put_start_and_end_on(start,pts[i])
        unit[1].put_start_and_end_on(pts[i],pts[i]+UP*strand.side*.12)
        unit[2].move_to(pts[i]+UP*strand.side*.3)
    if len(target.ends):
        target.ends[0].shift(UP*offsets[0]);target.ends[1].shift(UP*offsets[-1])
    return target


class DigitalPCR(Lesson):
    title="Digital PCR"
    steps=("partition","amplify","read","count","correct")

    def construct(self):
        vessel=RoundedRectangle(width=2.1,height=2.8,corner_radius=.25,
            color=HAIRLINE,stroke_width=1.5).move_to(P(-4.7,.2))
        sample=VGroup(*[molecule(.50).move_to(P(-5.2+(i%2)*.9,1.1-(i//2)*.57))
                        for i in range(8)])
        self.step(0,"Distribute DNA into separate reaction partitions.")
        self.play(Create(vessel),FadeIn(sample),run_time=1.5)
        self.pause(1.5)
        droplets=VGroup(*[Circle(radius=.37,color=HAIRLINE,stroke_width=1.4,
                                  fill_color=BG,fill_opacity=1).move_to(P(.1+c*1.15,1.75-r*1.05))
                          for r in range(4) for c in range(4)])
        droplets.set_z_index(-1)
        self.play(LaggedStart(*[Create(d) for d in droplets],lag_ratio=.045),run_time=1.6)
        occupied=[0,0,2,5,6,6,10,13]
        for i,j in enumerate(occupied):
            dy=.12 if occupied.count(j)>1 and occupied.index(j)==i else (-.12 if occupied.count(j)>1 else 0)
            self.play(sample[i].animate.scale(.67).move_to(droplets[j].get_center()+UP*dy),run_time=.35)
        self.play(FadeOut(vessel),run_time=.5)
        self.pause(2)
        self.step(1,"Each partition runs its own PCR reaction.")
        # Follow one real occupied partition into a molecular close-up.
        focus=VGroup(droplets[2],sample[2])
        rest=VGroup(*[d for i,d in enumerate(droplets) if i!=2],
                    *[m for i,m in enumerate(sample) if i!=2])
        self.play(rest.animate.set_opacity(.12),focus.animate.scale(3.8).move_to(P(-2.1,.2)),run_time=1.5)
        self.play(sample[2].animate.set_opacity(0),run_time=.25)
        seq="TACGTA"
        template=Strand(seq,x=-3.23,y=.65,step=.45,direction=-1,side=-1)
        product=Strand(complement(seq),x=-3.23,y=-.35,step=.45,role=NEW,side=1,labels=False)
        for u in product.units[:2]:u[0].set_color(PRIMER);u[1].set_color(PRIMER)
        pe=termini(-3.23,-2.78,-.35,color=PRIMER)
        self.play(Create(template),Create(VGroup(*product.units[:2])),FadeIn(pe),run_time=1)
        pol=enzyme().scale(.66).move_to(P(-2.78,-1.1))
        self.play(FadeIn(pol),run_time=.4)
        grow(self,product,range(2,6),pol,pe[1],template,seconds=.55,enzyme_y=-1.1,incoming_y=-2.0)
        self.play(FadeOut(pol),run_time=.4)
        self.pause(1.4)
        self.step(2,"Read fluorescence after amplification ends.")
        self.play(droplets[2].animate.set_fill(SIGNAL,.24),run_time=1)
        self.play(*[FadeOut(m) for m in (template,product.units,pe)],run_time=.5)
        # Actual close-up shrinks back into the corresponding partition.
        self.play(droplets[2].animate.scale(1/3.8).move_to(P(2.4,1.75)),
                  rest.animate.set_opacity(1),run_time=1.3)
        self.play(*[d.animate.set_fill(SIGNAL,.24) for i,d in enumerate(droplets) if i in set(occupied)],
                  *[m.animate.set_opacity(0) for m in sample],run_time=1.5)
        positives=caption("6 positive",P(-3.4,.85),26,SIGNAL)
        negatives=caption("10 negative",P(-3.4,-.05),26,MUTED)
        self.step(3,"Count positive and negative partitions.")
        self.play(FadeIn(positives),FadeIn(negatives),run_time=.8)
        for i in sorted(set(occupied)):
            self.play(Indicate(droplets[i],color=SIGNAL,scale_factor=1.1),run_time=.22)
        self.pause(1.5)
        self.step(4,"A positive partition may have started with two copies.")
        doubled=VGroup(molecule(.28),molecule(.28)).arrange(DOWN,buff=.09).move_to(droplets[0])
        single=molecule(.28).move_to(droplets[5])
        self.play(FadeIn(doubled),FadeIn(single),run_time=.6)
        self.pause(2.3)
        self.step(4,"The empty fraction gives a Poisson correction.")
        formula=caption("λ = −ln(10 / 16) = 0.47",P(-2.6,-1.55),25,NEW)
        meaning=caption("copies per partition",P(-2.6,-2.03),17,MUTED)
        self.play(FadeIn(formula),FadeIn(meaning),run_time=.9)
        self.pause(2.4)
        self.finish("Estimated starting copies: 16 × 0.47 ≈ 7.5.",hold=3.5)


class ProbeQPCR(Lesson):
    title="Probe qPCR"
    steps=("prime","probe","extend","cleave","measure")

    def construct(self):
        seq="TACGATCGATGC";x=-3.85;dx=.64
        template=Strand(seq,x=x,y=.9,step=dx,direction=-1,side=-1)
        product=Strand(complement(seq),x=x,y=-.25,step=dx,side=1,role=NEW,labels=False)
        for u in product.units[:3]:u[0].set_color(PRIMER);u[1].set_color(PRIMER)
        pe=termini(x,x+2*dx,-.25,color=PRIMER)
        self.step(0,"A primer binds the target DNA.")
        self.play(Create(template),run_time=1.1)
        self.play(Create(VGroup(*product.units[:3])),FadeIn(pe),run_time=1)
        self.play(*[Create(pair(template.at(i),product.at(i))) for i in range(3)],run_time=.7)
        self.pause(1.5)
        self.step(1,"A reporter–quencher probe binds farther ahead.")
        probe=Strand(complement(seq)[6:10],x=x+6*dx,y=-.25,step=dx,side=1,role=SIGNAL,labels=False)
        r=VGroup(Circle(radius=.12,color=SIGNAL,stroke_width=1.2,fill_color=SIGNAL,fill_opacity=.12),
                 caption("R",P(0,-.39),17,SIGNAL)).move_to(P(x+6*dx-.42,-.4))
        q=VGroup(Square(side_length=.21,color=MUTED,stroke_width=1.2,fill_color=MUTED,fill_opacity=.15),
                 caption("Q",P(0,-.39),17,MUTED)).move_to(P(x+9*dx+.42,-.4))
        r.add(Line(r[0].get_right(),probe.anchor(0),color=SIGNAL,stroke_width=1.4))
        q.add(Line(probe.anchor(3),q[0].get_left(),color=SIGNAL,stroke_width=1.4))
        probe_bonds=VGroup(*[pair(template.at(i+6),probe.at(i)) for i in range(4)])
        self.play(Create(probe),FadeIn(r),FadeIn(q),Create(probe_bonds),run_time=1.2)
        quiet=caption("quenched",P(1.0,-1.3),19,MUTED)
        self.play(FadeIn(quiet),run_time=.4)
        self.pause(2.5)
        self.step(2,"Polymerase approaches the bound probe.")
        pol=enzyme("Taq").move_to(P(x+2*dx,-1.5))
        self.play(FadeOut(quiet),FadeIn(pol),FadeOut(pe[1]),run_time=.5)
        grow(self,product,range(3,6),pol,None,template,seconds=.65,incoming_y=.35)
        self.pause(1.8)
        self.step(3,"The 5′ nuclease cleaves the probe.")
        self.play(Indicate(probe.units[1][0],color=STOP),run_time=.9)
        self.play(FadeOut(probe.units[1][0]),FadeOut(probe_bonds),run_time=.45)
        reporter_fragment=VGroup(probe.units[0],r)
        remainder=VGroup(*probe.units[1:],q)
        self.play(reporter_fragment.animate.shift(DOWN*1.05+RIGHT*.8),
                  remainder.animate.shift(RIGHT*.9+DOWN*1.0),run_time=1.4)
        self.step(3,"Separated from the quencher, the reporter glows.")
        self.play(r[0].animate.set_fill(SIGNAL,.85),
                  Flash(r[0],color=SIGNAL,flash_radius=.3,line_length=.12),run_time=1.1)
        self.pause(1.6)
        pe[1].move_to(product.anchor(5)+RIGHT*.4).set_color(NEW)
        self.play(FadeOut(reporter_fragment),FadeOut(remainder),FadeIn(pe[1]),run_time=.6)
        grow(self,product,range(6,12),pol,pe[1],template,seconds=.4,incoming_y=.35)
        self.play(FadeOut(pol),run_time=.4)
        self.pause(1.5)
        self.step(4,"Each cycle releases more fluorescent reporters.")
        reporters=VGroup()
        for i in range(6):
            light=Dot(P(-2.7+i*1.08,-1.75),radius=.11,color=SIGNAL)
            reporters.add(light)
            self.play(FadeIn(light,shift=UP*.4),Flash(light,color=SIGNAL,
                       flash_radius=.25,line_length=.08),run_time=.4)
        self.pause(1.4)
        self.finish("Fluorescence tracks amplification of this target.",hold=3.2)


class RPA(Lesson):
    title="Recombinase polymerase amplification"
    steps=("coat","invade","stabilize","extend","repeat")

    def construct(self):
        seq="TACGGTACCTAGCA";dx=.57;x=-3.7
        top=Strand(seq,x=x,y=.6,step=dx,direction=-1,side=-1)
        bottom=Strand(complement(seq),x=x,y=-.5,step=dx,direction=1,side=1)
        old_pairs=top.pairing(bottom)
        self.step(0,"Recombinase coats a matching DNA primer.")
        self.play(Create(top),Create(bottom),Create(old_pairs),run_time=1.4)
        nascent=Strand(complement(seq),x=x,y=-.5,step=dx,direction=1,side=1,role=NEW,labels=False)
        for u in nascent.units[:3]:u[0].set_color(PRIMER);u[1].set_color(PRIMER)
        primer=VGroup(*nascent.units[:3]).shift(DOWN*1.5)
        rec=VGroup(*[RoundedRectangle(width=.48,height=.50,corner_radius=.12,
                      color=ENZYME,stroke_width=1,fill_color=ENZYME,fill_opacity=.08)
                     .move_to(primer[i][2]) for i in range(3)])
        rec_name=caption("recombinase",P(-1.0,-2.1),18)
        self.play(FadeIn(primer),FadeIn(rec),FadeIn(rec_name),run_time=1)
        self.pause(2.5)
        self.step(1,"The coated primer opens a matching site.")
        offsets=[-1.1 if i<5 else (-.7 if i==5 else (-.3 if i==6 else 0)) for i in range(len(seq))]
        bent=bent_strand(bottom,offsets)
        self.play(FadeOut(VGroup(*old_pairs[:7])),Transform(bottom,bent),primer.animate.shift(UP*1.5),
                  rec.animate.shift(UP*1.5),FadeOut(rec_name),run_time=2)
        pe=termini(x,x+2*dx,-.5,color=PRIMER)
        new_pairs=VGroup(*[pair(top.at(i),nascent.at(i)) for i in range(3)])
        self.play(FadeIn(pe),Create(new_pairs),run_time=.7)
        self.pause(1.8)
        self.step(2,"SSB proteins hold the displaced strand open.")
        ssb=VGroup(*[enzyme("SSB",width=.7).scale(.62).move_to(P(x+(i+.5)*dx,-2.05))
                     for i in (0,2,4)])
        self.play(FadeIn(ssb),run_time=.7)
        self.play(rec.animate.shift(UP*.65).set_opacity(0),run_time=.8)
        self.pause(1.8)
        self.step(3,"Polymerase extends without thermal melting.")
        pol=enzyme().move_to(P(x+2*dx,1.55))
        self.play(FadeIn(pol),run_time=.6)
        for i in range(3,len(seq)):
            # The original partner is peeled away as synthesis advances.
            changed=[-1.1 if j<=i else (-.5 if j==i+1 else 0) for j in range(len(seq))]
            original=Strand(complement(seq),x=x,y=-.5,step=dx,direction=1,side=1)
            opening=[FadeOut(old_pairs[i+1])] if 6 <= i < len(seq)-1 else []
            self.play(Transform(bottom,bent_strand(original,changed)),*opening,run_time=.15)
            new_pairs.add(*grow(self,nascent,[i],pol,pe[1],top,seconds=.35,
                               enzyme_y=1.55,incoming_y=-.2))
        self.play(FadeOut(pol),FadeOut(ssb),run_time=.6)
        self.pause(1.6)
        self.step(4,"The opposite primer copies the other strand.")
        # Reorient the same displaced strand as the next template.
        self.play(FadeOut(top),FadeOut(nascent.units),FadeOut(pe),FadeOut(new_pairs),run_time=.6)
        straight=Strand(complement(seq),x=x,y=-.55,step=dx,direction=1,side=1)
        self.play(Transform(bottom,straight),run_time=1.2)
        daughter=Strand(seq,x=x,y=.55,step=dx,direction=-1,side=-1,role=NEW,labels=False)
        for u in daughter.units[-3:]:u[0].set_color(PRIMER);u[1].set_color(PRIMER)
        de=termini(x+11*dx,x+13*dx,.55,-1,PRIMER)
        self.play(Create(VGroup(*daughter.units[-3:])),FadeIn(de),run_time=.7)
        pol=enzyme().move_to(P(x+11*dx,1.45));self.play(FadeIn(pol),run_time=.3)
        grow(self,daughter,range(10,-1,-1),pol,de[0],bottom,seconds=.25,enzyme_y=1.45,incoming_y=2.15)
        self.play(FadeOut(pol),run_time=.4)
        self.finish("New duplexes support further primer invasion.",hold=3)


class RollingCircleAmplification(Lesson):
    title="Rolling circle amplification"
    steps=("circle","prime","copy","displace","repeat")

    def construct(self):
        motif="TGCAAC";copied=complement(motif);cx,cy=-4.45,.65
        ring=Circle(radius=.94,color=OLD,stroke_width=2).move_to(P(cx,cy))
        circle_bases=VGroup(*[base_tile(b,.75).move_to(P(cx+.94*np.cos(TAU*i/6),
                         cy+.94*np.sin(TAU*i/6))) for i,b in enumerate(motif)])
        closed=VGroup(ring,circle_bases)
        closed.rotate(-2*TAU/6,about_point=P(cx,cy))
        for tile in circle_bases:tile.rotate(2*TAU/6)
        self.step(0,"A closed DNA circle supplies the template.")
        self.play(Create(ring),FadeIn(circle_bases),run_time=1.5)
        self.play(FadeIn(caption("circular template",P(cx,-.85),18)),run_time=.5)
        self.pause(2.4)
        self.step(1,"A primer supplies a paired 3′ end.")
        # The right-hand drawing magnifies the active site of the same circle.
        x=-2.15;dx=.45;seq=copied*3
        product=Strand(seq,x=x,y=-.25,step=dx,role=NEW,side=1,labels=False)
        for u in product.units[:3]:u[0].set_color(PRIMER);u[1].set_color(PRIMER)
        primer=VGroup(*product.units[:3]);pe=termini(x,x+2*dx,-.25,color=PRIMER)
        window=Strand(motif*3,x=x,y=.8,step=dx,direction=-1,side=-1,labels=False)
        window.units[2][0].put_start_and_end_on(window.anchor(2)+RIGHT*.15,window.anchor(2))
        wt=termini(x,x+2*dx,.8,-1,OLD)
        focus=Dot(P(cx+1.20,cy),radius=.045,color=SIGNAL)
        guide=DashedLine(P(cx+1.27,cy),P(x-.42,.8),color=HAIRLINE,dash_length=.07,stroke_width=1)
        zoom=caption("active site, enlarged",P(1.6,1.85),17)
        self.play(FadeIn(focus),Create(guide),FadeIn(zoom),Create(VGroup(*window.units[:3])),FadeIn(wt),
                  Create(primer),FadeIn(pe),run_time=1.2)
        bonds=VGroup(*[pair(window.at(i),product.at(i)) for i in range(3)])
        self.play(Create(bonds),run_time=.6)
        self.pause(1.8)
        self.step(2,"Phi29 polymerase copies the circle, 5′ → 3′.")
        pol=enzyme("phi29",width=1.25).move_to(P(x+2*dx,-1.25))
        self.play(FadeIn(pol),run_time=.5)
        # Template bases advance through the magnified window as the circle
        # rotates beneath a stationary sampling point. DNA behind it peels off.
        for i in range(3,18):
            if i==6:
                self.step(3,"The new strand is displaced on the next lap.",hold=1.5)
            if i==12:
                self.step(4,"The same circle produces another tandem repeat.",hold=1.5)
            left=i-2
            new_ends=termini(x+left*dx,x+i*dx,.8,-1,OLD)
            window.units[i][0].put_start_and_end_on(window.anchor(i)+RIGHT*.15,window.anchor(i))
            orbit=[]
            for tile in circle_bases:
                delta=tile.get_center()-P(cx,cy)
                route=Arc(radius=.94,start_angle=np.arctan2(delta[1],delta[0]),
                          angle=-TAU/6,arc_center=P(cx,cy))
                orbit.append(MoveAlongPath(tile,route))
            self.play(FadeOut(bonds),FadeOut(window.units[i-3]),Create(window.units[i]),
                      Transform(wt,new_ends),
                      window.units[i-1][0].animate.put_start_and_end_on(window.anchor(i),window.anchor(i-1)),
                      guide.animate.put_start_and_end_on(P(cx+1.27,cy),P(x+left*dx-.7,.8)),
                      *orbit,run_time=.4)
            grow(self,product,[i],pol,pe[1],seconds=.38,enzyme_y=-1.25,incoming_y=-2.0,hide_end=True,incoming_dx=1.3)
            bonds=VGroup(*[pair(window.at(left+j),product.at(left+j)) for j in range(3)])
            self.play(Create(bonds),run_time=.10)
        self.play(FadeOut(pol),run_time=.4)
        repeat_marks=VGroup()
        for j in range(3):
            a=x+j*6*dx;b=x+(j*6+5)*dx
            repeat_marks.add(Line(P(a,-.75),P(b,-.75),color=SIGNAL,stroke_width=1),
                             caption(str(j+1),P((a+b)/2,-1.08),18,SIGNAL))
        self.play(Create(repeat_marks),run_time=.8)
        self.pause(2)
        self.finish("One continuous strand contains repeated circle copies.",hold=3.2)


class MultipleDisplacementAmplification(Lesson):
    title="Multiple displacement amplification"
    steps=("random primers","extend","displace","re-prime","branch")

    def construct(self):
        seq="TACGGTACCTAGCATGCA";comp=complement(seq);dx=.46;x=-3.91
        template=Strand(seq,x=x,y=1.25,step=dx,direction=-1,side=-1)
        self.step(0,"Random primers bind many matching sites.")
        self.play(Create(template),run_time=1.2)
        first=Strand(comp[1:],x=x+dx,y=.2,step=dx,role=NEW,side=1,labels=False)
        second=Strand(comp[10:],x=x+10*dx,y=.2,step=dx,role=NEW,side=1,labels=False)
        for chain in (first,second):
            for u in chain.units[:3]:u[0].set_color(PRIMER);u[1].set_color(PRIMER)
        first_end=termini(x+dx,x+3*dx,.2,color=PRIMER)
        second_end=termini(x+10*dx,x+12*dx,.2,color=PRIMER)
        second_end[0].shift(DOWN*.4)
        self.play(Create(VGroup(*first.units[:3])),Create(VGroup(*second.units[:3])),
                  FadeIn(first_end),FadeIn(second_end),run_time=1.2)
        initial_pairs=VGroup(*[pair(template.at(i+1),first.at(i)) for i in range(3)],
                            *[pair(template.at(i+10),second.at(i)) for i in range(3)])
        self.play(Create(initial_pairs),run_time=.7)
        self.pause(2.6)
        self.step(1,"Phi29 extends each paired primer.")
        pol2=enzyme("phi29",width=1.1).move_to(P(x+12*dx,-.55))
        self.play(FadeIn(pol2),run_time=.4)
        second_pairs=grow(self,second,range(3,len(second.sequence)),pol2,second_end[1],
                           template,lambda i:i+10,seconds=.5,enzyme_y=-.55,incoming_y=-.15,hide_end=True)
        self.play(FadeOut(pol2),run_time=.4)
        pol1=enzyme("phi29",width=1.1).move_to(P(x+3*dx,-.55))
        self.play(FadeIn(pol1),FadeOut(second_end[0]),run_time=.4)
        first_pairs=grow(self,first,range(3,9),pol1,first_end[1],template,
                          lambda i:i+1,seconds=.45,enzyme_y=-.55,incoming_y=-.15,hide_end=True)
        self.pause(1.3)
        self.step(2,"An advancing polymerase displaces DNA ahead.")
        downstream=VGroup(second,second_end)
        self.play(first_end[1].animate.set_opacity(0),second_end[0].animate.set_opacity(0),run_time=.25)
        self.play(FadeOut(second_pairs),FadeOut(VGroup(*initial_pairs[3:])),
                  downstream.animate.shift(DOWN*1.45),run_time=1.4)
        self.play(first_end[1].animate.set_opacity(1),second_end[0].animate.set_opacity(1),run_time=.25)
        more_pairs=grow(self,first,range(9,len(first.sequence)),pol1,first_end[1],
                         template,lambda i:i+1,seconds=.32,enzyme_y=-.55,incoming_y=-.15,hide_end=True)
        self.play(FadeOut(pol1),run_time=.4)
        self.pause(1.4)
        self.step(3,"A random primer binds the displaced strand.")
        # Focus on the genuine released daughter while the original duplex
        # moves upward out of the next polymerase's working lane.
        self.play(VGroup(template,first,first_end,initial_pairs,first_pairs,more_pairs).animate.shift(UP*.35),
                  downstream.animate.shift(LEFT*2.4),run_time=1.1)
        # Displaced strand is 5′→3′ and its bases face upward; the new copy
        # sits above it and extends in the opposite physical direction.
        sx=second.anchor(0)[0];sy=second.anchor(0)[1]
        daughter=Strand(complement(second.sequence),x=sx,y=sy+1.05,step=dx,
                        direction=-1,side=-1,role=NEW,labels=False)
        for u in daughter.units[-3:]:u[0].set_color(PRIMER);u[1].set_color(PRIMER)
        de=termini(sx+5*dx,sx+7*dx,sy+1.05,-1,PRIMER)
        self.play(Create(VGroup(*daughter.units[-3:])),FadeIn(de),run_time=.8)
        self.pause(1.5)
        self.step(4,"Copying the new template creates another branch.")
        pol=enzyme("phi29",width=1.1).scale(.8).move_to(P(sx+5*dx,-2.2))
        self.play(FadeIn(pol),run_time=.4)
        grow(self,daughter,range(4,-1,-1),pol,de[0],second,seconds=.45,enzyme_y=-2.2,incoming_y=.05)
        self.play(FadeOut(pol),run_time=.4)
        self.pause(1.4)
        self.step(4,"Many displaced strands create new priming sites.")
        self.clear_stage()
        # Molecular overview: each branch is a separate covalent DNA strand.
        # Dashed cross-links denote hybridization, never covalent branch joins.
        trunk=Line(P(-4.8,1.1),P(4.8,1.1),color=OLD,stroke_width=3.2)
        trunk_ends=termini(-4.8,4.8,1.1,-1,OLD)
        self.play(Create(trunk),FadeIn(trunk_ends),run_time=.7)
        branches=VGroup()
        specifications=[(-4.5,.05,-2.8,-1.7),(-4.5,-.8,-.1,1.0),(-4.5,-1.65,2.4,3.6)]
        for startx,starty,joinx,endx in specifications:
            # The tail emerges from an earlier copied region and is displaced
            # away from the still-hybridized growing end.
            chain=VMobject(color=NEW,stroke_width=3.2)
            tail_end = -1.6 if starty < -1 else startx+.65
            chain.set_points_as_corners([P(startx,starty),P(tail_end,starty),
                                        P(joinx-.65,.05),P(joinx,.05),P(endx,.05)])
            primer_mark=Line(P(startx,starty),P(startx+.45,starty),color=PRIMER,stroke_width=3.2)
            polarity=VGroup(caption("5′",P(startx-.30,starty),15,PRIMER),
                             caption("3′",P(endx+.27,.05),15,NEW))
            duplex_links=VGroup(*[DashedLine(P(xx,.16),P(xx,1.0),color=HAIRLINE,
                               stroke_width=1,dash_length=.07)
                                 for xx in np.linspace(joinx,endx,4)])
            fork=VGroup(chain,primer_mark,polarity,duplex_links)
            branches.add(fork)
            self.play(Create(chain),Create(primer_mark),FadeIn(polarity),Create(duplex_links),run_time=.9)
        # A newly made displaced tail is itself copied by a reverse primer.
        secondary=Line(P(-2.25,-2.35),P(-3.6,-2.35),color=NEW,stroke_width=3.2)
        secondary_primer=Line(P(-2.25,-2.35),P(-1.8,-2.35),color=PRIMER,stroke_width=3.2)
        subends=termini(-3.6,-1.8,-2.35,-1,NEW)
        link=VGroup(*[DashedLine(P(xx,-2.25),P(xx,-1.75),color=HAIRLINE,
                         stroke_width=1,dash_length=.07) for xx in (-3.4,-3,-2.6,-2.2)])
        self.play(Create(secondary_primer),run_time=.5)
        self.play(Create(secondary),Create(link),FadeIn(subends),run_time=1.1)
        self.pause(1.8)
        self.finish("Repeated priming builds a branched DNA network.",hold=3.5)


class Telomerase(Lesson):
    title="Telomerase"
    steps=("overhang","RNA template","extend","realign","fill in")

    def construct(self):
        # Human alignment register: terminal GTTAG pairs with CAAUC.
        # Copying the remaining CCAAUC adds GGTTAG before translocation.
        initial="TTAGGGTTAG";seq=initial+"GGTTAG"*2;dx=.44;x=-4.4
        dna=Strand(seq,x=x,y=.5,step=dx,role=NEW,side=-1,labels=False)
        for u in dna.units[:len(initial)]:u[0].set_color(OLD);u[1].set_color(OLD)
        ends=termini(x,x+9*dx,.5,color=OLD)
        old_partner=Strand(complement(seq[:5]),x=x,y=-.55,step=dx,direction=-1,side=1)
        paired=VGroup(*[pair(dna.at(i),old_partner.at(i)) for i in range(5)])
        self.step(0,"A chromosome ends with a single-stranded 3′ tail.")
        self.play(Create(VGroup(*dna.units[:10])),FadeIn(ends),Create(old_partner),Create(paired),run_time=1.6)
        overhang=BraceBetweenPoints(P(x+5*dx,.95),P(x+9*dx,.95),UP,color=SIGNAL)
        self.play(Create(overhang),run_time=.7)
        self.pause(2.2)
        self.step(1,"Telomerase aligns its RNA with the DNA end.")
        rna=Strand("CAAUCCCAAUC",x=x+5*dx,y=-.55,step=dx,direction=-1,side=1)
        rna.ends.shift(DOWN*.45)
        rn=caption("RNA template",P(0,-1.1),18,OLD)
        tel=enzyme("telomerase",width=1.85).move_to(P(0,-1.9))
        self.play(FadeOut(overhang),FadeOut(old_partner.ends[1]),Create(rna),FadeIn(rn),FadeIn(tel),run_time=1.4)
        hybrid=VGroup(*[pair(dna.at(i+5),rna.at(i)) for i in range(5)])
        self.play(Create(hybrid),run_time=.7)
        self.pause(2.3)
        self.step(2,"The RNA sequence guides six new DNA bases.")
        for i in range(10,16):
            grow(self,dna,[i],end=ends[1],seconds=.58,incoming_y=1.85)
            self.play(FadeOut(hybrid[0]),run_time=.12);hybrid.remove(hybrid[0])
            b=pair(dna.at(i),rna.at(i-5));hybrid.add(b);self.play(Create(b),run_time=.12)
        self.pause(1.7)
        self.step(3,"At the RNA boundary, realign by one repeat.")
        self.play(FadeOut(hybrid),run_time=.4)
        self.play(rna.animate.shift(RIGHT*6*dx),rn.animate.shift(RIGHT*6*dx),
                  tel.animate.shift(RIGHT*6*dx),run_time=1.6)
        hybrid=VGroup(*[pair(dna.at(i+11),rna.at(i)) for i in range(5)])
        self.play(Create(hybrid),run_time=.7)
        self.pause(1.8)
        self.step(3,"The same RNA template adds the next repeat.")
        for i in range(16,22):
            grow(self,dna,[i],end=ends[1],seconds=.48,incoming_y=1.85)
            self.play(FadeOut(hybrid[0]),run_time=.12);hybrid.remove(hybrid[0])
            b=pair(dna.at(i),rna.at(i-11));hybrid.add(b);self.play(Create(b),run_time=.12)
        self.pause(1.5)
        self.step(4,"Primase and polymerase α fill the partner strand.")
        self.play(FadeOut(hybrid),rna.animate.shift(DOWN*.65).set_opacity(0),
                  FadeOut(rn),FadeOut(tel),run_time=1)
        primer=Strand(complement(seq[13:16]).replace("T","U"),x=x+13*dx,y=-.55,
                      step=dx,direction=-1,side=1,role=PRIMER,labels=False)
        pe=termini(x+13*dx,x+15*dx,-.55,-1,PRIMER)
        self.play(Create(primer),FadeIn(pe),run_time=.8)
        filled=Strand(complement(seq[5:13]),x=x+5*dx,y=-.55,step=dx,direction=-1,
                      side=1,role=NEW,labels=False)
        filled.units[-1][0].put_start_and_end_on(primer.anchor(0),filled.anchor(7))
        pol=enzyme("pol α",width=1.05).move_to(P(x+13*dx,-1.5))
        self.play(FadeIn(pol),run_time=.4)
        grow(self,filled,range(7,-1,-1),pol,pe[0],dna,lambda i:i+5,
             seconds=.3,enzyme_y=-1.5,incoming_y=-2.25)
        self.play(FadeOut(pol),run_time=.35)
        self.step(4,"Primer removal leaves the protective 3′ overhang.")
        self.play(primer.animate.shift(DOWN*.65).set_opacity(0),FadeOut(pe),run_time=.9)
        join=Line(old_partner.anchor(4),filled.anchor(0),color=NEW,stroke_width=3.2)
        c_end=caption("5′",P(x+12*dx+.4,-.55),16,NEW)
        self.play(Create(join),FadeIn(c_end),run_time=.5)
        mark=BraceBetweenPoints(P(x+13*dx,1.05),P(x+21*dx,1.05),UP,color=SIGNAL)
        self.play(Create(mark),run_time=.6)
        self.finish("Telomerase extends the G-rich chromosome end.",hold=3)
