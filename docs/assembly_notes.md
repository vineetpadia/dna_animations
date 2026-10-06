# DNA assembly, mutagenesis and error filtering

These lessons preserve individual nucleotide objects across cutting, strand
exchange, extension and bending. Base letters identify sequence; the backbone
marks existing DNA, new DNA and retained primers. Sequences, distances, enzyme
sizes and times are schematic. None of the short examples is a working primer,
functional gene, plasmid design or experimental protocol.

## RestrictionLigation

EcoRI recognizes GAATTC and cuts G/AATTC opposite CTTAA/G, leaving complementary
5′ AATT overhangs. The animation explicitly separates the two backbone cuts,
base-pair annealing and ligase-mediated sealing of each 3′ hydroxyl / 5′ phosphate
junction. The original two pieces are rejoined to make the distinction clear.
Ligase cofactors and adenylation intermediates are omitted.

Sources: [NEB EcoRI recognition and cleavage](https://www.neb.com/en-de/products/r0101-ecori)
and [Addgene DNA ligation](https://www.addgene.org/protocols/dna-ligation/).

## PlasmidCloning

A circular duplex is opened, an insert approaches, and the same nucleotide
objects bend into the recombinant circle. Four backbone nicks are sealed, one
on each strand at each vector–insert junction. Uptake by a competent bacterium,
selection, clonal growth and sequence verification follow. The compatible ends
are drawn blunt here; the separate restriction lesson explains cohesive ends.

The 14 displayed base pairs stand for a complete plasmid that includes an origin
and selection marker, neither of which can be represented by this toy sequence.
Cell entry, replication and division are compressed. A selected colony may
contain an empty or otherwise incorrect vector; resistance is not insert
verification. Both junctions and the insert need checking. The curved-to-linear
movement changes the drawing geometry, not DNA sequence or chemical bonds.

Sources: [Addgene PCR cloning workflow](https://www.addgene.org/protocols/pcr-cloning/)
and [Addgene plasmid verification](https://help.addgene.org/hc/en-us/articles/205432629-How-can-I-verify-the-plasmids-from-my-Addgene-kit).

## GibsonAssembly

Two designed overlaps are exposed by 5′ exonuclease resection. The complementary
3′ single-stranded portions anneal; polymerase fills the remaining gaps; ligase
seals the nicks. Resection is deliberately drawn beyond the four-base overlap so
the polymerase's gap-filling role is visible. Two one-base gaps are illustrative,
not a claim about uniform resection length or a practical overlap design. The
single reaction is separated into readable chronological beats.

Sources: [Gibson et al. 2009, Nature Methods](https://pubmed.ncbi.nlm.nih.gov/19363495/),
DOI 10.1038/nmeth.1318; [NEB Gibson Assembly mechanism](https://www.neb.com/en/protocols/gibson-assembly-protocol-e5510).

## GoldenGateAssembly

BsaI recognizes GGTCTC and cuts outside that site, leaving a designed four-base
5′ overhang. The retained AGGT end pairs with a compatible neighboring fragment;
ligase seals both backbone nicks. The recognition-bearing piece is discarded,
so this assembled junction is no longer a BsaI substrate. The final product
accumulates through repeated digestion/ligation cycles.

Only one junction and one recognition-site orientation are enlarged. A complete
multi-part assembly requires correctly oriented sites and mutually compatible
designed ends throughout; internal unwanted sites and misligation are omitted.
No claim is made that every overhang performs equally well.

Sources: [Engler, Kandzia and Marillonnet 2008](https://pubmed.ncbi.nlm.nih.gov/18985154/),
DOI 10.1371/journal.pone.0003647; [NEB Golden Gate Assembly](https://www.neb.com/en-us/applications/cloning-and-synthetic-biology/dna-assembly-and-cloning/golden-gate-assembly).

## SiteDirectedMutagenesis

This is the primer-encoded substitution principle shown on a **linear PCR
target**, not a depiction of whole-plasmid QuikChange or a Q5/KLD workflow. An
internal primer mismatch introduces T→C in the displayed lower strand. Its 3′
terminal region remains matched so extension can proceed. The primer is retained
in the product; copying that strand in a later cycle establishes C–G in the
duplex. The original mismatched template is not chemically edited in place.

The two-strand drawing compresses denaturation, reverse-primer annealing and
extension into one subsequent cycle. Full amplicon amplification, primer design,
proofreading effects, template removal and cloning are outside this example.
Different named mutagenesis methods need their own downstream steps; no DpnI,
kinase or ligase treatment is implied here.

Sources: [Ho et al. 1989, primer-directed mutagenesis](https://pubmed.ncbi.nlm.nih.gov/2744487/),
DOI 10.1016/0378-1119(89)90358-2; [NEB Q5 mutagenic-primer overview](https://www.neb.com/en-us/tools-and-resources/video-library/overview-of-the-q5-site-directed-mutagenesis-kit)
supports the primer-encoded substitution concept, not the simplified linear
workflow's equivalence to that commercial method.

## OverlapExtensionPCR

Two PCR products have a designed terminal overlap. After denaturation, the
matching 3′ regions anneal and serve as primers for each other. Polymerase
extension makes a continuous assembled duplex. An explicit outer-primer PCR
round then produces two duplexes; original primer segments retain their copper
backbone identity. No ligase is needed to create this joining sequence.

Only one productive pair of strands and one amplification round are followed.
The short overlap and primers are readable stand-ins, not experimental lengths.
Unproductive reannealing and incomplete products are omitted.

Source: [Horton et al. 1989, gene splicing by overlap extension](https://pubmed.ncbi.nlm.nih.gov/2744488/),
DOI 10.1016/0378-1119(89)90359-4.

## MutSErrorCorrection

The class name groups this lesson with error-reduction methods; the visible
title says **MutS error filtering**. Strands from sequence variants reassort,
exposing mismatches in heteroduplexes. Immobilized MutS retains mismatch-bearing
molecules; unbound DNA is enriched for matched duplexes. MutS recognizes and
captures substrates here: it does not replace bases or execute cellular mismatch
repair. The scene makes that distinction in its final caption.

The chosen C–A and T–G mismatches illustrate recognition, not equal capture
efficiency. Binding depends on mismatch and sequence context. Capture can be
incomplete; erroneous homoduplexes can escape, and matched sequence is not proof
of the intended sequence. Three molecules are a teaching sample, not a measured
yield. Fragmentation/reassembly in combined consensus shuffling is a separate
lesson, not an additional unseen action by MutS.

Source: [Binkowski et al. 2005, Correcting errors in synthetic DNA through consensus shuffling](https://pubmed.ncbi.nlm.nih.gov/15800206/),
[open full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC1072806/),
DOI 10.1093/nar/gni053.

## DNAShuffling

Related parental sequences are fragmented, denatured and reannealed through
homologous regions. Overlapping fragments prime extension; subsequent outer
PCR amplifies a chimera containing variants from different parents. The example
retains the left C variant from parent 1 and right A variant from parent 2:
ATGCCGTATAGA. Actual nucleotide identities survive the fragmentation and
annealing transitions, and newly copied backbone appears during extension.

DNase I fragmentation is represented by two selected double-stranded boundaries
from a diverse fragment pool; this does not mean DNase I makes synchronized blunt
cuts or always produces these fragment lengths. One productive reassembly path
stands for many cycles and possible chimeras. DNA shuffling recombines homologous
variants; it does not itself identify a correct consensus or remove errors.

Sources: [Stemmer 1994, PNAS](https://pmc.ncbi.nlm.nih.gov/articles/PMC45099/),
DOI 10.1073/pnas.91.22.10747; [Stemmer 1994, Nature](https://www.nature.com/articles/370389a0),
DOI 10.1038/370389a0.

## Visual verification

Render with `BIO_LAYOUT_AUDIT=1` at 1280×720, 30 fps. Review the text-intersection
JSON reports and contact sheets, then inspect enlarged frames at cuts, gap fills,
fragment reassortment, ligation and circular-DNA bending. A clean text audit is
not proof of correct geometry or biology. The plasmid uses an explicit curvature
interpolation because ordinary point interpolation can carry nucleotide labels
through one another. Stage elements remain clear of the title and caption lanes.

Final review (2026-10-05): all eight 720p renders have empty text-intersection
reports in `media/expansion/assembly/layout_audit/`. Contact sheets cover every
chapter; additional full-resolution frames cover cuts, gap filling, primer
extension, plasmid bending and the complete MutS strand-exchange route. The
MutS exchange uses an open side lane after frame review found molecular crossings
that text-only intersection checks had missed. GIF samples were also inspected
after export. Canonical MP4s are in `media/videos/scenes/720p30/`, GIFs in
`previews/v5/`, and the reviewed contact sheets in `previews/review-v5/`.
