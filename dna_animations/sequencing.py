"""Sequencing mechanisms, using the common teaching grammar in core.py."""
import numpy as np
from manim import *
from dna_animations.core import (
    Lesson, Strand, label, caption, tag, base_tile, enzyme, arrow, block,
    complement, BG, OLD, NEW, PRIMER, ENZYME, SIGNAL, STOP, MUTED, WHITE,
    DYE_COLORS,
)


def dye(base, pos, radius=.1):
    return Dot(pos, radius=radius, color=DYE_COLORS[base])


def small_strand(length, x, y, color=NEW):
    """A molecule at overview scale; exact sequence is deliberately omitted."""
    return VGroup(Line([x,y,0], [x+length,y,0], color=color, stroke_width=5),
                  Line([x,y,0], [x+.3,y,0], color=PRIMER, stroke_width=5))


class Sanger(Lesson):
    title = "Sanger sequencing"
    subtitle = "A terminal dye identifies each fragment's last base"
    steps = ("Prime", "Terminate", "Many lengths", "Separate", "Read")

    def construct(self):
        seq = "ATGCTACG"
        template = Strand(complement(seq), x=-4.3, y=1.2, step=.68,
                          direction=-1, role=OLD, side=-1)
        product = Strand(seq, x=-4.3, y=-.25, step=.68, role=NEW, side=1,
                         labels=False)
        for unit in product.units[:2]:
            unit[0].set_color(PRIMER)
            unit[1].set_color(PRIMER)
        primer = VGroup(*product.units[:2]).copy().shift(DOWN*1.25)
        primer_5 = caption("5′", [-4.73,-.25,0], 18, PRIMER)
        end = caption("3′–OH", [-2.91,-.62,0], 18, NEW)
        template_name = caption("Template", [-1.9,1.88,0], 16, OLD)
        primer_name = caption("primer", [-4,-1.96,0], 19, PRIMER)
        self.step(0, "A primer defines the start of the read")
        self.play(Create(template), FadeIn(template_name), FadeIn(primer),
                  FadeIn(primer_name), run_time=1.4)
        self.play(primer.animate.shift(UP*1.25), primer_name.animate.move_to([-4.2,-.96,0]),
                  FadeIn(primer_5), FadeIn(end), run_time=1.5)
        bonds = template.pairing(product, [0,1])
        self.play(Create(bonds), run_time=.6)
        pol = enzyme().move_to([-2.8,-1.52,0])
        self.play(FadeIn(pol), run_time=.5)
        self.pause(1.4)

        self.step(1, "A 3′–OH allows the next nucleotide to join")
        incoming = base_tile("G").move_to([2.7,-.9,0])
        incoming_label = caption("dNTP", [2.7,-1.43,0], 20)
        self.play(FadeIn(incoming), FadeIn(incoming_label), run_time=.6)
        self.play(incoming.animate.move_to(product.at(2)),
                  pol.animate.move_to([-2.3,-1.52,0]), run_time=1.6)
        self.remove(incoming)
        self.play(Create(product.units[2]), Create(template.pairing(product,[2])),
                  end.animate.move_to([-2.23,-.62,0]), run_time=.65)
        self.pause(1.2)
        comparison = VGroup(
            caption("dNTP   3′–OH", [2.55,1.02,0], 18, NEW),
            caption("ddNTP   3′–H", [2.55,.2,0], 18, STOP),
            caption("extends", [4.6,1.02,0], 16, OLD),
            caption("stops", [4.6,.2,0], 16, STOP))
        self.play(FadeOut(incoming_label), FadeIn(comparison), run_time=.7)
        self.pause(1.8)
        self.step(1, "A ddNTP stops extension: no 3′–OH")
        terminal = base_tile("C").move_to([2.7,-1,0])
        terminal_dye = dye("C", terminal.get_center()+UP*.42)
        terminal_group = VGroup(terminal, terminal_dye)
        self.play(FadeIn(terminal_group), run_time=.4)
        self.play(terminal_group.animate.shift(product.at(3)-terminal.get_center()),
                  pol.animate.move_to([-1.62,-1.52,0]), run_time=1.5)
        self.remove(terminal)
        stop = block().move_to(product.anchor(3)+RIGHT*.25)
        no_oh = caption("3′–H", [-1.49,-.66,0], 18, STOP)
        self.play(Create(product.units[3]), Create(template.pairing(product,[3])),
                  FadeOut(end), FadeIn(no_oh), Create(stop), run_time=.7)
        next_base = base_tile("T").move_to([.9,-.65,0])
        self.play(FadeIn(next_base), run_time=.35)
        self.play(next_base.animate.shift(LEFT*.7), run_time=.6)
        self.play(Indicate(stop, color=STOP), next_base.animate.shift(RIGHT*.7), run_time=.7)
        self.pause(1.6)

        self.clear_stage()
        self.step(2, "Different copies stop at different positions")
        ladder = VGroup()
        for i in range(6):
            y = 1.65-i*.64
            strand = Strand(seq[:3+i],x=-3.6,y=y,step=.6,role=NEW,side=-1,labels=False)
            for unit in strand.units[:2]:
                unit[0].set_color(PRIMER); unit[1].set_color(PRIMER)
            ladder.add(strand)
            self.add(VGroup(*strand.units[:2]))
        primer_rule = DashedLine([-2.65,1.92,0],[-2.65,-2.02,0],color=PRIMER,
                                 dash_length=.1,stroke_width=1)
        self.play(Create(primer_rule), FadeIn(caption("Primer",[-4.1,2.05,0],16,PRIMER)),
                  run_time=.5)
        for j in range(2,8):
            additions = [Create(ladder[i].units[j]) for i in range(6) if j<len(ladder[i].sequence)]
            self.play(*additions, run_time=.55)
            i=j-2
            terminal_marker = VGroup(dye(seq[j],ladder[i].anchor(j)+RIGHT*.23),
                                    caption(f"+{i+1}",[2.4,1.63-i*.64,0],18,MUTED))
            self.play(FadeIn(terminal_marker),run_time=.22)
        self.pause(2.0)

        self.clear_stage()
        self.step(3,"Shorter fragments reach the detector first")
        tube = RoundedRectangle(width=10.5,height=.65,corner_radius=.22,
            stroke_color=MUTED,stroke_width=2,fill_color=OLD,fill_opacity=.035).move_to([0,.95,0])
        detector = Line([3.6,.32,0],[3.6,1.6,0],color=SIGNAL,stroke_width=3)
        laser = Polygon([3.6,1.63,0],[3.3,2.03,0],[3.9,2.03,0],
                        fill_color=SIGNAL,fill_opacity=.35,stroke_width=1,stroke_color=SIGNAL)
        self.play(Create(tube),Create(detector),FadeIn(laser),
                  FadeIn(caption("−",[-5.66,.95,0],26)),
                  FadeIn(caption("+",[5.65,.95,0],26)),
                  FadeIn(caption("detector",[4.72,1.82,0],17,SIGNAL)),run_time=1)
        bands=VGroup()
        for i,base in enumerate(seq[2:]):
            band=Line([0,-.2,0],[0,.2,0],color=DYE_COLORS[base],stroke_width=5)
            band.move_to([-4.7+i*.04,.95,0]); bands.add(band)
        self.play(FadeIn(bands),run_time=.5)
        axis = VGroup(arrow([-4.8,-2.18,0],[4.95,-2.18,0],MUTED),
                      arrow([-4.8,-2.18,0],[-4.8,-.48,0],MUTED),
                      caption("time",[5.2,-2.35,0],17),
                      caption("fluorescence",[-3.88,-.35,0],17))
        self.play(Create(axis),run_time=.7)
        read = VGroup()
        previous = 0
        # Arrival times encode shorter fragments moving faster in the matrix.
        arrivals=[3.1+.75*i for i in range(6)]
        for i,base in enumerate(seq[2:]):
            t=arrivals[i]
            motions=[]
            for j in range(i,6):
                x=-4.7+8.3*t/arrivals[j]
                motions.append(bands[j].animate.set_x(x))
            self.play(*motions,run_time=1.6 if i==0 else .85,rate_func=linear)
            cx=-3.95+i*1.46
            trace=VMobject(color=DYE_COLORS[base],stroke_width=3)
            points=[np.array([cx+d,-2.12+1.13*np.exp(-((d/.17)**2)),0])
                    for d in np.linspace(-.65,.65,65)]
            trace.set_points_smoothly(points)
            call=caption(base,[cx,-.73,0],24,DYE_COLORS[base]); read.add(call)
            self.play(Flash([3.6,.95,0],color=DYE_COLORS[base],flash_radius=.35),
                      Create(trace),FadeIn(call),bands[i].animate.set_opacity(0),run_time=.6)
            previous=t
        self.step(4,"Read the dyes in order, 5′ → 3′")
        self.play(FadeIn(caption("5′",[-4.48,-.73,0],19,NEW)),
                  FadeIn(caption("3′",[4.18,-.73,0],19,NEW)),run_time=.6)
        self.finish("Read the new strand after the primer",hold=3.5)


