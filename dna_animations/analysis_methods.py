"""Library preparation, molecular detection, and modification sequencing lessons."""
import numpy as np
from manim import *
from dna_animations.core import (
    Lesson, Strand, label, caption, base_tile, enzyme, arrow, complement,
    BG, OLD, NEW, PRIMER, ENZYME, SIGNAL, STOP, MUTED, WHITE, DYE_COLORS,
)


class Duplex(VGroup):
    def __init__(self, seq, x=-2.1, y=0, step=.6, **kwargs):
        self.top=Strand(seq,x=x,y=y+.6,step=step,role=OLD,direction=1,side=-1)
        self.bottom=Strand(complement(seq),x=x,y=y-.6,step=step,role=OLD,direction=-1,side=1)
        self.bonds=self.top.pairing(self.bottom)
        super().__init__(self.bonds,self.top,self.bottom,**kwargs)


def bond_between(a,b):
    p,q=a.get_center(),b.get_center()
    d=(q-p)/np.linalg.norm(q-p)
    return DashedLine(p+d*.18,q-d*.18,color=MUTED,dash_length=.07,stroke_width=1)


def fluor(point,color=SIGNAL):
    return Dot(point,radius=.085,color=color)


def add_base(scene, strand, i, source, *, duration=.65):
    incoming=base_tile(strand.sequence[i]).move_to(source)
    scene.play(FadeIn(incoming),run_time=.2)
    scene.play(incoming.animate.move_to(strand.at(i)),run_time=duration)
    scene.remove(incoming)
    scene.play(Create(strand.units[i]),run_time=.25)


def cut_mark(point):
    return VGroup(Line(point+UL*.18,point+DR*.18,color=STOP,stroke_width=2),
                  Line(point+UR*.18,point+DL*.18,color=STOP,stroke_width=2))


