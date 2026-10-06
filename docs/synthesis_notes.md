# Synthesis lessons: scientific scope and teaching notes

All three scenes use the shared visual contract in `dna_animations/core.py`: letters identify bases; backbone color identifies template, primer, or newly synthesized DNA. Drawings are mechanistic schematics. Molecular sizes, times, enzyme shapes, and strand lengths are intentionally simplified.

## EnzymaticSynthesis

**Learning objective:** explain why a complementary strand grows at an existing 3′ end.

Follow the gray template from 3′ toward 5′. The muted copper primer keeps its identity throughout extension. An incorrect incoming base leaves; a complementary G pairs with the next template C. The first incorporation is slowed down: the incoming alpha phosphate joins the backbone while the other two depart as pyrophosphate (PPi). The reactive 3′–OH reappears on the newly incorporated nucleotide. Further additions use the same visual action. The final product is antiparallel to the template.

The mismatch example illustrates selection, not a guarantee that polymerases never make errors. Base pairing alone does not form a covalent backbone bond. The enzyme label and its moving guide identify the catalyst. Magnesium coordination, proton transfer, proofreading, hydrolysis of PPi, and protein conformational changes are omitted; this is not an atomic reaction mechanism. The eight-base template and two-base primer are diagram lengths, not practical oligonucleotide recommendations.

**Primary evidence:** [Multiple deprotonation paths of the nucleophile 3′-OH in the DNA synthesis reaction, PNAS (2021)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8201771/) documents attack from the primer terminus at the incoming alpha phosphate. [Two proton transfers in the transition state for nucleotidyl transfer, PNAS (2007)](https://pmc.ncbi.nlm.nih.gov/articles/PMC1838591/) supports the conserved polymerase chemistry.

## PhosphoramiditeSynthesis

**Learning objective:** distinguish chemical growth at the 5′ end from polymerase growth at the 3′ end.

The first A remains tethered through its 3′ end to the solid support at the right. Growth proceeds leftward. Removing DMT exposes a 5′–OH. A protected C monomer couples through its phosphorus center, creating a P(III) linkage. A separate molecule that missed the coupling is capped and cannot resume extension in the next cycle. Oxidation makes the P(V) linkage. Repeating with G and T produces the spatial sequence 5′-TGCA-3′. Final removal of remaining protection and cleavage from the support release that same sequence.

DMT labels mark terminal 5′ protection. Small red squares symbolize base or phosphate protection; they are not chemical structures or literal counts of atoms. Thymine is not given an exocyclic amino protecting group. The P(III)/P(V) callouts describe the newly formed linkage; the incoming material is a phosphoramidite and the first coupled linkage is a phosphite triester. The reaction's activator, solvents, wash operations, detailed oxidation reagent, capping reagents, and leaving groups are omitted. Repeated cycles compress capping after its explicit first demonstration. Cleavage/deprotection order and final DMT handling vary by process. The released strand still needs purification and quality control.

**Manufacturer evidence:** [IDT's phosphoramidite synthesis explanation](https://www.idtdna.com/page/support-and-education/decoded-plus/oligo-synthesis-why-idt-leads-the-oligo-industry) supports the four operations and capping of failed molecules. [ATDBio's solid-phase synthesis chemistry](https://atdbio.com/nucleic-acids-book/Solid-phase-oligonucleotide-synthesis) supports the attachment, protection, cleavage, and deprotection distinctions. These are direct technical resources from oligonucleotide manufacturers.

## TemplateIndependentSynthesis

**Learning objective:** distinguish writing a chosen sequence from copying a template.

The animation chooses one verified example: engineered TdT incorporating nucleotides protected with a **3′ phosphate**. It does not imply that wild-type TdT inherently adds only one nucleotide. The incoming substrate still has its separate 5′ triphosphate. The 3′ blocking phosphate remains on the extended strand and prevents another addition. Excess substrate and TdT are removed before phosphatase regenerates a free 3′–OH. Removing phosphatase separates deblocking from the next addition cycle. The operator's sequence program selects G, C, A, then T; no complementary template is present.

The initiator remains muted copper and is visibly part of the final six-base diagram. Initiator cleavage, support chemistry, recovery, capping of synthesis failures, and practical fluid handling are outside this lesson. Phosphatase removal is shown schematically, without an operating protocol. The final ideal strand does not assert perfect conversion, universal sequence compatibility, or error-free synthesis. Other controlled synthesis strategies use different reversible groups or polymerase–nucleotide conjugates and should not be inferred to work identically.

**Primary evidence:** [Forget et al., Evolving a terminal deoxynucleotidyl transferase for commercial enzymatic DNA synthesis, Nucleic Acids Research (2025)](https://academic.oup.com/nar/article/53/4/gkaf115/8026291), [PubMed record](https://pubmed.ncbi.nlm.nih.gov/39988321/). This research reports engineered TdT activity on 3′-phosphate-blocked dNTPs and describes phosphatase removal of that blocking group.
