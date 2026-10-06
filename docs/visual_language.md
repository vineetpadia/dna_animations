# A common visual language

All lessons use a quiet, instrument-like design: warm white paper, charcoal
type, fine lines, generous spacing and restrained functional accents. Use
Nimbus Sans, a neutral Helvetica-like typeface available in this environment.
One left-aligned title and a small chapter counter anchor the frame. Show one
short action caption below the diagram. Do not add a subtitle, persistent
legend, progress-label row, decorative badges or repeated explanatory prose.
Full notes belong outside the frame. Keep the main molecular action between
y = −2.65 and +2.25; reserve y = −3.22 for the single caption and y = +3.35
for the title. A continuous strand entering a transport channel may extend
to y = +2.60, fading at that boundary before reaching the title lane.

## Color and shape

| Channel | Meaning |
| --- | --- |
| Fine gray backbone | Existing DNA or RNA template |
| Heavier charcoal backbone | Newly synthesized DNA |
| Muted copper backbone | Primer; preserve it after extension |
| Pale gray enclosure | Enzyme, motor or molecular machine |
| Terracotta stop mark | Chemical block or termination |
| Muted sage | Detection or a feature under discussion |
| Green nucleotide | A — `#26745B` |
| Amber nucleotide | T/U — `#B46335` |
| Blue nucleotide | C — `#2E72B8` |
| Violet nucleotide | G — `#8756AA` |
| Matching signal colors | Sanger/Illumina measured fluorescence identity |

Backbone tone and weight express a strand's role. Nucleotide tiles use a pale
tint, a colored outline and a matching letter. A base keeps its color when it
moves between a free reagent, a polymer, a readout and a signal. These are
illustrative identity colors, not calibrated instrument dye spectra. Letters
remain visible so identifying a base never requires color discrimination.
Every strand carries explicit polarity or an adjacent unambiguous directional
cue. RNA uses U. Drawing all bases as lettered tiles is a schematic choice;
these are not depictions of atomic structures.

## Motion

1. Incoming nucleotides move to the correct site before incorporation.
2. New backbone links appear as extension happens. A primer never silently
   changes identity; chemical removal is an explicit separate step.
3. Hybridized bases occupy matching positions on antiparallel strands.
4. DNA polymerase extends the free 3′ end. Conventional phosphoramidite
   synthesis has its 3′ end anchored and grows at the 5′ end.
5. Separate strand movement, bond breaking, incorporation and detection into
   visually readable beats. Hold finished states long enough to inspect them.
6. Use a genuine example of a mechanism and state its scope. Classic bridge
   amplification and four-color SBS are one Illumina example. TdT with 3′
   reversible blocking is one controlled enzymatic synthesis example.
7. Build membrane joins, pore walls, the motor opening and the transported
   strand from a shared centerline. Update strand clipping during motion,
   keeping endpoint labels clear of the membrane.

## Review before export

Review the rendered frames at each chapter and during each transformation.
Confirm sequence complementarity, end labels, direction of growth, preserved
primer segments, molecular connections, and the source of any signal. Check
that no text or enzyme covers the essential action. Check the GIF after
conversion; keep an MP4 at lesson resolution for pause/scrub/projector use.

Give endpoint labels, enzyme labels and axes their own lanes, away from base
letters and moving reagents. Remove a label once it has served its purpose.
Shorten prose rather than shrinking the font. Use `BIO_LAYOUT_AUDIT=1` when
rendering to record text intersections during motion in the media directory's
`layout_audit/` folder. Review flagged timestamps visually: a morph can briefly
produce duplicate text bounds, and a clean audit cannot detect every possible
text/line collision. Both the audit and frame review are required.

Source notes describe the processes and omitted details. They do not turn
short schematic sequences into laboratory protocols or quantitative data.