class LibraryPreparation(Lesson):
    title="DNA library preparation"
    steps=("Fragment","Repair","Tail","Ligate","Clean")

    def construct(self):
        self.step(0,"Fragment DNA into molecules the sequencer can read")
        dna=Duplex("ATGCCGTACGAT",x=-4.4,step=.8)
        self.play(Create(dna),run_time=1.5);self.pause(1.5)
        marks=VGroup(*[cut_mark([x,0,0]) for x in [-1.6,3.2]])
        self.play(Create(marks),run_time=.6);self.pause(.8)
        pieces=[]
        self.remove(dna)
        for start,end in [(0,4),(4,10),(10,12)]:
            group=VGroup(*dna.top.units[start:end],*dna.bottom.units[start:end],*dna.bonds[start:end])
            pieces.append(group);self.add(group)
        self.play(pieces[0].animate.shift(LEFT*.55),pieces[2].animate.shift(RIGHT*.55),
                  FadeOut(marks),run_time=1)
        self.pause(1.4)
        # The selected central molecule is enlarged, retaining its sequence.
        self.play(FadeOut(pieces[0]),FadeOut(pieces[2]),pieces[1].animate.move_to([0,.2,0]),run_time=.8)
        self.pause(.7)
        self.clear_stage()
        self.step(1,"Repair a recessed 3′ end to make a blunt end")
        seq="CGTACG";x=-1.8;spacing=.72
        top=Strand(seq,x=x,y=.65,step=spacing,side=-1)
        bottom=Strand(complement(seq),x=x,y=-.65,step=spacing,side=1,direction=-1)
        original=VGroup(*bottom.units[2:])
        self.play(Create(top),Create(original),Create(top.pairing(bottom,[2,3,4,5])),run_time=1)
        ends=VGroup(caption("3′",bottom.anchor(2)+LEFT*.42,17,OLD),
                    caption("5′",bottom.anchor(5)+RIGHT*.42,17,OLD))
        repair=enzyme("repair",1.15).move_to([-2.1,-1.72,0])
        self.play(FadeIn(ends),FadeIn(repair),run_time=.5)
        for i in [1,0]:
            bottom.units[i][0].set_color(NEW);bottom.units[i][1].set_color(NEW)
            self.play(ends[0].animate.move_to(bottom.anchor(i)+LEFT*.42),run_time=.25)
            add_base(self,bottom,i,[-4.5,-1.5,0],duration=.8)
            self.play(Create(top.pairing(bottom,[i])),run_time=.25)
        self.pause(1.5)
        self.play(FadeOut(repair),FadeOut(ends),FadeOut(top.ends),run_time=.4)
        self.step(2,"Add one A to each 3′ end")
        right=x+5*spacing
        a_top=base_tile("A").move_to([right+spacing,.35,0])
        a_bottom=base_tile("A").move_to([x-spacing,-.35,0])
        links=VGroup(Line([right,.65,0],[right+spacing,.65,0],color=NEW,stroke_width=3),
                     Line([x,-.65,0],[x-spacing,-.65,0],color=NEW,stroke_width=3),
                     Line([right+spacing,.65,0],[right+spacing,.53,0],color=NEW,stroke_width=2),
                     Line([x-spacing,-.65,0],[x-spacing,-.53,0],color=NEW,stroke_width=2))
        a_top.shift(UP*1.3);a_bottom.shift(DOWN*1.3)
        self.play(FadeIn(a_top),FadeIn(a_bottom),run_time=.4)
        self.play(a_top.animate.shift(DOWN*1.3),a_bottom.animate.shift(UP*1.3),run_time=1.2)
        self.play(Create(links),run_time=.5);self.pause(1.6)
        self.step(3,"T overhangs dock the adapters; ligase seals nicks")
        lt=Strand("GCT",x=x-3*spacing,y=.65,step=spacing,role=PRIMER,side=-1,labels=False)
        lb=Strand("CG",x=x-3*spacing,y=-.65,step=spacing,role=PRIMER,side=1,direction=-1,labels=False)
        rt=Strand("GC",x=right+2*spacing,y=.65,step=spacing,role=PRIMER,side=-1,labels=False)
        rb=Strand("TCG",x=right+spacing,y=-.65,step=spacing,role=PRIMER,side=1,direction=-1,labels=False)
        left=VGroup(lt,lb).shift(LEFT*1.0)
        right_adapter=VGroup(rt,rb).shift(RIGHT*1.0)
        self.play(FadeIn(left),FadeIn(right_adapter),run_time=.6)
        self.play(left.animate.shift(RIGHT),right_adapter.animate.shift(LEFT),run_time=1.5)
        self.play(Create(bond_between(a_bottom,lt.bases[-1])),
                  Create(bond_between(a_top,rb.bases[0])),run_time=.5)
        ligase=enzyme("ligase",1.15).move_to([0,-1.9,0])
        self.play(FadeIn(ligase),run_time=.4)
        joins=VGroup(Line(lt.anchor(2),top.anchor(0),color=NEW,stroke_width=3),
                     Line(lb.anchor(1),[x-spacing,-.65,0],color=NEW,stroke_width=3),
                     Line([right+spacing,.65,0],rt.anchor(0),color=NEW,stroke_width=3),
                     Line(bottom.anchor(5),rb.anchor(0),color=NEW,stroke_width=3))
        self.play(Create(joins),run_time=1.2);self.pause(1.5)
        self.step(4,"Remove free adapters; retain the indexed library")
        index_boxes=VGroup(*[SurroundingRectangle(tile,color=SIGNAL,buff=.06,stroke_width=1.5)
                            for tile in [lt.bases[0],rt.bases[-1]]])
        self.play(FadeOut(ligase),Create(index_boxes),
                  FadeIn(caption("sample indexes",[0,1.8,0],18)),run_time=.7)
        debris=VGroup(Strand("GC",x=-5,y=-1.9,role=PRIMER,labels=False),
                      Strand("GC",x=3.8,y=-1.9,role=PRIMER,labels=False))
        self.play(FadeIn(debris),run_time=.4)
        self.play(debris.animate.shift(DOWN*.65).set_opacity(0),run_time=1.2)
        outer=VGroup(caption("5′",lt.anchor(0)+LEFT*.43,17,OLD),
                     caption("3′",rt.anchor(1)+RIGHT*.43,17,OLD),
                     caption("3′",lb.anchor(0)+LEFT*.43,17,OLD),
                     caption("5′",rb.anchor(2)+RIGHT*.43,17,OLD))
        self.play(FadeIn(outer),run_time=.4)
        self.finish("Adapters make the same DNA fragment sequenceable",hold=4)


