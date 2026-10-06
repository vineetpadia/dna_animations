"""Causal, polarity-explicit lessons about three DNA synthesis strategies."""
from manim import *
import numpy as np
from dna_animations.core import (
    Lesson, Strand, label, caption, tag, base_tile, enzyme, arrow, block,
    BG, OLD, NEW, PRIMER, ENZYME, SIGNAL, STOP, MUTED, WHITE,
)


def _p(x, y):
    return np.array([x, y, 0.])


def _phosphate(name="P", color=SIGNAL):
    return VGroup(Circle(radius=.13, color=color, stroke_width=1.5,
                         fill_color=BG, fill_opacity=1), label(name, 12, color)).set_z_index(4)


def _triphosphate(at):
    marks = VGroup(*[_phosphate() for _ in range(3)]).arrange(RIGHT, buff=.09)
    marks.move_to(at)
    connectors = VGroup(*[Line(marks[i].get_right(), marks[i+1].get_left(),
        color=SIGNAL, stroke_width=2) for i in range(2)])
    return VGroup(connectors, marks)


def _bond(a, b):
    return DashedLine(a + DOWN*.19, b + UP*.19, dash_length=.06,
                      stroke_width=1.4, color=MUTED)


def _oh(at, color=NEW):
    return tag("3′–OH", color).scale(.85).move_to(at)


def _protection(at, small=False):
    if small:
        return Square(side_length=.105, color=STOP, fill_color=STOP,
                      fill_opacity=.85, stroke_width=1).move_to(at)
    return tag("DMT", STOP).scale(.8).move_to(at)


