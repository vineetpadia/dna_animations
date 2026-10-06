"""Amplification lessons: causal molecular steps, followed by an overview."""
import numpy as np
from manim import *
from dna_animations.core import (
    BG, OLD, NEW, PRIMER, ENZYME, SIGNAL, MUTED, WHITE,
    Lesson, Strand, label, caption, tag, enzyme, arrow, complement,
)


def p(x, y):
    return np.array([x, y, 0.])


def bond(a, b):
    d = b-a
    u = d/np.linalg.norm(d)
    return DashedLine(a+u*.18, b-u*.18, color=MUTED,
                      stroke_width=1.2, dash_length=.05)


def ends(x0, x1, y, direction=1, color=PRIMER):
    names = ("5′", "3′") if direction == 1 else ("3′", "5′")
    return VGroup(label(names[0], 16, color).move_to(p(x0-.40, y)),
                  label(names[1], 16, color).move_to(p(x1+.40, y)))


def duplex_icon(width=1.8, color=NEW):
    """Overview glyph: two antiparallel backbones, not a nucleotide."""
    upper = arrow(p(-width/2, .11), p(width/2, .11), color)
    lower = arrow(p(width/2, -.11), p(-width/2, -.11), color)
    links = VGroup(*[Line(p(x, -.09), p(x, .09), color=MUTED, stroke_width=1)
                     for x in np.linspace(-width*.4, width*.4, 6)])
    return VGroup(upper, lower, links)