class Tagmentation(Lesson):
    title="Tagmentation"
    steps=("Load","Cut + tag","Repair","Index","Library")

    def construct(self):
        self.step(0,"A transposase carries DNA adapter tags")
        dna=Duplex("ACGTACGTTAGC",x=-4.4,step=.8)
        self.play(Create(dna),run_time=1.5)
        complexes=VGroup()
        for x in [-1.6,2.4]:
            protein=enzyme("transposase",1.8).move_to([x,1.9,0])
            tag1=Strand("AG",x=x-.55,y=1.2,step=.45,role=PRIMER,labels=False).scale(.65)
            complexes.add(VGroup(protein,tag1))
        self.play(FadeIn(complexes),run_time=.8);self.pause(2)
        self.step(1,"Cleavage and tag transfer happen together")
        self.play(complexes.animate.shift(DOWN*.18),run_time=1.3)
        transfer_links=VGroup(*[Line(c[1].get_bottom(),[x,.6,0],color=PRIMER,
                                    stroke_width=2) for c,x in zip(complexes,[-1.6,2.4])])
        cuts=VGroup(*[cut_mark([x,0,0]) for x in [-1.6,2.4]])
        self.play(Create(cuts),Create(transfer_links),run_time=.5);self.pause(1)
        self.play(FadeOut(complexes),FadeOut(cuts),FadeOut(transfer_links),run_time=.5)
        self.remove(dna)
        pieces=[]
        for a,b in [(0,4),(4,9),(9,12)]:
            m=VGroup(*dna.top.units[a:b],*dna.bottom.units[a:b],*dna.bonds[a:b])
            pieces.append(m);self.add(m)
        self.play(pieces[0].animate.shift(LEFT*.45),pieces[2].animate.shift(RIGHT*.45),run_time=.8)
        tags=VGroup(*[Line(p+LEFT*.25,p+RIGHT*.25,color=PRIMER,stroke_width=6)
                    for p in [dna.top.anchor(4),dna.bottom.anchor(8)]])
        self.play(Create(tags),run_time=.6);self.pause(1.5)
        self.clear_stage()
        self.step(2,"Repair the short gaps beside the inserted tags")
        # Enlarged single junction: the 9-base gap is drawn explicitly.
        seq="AGCTACGTACGTA"
        top=Strand(seq,x=-4.2,y=.85,step=.65,side=-1)
        bottom=Strand(complement(seq),x=-4.2,y=-.5,step=.65,direction=-1,side=1,labels=False)
        for u in top.units[:2]:u[0].set_color(PRIMER);u[1].set_color(PRIMER)
        for u in bottom.units[:2]:u[0].set_color(PRIMER);u[1].set_color(PRIMER)
        self.play(Create(top),Create(VGroup(*bottom.units[:2],*bottom.units[11:])),run_time=1)
        gap_ends=VGroup(caption("3′",bottom.anchor(0)+LEFT*.42,17,OLD),
                        caption("5′",bottom.anchor(12)+RIGHT*.42,17,OLD),
                        caption("3′",bottom.anchor(11)+DOWN*.44,17,NEW))
        self.play(FadeIn(gap_ends),run_time=.3)
        gap=Line(bottom.anchor(2)+DOWN*.65,bottom.anchor(10)+DOWN*.65,color=MUTED,stroke_width=1)
        gap_name=caption("9-base gap",[0,-1.6,0],18)
        self.play(Create(gap),FadeIn(gap_name),run_time=.6);self.pause(1.8)
        pol=enzyme("repair",1.15).move_to([3.9,-1.95,0])
        self.play(FadeIn(pol),run_time=.4)
        for i in range(10,1,-1):
            incoming=base_tile(bottom.sequence[i]).move_to(bottom.at(i)+DOWN*.62)
            self.add(incoming)
            self.play(incoming.animate.move_to(bottom.at(i)),run_time=.4)
            self.remove(incoming);self.add(bottom.units[i])
            gap_ends[2].move_to(bottom.anchor(i)+DOWN*.44)
        self.play(Create(top.pairing(bottom)),FadeOut(pol),FadeOut(gap),FadeOut(gap_name),
                  FadeOut(gap_ends[2]),run_time=.8)
        self.pause(1.8)
        self.clear_stage()
        self.step(3,"Tailed primers add indexes during PCR")
        template=Strand("TCGATG",x=-2.1,y=.8,step=.65,direction=-1,side=-1)
        indexed=Strand("GGAGCTAC",x=-3.4,y=-.5,step=.65,role=NEW,side=1)
        for unit in indexed.units[:5]:
            unit[0].set_color(PRIMER);unit[1].set_color(PRIMER)
        primer=VGroup(*indexed.units[:5]).copy().shift(DOWN*1.25)
        self.play(Create(template),FadeIn(primer),run_time=.7)
        self.play(primer.animate.shift(UP*1.25),run_time=1)
        self.play(Create(VGroup(*[bond_between(template.bases[j],primer[j+2][2])
                                 for j in range(3)])),run_time=.4)
        self.play(FadeIn(caption("index",[-3.05,-1.27,0],17,PRIMER)),run_time=.4)
        pol=enzyme().move_to([.2,-1.65,0]);self.play(FadeIn(pol),run_time=.4)
        for i in [5,6,7]:
            add_base(self,indexed,i,[4.9,-.45,0],duration=.5)
            self.play(Create(bond_between(template.bases[i-2],indexed.bases[i])),run_time=.18)
        self.play(FadeOut(pol),FadeIn(indexed.ends),run_time=.4)
        self.pause(2)
        self.step(4,"Tagging starts the library; completion makes it usable")
        self.play(Circumscribe(VGroup(*primer[:2]),color=PRIMER,buff=.09),run_time=1)
        self.finish("Fragment + tag → repair → indexed library",hold=4)


