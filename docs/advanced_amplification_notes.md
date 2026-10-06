# Additional amplification lessons

All lengths, reaction times, molecular sizes and copy counts are teaching schematics. Base letters and colors are consistent with the shared visual language; backbone colors identify template, new DNA and incorporated primers. These are explanations of mechanisms, not experimental protocols or atomic models.

## DigitalPCR — partitioned endpoint PCR

The example distributes eight illustrated DNA molecules among sixteen equal partitions. Six partitions contain targets, including two partitions with two targets each. One occupied partition is enlarged to show primer extension. Endpoint fluorescence then classifies partitions. Counting six positives does not mean that the sample began with six molecules. With ten negatives, the Poisson occupancy estimate is λ = −ln(10/16) ≈ 0.470 molecules per partition; sixteen partitions therefore estimate about 7.52 starting molecules. The finite sample estimate need not equal the eight illustrated molecules exactly.

Assumptions: independent random loading, equal partition volumes, reliable classification and efficient target detection. A real concentration additionally uses partition volume and any sample dilution; those conversions and statistical confidence intervals are outside this scene. Sixteen partitions are deliberately far fewer than a real instrument uses. The circles represent physical reaction partitions, not DNA molecules. The close-up is explicitly a change of scale. It shows a six-base template, a two-base primer and one extension event as a compact reminder of PCR; the full thermal cycling mechanism is taught in the dedicated PCR lesson.

