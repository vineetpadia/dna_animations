# Foundations, editing and repair

All displayed sequences are shortened diagrams. The animations explain
mechanisms; they do not specify experimental protocols or predict efficiencies.
The normal nucleotide palette, strand roles and polarity rules apply.

## DNAExtraction

Follows cell disruption, protein digestion, silica binding, washing and
low-salt elution. The same DNA object moves through the workflow. Protein
fragments and the column are schematic; purification is neither perfectly
selective nor quantitative. One generic cell is shown without a nucleus.

Source: [NEB, silica-based purification](https://www.neb.com/en-us/applications/cloning-and-synthetic-biology/nucleic-acid-purification/silica-based-methods).

## GelElectrophoresis

Shows linear double-stranded DNA of 300, 600 and 1200 bp against a size
ladder. Migration positions are illustrative, not a calibrated gel model.
The small ladder-like shapes represent entire fragments, not individual
nucleotides. A band contains many molecules. Equal migration indicates
similar length, not matching sequence. Plasmid topology, staining chemistry,
gel concentration, damaged samples and unusual structures are omitted.

Source: [Addgene, agarose gel electrophoresis](https://www.addgene.org/protocols/gel-electrophoresis/).

## CRISPRCas9

The SpCas9 example retains an actual AGG PAM but shortens the protospacer
from 20 bases to eight. The RNA matches the non-target DNA sequence (U for
T), pairs with the opposite strand, and displaces the non-target strand.
Both backbones are cut three bases before the PAM. One end-joining example
removes a base pair before sealing. This is one possible outcome: end joining
can restore the original sequence or create varied changes; donor-directed
repair is a different pathway. The scene does not promise a knockout.

Source: [Addgene CRISPR guide](https://www.addgene.org/guides/crispr/).

## BaseEditing

One cytosine-base-editor mechanism is shown, not all base editor families.
Deamination produces U in exposed DNA; UGI inhibits uracil removal. A nick
in the opposite strand biases processing. The scene then follows one route
to an A-containing complementary strand and copying into a stable T·A pair.
That copying begins from a short retained primer; primer processing is omitted
from this focused view of fixation of the edited base pair.
Cellular outcomes vary. Bystander edits, indels and unwanted edits are omitted.
Protein labels locate catalytic functions, not atomic protein geometries.

Primary source: [Komor et al., 2016](https://doi.org/10.1038/nature17946).

## PrimeEditing

Shows a point substitution with a Cas9 nickase–reverse transcriptase and
a pegRNA. The nick creates a DNA 3′ end. A separate close view shows its
pairing to the primer-binding site and extension along the RNA template.
The original 5′ flap is removed; the edited 3′ flap is retained, its remaining
nick is explicitly ligated, and the mismatch is resolved. The RNA extension is drawn antiparallel:
3′ primer-binding region on the left, template toward the right and the
guide scaffold. The shorter DNA and RNA sequences are illustrative.

The source DNA is ATGCCATGAC; the illustrated edited strand is ATGCGATGAC.
The RNA extension ACGCUACU templates positions 1–8, including the new G.
Guide/PAM recognition is summarized here and expanded in CRISPRCas9.
Repair is a representative successful path; it is not deterministic, and
additional nicking strategies such as PE3 are not depicted.

Primary source: [Anzalone et al., 2019](https://doi.org/10.1038/s41586-019-1711-4).
Supporting diagrams: [Addgene prime editing](https://www.addgene.org/crispr/prime-edit/).

## DNARepair

The named repair lesson teaches **short-patch base-excision repair**, using
uracil produced by cytosine deamination. Glycosylase removes the base while
preserving the backbone. AP-site processing removes the sugar remnant;
polymerase fills the single-base gap and ligase seals the remaining nick.
The damaged strand is restored using its complementary strand. Enzyme
recruitment, scaffold proteins, end chemistry and other repair pathways are
outside this lesson. End joining is represented in CRISPRCas9; MutS-based
in-vitro filtering is separately covered and is not cellular mismatch repair.

Sources: [NEB DNA repair enzyme activities](https://www.neb.com/tools-and-resources/selection-charts/activities-of-dna-repair-enzymes-and-structure-specific-endonucleases),
[NEB uracil excision](https://www.neb.com/products/m5505-user-enzyme).