class PacBioHiFi(Lesson):
    title="PacBio HiFi sequencing"
    steps=("SMRTbell","Read","Repeat","Align","Consensus")

    def construct(self):
        self.step(0,"Hairpin adapters close both ends of one DNA insert")
        top=Strand("TACG",x=-4.2,y=.85,step=.85,side=-1,direction=-1,labels=False)
        bottom=Strand("ATGC",x=-4.2,y=-.85,step=.85,side=1,labels=False)
        self.play(Create(top),Create(bottom),Create(top.pairing(bottom)),run_time=1.2)
        left=ArcBetweenPoints([-4.2,-.85,0],[-4.2,.85,0],angle=-PI,color=PRIMER,stroke_width=3)
        right=ArcBetweenPoints([-1.65,.85,0],[-1.65,-.85,0],angle=-PI,color=PRIMER,stroke_width=3)
        self.play(Create(left),Create(right),run_time=1.6)
        template_label=caption("SMRTbell",[-2.95,1.95,0],19)
        self.play(FadeIn(template_label),run_time=.5);self.pause(2)
        self.step(1,"Each incorporated base produces a fluorescent pulse")
        self.play(FadeOut(template_label),run_time=.3)
        pol=enzyme("pol",.8).move_to([-4.2,1.35,0])
        self.play(FadeIn(pol),run_time=.4)
        row_labels=VGroup(*[caption(f"pass {i+1}",[.5,1.55-i*.9,0],17) for i in range(3)])
        self.play(FadeIn(row_labels),run_time=.5)
        rows=[]
        pulses=VGroup()
        for turn,readseq in enumerate(["ATGC","GCAT","ATGC"]):
            if turn:
                self.step(2,"The same polymerase reads the insert again",hold=.25)
                loop=(ArcBetweenPoints([-1.65,1.38,0],[-1.65,-1.45,0],angle=-PI)
                      if turn==1 else ArcBetweenPoints([-4.2,-1.45,0],[-4.2,1.38,0],angle=-PI))
                self.play(MoveAlongPath(pol,loop),run_time=1.0)
            row=VGroup()
            for j,base in enumerate(readseq):
                target=top.at(j) if turn!=1 else bottom.at(3-j)
                pol_y=1.38 if turn!=1 else -1.45
                self.play(pol.animate.move_to([target[0],pol_y,0]),run_time=.25)
                nt=base_tile(base,.8).move_to([-5.65,2.1 if turn!=1 else -2.2,0])
                dye=fluor(nt.get_center()+UP*.26,DYE_COLORS[base])
                incoming=VGroup(nt,dye)
                self.play(FadeIn(incoming),run_time=.15)
                self.play(incoming.animate.move_to([target[0],pol_y+.42 if turn!=1 else pol_y-.42,0]),run_time=.35)
                pulse=Line([1.3+j*.8,.98-turn*.9,0],[1.3+j*.8,1.24-turn*.9,0],
                           color=DYE_COLORS[base],stroke_width=3)
                pulses.add(pulse)
                call=caption(base,[1.3+j*.8,1.55-turn*.9,0],23,DYE_COLORS[base]);row.add(call)
                self.play(Flash(incoming.get_center(),color=DYE_COLORS[base],flash_radius=.22),
                          Create(pulse),FadeIn(call),run_time=.35)
                self.play(FadeOut(incoming,shift=RIGHT*.3),run_time=.15)
            rows.append(row);self.pause(.65)
        self.step(3,"Align observations from both strand directions")
        normalized=VGroup(*[caption(b,[1.3+j*.8,.65,0],23,DYE_COLORS[b]) for j,b in enumerate("ATGC")])
        self.play(FadeOut(rows[1]),FadeOut(pulses),run_time=.35)
        self.play(FadeIn(normalized),run_time=.45)
        self.pause(2)
        self.step(4,"Combine repeated observations into one HiFi read")
        consensus=VGroup(*[base_tile(b,1.15).move_to([1.3+j*.8,-1.55,0]) for j,b in enumerate("ATGC")])
        for j in range(4):
            column=SurroundingRectangle(VGroup(rows[0][j],normalized[j],rows[2][j]),
                                       buff=.13,color=SIGNAL,stroke_width=1)
            self.play(Create(column),run_time=.18)
            self.play(FadeIn(consensus[j]),run_time=.3)
            self.play(FadeOut(column),run_time=.15)
        self.play(FadeIn(caption("consensus",[2.5,-2.25,0],18,SIGNAL)),run_time=.5)
        self.finish("Repeated reads of one molecule improve confidence",hold=4)


