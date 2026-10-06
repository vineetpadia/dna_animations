# Analysis and preparation methods: scientific notes

All eight lessons use short schematic molecules, enlarged bases, compressed time, and illustrative signal colors. They teach mechanisms rather than laboratory operating instructions. Backbone continuity, primer retention, antiparallel pairing, and 3′ extension follow the shared visual contract. The diagrams omit molecular scale and atomic geometry.

## LibraryPreparation — ligation library preparation

The lesson follows fragmentation, repair of a recessed 3′ end, addition of A overhangs, docking of complementary T-overhang adapters, ligase sealing, and removal of free adapters. The enlarged repair example uses the selected fragment's sequence but exposes a schematic recessed end. Adapter sequences and indexes are illustrative. This is one ligation-based, preindexed-adapter example, not every commercial workflow. End phosphorylation, cleanup chemistry, size selection, amplification, and quality control are omitted. Copper denotes the supplied adapter/primer oligonucleotides; they remain part of the library.

Sources checked 2026-10-05:

- [NEB: DNA library preparation protocol](https://www.neb.com/en/protocols/2012/09/27/protocol-for-dna-e7350), for end repair, A-tailing, and adapter ligation.
- [NEB: A-tailing](https://www.neb.com/en-us/applications/cloning-and-synthetic-biology/dna-end-modification/a-tailing), for non-templated 3′ A addition and complementary T-overhang docking.

## Tagmentation

A loaded transposase cuts DNA and transfers adapter tags. The overview compresses the staggered cleavage into two visible fragmentation events. A separate enlarged junction explicitly shows a nine-base gap and repair from the available 3′ end. A tailed PCR primer retains its unpaired index-bearing 5′ segment while its paired 3′ segment extends. This is an illustrative Nextera-style workflow; tags are not presented as complete P5/P7 adapters immediately after tagmentation. Only one indexed primer and one junction are enlarged. The other end, reverse primer, and repeated PCR cycles are omitted. The detailed inserted oligonucleotide lengths are abbreviated.

Sources:

- [Illumina: Tagmentation](https://www.illumina.com/techniques/sequencing/ngs-library-prep/tagmentation.html).
- [Illumina: Transposome tags and subsequent adapter completion](https://knowledge.illumina.com/library-preparation/dna-library-prep/library-preparation-dna-library-prep-faq-list/000005831).
- [Illumina: DNA Prep reference guide](https://www.illumina.com/content/dam/illumina-support/documents/documentation/chemistry_documentation/illumina_prep/illumina-dna-prep-reference-guide-1000000025416-10.pdf).
- [Feng et al.: Next-generation sequencing library construction on a surface](https://pmc.ncbi.nlm.nih.gov/articles/PMC5975494/), for polymerase filling of the nine-base gap left by Tn5.

## PacBioHiFi

Hairpin adapters connect both ends of a double-stranded insert into one continuous SMRTbell template. The animation follows three insert traversals: forward, reverse, then forward. Fluorescence during nucleotide incorporation produces the recorded base identities. Reverse-direction observations are reverse-complemented for alignment before consensus is formed. The example uses ideal observations to establish the process; actual consensus uses quality information and probabilistic methods, rather than a guarantee of accuracy from three identical strings.

The moving polymerase is a coordinate-frame simplification showing movement relative to the DNA. Real SMRT sequencing observes an immobilized polymerase in a zero-mode waveguide. Well optics, adapter base calls, long growing products, pulse kinetics, and native modification calling are omitted. Dyes are phosphate-linked and released with incorporation; they do not accumulate on the finished strand.

Sources:

- [PacBio: How HiFi sequencing works](https://www.pacb.com/technology/hifi-sequencing/how-it-works/).
- [PacBio: SMRTbell library preparation](https://www.pacb.com/technology/library-prep/).
- [PacBio: Circular consensus from both insert strands](https://www.pacb.com/products-and-services/analytical-software/targeted-sequencing/).
- [PacBio: Phospholinked nucleotides](https://investor.pacificbiosciences.com/static-files/be2df757-adbf-437c-a896-0acff94736ce).

## SouthernBlot

The lesson begins with already-fragmented DNA. Shorter molecules migrate farther through the gel. Denaturation makes single-stranded DNA available for hybridization. Transfer preserves the separated band positions; the side-by-side gel and membrane are a schematic projection of that transfer. An enlarged target pairs with a complementary labeled probe. Washing removes unbound probe, leaving a detectable signal at the corresponding band. A band represents many molecules. Nucleotide letters are unresolved in the gel overview and become readable in the molecular enlargement.

Restriction digestion, transfer apparatus, immobilization chemistry, stringency control, and the choice of fluorescence, radioactivity, or enzyme-mediated detection are outside this lesson.

Source: [Thermo Fisher: Southern blot workflow](https://www.thermofisher.com/br/en/home/life-science/dna-rna-purification-analysis/nucleic-acid-gel-electrophoresis/southern-blotting.html).

## FISH — DNA fluorescence in situ hybridization

A fixed-cell context is maintained while one DNA locus is enlarged. Strand separation exposes the sequence; a fluorescent probe anneals to the complementary strand. Unbound probes wash away and retained fluorescence identifies the locus in the cell. Two spots are an illustrative two-locus example, not a general diagnostic rule or a complete chromosome count. The lower denatured strand is hidden in the enlarged view for legibility; it is not chemically destroyed.

Fixation, permeabilization, probe length, chromatin packing, microscope optics, and quantitative interpretation are omitted. This lesson concerns DNA FISH, not RNA FISH.

Sources:

- [NHGRI: FISH fact sheet](https://www.genome.gov/about-genomics/fact-sheets/Fluorescence-In-Situ-Hybridization).
- [NCI: Fluorescence in situ hybridization to detect DNA sequences](https://ccr.cancer.gov/sites/default/files/dna_fish.508.pdf).

## HybridizationCapture

A single-stranded DNA library is exposed to a complementary biotinylated RNA bait. Streptavidin on a magnetic bead binds the biotin, allowing target–bait complexes to be retained while unbound library molecules wash away. Separating the duplex releases enriched target DNA while the bait remains associated with the bead. The lesson uses RNA baits with U; commercial capture can also use DNA baits. The starting library is already prepared and denatured. Adapter blocking, bait tiling, enrichment bias, amplification, and exact release chemistry are omitted.

Sources:

- [Agilent: SureSelect enrichment libraries](https://earray.chem.agilent.com/earray/helppages/overview_of_sureselect_enrichment_libraries.htm).
- [Agilent: SureSelect capture workflow](https://www.agilent.com/cs/library/brochures/GeneRegulationBrochure%204.0%20%281pager%295991-7574EN.pdf).

## BisulfiteSequencing

Three matched sequence contexts compare unmodified C, 5mC, and 5hmC. Bisulfite treatment converts unmodified C to U. The scene then shows actual complementary copying: U templates A, and A templates T in the next copying round. Sites originating as 5mC or 5hmC are subsequently represented as C. This is a comparison with the original genomic orientation, not direct chemical replacement of U by T.

Conventional bisulfite sequencing does not distinguish 5mC from 5hmC. The 5hmC bisulfite adduct is not drawn structurally; conversion intermediates, DNA degradation, incomplete-conversion controls, library preparation, and mapping are omitted. The three bases do not imply equal population abundance.

Sources:

- [Zymo Research: Bisulfite conversion](https://www.zymoresearch.com/products/ez-dna-methylation-kit).
- [Huang et al.: Specificity of profiling techniques toward 5mC and 5hmC](https://pmc.ncbi.nlm.nih.gov/articles/PMC2887978/).

## EnzymaticMethylSequencing

The protection step comes first: TET2 oxidizes 5mC toward protected 5caC, while T4-BGT glucosylates 5hmC. APOBEC then deaminates unprotected C to U. The same complementary copying sequence explains the eventual T call at unmodified sites and C calls at protected sites. The boxes around modified bases are functional protection symbols, not molecular cages.

This is the NEB EM-seq principle, not a generic name for every enzymatic methylation assay. Conventional EM-seq groups 5mC and 5hmC in its retained-C readout. Oxidation intermediates, parallel routes of 5hmC protection, reaction conditions, controls, and modification-specific alternatives are omitted.

Sources:

- [NEB: Enzymatic methyl-seq conversion module](https://www.neb.com/en/products/e8020-nebnext-enzymatic-methyl-seq-v2-conversion-module).
- [NEB: Enzymatic methyl-seq workflow](https://www.neb.com/en/tools-and-resources/video-library/nebnext-enzymatic-methyl-seq-workflow).

## Review record

Final lessons were rendered at 1280 × 720 and 30 fps with `BIO_LAYOUT_AUDIT=1`. All eight final audit files contain zero sampled text intersections. Twelve-frame contact sheets were reviewed for each lesson, followed by full-resolution checks of molecular transitions, primer junctions, probe attachment, modification conversion, and readout. The audit is a sampled text check; visual inspection also caught moving-base collisions and attachment geometry that it cannot detect.

| Scene | Duration |
| --- | ---: |
| LibraryPreparation | 36.8 s |
| Tagmentation | 40.6 s |
| PacBioHiFi | 41.7 s |
| SouthernBlot | 35.4 s |
| FISH | 35.5 s |
| HybridizationCapture | 35.7 s |
| BisulfiteSequencing | 35.8 s |
| EnzymaticMethylSequencing | 42.3 s |

Review artifacts are in `previews/review-v5/`; audit files are in `media/expansion/analysis_methods/layout_audit/`. The GIFs are in `previews/v5/`, with lesson-resolution MP4s in `media/videos/scenes/720p30/`. Molecular drawings and signal traces remain instructional schematics.

All GIFs were decoded after conversion and checked for 768 × 432 dimensions, indefinite looping, complete frame sequences, and duration agreement with their MP4s. Representative converted frames were inspected in `analysis_methods_gif_check.jpg`. Exact video/GIF metadata is retained in `analysis_methods_validation.json` beside that sheet.