class EnzymaticSynthesis(Lesson):
    title = "Enzymatic DNA synthesis"
    subtitle = "A template chooses the base; the 3′ end grows"
    steps = ("Primer", "Match", "Join", "Extend", "Product")

    def construct(self):
        x, gap, ty, py = -4.0, 1.05, .88, -.48
        seq = "ATGCCAGT"
        template = Strand("TACGGTCA", x=x, y=ty, step=gap, direction=-1,
                          role=OLD, side=-1)
        primer = Strand(seq[:2], x=x, y=py, step=gap, role=PRIMER, side=1,
                        labels=False)
        final = Strand(seq, x=x, y=py, step=gap, role=NEW, side=1,
                       labels=False)
        primer5 = caption("5′", _p(x-.45,py), 17, PRIMER)
        terminus = _oh(_p(x+gap+.6, py-.26), PRIMER)
        tl = caption("template", _p(-4.6,1.58), 17, OLD)
        pl = caption("primer", _p(-4.0,-1.18), 17, PRIMER)
        pairs = VGroup(*[_bond(template.at(i),primer.at(i)) for i in range(2)])
        self.step(0, "A primer provides a free 3′–OH.")
        self.play(FadeIn(template), FadeIn(tl), run_time=1)
        self.play(FadeIn(primer, shift=UP*.4), FadeIn(primer5),
                  FadeIn(pl), FadeIn(terminus), Create(pairs), run_time=1.3)
        self.wait(2)
        pol = enzyme("polymerase", 1.7).move_to(_p(x+2*gap,-1.95))
        guide = DashedLine(pol.get_top(), _p(x+2*gap,-1.15),
                           color=ENZYME, dash_length=.06, stroke_width=1.5)
        self.play(FadeOut(pl), run_time=.25)
        self.play(FadeIn(pol), Create(guide), run_time=.8)
        self.wait(1)
        self.step(1, "C on the template pairs with G.")
        highlight = SurroundingRectangle(template.bases[2], buff=.13,
                                          color=SIGNAL, corner_radius=.1)
        self.play(Create(highlight), run_time=.6)
        wrong = base_tile("A").move_to(_p(x+2*gap+1.65,-1.0))
        self.play(FadeIn(wrong), run_time=.4)
        self.play(wrong.animate.move_to(_p(x+2*gap,-.05)), run_time=.9)
        cross = VGroup(Line(UP*.13+LEFT*.13,DOWN*.13+RIGHT*.13,color=STOP),
                       Line(UP*.13+RIGHT*.13,DOWN*.13+LEFT*.13,color=STOP))
        cross.next_to(wrong, RIGHT, buff=.16)
        self.play(FadeIn(cross), run_time=.25)
        self.wait(.8)
        self.play(FadeOut(wrong, shift=RIGHT*.7), FadeOut(cross), run_time=.7)
        incoming = base_tile("G").move_to(_p(x+2*gap+1.65,-.9))
        p3 = _triphosphate(incoming.get_center()+DOWN*.70)
        nt = VGroup(incoming,p3)
        nt_label = caption("dGTP", nt.get_center()+RIGHT*1.0, 17, MUTED)
        self.play(FadeIn(nt), FadeIn(nt_label), run_time=.6)
        self.play(FadeOut(terminus), FadeOut(nt_label), run_time=.3)
        self.play(nt.animate.shift(final.at(2)-incoming.get_center()), run_time=1.25)
        pair = _bond(template.at(2),final.at(2))
        self.play(Create(pair), run_time=.5)
        self.wait(1.6)
        self.step(2, "Join at 3′–OH; release pyrophosphate.")
        # Alpha phosphate stays in the new backbone. Beta and gamma leave.
        p3target = _p((x+gap+x+2*gap)/2,py)
        alpha = p3[1][0]
        leaving = VGroup(p3[1][1],p3[1][2],p3[0][1])
        self.play(alpha.animate.move_to(p3target),
                  leaving.animate.shift(RIGHT*1.65+DOWN*.38),
                  FadeOut(p3[0][0]), run_time=1.4)
        ppilabel = caption("PPi", leaving.get_center()+DOWN*.33, 18, SIGNAL)
        join = VGroup(final.units[2][0],final.units[2][1])
        self.play(Create(join), FadeIn(ppilabel), run_time=.9)
        self.wait(1.3)
        self.play(FadeOut(alpha), FadeOut(leaving), FadeOut(ppilabel),
                  FadeOut(incoming), FadeIn(final.bases[2]),
                  FadeOut(highlight), run_time=.65)
        self.add(final.units[2])
        terminus = _oh(_p(x+2*gap+.63,py-.4))
        self.play(FadeIn(terminus),run_time=.4)
        self.wait(1.4)
        self.step(3, "Match, join, then move forward.")
        growth = arrow(_p(-3.7,-2.58), _p(3.4,-2.58))
        growth_label = caption("5′ → 3′",_p(0,-2.3),20,NEW)
        for i in range(3,len(seq)):
            newx = x+i*gap
            self.play(pol.animate.move_to(_p(newx,-1.95)),
                      guide.animate.put_start_and_end_on(_p(newx,-1.625),_p(newx,-1.15)),
                      run_time=.45)
            arriving = base_tile(seq[i]).move_to(_p(newx+1.65,-.90))
            pool = _triphosphate(arriving.get_center()+DOWN*.7).scale(.7)
            free = VGroup(arriving,pool)
            self.play(FadeOut(terminus), FadeIn(free), run_time=.25)
            self.play(free.animate.shift(final.at(i)-arriving.get_center()),run_time=.7)
            retained = pool[1][0]
            released = VGroup(pool[1][1],pool[1][2],pool[0][1])
            self.play(Create(_bond(template.at(i),final.at(i))),
                      Create(VGroup(final.units[i][0],final.units[i][1])),
                      retained.animate.move_to(_p(newx-gap/2,py)),
                      FadeOut(released,shift=RIGHT*.8+DOWN*.3),FadeOut(pool[0][0]),run_time=.65)
            self.play(FadeOut(retained),run_time=.2)
            self.remove(arriving)
            self.add(final.units[i])
            terminus = _oh(_p(newx+.63,py-.4))
            self.play(FadeIn(terminus), run_time=.2)
            self.wait(.6)
        self.step(4, "The complementary strand grows 5′ → 3′.")
        self.play(FadeOut(pol),FadeOut(guide),run_time=.6)
        self.play(Create(growth),FadeIn(growth_label),run_time=.8)
        self.wait(3.8)


