"""Replication at a single fork, followed by primer processing and ligation."""
import numpy as np
from manim import *
from dna_animations.core import *


class Replication(Lesson):
    title = "DNA replication"
    subtitle = "One replication fork · every new strand grows 5′ → 3′"
    steps = ("unwind", "prime", "leading", "lagging", "replace", "join")

    def construct(self):
        seq = "TACGGTACGATC"
        x, dx = -4.8, .79
        top = Strand(seq, x=x, y=.52, step=dx, direction=-1, role=OLD, side=-1)
        bottom = Strand(complement(seq), x=x, y=-.52, step=dx, direction=1, role=OLD, side=1)
        pairs = top.pairing(bottom)
        self.step(0, "The two templates run in opposite directions")
        self.play(LaggedStart(FadeIn(top), FadeIn(bottom), Create(pairs), lag_ratio=.18), run_time=1.8)
        self.pause(2)

        # Open the left portion into a continuous Y-shaped fork. The right end
        # remains a duplex: templates never become disconnected free beads.
        fork_top, fork_bottom = top.copy(), bottom.copy()
        for rail, sign in ((fork_top,1),(fork_bottom,-1)):
            for i in range(12):
                target_y = sign * (1.45 if i < 9 else (.9 if i == 9 else .52))
                rail.units[i].shift(UP * (target_y-rail.anchor(i)[1]))
            for i, unit in enumerate(rail.units):
                j = i+1 if rail.direction == -1 else i-1
                start = rail.anchor(j) if 0 <= j < 12 else rail.anchor(i)+RIGHT*.15*rail.direction*-1
                unit[0].put_start_and_end_on(start, rail.anchor(i))
            rail.ends[0].move_to([x-.43, sign*1.45, 0])
        helicase = enzyme("helicase", 1.25).move_to([2.15,0,0])
        motion = arrow([2.1,1.86,0],[4.4,1.86,0],OLD)
        motion_label = caption("fork moves", [3.25,2.10,0],16)
        self.step(0, "Helicase separates the paired bases")
        self.play(FadeOut(pairs), Transform(top,fork_top), Transform(bottom,fork_bottom),
                  FadeIn(helicase), run_time=2)
        retained = VGroup(*[DashedLine(top.at(i)+DOWN*.18,bottom.at(i)+UP*.18,
                             color=MUTED,dash_length=.06,stroke_width=1.2) for i in (10,11)])
        self.play(Create(retained),GrowArrow(motion),FadeIn(motion_label),run_time=.8)
        self.pause(1.6)

        self.step(1, "An RNA primer supplies a free 3′ end")
        lead = Strand(complement(seq[:9]), x=x, y=.46, step=dx,
                      direction=1,role=NEW,side=1,labels=False)
        lead_primer = Strand(complement(seq[:2]).replace("T","U"),x=x,y=.46,step=dx,
                             direction=1,role=PRIMER,side=1,labels=False)
        primase = enzyme("primase",1.25).move_to([-4.35,-.12,0])
        p5 = caption("5′",[x-.38,.46,0],18,PRIMER)
        growing3 = caption("3′",[x+dx+.43,.46,0],18,NEW)
        self.play(FadeIn(primase),run_time=.7)
        self.play(LaggedStart(*[FadeIn(u,shift=DOWN*.25) for u in lead_primer.units],lag_ratio=.6),
                  FadeIn(p5),FadeIn(growing3),run_time=1.6)
        self.pause(1)
        self.play(FadeOut(primase),run_time=.5)

        self.step(2, "Continuous synthesis toward the fork")
        leading_name = caption("leading",[-4,1.95,0],20,NEW)
        pol = enzyme("DNA pol",1.13).move_to(lead.anchor(1)+DOWN*.56+LEFT*.65)
        self.play(FadeIn(pol),FadeIn(leading_name),run_time=.6)
        for i in range(2,9):
            incoming = base_tile(lead.sequence[i]).move_to(lead.at(i)+RIGHT*.3)
            self.play(FadeIn(incoming),run_time=.14)
            self.play(incoming.animate.move_to(lead.at(i)),run_time=.48)
            self.remove(incoming)
            self.play(FadeIn(lead.units[i]),
                      pol.animate.move_to(lead.anchor(i)+DOWN*.56+LEFT*.65),
                      growing3.animate.move_to(lead.anchor(i)+RIGHT*.4),run_time=.40)
        self.pause(1.4)
        self.play(FadeOut(pol),FadeOut(growing3),run_time=.5)

        self.step(3, "Each primer starts another lagging-strand fragment")
        lagging_name = caption("lagging",[-4,-2.63,0],20,NEW)
        lag = Strand(seq[:9],x=x,y=-.46,step=dx,direction=-1,role=NEW,side=-1,labels=False)
        lag_primers, fragment_caps, frag_arrows = VGroup(), VGroup(), VGroup()
        self.play(FadeIn(lagging_name),run_time=.5)
        for stop_index in (3,7):
            primer_base = Strand(seq[stop_index].replace("T","U"),
                    x=x+dx*stop_index,y=-.46,step=dx,direction=-1,
                    role=PRIMER,side=-1,labels=False)
            # A single displayed tile represents a short multi-base RNA primer.
            lag_primers.add(primer_base)
            p = enzyme("primase",1.2).move_to(lag.anchor(stop_index)+DOWN*1.55)
            self.play(FadeIn(p),run_time=.4)
            self.play(FadeIn(primer_base,shift=DOWN*.2),run_time=.7)
            self.play(FadeOut(p),run_time=.4)
            lp = enzyme("DNA pol",1.1).move_to(lag.anchor(stop_index)+DOWN*1.48)
            end5 = caption("5′",lag.anchor(stop_index)+RIGHT*.16+UP*.25,16,PRIMER)
            end3 = caption("3′",lag.anchor(stop_index)+LEFT*.16+UP*.25,16,NEW)
            fragment_caps.add(end5,end3)
            self.play(FadeIn(lp),FadeIn(end5),FadeIn(end3),run_time=.5)
            for i in range(stop_index-1,stop_index-4,-1):
                self.play(FadeIn(lag.units[i],shift=DOWN*.25),
                          lp.animate.move_to(lag.anchor(i)+DOWN*1.48),
                          end3.animate.move_to(lag.anchor(i)+LEFT*.16+UP*.25),run_time=.8)
            flow = arrow(lag.anchor(stop_index)+DOWN*1.34,
                         lag.anchor(stop_index-3)+DOWN*1.34,NEW)
            frag_arrows.add(flow)
            self.play(FadeOut(lp),GrowArrow(flow),run_time=.55)
        self.step(3, "Both strands grow 5′ → 3′")
        self.pause(2.2)

        # Zoom to an isolated maturation view so the primer replacement and
        # phosphodiester nick are large enough to see.
        self.clear_stage()
        self.step(4, "Remove RNA primers. Fill the gaps with DNA.")
        mature_template = Strand("ATGCCATG",x=-3.3,y=1.2,step=.94,role=OLD,side=-1)
        mature = Strand("TACGGTAC",x=-3.3,y=.15,step=.94,direction=-1,role=NEW,side=1,labels=True)
        old_primers = VGroup()
        for i in (3,):
            old_primers.add(Strand(mature.sequence[i].replace("T","U"),x=-3.3+i*.94,
                         y=.15,step=.94,direction=-1,role=PRIMER,side=1,labels=False))
        self.play(FadeIn(mature_template),*[FadeIn(mature.units[i]) for i in (0,1,2,4,5,6,7)],
                  FadeIn(mature.ends), FadeIn(old_primers),run_time=1.3)
        process = enzyme("primer removal",2).move_to([-1.2,-1.15,0])
        self.play(FadeIn(process),run_time=.6)
        for k,i in enumerate((3,)):
            self.play(process.animate.move_to(mature.anchor(i)+DOWN*1.4),run_time=.6)
            # Removing this 5′ primer also exposes the 5′ end of the retained
            # fragment on its LEFT. Fill comes from the neighboring 3′ end on
            # the RIGHT, so the eventual ligation nick is between sites 2/3.
            self.play(FadeOut(old_primers[k],shift=DOWN*.55),
                      FadeOut(mature.units[i-1][0]),run_time=.8)
            mature.units[i-1][0].set_opacity(0)
            self.pause(.5)
            fill = enzyme("DNA pol",1.1).move_to(mature.anchor(i)+DOWN*1.4)
            self.play(ReplacementTransform(process,fill),run_time=.5)
            # Leave a real nick on the 5′ side: filling supplies the base, while
            # ligase will make the final covalent bond to the adjacent fragment.
            self.play(FadeIn(mature.units[i],shift=DOWN*.3),run_time=.8)
            process=fill
        self.play(FadeOut(process),run_time=.6)
        self.pause(1)
        self.step(5, "Ligase seals the remaining backbone nick")
        nick_x = (mature.anchor(2)[0]+mature.anchor(3)[0])/2
        nick = DashedLine([nick_x,.4,0],[nick_x,-.35,0],color=SIGNAL,dash_length=.07)
        ligase = enzyme("ligase",1.2).move_to([nick_x,-1.1,0])
        self.play(Create(nick),FadeIn(ligase),run_time=.7)
        seal = Line(mature.anchor(2),mature.anchor(3),color=NEW,stroke_width=4)
        self.play(Create(seal),Indicate(ligase,color=SIGNAL),run_time=1.3)
        self.play(FadeOut(nick),FadeOut(ligase),run_time=.6)
        self.pause(1.2)
        self.clear_stage()

        copies = VGroup()
        for yy,old_on_top in ((1.2,True),(-1.0,False)):
            a=Strand("TACGGTAC",x=-3.3,y=yy+.35,step=.94,direction=-1,
                     role=OLD if old_on_top else NEW,side=-1)
            b=Strand("ATGCCATG",x=-3.3,y=yy-.55,step=.94,direction=1,
                     role=NEW if old_on_top else OLD,side=1)
            copies.add(VGroup(a,b,a.pairing(b)))
        self.play(FadeIn(copies,shift=UP*.1),run_time=1.2)
        self.finish("Each copy has one parental and one new strand",3.5)