class SouthernBlot(Lesson):
    title="Southern blot"
    steps=("Separate","Denature","Transfer","Probe","Detect")

    def construct(self):
        self.step(0,"A gel separates DNA fragments by length")
        gel=Rectangle(width=3.2,height=3.8,stroke_color=MUTED,fill_color=OLD,
                      fill_opacity=.05).move_to([-3.2,0,0])
        well=Line([-4.1,1.5,0],[-2.3,1.5,0],color=MUTED,stroke_width=3)
        self.play(Create(gel),Create(well),run_time=.7)
        seqs=["ATG","ACGTAC","GATTACAGA"]
        fragments=VGroup(*[Duplex(s,x=0,step=.55).scale(.32).move_to([-3.2,1.4,0]) for s in seqs])
        # Individual bases are unresolved at gel scale; the later zoom exposes them.
        for molecule in fragments:
            for strand in [molecule.top,molecule.bottom]:
                strand.ends.set_opacity(0)
                for unit in strand.units:unit[2][1].set_opacity(0)
        self.play(FadeIn(fragments),run_time=.7)
        targets=[-1.4,-.2,.9]
        self.play(*[m.animate.set_y(y) for m,y in zip(fragments,targets)],run_time=3.3,rate_func=linear)
        self.play(FadeIn(caption("shorter",[-5.55,-1.4,0],16)),
                  FadeIn(caption("longer",[-5.55,.9,0],16)),run_time=.5)
        self.pause(2)
        self.step(1,"Denature the DNA so a probe can bind")
        self.play(*[FadeOut(m.bonds) for m in fragments],run_time=.6)
        self.play(*[m.bottom.animate.shift(DOWN*.13) for m in fragments],run_time=1.1)
        self.pause(1.6)
        self.step(2,"Transfer the same band pattern onto a membrane")
        membrane=Rectangle(width=3.2,height=3.8,color=MUTED,stroke_width=1.3).move_to([3,0,0])
        self.play(Create(membrane),FadeIn(caption("membrane",[3,2.13,0],18)),run_time=.7)
        guides=VGroup(*[DashedLine([-1.55,y,0],[1.34,y,0],dash_length=.1,color=MUTED,
                                   stroke_width=1) for y in targets])
        self.play(Create(guides),run_time=.6)
        self.play(*[m.animate.set_x(3) for m in fragments],run_time=2.5)
        self.pause(1.5)
        self.clear_stage()
        self.step(3,"A labeled probe pairs with its matching sequence")
        target=Strand("ACGTAC",x=-2.1,y=.8,step=.8,side=-1)
        probe=Strand("TGCATG",x=-2.1,y=-.5,step=.8,direction=-1,role=PRIMER,side=1)
        probe.ends[1].shift(DOWN*.35)
        probe.shift(DOWN*1.4)
        marker=fluor(probe.anchor(5)+RIGHT*.76)
        tether=Line(probe.anchor(5)+RIGHT*.15,marker.get_left(),color=PRIMER,stroke_width=1.5)
        self.play(Create(target),FadeIn(probe),FadeIn(marker),Create(tether),run_time=.9)
        self.play(probe.animate.shift(UP*1.4),marker.animate.shift(UP*1.4),
                  tether.animate.shift(UP*1.4),run_time=1.6)
        self.play(Create(target.pairing(probe)),run_time=.8);self.pause(2)
        self.step(4,"Wash away unbound probe; detect the retained label")
        unbound=VGroup(*[Strand("TGC",x=x,y=-1.9,step=.48,role=PRIMER,labels=False)
                        for x in [-4.4,2.7]])
        self.play(FadeIn(unbound),run_time=.4)
        self.play(unbound.animate.shift(DOWN*.7).set_opacity(0),run_time=1.2)
        self.play(Flash(marker.get_center(),color=SIGNAL,flash_radius=.4),run_time=.8)
        self.pause(1.5)
        miniature=Rectangle(width=1.5,height=2.7,color=MUTED,stroke_width=1).move_to([5.2,.1,0])
        signal=Line([4.68,.02,0],[5.72,.02,0],color=SIGNAL,stroke_width=6)
        self.play(Create(miniature),TransformFromCopy(marker,signal),run_time=1)
        self.finish("A visible band locates the fragment with the target",hold=4)