class PCR(Lesson):
    title = "PCR"
    subtitle = "Two primers turn one chosen region into many copies"
    steps = ("target", "separate", "prime", "extend", "repeat")

    def construct(self):
        seq = "GACTACGGTACCATGCTA"
        comp = complement(seq)
        spacing, x = .50, -4.25
        top = Strand(seq, x=x, y=.50, step=spacing, direction=1, side=-1)
        low = Strand(comp, x=x, y=-.50, step=spacing, direction=-1, side=1)
        links = top.pairing(low)
        target = RoundedRectangle(width=5.9, height=1.5, corner_radius=.12,
            stroke_color=SIGNAL, stroke_width=1.2, fill_color=SIGNAL,
            fill_opacity=.035).move_to(p(0,0))
        target_name = caption("target region", p(0,1.15), color=SIGNAL)
        self.step(0, "Choose a target within the DNA.")
        self.play(FadeIn(top), FadeIn(low), Create(links), run_time=1.5)
        self.play(Create(target), FadeIn(target_name), run_time=.8)
        self.pause(2.0)
        self.step(1, "Heat separates the two intact strands.")
        temp = tag("~95 °C", SIGNAL).move_to(p(5.55,1.0))
        self.play(FadeOut(links), FadeOut(target), FadeOut(target_name),
            top.animate.shift(UP*1.35), low.animate.shift(DOWN*1.35),
            FadeIn(temp), run_time=2)
        self.pause(1.6)
        self.step(2, "Cool. Primers bind their matching sites.")
        next_temp = tag("cool", SIGNAL).move_to(p(5.55,1.0))
        reverse = Strand(comp[12:15], x=x+12*spacing, y=.85, step=spacing,
                         direction=-1, role=PRIMER, side=1, labels=False)
        forward = Strand(seq[3:6], x=x+3*spacing, y=-.85, step=spacing,
                         direction=1, role=PRIMER, side=-1, labels=False)
        re = ends(x+12*spacing,x+14*spacing,.85,-1)
        fe = ends(x+3*spacing,x+5*spacing,-.85,1)
        primer_links = VGroup(*[bond(top.at(12+i), reverse.at(i)) for i in range(3)],
                              *[bond(low.at(3+i), forward.at(i)) for i in range(3)])
        reverse.shift(DOWN*.4); re.shift(DOWN*.4)
        forward.shift(UP*.4); fe.shift(UP*.4)
        self.play(ReplacementTransform(temp,next_temp),FadeIn(reverse),FadeIn(forward),
                  FadeIn(re),FadeIn(fe),run_time=.7)
        self.play(reverse.animate.shift(UP*.4),re.animate.shift(UP*.4),
                  forward.animate.shift(DOWN*.4),fe.animate.shift(DOWN*.4),run_time=1.2)
        self.play(Create(primer_links),run_time=.7)
        inward = VGroup(arrow(p(1.65,.35),p(.35,.35),PRIMER),
                         arrow(p(-1.65,-.35),p(-.35,-.35),PRIMER))
        self.play(Create(inward),run_time=.7)
        self.step(2, "Both 3′ ends point into the target.",hold=1.8)
        self.step(3, "Polymerase extends each paired 3′ end.")
        warm = tag("~72 °C", SIGNAL).move_to(p(5.55,1.0))
        self.play(FadeOut(inward),ReplacementTransform(next_temp,warm),run_time=.6)
        rp = enzyme("pol").scale(.82).move_to(p(x+12*spacing,.36))
        fp = enzyme("pol").scale(.82).move_to(p(x+5*spacing,-.36))
        ru = Strand(comp[:12],x=x,y=.85,step=spacing,direction=-1,role=NEW,
                    side=1,labels=False)
        fu = Strand(seq[6:],x=x+6*spacing,y=-.85,step=spacing,direction=1,
                    role=NEW,side=-1,labels=False)
        ru.units[-1][0].put_start_and_end_on(reverse.anchor(0),ru.anchor(11))
        fu.units[0][0].put_start_and_end_on(forward.anchor(2),fu.anchor(0))
        self.play(FadeIn(rp),FadeIn(fp),run_time=.7)
        new_links = VGroup()
        for j in range(12):
            ri, fi = 11-j,j
            bl = VGroup(bond(top.at(ri),ru.at(ri)),bond(low.at(fi+6),fu.at(fi)))
            new_links.add(bl)
            self.play(FadeIn(ru.units[ri]),FadeIn(fu.units[fi]),Create(bl),
                rp.animate.move_to(p(x+ri*spacing,.36)),
                fp.animate.move_to(p(x+(fi+6)*spacing,-.36)),
                re[0].animate.move_to(p(x+ri*spacing-.4,.85)).set_color(NEW),
                fe[1].animate.move_to(p(x+(fi+6)*spacing+.4,-.85)).set_color(NEW),
                run_time=.34)
        self.play(FadeOut(rp),FadeOut(fp),run_time=.5)
        self.step(3,"Cycle 1 copies extend beyond the target.",hold=2)
        self.clear_stage()
        self.step(4,"Cycle 2 uses the new strands as templates.")
        # Follow one cycle-1 long product; the opposite lineage is symmetric.
        x2=-3.5
        template=Strand(seq[3:],x=x2,y=.65,step=.50,direction=1,role=NEW,side=-1)
        for i in range(3):
            template.units[i][0].set_color(PRIMER)
            template.units[i][1].set_color(PRIMER)
        reverse2=Strand(comp[12:15],x=x2+9*.50,y=-.35,step=.50,
                        direction=-1,role=PRIMER,side=1,labels=False)
        r2ends=ends(x2+9*.50,x2+11*.50,-.35,-1)
        boundaries=VGroup(*[DashedLine(p(xx,1.25),p(xx,-1.15),color=SIGNAL,
                               stroke_width=1.2,dash_length=.09)
                           for xx in (x2-.24,x2+11*.50+.24)])
        names=VGroup(caption("two defined ends",p(-.65,1.65),color=SIGNAL),
                      caption("",p(0,-2.12),size=16))
        self.play(FadeIn(template),FadeIn(reverse2),FadeIn(r2ends),FadeIn(names),run_time=1.1)
        nascent=Strand(comp[3:12],x=x2,y=-.35,step=.5,direction=-1,role=NEW,
                       side=1,labels=False)
        nascent.units[-1][0].put_start_and_end_on(reverse2.anchor(0),nascent.anchor(8))
        pol=enzyme().move_to(p(x2+9*.5,-1.15))
        self.play(FadeIn(pol),run_time=.4)
        for i in range(8,-1,-1):
            self.play(FadeIn(nascent.units[i]),
                Create(bond(template.at(i),nascent.at(i))),
                pol.animate.move_to(p(x2+i*.5,-1.15)),
                r2ends[0].animate.move_to(p(x2+i*.5-.4,-.35)).set_color(NEW),run_time=.28)
        self.play(FadeOut(pol),Create(boundaries),run_time=.6)
        self.step(4,"Reaching the template end fixes both boundaries.",hold=2)
        self.clear_stage()
        self.step(4,"Cycle 3 produces the first bounded duplexes.")
        t=Strand(seq[3:15],x=-2.75,y=.55,step=.5,direction=1,role=NEW,side=-1)
        b=Strand(comp[3:15],x=-2.75,y=-.45,step=.5,direction=-1,role=NEW,side=1)
        for i in range(3):
            t.units[i][0].set_color(PRIMER); t.units[i][1].set_color(PRIMER)
            b.units[-1-i][0].set_color(PRIMER); b.units[-1-i][1].set_color(PRIMER)
        bounded=VGroup(t,b,t.pairing(b))
        bound_mark=Brace(bounded,UP,color=SIGNAL)
        bounded_name=caption("amplicon",p(0,1.62),color=SIGNAL)
        self.play(FadeIn(bounded),Create(bound_mark),FadeIn(bounded_name),run_time=1.3)
        self.pause(2)
        self.clear_stage()
        self.step(4,"Separate, prime, extend. Repeat.")
        groups=[]
        for n,xx in [(1,-4.8),(2,-1.6),(4,1.6),(8,4.8)]:
            g=VGroup(*[duplex_icon(width=.95 if n==8 else 1.4) for _ in range(n)])
            g.arrange_in_grid(rows=min(n,4),cols=1 if n<8 else 2,buff=.32).move_to(p(xx,.2))
            groups.append(g)
        for i,g in enumerate(groups):
            count=caption(str(2**i),p(-4.8+i*3.2,-1.75),size=27,color=NEW)
            anim=[FadeIn(g,shift=RIGHT*.15),FadeIn(count)]
            if i:
                anim.append(Create(arrow(groups[i-1].get_right()+RIGHT*.22,
                                         g.get_left()-RIGHT*.22,MUTED)))
            self.play(*anim,run_time=.9)
            self.pause(.45)
        self.play(FadeIn(caption("ideal doubling",p(0,-2.42),17)),run_time=.4)
        self.finish("Each new copy becomes another template.",hold=3)


