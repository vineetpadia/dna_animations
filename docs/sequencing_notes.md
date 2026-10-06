# Sequencing scenes: teaching intent and scientific boundaries

These are idealized mechanism diagrams. Molecule size, elapsed time, signal amplitudes, colors, and the number of molecules are schematic. Letters remain visible wherever nucleotide identity matters. Gray indicates the molecule being read, charcoal indicates a newly synthesized strand, and muted copper indicates a primer. Nucleotides and sequencing signals share a fixed green/amber/blue/violet identity palette; the letters also identify each base. Backbone tones independently show strand roles.

## Sanger

The scene follows one sequencing primer extending on one template, then shows a population of extension products with different terminating positions. The primer remains part of every product. Normal dNTP incorporation permits subsequent extension because the incorporated nucleotide has a 3′ hydroxyl. A dye-labeled ddNTP lacks that hydroxyl, so its incorporation ends extension. The fragment population is made across many template copies and extension reactions, not by breaking a single completed strand.

Denatured products move through a capillary separation matrix. Smaller products reach the detector earlier; the dye at each terminal nucleotide provides its base identity. The idealized chromatogram reconstructs the newly synthesized sequence in the 5′→3′ direction, starting after the primer. Peak shape, dye palette, mobility, and fragment lengths are illustrative. The animation compresses cleanup, denaturation, and instrument optics.

Sources checked 2026-10-05:

- [Thermo Fisher: Sanger sequencing getting started](https://www.thermofisher.com/jp/en/home/technical-resources/technical-reference-library/capillary-electrophoresis-applications-support-center/sanger-sequencing-support/sanger-sequencing-support-getting-started.html): single template/primer, terminated extension products, capillary separation.
- [Thermo Fisher: DNA Sequencing by Capillary Electrophoresis Chemistry Guide](https://documents.thermofisher.com/TFS-Assets/LSG/manuals/cms_041003.pdf): dye terminator reactions, electrophoresis, detection.

## Illumina

The scene explicitly represents the **classic bridge amplification and four-color sequencing-by-synthesis workflow**. Adapter-bearing library strands bind flow-cell oligonucleotides; extension creates a surface-bound copy and the original library molecule washes away. The anchored copy bends to a nearby oligonucleotide, polymerase creates its complementary strand, and denaturation leaves two anchored strands. Repetition produces a clonal cluster. Orientation selection is shown before a sequencing primer is introduced.

The enlarged sequencing view follows one representative molecule within a cluster. All four reversible terminators are available; the complementary nucleotide is incorporated, its temporary block prevents another incorporation in the same cycle, imaging determines identity, and dye/block removal restores extension. The repeated cycle builds one read while many clusters are measured in parallel. The symbols for the dye and block represent distinct functions, not an exact chemical structure.

The animation does not generalize bridge amplification or four separate dye colors to every modern Illumina instrument. Patterned-flow-cell ExAmp workflows and two-channel signal encoding require separate lessons. Adapter/index structure, phasing, quality scores, and paired-end turnaround are omitted from this introductory mechanism.

Sources checked 2026-10-05:

- [Illumina: Sequencing Technology spotlight](https://support.illumina.com/content/dam/illumina-marketing/documents/products/techspotlights/techspotlight_sequencing.pdf): library adapters, surface amplification, fluorescence imaging, repeated sequencing cycles.
- [Illumina: Sequencing by synthesis technology](https://www.illumina.com/science/technology/next-generation-sequencing/sequencing-technology.html): reversible terminator incorporation, imaging, cleavage.
- [Thermo Fisher: Illumina workflow](https://www.thermofisher.com/us/en/home/life-science/cloning/cloning-learning-center/invitrogen-school-of-molecular-biology/next-generation-sequencing/illumina-workflow.html): anchored complementary copy, template removal, bridge cycle, orientation selection; distinguishes ExAmp.

## Nanopore

An adapter-associated motor controls strand passage into a membrane nanopore. A voltage drives ionic current through the pore; DNA occupancy changes that current. Successive overlapping groups of bases influence successive regions of the current trace. A basecalling model uses the signal context to estimate a DNA sequence. No fluorescent labels or DNA synthesis are required for this reading mechanism.

The highlighted window is a teaching symbol for a multi-base sensing region, not a fixed k-mer count shared by every pore. Current levels, dwell times, and noise are illustrative rather than a calibrated pore model. Modern pores can have multiple sensing regions, which are condensed here into one diagrammatic window. The scene depicts an adapter-prepared single strand at the motor; upstream library chemistry and double-strand unzipping are summarized, not structurally modeled. The displayed base calls are a schematic ideal result, not an assertion of perfect accuracy.

Sources checked 2026-10-05:

- [Oxford Nanopore: How nanopore sequencing works](https://nanoporetech.com/platform/technology): motor-bearing adapters, applied voltage, strand feeding, combinations of bases affecting ionic current.
- [Oxford Nanopore: How basecalling works](https://nanoporetech.com/platform/technology/basecalling): raw current signal, context-sensitive model decoding, pore-dependent sensing regions.
- [Oxford Nanopore: Direct RNA protocol](https://nanoporetech.com/document/direct-rna-sequencing-sqk-rna004): distinguishes RNA's 3′-first translocation from DNA; this lesson depicts DNA with its 5′ end leading.

## Render review

Each scene was rendered at 480p/15 fps for storyboard review and at 720p/30 fps for final playback. Eight representative frames per initial scene and targeted final frames were inspected for typography, molecule continuity, polarity, overlap, and signal/read correspondence. The final scenes run approximately 49 seconds (Sanger), 56 seconds (Illumina), and 42 seconds (nanopore). Scientific limitations above remain intentional; the animations are mechanism lessons rather than instrument simulations.