class FISH(Lesson):
    title="DNA FISH"
    steps=("Fix","Expose","Hybridize","Wash","Locate")

    def construct(self):
        self.step(0,"Keep the DNA in its original cellular location")
        slide=RoundedRectangle(width=5,height=3.5,corner_radius=.08,
                    stroke_color=MUTED,stroke_width=1).move_to([-3.2,.15,0])
        nucleus=Ellipse(width=3.7,height=2.8,stroke_color=OLD,stroke_width=1.5,
                        fill_color=OLD,fill_opacity=.025).move_to([-3.2,.15,0])
        chromatin=VGroup()
        for dx,dy in [(-.55,.32),(.5,-.38)]:
            p=VMobject(color=OLD,stroke_width=2)
            p.set_points_smoothly([[-4.25+dx,.8+dy,0],[-3.6+dx,1.05+dy,0],
                                  [-3.15+dx,.2+dy,0],[-3.6+dx,-.65+dy,0],[-2.6+dx,-.65+dy,0]])
            chromatin.add(p)
        loci=[chromatin[0].point_from_proportion(.40),chromatin[1].point_from_proportion(.62)]
        self.play(Create(slide),Create(nucleus),Create(chromatin),run_time=1.5)
        fixed_label=caption("fixed cell",[-3.2,-2.05,0],18)
        self.play(FadeIn(fixed_label),run_time=.4);self.pause(2)
        self.step(1,"Separate the DNA strands at the target site")
        target=Strand("ACGTCG",x=.65,y=.85,step=.72,side=-1)
        partner=Strand("TGCAGC",x=.65,y=-.45,step=.72,direction=-1,side=1)
        bonds=target.pairing(partner)
        zoom=DashedLine(loci[0]+RIGHT*.2,[-.05,.2,0],color=MUTED,stroke_width=1,dash_length=.08)
        self.play(Create(zoom),Create(target),Create(partner),Create(bonds),run_time=1)
        self.play(FadeOut(bonds),partner.animate.shift(DOWN*1.2).set_opacity(0),run_time=1.5)
        self.pause(2)
        self.step(2,"A fluorescent probe binds its complementary sequence")
        probe=Strand("TGCAGC",x=.65,y=-.45,step=.72,direction=-1,role=PRIMER,side=1)
        probe.ends[1].shift(DOWN*.35)
        probe.shift(DOWN*1.25)
        marker=fluor(probe.anchor(5)+RIGHT*.82)
        tether=Line(probe.anchor(5)+RIGHT*.15,marker.get_left(),color=PRIMER,stroke_width=1.5)
        self.play(FadeIn(probe),FadeIn(marker),Create(tether),run_time=.5)
        self.play(probe.animate.shift(UP*1.25),marker.animate.shift(UP*1.25),
                  tether.animate.shift(UP*1.25),run_time=1.6)
        probe_bonds=target.pairing(probe)
        self.play(Create(probe_bonds),run_time=.8)
        self.pause(4.0)
        self.step(3,"Wash away unbound probes")
        loose=VGroup(*[VGroup(Line(LEFT*.18,RIGHT*.18,color=PRIMER,stroke_width=2),
                              fluor(RIGHT*.25)).move_to(p)
                       for p in [[-4.7,-.55,0],[-2.1,.8,0],[-4.8,1.3,0]]])
        self.play(FadeIn(loose),run_time=.5)
        self.play(loose.animate.shift(DOWN*1.5).set_opacity(0),run_time=1.6)
        self.pause(1.5)
        self.step(4,"Fluorescence reveals where the target remains")
        spots=VGroup(*[fluor(p,SIGNAL) for p in loci])
        self.play(TransformFromCopy(marker,spots[0]),FadeIn(spots[1]),run_time=1)
        self.play(*[Flash(p,color=SIGNAL,flash_radius=.30) for p in loci],run_time=1)
        self.pause(3.8)
        self.play(FadeOut(VGroup(target,partner,probe,marker,tether,zoom,probe_bonds,fixed_label)),run_time=.7)
        local=VGroup(slide,nucleus,chromatin,spots)
        self.play(local.animate.move_to([0,.15,0]).scale(1.2),run_time=1.3)
        self.finish("The signal marks a DNA location inside the cell",hold=4)