class Illumina(Lesson):
    title = "Illumina: classic workflow"
    subtitle = "Classic bridge amplification + four-color sequencing by synthesis"
    steps = ("Adapters", "Bridge", "Cluster", "Add · image · reset", "Read")

    def construct(self):
        self.step(0,"Adapters attach DNA to the flow cell")
        surface=Line([-5.65,-1.65,0],[5.65,-1.65,0],color=MUTED,stroke_width=5)
        surface_name=caption("flow cell",[4.75,-2.0,0],18)
        primers=VGroup(*[Line([x,-1.65,0],[x,-1.12,0],color=PRIMER,stroke_width=5)
                         for x in [-4.4,-3.3,-2.2,-1.1,0,1.1,2.2,3.3,4.4]])
        library=VGroup(Line([-4.95,1.3,0],[-1.8,1.3,0],color=OLD,stroke_width=5),
                       Line([-4.95,1.3,0],[-4.45,1.3,0],color=PRIMER,stroke_width=7),
                       Line([-2.3,1.3,0],[-1.8,1.3,0],color=PRIMER,stroke_width=7))
        adapter_label=caption("adapters",[-3.4,1.95,0],20,PRIMER)
        self.play(Create(surface),FadeIn(surface_name),Create(primers),Create(library),
                  FadeIn(adapter_label),run_time=1.2)
        self.pause(1.2)
        attached=VGroup(Line([-3.58,-1.12,0],[-3.58,1.65,0],color=OLD,stroke_width=5),
                        Line([-3.58,-1.12,0],[-3.58,-.65,0],color=PRIMER,stroke_width=7),
                        Line([-3.58,1.2,0],[-3.58,1.65,0],color=PRIMER,stroke_width=7))
        self.play(Transform(library,attached),FadeOut(adapter_label),run_time=1.5)
        newcopy=Line([-3.3,-1.12,0],[-3.3,1.65,0],color=NEW,stroke_width=5)
        pol=enzyme().scale(.65).move_to([-2.6,-.8,0])
        self.play(FadeIn(pol),run_time=.4)
        self.play(Create(newcopy),pol.animate.move_to([-2.6,1.4,0]),run_time=1.8)
        self.play(library.animate.shift(LEFT*1.8).set_opacity(0),FadeOut(pol),run_time=.8)
        anchored_five=caption("5′",[-3.73,-1.36,0],16,NEW)
        free_three=caption("3′",[-2.92,1.65,0],16,NEW)
        self.play(FadeIn(anchored_five),FadeIn(free_three),run_time=.35)
        self.pause(.8)

        self.step(1,"The anchored copy bends to another primer")
        bridge=CubicBezier([-3.3,-1.12,0],[-3.3,2.3,0],[-1.1,2.3,0],[-1.1,-1.12,0],
                           color=NEW,stroke_width=5)
        self.play(Transform(newcopy,bridge),free_three.animate.move_to([-.66,-1.0,0]),run_time=2.0)
        self.pause(1.1)
        complement_bridge=CubicBezier([-1.1,-1.12,0],[-.86,2.6,0],[-3.54,2.6,0],[-3.54,-1.12,0],
                                      color=NEW,stroke_width=4)
        pol.move_to([-.45,-.65,0])
        self.play(FadeIn(pol),run_time=.3)
        self.play(Create(complement_bridge),MoveAlongPath(pol,
            CubicBezier([-.45,-.65,0],[-.45,2,0],[-4.1,2,0],[-4.1,-.65,0])),run_time=2)
        self.play(FadeOut(pol),run_time=.3)
        self.pause(1.1)
        self.step(2,"Copy and separate to build a cluster")
        left=Line([-3.3,-1.12,0],[-3.3,1.4,0],color=NEW,stroke_width=5)
        right=Line([-1.1,-1.12,0],[-1.1,1.4,0],color=NEW,stroke_width=5)
        other_ends=VGroup(caption("5′",[-.69,-1.36,0],16,NEW),
                          caption("3′",[-.69,1.4,0],16,NEW))
        self.play(Transform(newcopy,left),Transform(complement_bridge,right),
                  free_three.animate.move_to([-2.92,1.4,0]),FadeIn(other_ends),run_time=1.5)
        self.pause(.7)
        strands=VGroup(newcopy,complement_bridge)
        for x in [-4.4,-2.2,0,1.1,2.2,3.3]:
            strand=Line([x,-1.12,0],[x,1.35,0],color=NEW,
                        stroke_width=4)
            self.play(TransformFromCopy(newcopy if x<0 else complement_bridge,strand),run_time=.3)
            strands.add(strand)
        self.play(FadeIn(tag("Clonal cluster",NEW).move_to([.3,1.88,0])),run_time=.4)
        self.pause(1.6)
        self.step(2,"Keep one orientation; add a sequencing primer")
        self.play(*[FadeOut(strands[j],shift=UP*.4) for j in range(1,len(strands),2)],
                  FadeOut(other_ends),run_time=.9)
        self.pause(.8)
        self.clear_stage()

        seq="ATGCTA"
        template=Strand(complement(seq),x=-4.6,y=1.2,step=.76,direction=-1,role=OLD,side=-1)
        product=Strand(seq,x=-4.6,y=-.15,step=.76,role=NEW,side=1,labels=False)
        for u in product.units[:2]:
            u[0].set_color(PRIMER);u[1].set_color(PRIMER)
        primer=VGroup(*product.units[:2])
        self.play(Create(template),Create(primer),Create(template.pairing(product,[0,1])),
                  FadeIn(caption("One cluster, enlarged",[-2.65,1.91,0],18)),run_time=1)
        clusters=VGroup(*[VGroup(*[Dot(radius=.037,color=MUTED).move_to([x+dx,y+dy,0])
                                      for dx,dy in [(-.08,0),(.08,0),(0,.1),(0,-.1),(0,0)]])
                          for x,y in [(2.4,.95),(3.5,1.12),(4.6,.8),(2.9,.05),(4.1,-.12),(5.1,.03)]])
        cluster_panel=RoundedRectangle(width=3.85,height=2.15,corner_radius=.2,
                           stroke_color=MUTED,stroke_width=1).move_to([3.75,.6,0])
        self.play(FadeIn(clusters),Create(cluster_panel),
                  FadeIn(caption("Flow cell",[3.75,1.91,0],18)),run_time=.6)
        cycle_labels=VGroup()
        for k,t in enumerate(("Add","Image","Reset")):
            x=-3.8+k*1.35
            word=caption(t,[x,-1.65,0],17,NEW if k==0 else MUTED)
            underline=Line([x-.38,-1.92,0],[x+.38,-1.92,0],color=NEW,
                           stroke_width=1.5,stroke_opacity=1 if k==0 else 0)
            cycle_labels.add(VGroup(underline,word))
        self.play(FadeIn(cycle_labels),run_time=.4)
        def select_cycle(index, color=NEW):
            for k,m in enumerate(cycle_labels):
                tone=color if k==index else MUTED
                m[0].set_stroke(tone,opacity=1 if k==index else 0)
                m[1].set_color(tone)
        pol=enzyme().scale(.75).move_to([-3.6,-.8,0]);self.add(pol)
        read=VGroup()
        for j,base in enumerate(seq[2:]):
            self.step(3,f"Cycle {j+1}: add one complementary base",hold=.2)
            select_cycle(0)
            # Feed from the open space beside the molecule. A bottom-to-top
            # trajectory would cross the cycle labels and confuse the diagram.
            pool=VGroup(*[base_tile(b,.82).move_to([.8,.88-k*.56,0]) for k,b in enumerate("ACGT")])
            self.play(FadeIn(pool),run_time=.35)
            nt=pool["ACGT".index(base)]
            self.play(nt.animate.move_to(product.at(j+2)),
                      pol.animate.move_to(product.anchor(j+2)+DOWN*.72),run_time=.85)
            self.remove(nt)
            terminal=block().scale(.7).move_to(product.anchor(j+2)+RIGHT*.2)
            fluor=dye(base,product.at(j+2)+UP*.37,.075)
            self.play(Create(product.units[j+2]),Create(template.pairing(product,[j+2])),
                      FadeIn(terminal),FadeIn(fluor),FadeOut(pool),run_time=.4)
            self.pause(.45)
            select_cycle(1,SIGNAL)
            self.play(*[c.animate.set_color(DYE_COLORS["GCTA"[(j+i)%4]]) for i,c in enumerate(clusters)],
                      Flash(fluor.get_center(),color=DYE_COLORS[base],flash_radius=.26),run_time=.55)
            call=caption(base,[2.48+j*.74,-1.73,0],25,DYE_COLORS[base]);read.add(call)
            self.play(TransformFromCopy(fluor,call),run_time=.55)
            self.pause(.45)
            select_cycle(2)
            self.play(terminal.animate.shift(DOWN*.4).set_opacity(0),
                      fluor.animate.shift(UP*.4).set_opacity(0),
                      *[c.animate.set_color(MUTED) for c in clusters],run_time=.65)
            self.pause(.5)
        self.step(4,"Remove the dye and block; repeat")
        self.play(FadeIn(caption("5′",[1.88,-1.73,0],19,NEW)),
                  FadeIn(caption("3′",[5.3,-1.73,0],19,NEW)),
                  FadeIn(caption("Read",[3.68,-2.28,0],16,OLD)),run_time=.6)
        self.finish("One base per cycle, across many clusters",hold=3)