class PhosphoramiditeSynthesis(Lesson):
    title = "Phosphoramidite DNA synthesis"
    subtitle = "Build a chosen sequence on a solid support"
    steps = ("Deprotect", "Couple", "Cap", "Oxidize", "Repeat", "Release")

    def construct(self):
        y, dx, right = .4, 1.3, 3.0
        support = RoundedRectangle(width=.65,height=1.05,corner_radius=.15,
            color=MUTED,fill_color=MUTED,fill_opacity=.15).move_to(_p(4.65,y))
        pores=VGroup(*[Dot(_p(4.5+(i%2)*.25,y-.28+(i//2)*.28),radius=.035,
                          color=MUTED) for i in range(6)])
        support.add(pores)
        linker=Line(_p(right+.16,y),support.get_left(),color=MUTED,stroke_width=3)
        first=Strand("A",x=right,y=y,side=-1,role=NEW,labels=False)
        end3=caption("3′",_p(right+.43,y+.25),19,NEW)
        support_label=caption("solid support",_p(4.65,-.45),18,MUTED)
        dmt=_protection(_p(right-.67,y))
        dmtlink=Line(dmt.get_right(),_p(right-.15,y),color=STOP,stroke_width=2)
        protect=VGroup(_protection(first.at(0)+DOWN*.25,small=True))
        chain=VGroup(first)
        bond_protect=VGroup()
        self.step(0,"Anchor the first base at its 3′ end.")
        self.play(FadeIn(support),Create(linker),FadeIn(first),FadeIn(end3),
                  FadeIn(support_label),FadeIn(dmt),Create(dmtlink),FadeIn(protect),run_time=1.4)
        self.wait(2)
        flow=arrow(_p(3.0,1.78),_p(-3.3,1.78),NEW)
        flowtext=caption("5′ extension",_p(0,2.12),17,NEW)
        self.play(Create(flow),FadeIn(flowtext),run_time=.7)
        self.step(0,"Remove DMT to expose 5′–OH.")
        oh=tag("5′–OH",NEW).scale(.82).move_to(dmt)
        self.play(FadeOut(dmt,shift=UP*.45),FadeOut(dmtlink),run_time=.6)
        self.play(FadeIn(oh),run_time=.4)
        self.wait(1.3)
        # Two anchored molecules: the lower one will miss the coupling.
        fail_support=support.copy().scale(.52).move_to(_p(4.55,-1.6))
        failbase=Strand("A",x=3.5,y=-1.6,role=NEW,side=-1,labels=False)
        fail_link=Line(_p(3.65,-1.6),fail_support.get_left(),color=MUTED,stroke_width=2)
        fail_oh=tag("5′–OH",NEW).scale(.68).move_to(_p(2.65,-1.6))
        failgroup=VGroup(fail_support,failbase,fail_link,fail_oh)
        fail_label=caption("unreacted chain",_p(2.5,-2.26),16,MUTED)
        self.play(FadeIn(failgroup),FadeIn(fail_label),run_time=.65)
        self.step(1,"Couple a protected base to 5′–OH.")
        newx=right-dx
        unit=Strand("C",x=newx,y=y,role=NEW,side=-1,labels=False)
        monomer=VGroup(unit.copy(),_protection(_p(newx-.63,y)),
            tag("P(III)",SIGNAL).scale(.8).move_to(_p(newx+.68,y)))
        monomer.shift(LEFT*2.2+UP*.65)
        self.play(FadeIn(monomer),run_time=.7)
        self.play(FadeOut(oh),run_time=.25)
        self.play(monomer.animate.shift(RIGHT*2.2+DOWN*.65),run_time=1.4)
        bond=Line(_p(newx,y),_p(right,y),color=SIGNAL,stroke_width=4)
        pstate=monomer[2]
        self.play(Create(bond),pstate.animate.move_to(_p((newx+right)/2,y+.65)),run_time=.7)
        self.remove(monomer)
        self.add(pstate)
        dmt=_protection(_p(newx-.63,y))
        dmtlink=Line(dmt.get_right(),_p(newx-.15,y),color=STOP,stroke_width=2)
        basep=_protection(unit.at(0)+DOWN*.25,small=True)
        protect.add(basep)
        self.add(unit,dmt,dmtlink,basep)
        chain.add(unit,bond)
        self.wait(1.5)
        self.step(2,"Cap failed chains to stop further growth.")
        cap=tag("CAP",STOP).scale(.72).move_to(_p(1.25,-1.6))
        self.play(FadeIn(cap),run_time=.5)
        cap_destination=fail_oh.get_center()
        self.play(FadeOut(fail_oh),run_time=.25)
        self.play(cap.animate.move_to(cap_destination),run_time=.8)
        self.play(FadeOut(fail_label),run_time=.2)
        fail_label=caption("capped",fail_label.get_center(),17,STOP)
        self.play(FadeIn(fail_label),run_time=.3)
        self.wait(1.8)
        self.step(3,"Oxidize the new bond: P(III) → P(V).")
        self.play(bond.animate.set_color(NEW),
                  Transform(pstate,tag("P(V)",NEW).scale(.76).move_to(pstate)),run_time=1.1)
        bprot=_protection(_p((newx+right)/2,y-.15),small=True)
        bond_protect.add(bprot)
        self.play(FadeIn(bprot),run_time=.4)
        self.wait(1.8)
        self.play(FadeOut(pstate),FadeOut(fail_support),FadeOut(failbase),
                  FadeOut(fail_link),FadeOut(cap),FadeOut(fail_label),run_time=.8)
        self.step(4,"Repeat for each chosen base.")
        # C → GC → TGC; the first A always remains nearest the support.
        for number,base in enumerate("GT",start=2):
            nextx=right-number*dx
            self.play(FadeOut(dmt,shift=UP*.35),FadeOut(dmtlink),run_time=.55)
            oh=tag("5′–OH",NEW).scale(.8).move_to(_p(nextx+dx-.6,y))
            self.play(FadeIn(oh),run_time=.25)
            self.wait(.5)
            nextunit=Strand(base,x=nextx,y=y,role=NEW,side=-1,labels=False)
            nextdmt=_protection(_p(nextx-.63,y))
            mon=VGroup(nextunit,nextdmt).shift(LEFT*.7+UP*.6)
            self.play(FadeIn(mon),run_time=.4)
            self.play(FadeOut(oh),run_time=.25)
            self.play(mon.animate.shift(RIGHT*.7+DOWN*.6),run_time=.9)
            nextbond=Line(_p(nextx,y),_p(nextx+dx,y),color=SIGNAL,stroke_width=4)
            pstate=tag("P(III)",SIGNAL).scale(.7).move_to(_p(nextx+dx*.5,y+.65))
            self.play(Create(nextbond),FadeIn(pstate),run_time=.5)
            # Capping acts on failed molecules, shown explicitly in cycle one.
            self.step(4,"Deprotect, couple, cap, then oxidize.",hold=.25)
            self.play(nextbond.animate.set_color(NEW),
                Transform(pstate,tag("P(V)",NEW).scale(.7).move_to(pstate)),run_time=.65)
            bp=_protection(_p(nextx+dx*.5,y-.15),small=True)
            bond_protect.add(bp)
            self.play(FadeIn(bp),FadeOut(pstate),run_time=.3)
            self.remove(mon)
            self.add(nextunit,nextdmt)
            dmt=nextdmt
            dmtlink=Line(dmt.get_right(),_p(nextx-.15,y),color=STOP,stroke_width=2)
            self.add(dmtlink)
            chain.add(nextunit,nextbond)
            if base!="T":
                bp=_protection(nextunit.at(0)+DOWN*.25,small=True)
                protect.add(bp)
                self.add(bp)
            self.wait(.6)
        self.step(5,"Remove protection and release the strand.")
        scissors=VGroup(Line(_p(3.75,y-.25),_p(4.05,y+.25),color=SIGNAL,stroke_width=3),
                        Line(_p(3.75,y+.25),_p(4.05,y-.25),color=SIGNAL,stroke_width=3))
        self.play(FadeOut(dmt,shift=UP*.5),FadeOut(dmtlink),
                  *[FadeOut(m,shift=DOWN*.35) for m in protect],
                  *[FadeOut(m,shift=DOWN*.35) for m in bond_protect],
                  FadeIn(scissors),run_time=1.2)
        self.wait(.7)
        self.play(FadeOut(linker),FadeOut(scissors),FadeOut(end3),
                  FadeOut(support),FadeOut(support_label),FadeOut(flow),FadeOut(flowtext),run_time=.8)
        product=Strand("TGCA",x=-1.95,y=.4,step=dx,role=NEW,side=-1)
        self.play(ReplacementTransform(chain,product),run_time=1.1)
        self.finish("The single strand is ready for purification.",hold=3.5)


class TemplateIndependentSynthesis(Lesson):
    title = "Template-independent DNA synthesis"
    subtitle = "Engineered TdT + reversible 3′-phosphate blocking"
    steps = ("Choose", "Add one", "Wash", "Unblock", "Repeat")

    def construct(self):
        x,gap,y=-4.2,1.12,-.15
        initiator=Strand("AT",x=x,y=y,step=gap,role=PRIMER,side=1,labels=False)
        five=caption("5′",_p(x-.45,y),20,PRIMER)
        whole=Strand("ATGCAT",x=x,y=y,step=gap,role=NEW,side=1,labels=False)
        oh=_oh(_p(x+gap+.62,y-.25),PRIMER)
        note=caption("initiator",_p(-3.7,-.85),20,PRIMER)
        program=VGroup(*[base_tile(b) for b in "GCAT"]).arrange(RIGHT,buff=.34).move_to(_p(.7,1.65))
        program_label=caption("program",_p(-1.6,1.65),17,MUTED)
        self.step(0,"Choose a base. No template is needed.")
        self.play(FadeIn(initiator),FadeIn(five),FadeIn(oh),FadeIn(note),
                  FadeIn(program),FadeIn(program_label),run_time=1.2)
        self.wait(2.1)
        pol=enzyme("engineered TdT",2.0).move_to(_p(-1.96,-1.95))
        self.play(FadeOut(note),run_time=.25)
        self.play(FadeIn(pol),run_time=.6)
        self.wait(.7)
        selector=SurroundingRectangle(program[0],color=SIGNAL,buff=.13,corner_radius=.1)
        self.play(Create(selector),run_time=.5)
        for j,base in enumerate("GCAT"):
            i=j+2
            newx=x+i*gap
            if j:
                self.play(Transform(selector,SurroundingRectangle(program[j],color=SIGNAL,buff=.13,corner_radius=.1)),
                    FadeIn(pol.move_to(_p(newx,-1.95))),run_time=.45)
            self.step(1,"Add one blocked nucleotide.",hold=.25)
            incoming=base_tile(base).move_to(_p(newx+1.65,-.85))
            blockmark=tag("3′–P",STOP).scale(.75).next_to(incoming,RIGHT,buff=.1)
            phosphate=_triphosphate(incoming.get_center()+DOWN*.70).scale(.7)
            nt=VGroup(incoming,blockmark,phosphate)
            self.play(FadeIn(nt),run_time=.45)
            self.play(FadeOut(oh),run_time=.25)
            self.play(nt.animate.shift(whole.at(i)-incoming.get_center()),run_time=1.0 if j==0 else .7)
            retained = phosphate[1][0]
            released = VGroup(phosphate[1][1],phosphate[1][2],phosphate[0][1])
            self.play(Create(VGroup(whole.units[i][0],whole.units[i][1])),
                retained.animate.move_to(_p(newx-gap/2,y)),
                FadeOut(released,shift=DOWN*.4+RIGHT*.9),FadeOut(phosphate[0][0]),run_time=.7)
            self.play(FadeOut(retained),run_time=.2)
            self.remove(incoming)
            self.add(whole.units[i])
            self.play(blockmark.animate.move_to(_p(newx+.63,y-.15)),run_time=.4)
            self.wait(1 if j==0 else .4)
            if j==0:
                self.step(1,"The 3′ phosphate stops further extension.",hold=.25)
                extra=base_tile(base).move_to(_p(newx+2.0,y+.28))
                self.play(FadeIn(extra),run_time=.3)
                self.play(extra.animate.shift(LEFT*.9),run_time=.6)
                self.play(Circumscribe(blockmark,color=STOP,buff=.10),run_time=.7)
                self.play(extra.animate.shift(RIGHT*.55),run_time=.45)
                self.wait(.8)
            else:
                extra=base_tile(base).move_to(_p(newx+1.2,y+1.0))
                self.add(extra)
            self.step(2,"Wash out unused nucleotide and TdT.",hold=.25)
            washes=VGroup(*[Line(_p(-4.8,-.6-k*.2),_p(-3.6,-.6-k*.2),
                                  color=OLD,stroke_opacity=.5,stroke_width=2) for k in range(3)])
            self.play(FadeIn(washes),run_time=.2)
            self.play(washes.animate.shift(RIGHT*9),FadeOut(extra,shift=RIGHT*1.1),
                      FadeOut(pol,shift=DOWN*.35),run_time=1.0 if j==0 else .7)
            self.remove(washes)
            self.step(3,"Phosphatase restores the 3′–OH.",hold=.25)
            phos=enzyme("phosphatase",1.9).move_to(_p(newx+.6,-1.75))
            self.play(FadeIn(phos),run_time=.4)
            oh=_oh(_p(newx+.63,y-.15))
            self.play(FadeOut(blockmark,shift=DOWN*.45),run_time=.5)
            self.play(FadeIn(oh),run_time=.3)
            self.wait(1 if j==0 else .35)
            self.play(FadeOut(phos,shift=RIGHT*.7),run_time=.4)
            if j<3:
                self.step(4,"Wash, then choose the next base.",hold=.5)
        self.play(FadeOut(selector),run_time=.5)
        growth=arrow(_p(-4.0,-2.2),_p(2.0,-2.2))
        growth_label=caption("5′ → 3′",_p(-1,-1.88),20,NEW)
        self.play(Create(growth),FadeIn(growth_label),run_time=.7)
        self.finish("Build the chosen sequence, one base per cycle.",hold=3)