class HybridizationCapture(Lesson):
    title="Hybridization capture"
    steps=("Library","Hybridize","Capture","Wash","Release")

    def construct(self):
        self.step(0,"Start with a library containing many sequences")
        targets=VGroup(*[Strand(s,x=-4.5,y=y,step=.62,side=-1)
                         for s,y in [("ACGTTAG",1.4),("GATCCGA",.0),("TTAAGGC",-1.4)]])
        self.play(LaggedStart(*[Create(t) for t in targets],lag_ratio=.2),run_time=1.4)
        self.pause(2)
        self.step(1,"A biotinylated bait selects a matching molecule")
        bait=Strand("UGCAAUC",x=-4.5,y=.1,step=.62,direction=-1,role=PRIMER,side=1)
        bait.ends[1].shift(DOWN*.35)
        bait.shift(RIGHT*5.4)
        biotin=Square(side_length=.18,color=SIGNAL,fill_color=SIGNAL,fill_opacity=1).rotate(PI/4).move_to(
            bait.anchor(6)+RIGHT*.85)
        bait_group=VGroup(bait,biotin)
        self.play(targets[1].animate.shift(DOWN*.7),targets[2].animate.shift(DOWN*.2),run_time=.8)
        self.play(FadeIn(bait_group),run_time=.7)
        self.play(bait_group.animate.shift(LEFT*5.4),run_time=1.8)
        bonds=targets[0].pairing(bait)
        tether=Line(bait.anchor(6)+RIGHT*.15,biotin.get_left(),color=SIGNAL,stroke_width=1)
        self.play(Create(bonds),Create(tether),run_time=.7)
        biotin_label=caption("biotin",[1.25,.12,0],17,SIGNAL)
        self.play(FadeIn(biotin_label),run_time=.4);self.pause(3)
        self.step(2,"Streptavidin on a magnetic bead binds biotin")
        bead=Circle(radius=.57,color=ENZYME,fill_color=ENZYME,fill_opacity=.12).move_to([3.8,.1,0])
        bead_label=caption("bead",[3.8,1.2,0],18)
        self.play(FadeIn(bead),FadeIn(bead_label),run_time=.7)
        self.play(FadeOut(biotin_label),bead.animate.move_to(biotin.get_center()+RIGHT*.61),
                  bead_label.animate.move_to(biotin.get_center()+RIGHT*.61+UP*1.1),run_time=1.5)
        self.pause(2)
        self.step(3,"Hold the captured DNA while other molecules wash away")
        magnet=VGroup(Line([5.0,-.9,0],[5.0,1.0,0],color=STOP,stroke_width=8),
                      Line([5.0,1,0],[5.7,1,0],color=STOP,stroke_width=8),
                      Line([5.0,-.9,0],[5.7,-.9,0],color=STOP,stroke_width=8))
        self.play(Create(magnet),FadeOut(bead_label),run_time=.7)
        captured=VGroup(targets[0],bait,biotin,bonds,tether,bead)
        self.play(captured.animate.shift(RIGHT*2.5),run_time=1.5)
        self.play(targets[1].animate.shift(DOWN*1.0).set_opacity(0),
                  targets[2].animate.shift(DOWN*.7).set_opacity(0),run_time=1.8)
        self.pause(2)
        self.step(4,"Release the enriched DNA; the bait stays on the bead")
        self.play(FadeOut(bonds),run_time=.6)
        self.play(targets[0].animate.shift(UP*.5+LEFT*1.0),run_time=1.5)
        self.pause(2.8)
        self.play(FadeOut(VGroup(bait,biotin,tether,bead,magnet)),
                  targets[0].animate.move_to([0,.25,0]),run_time=1)
        self.finish("Sequence the enriched targets from the original library",hold=4)