class Nanopore(Lesson):
    title = "Nanopore sequencing"
    subtitle = "A passing DNA molecule changes an electrical current"
    steps = ("Capture", "Motor", "Current", "Decode", "Read")

    def construct(self):
        # One coordinate system defines the entire molecular cross-section.
        # The membrane meets both pore walls exactly at their outer faces.
        cx, sense_y = -3.1, .25
        channel_half, wall_width = .33, .33
        outer_half = channel_half + wall_width
        wall_offset = channel_half + wall_width / 2
        pore_height, motor_y = 1.6, 1.86
        molecule_left, molecule_right = cx - 3.0, cx + 3.0
        pitch, tile_scale = .38, .88
        first_y = 1.22
        capture_travel = first_y - (sense_y - pitch)
        clip_low, clip_high, feather = -2.58, 2.60, .27
        sequence = "ATGCCATGACTGACGATCAT"
        travel = ValueTracker(0.)

        self.step(0, "An adapter brings DNA to the pore")
        membrane = VGroup()
        for left, right in ((molecule_left, cx-outer_half),
                            (cx+outer_half, molecule_right)):
            membrane.add(Rectangle(width=right-left, height=.48,
                stroke_color=MUTED, stroke_width=1.2,
                fill_color=OLD, fill_opacity=.12).move_to([(left+right)/2,sense_y,0]))
        pore = VGroup(*[RoundedRectangle(width=wall_width, height=pore_height,
            corner_radius=.14, stroke_color=ENZYME, stroke_width=1.5,
            fill_color=ENZYME, fill_opacity=.2).move_to([cx+sign*wall_offset,sense_y,0])
            for sign in (-1,1)])
        # A centered opening through the motor continues the pore channel.
        motor = VGroup(*[RoundedRectangle(width=.4, height=.62,
            corner_radius=.12, stroke_color=ENZYME, stroke_width=1.3,
            fill_color=ENZYME, fill_opacity=.10).move_to([cx+sign*(channel_half+.2),motor_y,0])
            for sign in (-1,1)])
        motor_name = caption("motor", [cx-1.78,motor_y,0], 18, ENZYME)
        motor_pointer = Line(motor_name.get_right()+RIGHT*.10,
                             motor.get_left()+LEFT*.10, color=ENZYME, stroke_width=1)
        pore_name = caption("nanopore", [cx-1.72,-.92,0], 18, ENZYME)
        pore_pointer = Line(pore_name.get_right()+RIGHT*.09,
                            pore[0].get_corner(DL)+LEFT*.07, color=ENZYME, stroke_width=1)
        membrane_name = caption("membrane", [cx+1.75,-.36,0], 16)
        self.play(Create(membrane), Create(pore), FadeIn(pore_name),
                  Create(pore_pointer), FadeIn(membrane_name), run_time=1)
        voltage_x = molecule_left+.12
        voltage = VGroup(caption("−",[voltage_x,1.38,0],24),
                         caption("+",[voltage_x,-1.40,0],24),
                         Arrow([voltage_x,1.05,0],[voltage_x,-1.07,0],buff=0,
                               color=SIGNAL,stroke_width=2,tip_length=.14))
        self.play(FadeIn(voltage),run_time=.65)

        # Animate only travel. Updating positions and clipping on every frame
        # prevents Manim from suspending visibility while the strand moves.
        dna = VGroup()
        for i, base in enumerate(sequence):
            y = first_y+i*pitch
            backbone = Line([cx,y-pitch/2,0],[cx,y+pitch/2,0],
                            color=OLD,stroke_width=2)
            tile = base_tile(base,tile_scale).move_to([cx,y,0])
            dna.add(VGroup(backbone,tile))
        def visibility(y):
            return float(np.clip((y-clip_low)/feather,0,1)
                         * np.clip((clip_high-y)/feather,0,1))
        def update_dna(group):
            offset = travel.get_value()
            for i, unit in enumerate(group):
                y = first_y+i*pitch-offset
                unit.move_to([cx,y,0])
                unit.set_opacity(visibility(y))
        dna.add_updater(update_dna)
        update_dna(dna)
        five = caption("5′",[cx+.98,first_y,0],16,OLD)
        def update_five(m):
            y = first_y-travel.get_value()
            # The end label sits beside the molecule; briefly hide it while
            # that position crosses the membrane instead of drawing on it.
            clear_of_membrane = float(np.clip((abs(y-sense_y)-.40)/.15,0,1))
            m.move_to([cx+.98,y,0]).set_opacity(visibility(y)*clear_of_membrane)
        five.add_updater(update_five)
        self.add(dna,five)
        self.play(FadeIn(motor),FadeIn(motor_name),Create(motor_pointer),run_time=1)
        self.pause(1.3)
        self.step(1,"The motor controls how fast DNA passes")
        self.play(travel.animate.set_value(capture_travel),run_time=2.5,rate_func=linear)
        self.play(Indicate(motor,color=ENZYME,scale_factor=1.045),run_time=.7)
        self.pause(1.2)

        window = RoundedRectangle(width=2*channel_half+.06, height=3*pitch,
            corner_radius=.07,stroke_color=SIGNAL,stroke_width=2,
            fill_color=SIGNAL,fill_opacity=.025).move_to([cx,sense_y,0])
        kmer_center = np.array([cx+1.98,1.83,0])
        sense = caption("Sensing window",kmer_center+DOWN*.54,15,OLD)
        # The connector bends through the open space beside the motor.
        bend = np.array([cx+.98,kmer_center[1]-.21,0])
        connector = VMobject(color=SIGNAL,stroke_width=1)
        connector.set_points_as_corners([window.get_corner(UR),bend,
                                         kmer_center+LEFT*.61+DOWN*.21])
        self.step(2,"Several bases shape each current measurement")
        self.play(Create(window),Create(connector),FadeIn(sense),
                  FadeOut(membrane_name),run_time=.75)
        self.pause(1.7)

        gx0,gx1,gy0,gy1 = .5,5.9,-.50,1.72
        graph_cx = (gx0+gx1)/2
        axes = VGroup(
            Arrow([gx0,gy0,0],[gx1,gy0,0],buff=0,color=MUTED,stroke_width=1.5,tip_length=.12),
            Arrow([gx0,gy0,0],[gx0,gy1,0],buff=0,color=MUTED,stroke_width=1.5,tip_length=.12),
            caption("time",[gx1-.18,gy0-.27,0],16),
            caption("Current",[graph_cx,gy1+.38,0],18,OLD))
        self.play(Create(axes),run_time=.8)
        current_connector = DashedLine([cx+outer_half+.08,sense_y,0],
                                      [gx0-.12,sense_y,0],color=SIGNAL,
                                      dash_length=.09,stroke_width=1)
        self.play(Create(current_connector),run_time=.5)
        self.pause(.8)

        def kmer_display(index):
            return VGroup(*[base_tile(b,.9) for b in sequence[index:index+3]]).arrange(
                RIGHT,buff=.07).move_to(kmer_center)
        window_read = kmer_display(0)
        self.play(FadeIn(window_read),run_time=.4)
        # Synthetic currents represent overlapping three-base windows. The
        # repeated ATG window repeats its level; different windows can share a
        # similar level, illustrating why the basecaller needs signal context.
        levels = [.64,1.03,.78,.36,.59,.64,.41,.78,.55,1.1]
        trace = VGroup()
        segment_width = (gx1-gx0-.32)/len(levels)
        trace_left = gx0+.12
        prev = None
        for i,level in enumerate(levels):
            if i:
                self.play(travel.animate.set_value(capture_travel+i*pitch),
                          run_time=.3,rate_func=linear)
                self.remove(window_read)
                window_read=kmer_display(i)
                self.add(window_read)
            x = trace_left+i*segment_width
            points = [np.array([x+d,gy0+.40+level+.025*np.sin(85*d+i),0])
                      for d in np.linspace(0,segment_width,30)]
            if prev is not None:
                points.insert(0,prev)
            segment = VMobject(color=SIGNAL,stroke_width=2.5).set_points_as_corners(points)
            self.play(Create(segment),run_time=.75,rate_func=linear)
            trace.add(segment)
            prev=points[-1]
            if i in (1,4,7):
                self.pause(.55)
        self.pause(1.5)

        self.step(3,"A model decodes the current pattern")
        decoder_y, read_y = -1.48,-2.30
        decoder = RoundedRectangle(width=2.2,height=.6,corner_radius=.10,
            stroke_color=ENZYME,stroke_width=1.2,fill_color=ENZYME,
            fill_opacity=.06).move_to([graph_cx,decoder_y,0])
        decoder_label = caption("basecalling",decoder.get_center(),19,ENZYME)
        down = Arrow([graph_cx,gy0-.13,0],decoder.get_top()+UP*.09,
                     buff=0,color=SIGNAL,stroke_width=1.3,tip_length=.10)
        self.play(Create(decoder),FadeIn(decoder_label),Create(down),run_time=.8)
        self.pause(1.3)
        read = VGroup(*[base_tile(b,.82) for b in sequence[:12]]).arrange(
            RIGHT,buff=.04).move_to([graph_cx,read_y,0])
        # Sliding signal context and the output read share the plot's center.
        highlight_width = (gx1-gx0-.25)/4
        highlight = RoundedRectangle(width=highlight_width,height=1.55,corner_radius=.05,
            stroke_color=ENZYME,stroke_width=1,fill_color=ENZYME,fill_opacity=.025).move_to(
                [trace_left+highlight_width/2,.61,0])
        self.play(Create(highlight),run_time=.4)
        for i in range(4):
            self.play(highlight.animate.set_x(trace_left+(i+.5)*highlight_width),
                      Indicate(decoder,color=ENZYME,scale_factor=1.035),
                      FadeIn(VGroup(*read[3*i:3*i+3]),shift=DOWN*.08),run_time=1)
        self.play(FadeOut(highlight),run_time=.4)
        self.step(4,"One molecule becomes one continuous read")
        self.play(FadeIn(caption("5′",read.get_left()+LEFT*.25,16,NEW)),
                  FadeIn(caption("3′",read.get_right()+RIGHT*.25,16,NEW)),run_time=.5)
        self.finish("DNA → current → estimated sequence",hold=3.5)

        if getattr(self,"_audit_enabled",False):
            # Record coordinates of the actual rendered objects so alignment
            # can be checked independently of a reduced preview image.
            import json
            from pathlib import Path
            geometry = {
                "centerline_x": cx,
                "membrane_left_join_gap": float(pore[0].get_left()[0]-membrane[0].get_right()[0]),
                "membrane_right_join_gap": float(membrane[1].get_left()[0]-pore[1].get_right()[0]),
                "pore_center_x": float(pore.get_center()[0]),
                "motor_center_x": float(motor.get_center()[0]),
                "sensing_center_x": float(window.get_center()[0]),
                "dna_max_centerline_error": max(abs(float(u[1].get_center()[0])-cx) for u in dna),
                "final_window_bases": sequence[len(levels)-1:len(levels)+2],
                "final_window_y": [float(dna[len(levels)-1+k][1].get_center()[1]) for k in range(3)],
                "expected_window_y": [sense_y+(k-1)*pitch for k in range(3)],
                "graph_center_x": graph_cx,
                "decoder_center_x": float(decoder.get_center()[0]),
                "read_center_x": float(read.get_center()[0]),
            }
            folder=Path(config.media_dir)/"geometry_audit"
            folder.mkdir(parents=True,exist_ok=True)
            (folder/"Nanopore.json").write_text(json.dumps(geometry,indent=2))