class RTqPCR(Lesson):
    title="RT-qPCR"
    subtitle="Copy RNA into DNA, then measure amplification as it happens"
    steps=("RNA", "reverse transcribe", "amplify", "measure", "compare")

    def construct(self):
        rna_seq="UGACCUAGGCUAUC"
        cdna_seq=complement(rna_seq)
        x,spacing=-3.3,.55
        rna=Strand(rna_seq,x=x,y=.65,step=spacing,direction=-1,role=OLD,side=-1)
        self.step(0,"RNA contains U instead of T.")
        self.play(FadeIn(rna),run_time=1.2)
        rn=caption("RNA",p(-5.0,.65),color=OLD)
        self.play(FadeIn(rn),run_time=.5)
        self.pause(1.6)
        self.step(1,"A DNA primer supplies the paired 3′ end.")
        primer=Strand(cdna_seq[:3],x=x,y=-.35,step=spacing,direction=1,
                      role=PRIMER,side=1,labels=False)
        pe=ends(x,x+2*spacing,-.35,1)
        self.play(FadeIn(primer,shift=DOWN*.25),FadeIn(pe),run_time=.9)
        hybrid_bonds=VGroup(*[bond(rna.at(i),primer.at(i)) for i in range(3)])
        self.play(Create(hybrid_bonds),run_time=.7)
        self.pause(1.3)
        self.step(1,"Reverse transcriptase builds DNA, 5′ → 3′.")
        nascent=Strand(cdna_seq[3:],x=x+3*spacing,y=-.35,step=spacing,
                      direction=1,role=NEW,side=1,labels=False)
        nascent.units[0][0].put_start_and_end_on(primer.anchor(2),nascent.anchor(0))
        rt=enzyme("RT").move_to(p(x+2*spacing,-1.15))
        self.play(FadeIn(rt),run_time=.7)
        for j in range(len(nascent.sequence)):
            pair=bond(rna.at(j+3),nascent.at(j))
            hybrid_bonds.add(pair)
            self.play(FadeIn(nascent.units[j]),Create(pair),
                rt.animate.move_to(p(x+(j+3)*spacing,-1.15)),
                pe[1].animate.move_to(p(x+(j+3)*spacing+.4,-.35)).set_color(NEW),run_time=.38)
        name=caption("cDNA",p(-5.0,-.35),color=NEW)
        self.play(FadeOut(rt),FadeIn(name),run_time=.6)
        self.pause(1.7)
        self.step(2,"Separate the hybrid. cDNA becomes the template.")
        self.play(FadeOut(hybrid_bonds),rna.animate.shift(UP*.65),rn.animate.shift(UP*.65),run_time=1)
        self.pause(.6)
        self.clear_stage()
        dna=Strand(cdna_seq,x=x,y=.65,step=spacing,direction=1,role=NEW,side=-1)
        for i in range(3):
            dna.units[i][0].set_color(PRIMER)
            dna.units[i][1].set_color(PRIMER)
        mate_seq=complement(cdna_seq)
        rp=Strand(mate_seq[-3:],x=x+11*spacing,y=-.35,step=spacing,
                   direction=-1,role=PRIMER,side=1,labels=False)
        rpends=ends(x+11*spacing,x+13*spacing,-.35,-1)
        mate=Strand(mate_seq[:-3],x=x,y=-.35,step=spacing,direction=-1,
                     role=NEW,side=1,labels=False)
        mate.units[-1][0].put_start_and_end_on(rp.anchor(0),mate.anchor(10))
        pol=enzyme().move_to(p(x+11*spacing,-1.15))
        self.play(FadeIn(dna),FadeIn(rp),FadeIn(rpends),FadeIn(pol),run_time=.9)
        self.step(2,"DNA polymerase builds the partner strand.")
        for j in range(10,-1,-1):
            self.play(FadeIn(mate.units[j]),Create(bond(dna.at(j),mate.at(j))),
                pol.animate.move_to(p(x+j*spacing,-1.15)),
                rpends[0].animate.move_to(p(x+j*spacing-.4,-.35)).set_color(NEW),run_time=.24)
        self.play(FadeOut(pol),run_time=.4)
        self.step(3,"Dye fluoresces when bound to duplex DNA.")
        glow=VGroup(*[Dot(p(x+i*spacing,.15),radius=.075,color=SIGNAL)
                      for i in (2,5,8,11)])
        self.play(LaggedStart(*[FadeIn(d) for d in glow],lag_ratio=.25),run_time=1.2)
        self.play(*[Flash(d,flash_radius=.18,color=SIGNAL,line_length=.07) for d in glow],run_time=.8)
        self.pause(1.6)
        self.clear_stage()
        self.step(3,"Measure fluorescence after each cycle.")
        copies=VGroup(duplex_icon(2)).move_to(p(-3.7,.1))
        sensor=VGroup(Circle(radius=.6,color=SIGNAL,stroke_width=2),
                      label("read",20,SIGNAL)).move_to(p(3.8,.1))
        self.play(FadeIn(copies),FadeIn(sensor),run_time=.7)
        light=None
        for i,n in enumerate((2,4,8)):
            more=VGroup(*[duplex_icon(1.5) for _ in range(n)])
            more.arrange_in_grid(rows=min(4,n),cols=1 if n<8 else 2,buff=.30).move_to(p(-3.4,.1))
            signal=arrow(p(-.5,.1),p(2.85,.1),SIGNAL).set_stroke(width=2+i*2)
            text=caption(f"cycle {i+1}",p(-3.4,-1.6),color=NEW)
            if light is not None:
                self.remove(light)
            self.play(ReplacementTransform(copies,more),FadeIn(text),Create(signal),run_time=.8)
            self.play(Indicate(sensor,color=SIGNAL,scale_factor=1.12),run_time=.6)
            self.play(FadeOut(text),FadeOut(signal),run_time=.3)
            copies=more
        self.pause(.5)
        self.clear_stage()
        self.step(4,"Set a threshold above background.")
        axes=Axes(x_range=[0,40,10],y_range=[0,1.1,.2],x_length=8.9,y_length=3.6,
            axis_config={"color":MUTED,"stroke_width":1.5,"include_ticks":True},
            tips=False).move_to(p(.6,-.1))
        xlabels=VGroup(*[caption(str(i),axes.c2p(i,0)+DOWN*.23,size=15) for i in (0,10,20,30,40)])
        xlabel=caption("PCR cycle",p(4.55,-2.42),size=18)
        ylabel=caption("fluorescence",p(-4.55,.1),size=17).rotate(PI/2)
        illustration=caption("illustrative curves",p(4.1,1.93),size=14)
        threshold=.20
        th=DashedLine(axes.c2p(0,threshold),axes.c2p(40,threshold),
                      color=SIGNAL,stroke_width=1.7,dash_length=.09)
        thname=caption("threshold",axes.c2p(34,threshold)+UP*.22,size=16,color=SIGNAL)
        self.play(Create(axes),FadeIn(xlabels),FadeIn(xlabel),FadeIn(ylabel),
                  FadeIn(illustration),run_time=1.1)
        self.play(Create(th),FadeIn(thname),run_time=.8)
        self.pause(1.5)
        self.step(4,"More starting RNA crosses the threshold earlier.")
        delta=np.log(4)/.55
        fa=lambda c:1/(1+np.exp(-.55*(c-(18+delta))))
        fb=lambda c:1/(1+np.exp(-.55*(c-(25+delta))))
        a=axes.plot(fa,x_range=[0,40,.12],color=NEW,stroke_width=3.5)
        b=axes.plot(fb,x_range=[0,40,.12],color=OLD,stroke_width=3.5)
        legend=VGroup(caption("more RNA",p(-2.5,1.65),18,NEW),
                       caption("less RNA",p(-2.5,1.23),18,OLD))
        self.play(FadeIn(legend),run_time=.4)
        self.play(Create(a),Create(b),run_time=5,rate_func=linear)
        crossings=VGroup()
        for cq,color in ((18,NEW),(25,OLD)):
            crossings.add(Dot(axes.c2p(cq,threshold),radius=.07,color=color),
                DashedLine(axes.c2p(cq,threshold),axes.c2p(cq,0),color=color,
                           stroke_width=1.7,dash_length=.06),
                caption("Cq",axes.c2p(cq,0)+DOWN*.57,size=18,color=color))
        self.play(FadeIn(crossings),run_time=.9)
        self.play(FadeIn(caption("same assay • comparable efficiency",p(.6,-2.81),16)),run_time=.5)
        self.finish("Cq marks the cycle of threshold crossing.",hold=3.5)


