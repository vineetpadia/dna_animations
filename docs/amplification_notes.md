# Amplification scenes: teaching notes and evidence

These diagrams are conceptual explanations, not experimental protocols. Distances, base counts, enzyme sizes and times are schematic. Primer segments retain the same muted copper color after incorporation. Charcoal indicates newly synthesized DNA and medium gray indicates the starting DNA template. Strand polarity is explicit.

## PCR

Learning sequence: locate a target within longer DNA; separate the strands; align two antiparallel primers with their 3′ ends facing inward; extend both primers 5′ to 3′; let the new products become templates; establish both primer-defined boundaries; repeat.

The first products visibly extend beyond the opposite primer position. A strand bounded at both ends first appears in cycle 2; fully bounded duplexes first appear in cycle 3. Later cycles enrich these defined products. Doubling is an idealization during efficient amplification, not a guarantee through the plateau. A compact molecular glyph represents a duplex at overview scale; it does not represent a single base.

Temperature badges are illustrative of conventional Taq PCR and are not a universal protocol. Real annealing and extension conditions depend on primers, enzyme and target.

Evidence:

- [NEB: PCR overview](https://www.neb.com/en-us/applications/dna-amplification-pcr-and-qpcr/pcr) — manufacturer explanation of separation, primer annealing, extension and reuse of products as templates.
- [Saiki et al., 1988: Primer-directed enzymatic amplification of DNA with a thermostable DNA polymerase](https://doi.org/10.1126/science.2448875) — primary description of thermostable polymerase PCR.
- [Studying DNA, Genomes](https://www.ncbi.nlm.nih.gov/books/NBK21129/) — explanatory check on first-cycle long products and subsequent primer-defined products. Secondary teaching reference; the topology also follows directly from the shown primer orientations.

## RT-qPCR

Learning sequence: bind a DNA primer to RNA; extend complementary DNA with reverse transcriptase; separate the RNA/cDNA hybrid; synthesize a DNA partner; amplify DNA with fluorescence measurements; compare threshold crossings.

RNA contains U and is labeled in the 3′→5′ direction across the frame so cDNA can visibly extend left to right in its 5′→3′ direction. The RNA is physically separated at the transition to PCR; its disappearance is not presented as conversion into DNA. The primer is gene specific for clarity; random primers and oligo(dT) are other RT choices.

The scene shows a DNA-binding fluorescent dye model, not probe hydrolysis. Dye is a muted sage light cue on duplex DNA; no sequence-specific probe is implied. The amplification curves are synthetic teaching curves. A shared threshold lies above baseline and in the rising part of both curves. Earlier Cq suggests more starting target only when assay efficiency and sample handling are comparable; the scene states this condition. These curves are not measured data and do not establish an absolute concentration. Quantitative use requires appropriate controls, calibration or normalization, which are outside this mechanism-focused scene.

Evidence:

- [Thermo Fisher: Reverse Transcription Basics](https://www.thermofisher.com/us/en/home/life-science/cloning/cloning-learning-center/invitrogen-school-of-molecular-biology/rt-education/reverse-transcription-basics.html) — RNA-dependent DNA synthesis and the cDNA product.
- [Thermo Fisher: SuperScript IV first-strand synthesis guide](https://documents.thermofisher.com/TFS-Assets/LSG/manuals/SSIV_First_Strand_Synthesis_System_UG.pdf) — primer choices and cDNA use in subsequent PCR.
- [Bio-Rad: qPCR amplification](https://www.bio-rad.com/es-py/applications-technologies/qpcr-amplification?ID=3edb4096-4520-87be-7382-9bd9c130e419) — cyclewise fluorescence as a readout of amplified product.
- [Bio-Rad: qPCR analysis](https://www.bio-rad.com/en-us/applications-technologies/qpcr-analysis?ID=8bf12444-522e-e3cb-18cd-ccd0ec94f91a) — baseline, rising phase, plateau, Cq and threshold placement.

## LAMP

Learning sequence: identify inner and outer primer sites; extend the F2 portion of FIP while retaining its F1c tail; start synthesis from outer primer F3 and displace that product; pair F1c with F1 within the displaced strand; repeat inner/outer priming from the opposite end with BIP/B3; form a dumbbell seed; grow stem-loop products through self-priming and displacement.

LAMP is shown at constant temperature with a strand-displacing polymerase. FIP and BIP are composite primers, each with an annealing 3′ part and a 5′ tail that later makes a loop. Each labeled F/B segment represents a sequence domain containing multiple nucleotides; displayed domain widths are not actual primer lengths. The initial target is shown locally accessible; the animation does not imply a PCR-style repeated thermal denaturation step. The four essential primers are included. Optional loop primers, full branched concatemer topology, reaction initiation probabilities and all simultaneous branches are omitted so one productive lineage can be followed. Hairpins and dumbbells are connected paths with a visible strand break and explicit free ends; they are not covalently closed circular DNA. The final connected strand illustrates repeated paired stems and exposed loops, rather than an exact conformation or complete sequence map. Loop shapes are geometric schematics, not molecular conformations.

Evidence:

- [Notomi et al., 2000: Loop-mediated isothermal amplification of DNA](https://pubmed.ncbi.nlm.nih.gov/10871386/) — original LAMP publication, Nucleic Acids Research 28:e63, DOI [10.1093/nar/28.12.e63](https://doi.org/10.1093/nar/28.12.e63).
- [NEB: LAMP mechanism tutorial](https://www.neb.com/en-gb/tools-and-resources/video-library/loop-mediated-isothermal-amplification-lamp-tutorial) — verified sequence of inner-primer extension, outer-primer displacement, self-hybridization, opposite-end repetition, dumbbell formation and concatemer growth.
- [NEB: Isothermal amplification brochure](https://www.neb.com/en/-/media/nebus/files/brochures/isothermal_amplification_trifold.pdf) — primer architecture and F1/F1c, F2/F2c, B1/B1c and B2/B2c domain relationships.

Sources checked 2026-10-05. The original LAMP publication metadata was accessible; its full text was blocked by a browser gate during this work. The mechanism was cross-checked against NEB's original manufacturer diagram and tutorial.