class _CytosineConversion(Lesson):
    """Shared amplification/readout geometry; the chemistry differs by lesson."""
    enzymatic=False

    def construct(self):
        self.step(0,"Follow unmodified C, 5mC, and 5hmC")
        xs=[-4.78,-.62,3.54]
        headings=VGroup(*[caption(t,[x+.62,1.9,0],21) for x,t in zip(xs,["C","5mC","5hmC"])])
        templates=VGroup(*[Strand("ACG",x=x,y=.8,step=.62,side=-1) for x in xs])
        partners=VGroup(*[Strand("TGC",x=x,y=-.5,step=.62,direction=-1,side=1) for x in xs])
        bonds=VGroup(*[a.pairing(b) for a,b in zip(templates,partners)])
        marks=VGroup(*[Dot([xs[i]+.62,1.2,0],radius=.065,color=SIGNAL) for i in [1,2]])
        self.play(FadeIn(headings),Create(templates),Create(partners),Create(bonds),FadeIn(marks),run_time=1.2)
        self.pause(2)
        self.play(FadeOut(bonds),partners.animate.shift(DOWN*.65).set_opacity(0),run_time=1.2)
        self.pause(1)
        if self.enzymatic:
            self.step(1,"TET2 and T4-BGT protect the modified cytosines")
            enzymes=VGroup(enzyme("TET2",1.25).move_to([0,-1.05,0]),
                           enzyme("T4-BGT",1.45).move_to([4.16,-1.05,0]))
            self.play(FadeIn(enzymes),run_time=.7)
            protect=VGroup(*[SurroundingRectangle(templates[i].bases[1],buff=.13,
                              color=SIGNAL,stroke_width=2) for i in [1,2]])
            self.play(Create(protect),run_time=1)
            new_heads=VGroup(caption("5caC",headings[1].get_center(),21,SIGNAL),
                            caption("g5hmC",headings[2].get_center(),21,SIGNAL))
            self.play(FadeOut(headings[1]),FadeOut(headings[2]),FadeOut(marks),run_time=.4)
            self.play(FadeIn(new_heads),run_time=.6);self.pause(2.4)
            self.play(FadeOut(enzymes),run_time=.5)
            self.step(2,"APOBEC converts only unprotected C to U")
            reagent=enzyme("APOBEC",1.55).move_to([-4.16,-1.05,0])
        else:
            self.step(1,"Bisulfite converts unmodified C to U")
            reagent=caption("bisulfite",[0,-1.05,0],21)
        self.play(FadeIn(reagent),run_time=.7)
        self.play(Circumscribe(templates[0].bases[1],color=SIGNAL,buff=.08),run_time=.7)
        u=base_tile("U").move_to(templates[0].at(1))
        self.play(Transform(templates[0].bases[1],u),run_time=.7)
        self.pause(2)
        self.play(*[Circumscribe(t.bases[1],color=SIGNAL,buff=.08) for t in templates[1:]],run_time=.8)
        self.pause(1.5)
        self.play(FadeOut(reagent),run_time=.4)
        if self.enzymatic:
            self.play(FadeOut(protect),FadeOut(new_heads),run_time=.5)
        else:
            self.play(FadeOut(marks),FadeOut(headings[1]),FadeOut(headings[2]),run_time=.5)
        self.play(FadeOut(headings[0]),run_time=.3)

        self.step(3 if self.enzymatic else 2,"A polymerase copies U as A")
        first=VGroup(*[Strand(s,x=x,y=-.5,step=.62,direction=-1,side=1,role=NEW)
                       for x,s in zip(xs,["TAC","TGC","TGC"])])
        pols=VGroup(*[enzyme("pol",.7).move_to([x+.9,-1.6,0]) for x in xs])
        for strand in first:
            strand.units[2][0].set_color(PRIMER);strand.units[2][1].set_color(PRIMER)
        self.play(*[Create(s.units[2]) for s in first],FadeIn(pols),run_time=.7)
        first_bonds=VGroup()
        for i in [1,0]:
            incoming=VGroup(*[base_tile(s.sequence[i]).move_to([x+.1,-2.3,0]) for x,s in zip(xs,first)])
            self.play(FadeIn(incoming),run_time=.25)
            self.play(*[m.animate.move_to(s.at(i)) for m,s in zip(incoming,first)],run_time=.8)
            self.remove(incoming)
            self.play(*[Create(s.units[i]) for s in first],run_time=.35)
        for t,s in zip(templates,first):first_bonds.add(t.pairing(s))
        self.play(Create(first_bonds),FadeOut(pols),run_time=.6);self.pause(1.5)
        self.step(4 if self.enzymatic else 3,"Another copying round records that A as T")
        self.play(FadeOut(templates),FadeOut(first_bonds),run_time=.7)
        for s in first:
            self.add(s.ends)
        self.play(*[s.animate.shift(UP*1.3) for s in first],run_time=.8)
        # Turn exposed bases toward the next strand without changing polarity.
        self.play(*[u[2].animate.shift(DOWN*.6) for s in first for u in s.units],
                  *[Transform(u[1],Line(u[1].get_start(),u[1].get_start()+DOWN*.12,
                                       color=NEW,stroke_width=1.3)) for s in first for u in s.units],run_time=.7)
        second=VGroup(*[Strand(s,x=x,y=-.5,step=.62,side=1,role=NEW)
                        for x,s in zip(xs,["ATG","ACG","ACG"])])
        for s in second:
            s.units[0][0].set_color(PRIMER);s.units[0][1].set_color(PRIMER)
        self.play(*[Create(s.units[0]) for s in second],run_time=.5)
        for i in [1,2]:
            incoming=VGroup(*[base_tile(s.sequence[i]).move_to([x+1.8,-1.75,0]) for x,s in zip(xs,second)])
            self.play(FadeIn(incoming),run_time=.2)
            self.play(*[m.animate.move_to(s.at(i)) for m,s in zip(incoming,second)],run_time=.7)
            self.remove(incoming);self.play(*[Create(s.units[i]) for s in second],run_time=.3)
        self.play(*[Create(a.pairing(b)) for a,b in zip(first,second)],
                  *[FadeIn(s.ends) for s in second],run_time=.6)
        outcomes=VGroup(*[caption(t,[x+.62,-1.6,0],21,SIGNAL)
                           for x,t in zip(xs,["read T","read C","read C"])])
        self.play(FadeIn(outcomes),run_time=.7);self.pause(2.8)
        self.finish("A retained C can represent 5mC or 5hmC",hold=4)


class BisulfiteSequencing(_CytosineConversion):
    title="Bisulfite sequencing"
    steps=("Cytosines","Convert","Copy","Amplify","Read")


class EnzymaticMethylSequencing(_CytosineConversion):
    title="Enzymatic methyl sequencing"
    steps=("Cytosines","Protect","Deaminate","Copy","Read")
    enzymatic=True