def path(points,color=NEW,width=5,smooth=False):
    result=VMobject(stroke_color=color,stroke_width=width)
    if smooth:
        result.set_points_smoothly([p(*q) for q in points])
    else:
        result.set_points_as_corners([p(*q) for q in points])
    return result


def domain(name,x,y,width=1.2,color=OLD):
    return VGroup(Line(p(x-width/2,y),p(x+width/2,y),color=color,stroke_width=5),
                  caption(name,p(x,y+.23),size=16,color=color))


def hairpin_seed(dumbbell=False):
    """Connected single DNA strand. A gap exposes its unligated 5′/3′ ends."""
    if dumbbell:
        points=[(-.25,.45),(-2,.45),(-2.6,.8),(-3.2,.5),(-3.35,0),
                (-3.2,-.5),(-2.6,-.8),(-2,-.45),(2,-.45),
                (2.6,-.8),(3.2,-.5),(3.35,0),(3.2,.5),(2.6,.8),(2,.45),(.25,.45)]
        # Follow the BIP-derived strand 5′→3′: B1c/B2 on the right,
        # then copied target domains through the left F loop.
        backbone=path(list(reversed(points)),NEW,smooth=True)
        primer_ink=backbone.copy().pointwise_become_partial(backbone,0,7/15).set_color(PRIMER)
        pairs=VGroup(*[DashedLine(p(x,-.38),p(x,.38),color=MUTED,
                          stroke_width=1.2,dash_length=.06)
                      for x in np.linspace(-1.8,1.8,12) if abs(x)>.4])
        termini=VGroup(caption("3′",p(-.32,.77),17,NEW),
                         caption("5′",p(.32,.77),17,PRIMER))
        names=VGroup(caption("F loop",p(-3.1,-1.13),17,PRIMER),
                      caption("B loop",p(3.1,-1.13),17,PRIMER))
        return VGroup(backbone,pairs,termini,names,primer_ink)
    points=[(-.6,.7),(-2,.7),(-2.65,.95),(-3.2,.45),(-3.15,-.15),
             (-2.65,-.65),(-2,-.2),(4.4,-.2)]
    backbone=path(points,NEW,smooth=True)
    primer_ink=backbone.copy().pointwise_become_partial(backbone,0,6/7).set_color(PRIMER)
    # Straight domain labels identify complementary regions that fold together.
    names=VGroup(caption("F1c",p(-1.35,1.0),17,PRIMER),
        caption("F1",p(-1.35,-.49),17,NEW),
        caption("F2",p(-3.55,.20),17,PRIMER),
        caption("B1c",p(.6,.10),17,NEW),caption("B2c",p(2.3,.10),17,NEW),
        caption("B3c",p(4,.10),17,NEW),
        caption("5′",p(-.35,.70),17,PRIMER),caption("3′",p(4.72,-.2),17,NEW))
    pairs=VGroup(*[DashedLine(p(xx,.59),p(xx,-.08),color=MUTED,
                       stroke_width=1.2,dash_length=.07) for xx in (-1.9,-1.5,-1.1,-.7)])
    return VGroup(backbone,pairs,names,primer_ink)