Sources: [Bio-Rad, droplet digital PCR technology](https://www.bio-rad.com/es-mx/life-science/learning-center/introduction-to-digital-pcr/what-is-droplet-digital-pcr); [Bio-Rad, digital PCR introduction](https://www.bio-rad.com/de/life-science/learning-center/introduction-to-digital-pcr). These manufacturer descriptions verify partitioning, endpoint classification and Poisson occupancy correction. The displayed calculation is independently computed for this illustrative sample.

## ProbeQPCR — hydrolysis-probe detection

A TaqMan-style probe hybridizes downstream of an extending primer. The probe carries a 5′ reporter and a 3′ quencher. While the probe is intact, reporter emission is suppressed. The DNA polymerase's 5′ nuclease activity cleaves the bound probe; reporter-bearing and quencher-bearing fragments separate, permitting increased fluorescence. Polymerase continues DNA synthesis. Repeated amplification cycles release more reporters.

Only one productive DNA strand is followed. The probe is drawn as four bases for legibility; real probe design, blocking chemistry, polymerase kinetics, excitation optics and fluorescence calibration are omitted. Fragment trajectories and the depicted cleavage position are schematic. The reporter does not become part of the new DNA, and the probe is not used as a primer. Fluorescence is a target-linked readout, not proof of exact input concentration without assay calibration or controls.

Sources: [Thermo Fisher, Real-Time PCR Systems Chemistry Guide, chapter 2](https://documents.thermofisher.com/TFS-Assets/LSG/manuals/cms_042681.pdf); [Thermo Fisher, TaqMan primer and probe support](https://www.thermofisher.com/ar/en/home/technical-resources/technical-reference-library/real-time-digital-PCR-applications-support-center/taqman-primers-and-probes-support/taqman-primers-and-probes-support-getting-started.html?open=o5).

## RollingCircleAmplification — one-primer RCA

A primer on a circular single-stranded DNA template is extended by phi29 DNA polymerase. Strand displacement lets polymerase reuse the same circle. The output is one continuous single strand containing tandem complements of the circular sequence. The small circular view and the moving enlarged active-site window depict the same reaction at two scales. The window exposes only the nearby template bases; it is not a separate linear template. The original primer remains copper in the continuous product.

The six-base circle is a sequence schematic, not a physically realistic circle of six nucleotides. Three repeats are shown; actual products can be much longer. This is single-primer linear RCA. Random-primer RCA can instead make branched products, and nick-initiated biological rolling-circle replication has additional steps not shown here. The circle's drawn rotation communicates traversal and reuse, not measured rigid-body motion.

Sources: [NEB, whole-genome amplification and multiple displacement amplification](https://www.neb.com/en-us/applications/dna-amplification-pcr-and-qpcr/isothermal-amplification/whole-genome-amplification-and-multiple-displacement-amplification); [NEB, phi29-XT RCA mechanism and priming strategies](https://www.neb.com/de-de/protocols/protocols-for-amplification-of-dna-using-the-phi29-xt-rca-kit-neb-e1603).

## RPA — recombinase-assisted primer invasion

Recombinase associates with a DNA primer and promotes invasion of a homologous site in duplex DNA. The displaced partner bends away while the invading primer pairs with its target. Single-stranded DNA-binding proteins stabilize the displaced strand. Recombinase clears, allowing a strand-displacing polymerase to extend the primer. Oppositely directed priming on the other strand supplies the second product lineage; products can then support additional rounds.

The scene follows the two primer directions in sequence for clarity. Real reactions contain many molecules and overlapping events. The invading primers are shortened to three bases for legibility. Loading factors, ATP turnover, crowding agents and detection chemistry are omitted. No thermal melting step is implied. Curves are schematic conformations, and SSB spacing is not molecular stoichiometry.

Sources: [Piepenburg et al., 2006, DNA Detection Using Recombination Proteins](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.0040204), PLOS Biology 4:e204; [TwistDx, RPA mechanism](https://www.twistdx.co.uk/rpa/).

## MultipleDisplacementAmplification — random-primed MDA

Random primers can initiate synthesis at multiple sites on an accessible DNA template. A downstream primer first produces a daughter strand. Extension from an upstream primer displaces that daughter. The released strand can bind another random primer and serve as a new template, producing further displacement branches. The scene follows a small section of this network so each new DNA strand has an identifiable template. The final molecular overview changes scale: each solid path is a distinct covalent strand, copper marks its retained primer, and dashed cross-links show the remaining hybridized regions. A displaced tail also supports an antiparallel daughter strand; there are no covalent branch-point joins.

The displayed primers have three bases for legibility; they illustrate matching sites rather than a recommended primer design. DNA preparation, long-range genome topology, competition among many primers and full branch density are omitted. The displacement products are distinct covalent strands; they are associated through hybridization rather than covalently joined into a single tree. The scene makes no claim of uniform genome coverage: amplification bias, chimera formation and allele dropout matter in real whole-genome amplification.

Sources: [Dean et al., 2002, Comprehensive human genome amplification using multiple displacement amplification](https://pubmed.ncbi.nlm.nih.gov/11959976/), PNAS 99:5261–5266, DOI [10.1073/pnas.082089499](https://doi.org/10.1073/pnas.082089499); [NEB, phi29-XT WGA manual](https://prd-sccd02.neb.com/en/-/media/nebus/files/manuals/manuale1604.pdf).

## Telomerase — human repeat addition and fill-in

The human RNA template is shown in spatial 3′→5′ order as CAAUCCCAAUC. The terminal DNA GTTAG aligns with its first five bases CAAUC. Copying the remaining six RNA bases adds GGTTAG. The newly extended terminal GTTAG realigns with the RNA's alignment region for another six-base addition. This register preserves the human TTAGGG repeat while ending each illustrated repeat-addition cycle in TAG.

Only a short RNA–DNA hybrid is paired at a time; older base pairs are released as synthesis progresses. Telomerase is a ribonucleoprotein reverse transcriptase, and the drawing shows only its template region rather than the complete RNA or protein structure. Subsequent C-strand fill-in is performed by primase/polymerase α-associated machinery. RNA-primer removal and completion leave a 3′ G-rich overhang. Recruitment by shelterin, CST regulation, nucleases, ligase identity, actual overhang length and cell-cycle control are compressed or omitted; fill-in is not attributed to telomerase.

Sources: [Human telomerase holoenzyme structure and catalytic cycle, Nature 2021](https://www.nature.com/articles/s41586-021-03415-4); [Mechanisms of telomerase inhibition by modified dNTPs, Nature Communications 2020](https://www.nature.com/articles/s41467-020-19115-y); [Coordinated DNA dynamics during the human telomerase catalytic cycle](https://www.nature.com/articles/ncomms5146); [CST–polymerase α–primase solves a second telomere end-replication problem](https://pubmed.ncbi.nlm.nih.gov/38418884/).

Sources checked 2026-10-05. The illustrations show representative mechanisms rather than every variant or instrument implementation.