class LAMP(Lesson):
    title="LAMP"
    subtitle="Strand displacement creates loops that drive further amplification"
    steps=("inner primer", "displace", "fold", "opposite end", "amplify")

    def construct(self):
        xs=[-4.5,-2.8,-1.1,.6,2.3,4.0]
        names=["F3c","F2c","F1c","B1","B2","B3"]
        template=VGroup(*[domain(n,x,1.15) for n,x in zip(names,xs)])
        connectors=VGroup(*[Line(p(xs[i]+.6,1.15),p(xs[i+1]-.6,1.15),
                            color=OLD,stroke_width=5) for i in range(5)])
        labels=ends(-5.1,4.6,1.15,-1,OLD)
        temp=tag("65 °C",MUTED).move_to(p(5.35,2.0))
        self.step(0,"FIP has a tail and a matching 3′ end.")
        self.play(FadeIn(template),Create(connectors),FadeIn(labels),FadeIn(temp),run_time=1.1)
        f2=domain("F2",-2.8,.35,color=PRIMER)
        tail=domain("F1c",-4.5,-.5,color=PRIMER)
        tether=path([(-3.9,-.5),(-3.6,-.45),(-3.65,.35),(-3.4,.35)],PRIMER,smooth=True)
        fipname=caption("FIP",p(-4.5,-1.02),19,PRIMER)
        fipends=VGroup(caption("5′",p(-5.42,-.5),17,PRIMER),caption("3′",p(-1.98,.35),17,PRIMER))
        fip=VGroup(tail,tether,f2,fipname,fipends)
        paired=VGroup(*[DashedLine(p(xx,.44),p(xx,1.05),color=MUTED,
                          dash_length=.06,stroke_width=1.2) for xx in (-3.2,-2.8,-2.4)])
        self.play(FadeIn(fip,shift=DOWN*.2),Create(paired),run_time=1.3)
        self.pause(2)
        self.step(0,"Bst polymerase extends the paired 3′ end.")
        extension=VGroup()
        pol=enzyme("Bst").move_to(p(-1.98,-.5))
        self.play(FadeIn(pol),run_time=.4)
        for i,n in enumerate(("F1","B1c","B2c","B3c")):
            xx=xs[i+2]
            seg=domain(n,xx,.35,color=NEW)
            join=Line(p(xx-1.1,.35),p(xx-.6,.35),color=NEW,stroke_width=5)
            extension.add(join,seg)
            self.play(Create(join),FadeIn(seg),pol.animate.move_to(p(xx+.5,-.5)),
                      fipends[1].animate.move_to(p(xx+.88,.35)).set_color(NEW),run_time=.75)
        self.play(FadeOut(pol),run_time=.4)
        self.pause(.7)
        self.step(1,"F3 starts upstream and displaces the new strand.")
        # Labels have their own static reading beat. Clear them before the
        # displaced product moves through the polymerase's visual lane.
        moving_names=[tail[1],f2[1],fipname]
        moving_names.extend(extension[i][1] for i in (1,3,5,7))
        self.play(*[m.animate.set_opacity(0) for m in moving_names],run_time=.35)
        # Release all FIP-derived material together as the outer product grows.
        f3=domain("F3",-4.5,.35,color=PRIMER)
        f3ends=ends(-5.1,-3.9,.35,1)
        first=VGroup(fip,extension)
        self.play(FadeOut(paired),FadeIn(f3),FadeIn(f3ends),run_time=.8)
        outer=Line(p(-3.9,.35),p(4.6,.35),color=NEW,stroke_width=5)
        pol=enzyme("Bst").move_to(p(-3.9,-.2))
        self.play(FadeIn(pol),run_time=.4)
        self.play(Create(outer),pol.animate.move_to(p(4.6,-.2)),
                  first.animate.shift(DOWN*1.25),
                  f3ends[1].animate.move_to(p(4.92,.35)).set_color(NEW),run_time=2.9,rate_func=linear)
        self.play(FadeOut(pol),run_time=.4)
        self.pause(1.2)
        self.step(2,"F1c pairs with F1. The strand folds back.")
        seed=hairpin_seed()
        self.play(*[FadeOut(m) for m in (template,connectors,labels,temp,f3,f3ends,outer)],
                  ReplacementTransform(first,seed),run_time=1.8)
        self.pause(2)
        self.step(3,"BIP primes from the other end.")
        bip=VGroup(domain("B2",2.3,-.95,color=PRIMER),
            domain("B1c",4.0,-1.65,color=PRIMER),
            path([(2.9,-.95),(3.15,-1),(3.1,-1.65),(3.4,-1.65)],PRIMER,smooth=True),
            caption("BIP",p(4,-2.12),19,PRIMER),
            caption("3′",p(1.45,-.95),17,PRIMER),caption("5′",p(4.87,-1.65),17,PRIMER))
        self.play(FadeIn(bip),run_time=.8)
        self.play(*[Create(DashedLine(p(xx,-.85),p(xx,-.3),color=MUTED,
                    stroke_width=1.2,dash_length=.06)) for xx in (1.9,2.3,2.7)],run_time=.6)
        # Domain names are taught before this motion; keep only the terminal
        # polarity markers while polymerase follows the folded template.
        self.play(*[m.animate.set_opacity(0) for m in seed[2][0:6]],
                  bip[0][1].animate.set_opacity(0),run_time=.35)
        reverse_copy=path([(1.7,-.95),(-2,-.95),(-3,-1.1),(-3.8,-.3),
                           (-3.85,.6),(-3,1.55),(-2,1.4),(-.6,1.4)],NEW,smooth=True)
        pol=enzyme("Bst").scale(.8).move_to(p(1.7,-1.6))
        self.play(FadeIn(pol),run_time=.3)
        motion=path([(1.7,-1.6),(-2,-1.6),(-3.6,-1.8),(-4.5,-.5),
                     (-4.5,.8),(-3,2.05),(-2,2.0),(-.6,2.0)],NEW,smooth=True)
        moving_end=reverse_copy.copy().shift(RIGHT*.22+UP*.22)
        bip[4].set_color(NEW)
        self.play(Create(reverse_copy),MoveAlongPath(pol,motion),
                  MoveAlongPath(bip[4],moving_end),run_time=2.8,rate_func=linear)
        self.play(FadeOut(pol),run_time=.3)
        self.step(3,"B3 displaces this new strand.")
        b3=domain("B3",4,-.95,color=PRIMER)
        b3names=ends(3.4,4.6,-.95,-1)
        b3names[0].move_to(p(3.0,-.62))
        self.play(FadeIn(b3),FadeIn(b3names),run_time=.9)
        displacement=arrow(p(3.4,-.95),p(-1.6,-.95),NEW)
        self.play(Create(displacement),b3names[0].animate.move_to(p(-1.95,-.62)).set_color(NEW),
                  VGroup(bip,reverse_copy).animate.shift(DOWN*.4),run_time=1.8)
        self.pause(.8)
        self.clear_stage()
        self.step(4,"Both ends fold into an open dumbbell seed.")
        dumbbell=hairpin_seed(True)
        self.play(Create(dumbbell[0]),Create(dumbbell[1]),FadeIn(dumbbell[2]),
                  FadeIn(dumbbell[3]),Create(dumbbell[4]),run_time=1.7)
        constant=tag("65 °C",MUTED).move_to(p(5.35,2.0))
        self.play(FadeIn(constant),run_time=.3)
        self.pause(2.5)
        self.step(4,"The 3′ end extends, displacing DNA ahead.")
        # The nick is visible: the molecule is never drawn as a covalent circle.
        selfprime=path([(-.25,.45),(2,.45),(2.6,.8),(3.2,.5),(3.35,0),
                        (3.2,-.5),(2.6,-.8),(2,-.45),(-2,-.45)],NEW,smooth=True)
        poly=enzyme("Bst").scale(.78).move_to(p(-.25,1.3))
        trace=selfprime.copy().shift(UP*.85)
        self.play(FadeIn(poly),run_time=.4)
        self.play(MoveAlongPath(poly,trace),ShowPassingFlash(selfprime.copy().set_stroke(SIGNAL,8),
                    time_width=.45),run_time=3,rate_func=linear)
        self.play(FadeOut(poly),run_time=.3)
        self.step(4,"Inner primers bind the exposed loops.")
        loop_primer=path([(-3.32,.05),(-3.23,-.38),(-2.88,-.68)],PRIMER,width=7,smooth=True)
        lpname=caption("FIP",p(-4.0,-.7),18,PRIMER)
        self.play(Create(loop_primer),FadeIn(lpname),run_time=.8)
        self.pause(1)
        self.step(4,"Further copying creates connected stem-loops.")
        self.play(FadeOut(dumbbell),FadeOut(loop_primer),FadeOut(lpname),run_time=.7)
        chain=VMobject(stroke_color=NEW,stroke_width=5)
        chain.start_new_path(p(-5.4,-.85))
        stems=VGroup()
        for xx in (-3.6,-.5,2.6):
            chain.add_line_to(p(xx-.4,-.85))
            chain.add_line_to(p(xx-.4,.3))
            chain.add_cubic_bezier_curve_to(p(xx-.4,1.35),p(xx+.4,1.35),p(xx+.4,.3))
            chain.add_line_to(p(xx+.4,-.85))
            for yy in np.linspace(-.65,.25,5):
                stems.add(DashedLine(p(xx-.33,yy),p(xx+.33,yy),color=MUTED,
                           stroke_width=1.2,dash_length=.06))
        chain.add_line_to(p(5.3,-.85))
        tips=VGroup(caption("5′",p(-5.72,-.85),17,NEW),
                     caption("3′",p(5.64,-.85),17,NEW))
        self.play(Create(chain),run_time=2.5,rate_func=linear)
        self.play(Create(stems),FadeIn(tips),run_time=.8)
        self.play(FadeIn(caption("target repeats",p(0,-1.65),20,NEW)),run_time=.5)
        self.play(FadeIn(caption("",p(0,-2.6),15)),run_time=.5)
        self.finish("More loops provide more sites for synthesis.",hold=3)
