# DNA method animations

39 Manim lessons explain DNA preparation, biological processes, synthesis,
assembly, amplification, sequencing, hybridization, methylation analysis and
genome editing. Most run 35–60 seconds. They are conceptual teaching diagrams,
not molecular dynamics simulations or complete laboratory protocols.

## Watch

**[Open the online animation gallery](https://vineetpadia.github.io/dna_animations/)**

Open the [animation gallery](previews/index.html) to search by method or filter
by family. The gallery shows one large preview per row, with **Enlarge** and
**Full screen** controls. Each lesson has a looping 1280×720 GIF, a smooth 720p
video and teaching notes with sources and scope. GIFs start when selected;
**Stop all** stops them.

Start or restart the local gallery server from the project folder:

```bash
.venv/bin/python tools/serve_gallery.py --start
```

Open the URL printed by the command. It reuses a healthy gallery server if one
is already running.

- Current GIFs: [previews/v5](previews/v5/)
- Videos: [media/videos/scenes/720p30](media/videos/scenes/720p30/)
- Review frames: [previews/review-v5](previews/review-v5/)
- Export/audit manifest: [previews/v5/manifest.json](previews/v5/manifest.json)

## Lessons

### Foundations

- **DNA extraction & purification** — [DNAExtraction GIF](previews/v5/DNAExtraction.gif) · [notes](docs/foundations_editing_notes.md)
- **Gel electrophoresis** — [GelElectrophoresis GIF](previews/v5/GelElectrophoresis.gif) · [notes](docs/foundations_editing_notes.md)

### Biological processes

- **DNA replication** — [Replication GIF](previews/v5/Replication.gif) · [notes](docs/replication_notes.md)
- **DNA repair · base excision** — [DNARepair GIF](previews/v5/DNARepair.gif) · [notes](docs/foundations_editing_notes.md)
- **Telomerase** — [Telomerase GIF](previews/v5/Telomerase.gif) · [notes](docs/advanced_amplification_notes.md)

### Synthesis

- **Enzymatic DNA synthesis** — [EnzymaticSynthesis GIF](previews/v5/EnzymaticSynthesis.gif) · [notes](docs/synthesis_notes.md)
- **Template-independent DNA synthesis** — [TemplateIndependentSynthesis GIF](previews/v5/TemplateIndependentSynthesis.gif) · [notes](docs/synthesis_notes.md)
- **Phosphoramidite DNA synthesis** — [PhosphoramiditeSynthesis GIF](previews/v5/PhosphoramiditeSynthesis.gif) · [notes](docs/synthesis_notes.md)
- **MutS error filtering** — [MutSErrorCorrection GIF](previews/v5/MutSErrorCorrection.gif) · [notes](docs/assembly_notes.md)
- **Consensus shuffling** — [ConsensusShuffling GIF](previews/v5/ConsensusShuffling.gif) · [notes](docs/consensus_notes.md)

### Cloning & assembly

- **Restriction digestion and ligation** — [RestrictionLigation GIF](previews/v5/RestrictionLigation.gif) · [notes](docs/assembly_notes.md)
- **Plasmid cloning** — [PlasmidCloning GIF](previews/v5/PlasmidCloning.gif) · [notes](docs/assembly_notes.md)
- **Gibson assembly** — [GibsonAssembly GIF](previews/v5/GibsonAssembly.gif) · [notes](docs/assembly_notes.md)
- **Golden Gate assembly** — [GoldenGateAssembly GIF](previews/v5/GoldenGateAssembly.gif) · [notes](docs/assembly_notes.md)
- **DNA shuffling** — [DNAShuffling GIF](previews/v5/DNAShuffling.gif) · [notes](docs/assembly_notes.md)
- **Site-directed mutagenesis** — [SiteDirectedMutagenesis GIF](previews/v5/SiteDirectedMutagenesis.gif) · [notes](docs/assembly_notes.md)
- **Overlap-extension PCR** — [OverlapExtensionPCR GIF](previews/v5/OverlapExtensionPCR.gif) · [notes](docs/assembly_notes.md)

### Amplification & counting

- **PCR** — [PCR GIF](previews/v5/PCR.gif) · [notes](docs/amplification_notes.md)
- **RT-qPCR** — [RTqPCR GIF](previews/v5/RTqPCR.gif) · [notes](docs/amplification_notes.md)
- **LAMP** — [LAMP GIF](previews/v5/LAMP.gif) · [notes](docs/amplification_notes.md)
- **Probe qPCR** — [ProbeQPCR GIF](previews/v5/ProbeQPCR.gif) · [notes](docs/advanced_amplification_notes.md)
- **Digital PCR** — [DigitalPCR GIF](previews/v5/DigitalPCR.gif) · [notes](docs/advanced_amplification_notes.md)
- **Recombinase polymerase amplification** — [RPA GIF](previews/v5/RPA.gif) · [notes](docs/advanced_amplification_notes.md)
- **Rolling circle amplification** — [RollingCircleAmplification GIF](previews/v5/RollingCircleAmplification.gif) · [notes](docs/advanced_amplification_notes.md)
- **Multiple displacement amplification** — [MultipleDisplacementAmplification GIF](previews/v5/MultipleDisplacementAmplification.gif) · [notes](docs/advanced_amplification_notes.md)

### Sequencing

- **DNA library preparation** — [LibraryPreparation GIF](previews/v5/LibraryPreparation.gif) · [notes](docs/analysis_methods_notes.md)
- **Tagmentation** — [Tagmentation GIF](previews/v5/Tagmentation.gif) · [notes](docs/analysis_methods_notes.md)
- **PacBio HiFi sequencing** — [PacBioHiFi GIF](previews/v5/PacBioHiFi.gif) · [notes](docs/analysis_methods_notes.md)
- **Sanger sequencing** — [Sanger GIF](previews/v5/Sanger.gif) · [notes](docs/sequencing_notes.md)
- **Illumina: classic workflow** — [Illumina GIF](previews/v5/Illumina.gif) · [notes](docs/sequencing_notes.md)
- **Nanopore sequencing** — [Nanopore GIF](previews/v5/Nanopore.gif) · [notes](docs/sequencing_notes.md)

### Hybridization & epigenetics

- **Southern blot** — [SouthernBlot GIF](previews/v5/SouthernBlot.gif) · [notes](docs/analysis_methods_notes.md)
- **DNA FISH** — [FISH GIF](previews/v5/FISH.gif) · [notes](docs/analysis_methods_notes.md)
- **Hybridization capture** — [HybridizationCapture GIF](previews/v5/HybridizationCapture.gif) · [notes](docs/analysis_methods_notes.md)
- **Bisulfite sequencing** — [BisulfiteSequencing GIF](previews/v5/BisulfiteSequencing.gif) · [notes](docs/analysis_methods_notes.md)
- **Enzymatic methyl sequencing** — [EnzymaticMethylSequencing GIF](previews/v5/EnzymaticMethylSequencing.gif) · [notes](docs/analysis_methods_notes.md)

### Genome editing

- **CRISPR–Cas9 editing** — [CRISPRCas9 GIF](previews/v5/CRISPRCas9.gif) · [notes](docs/foundations_editing_notes.md)
- **Base editing · C → T** — [BaseEditing GIF](previews/v5/BaseEditing.gif) · [notes](docs/foundations_editing_notes.md)
- **Prime editing** — [PrimeEditing GIF](previews/v5/PrimeEditing.gif) · [notes](docs/foundations_editing_notes.md)

## Render and export

Manim is installed in the local `.venv`. Rebuild any lesson, its GIF and its
review contact sheet:

```bash
.venv/bin/python tools/render_lessons.py ConsensusShuffling --gif --contact-sheet
```

Pass multiple class names or omit names for the entire catalogue. The default
is 1280×720 at 30 fps; `--quality draft` produces 480p review movies.
`--exports-only` refreshes exports from existing movies. GIFs are 1280×720,
12 fps and loop continuously. Their flat palette preserves the paper background.

Enable motion-time text auditing when rendering:

```bash
BIO_LAYOUT_AUDIT=1 .venv/bin/manim -qm dna_animations/scenes.py PrimeEditing
```

After completing and reviewing exports:

```bash
.venv/bin/python tools/build_gallery.py
.venv/bin/python tools/validate_library.py
```

The validation script checks the reviewed expansion's family-specific audits,
media integrity and catalogue completeness. A later canonical rerender needs
its own new audit review; passing an older audit does not validate changed code.

## Publish to GitHub Pages

The repository includes the current GIFs, posters, 720p movies, review frames,
and audit records. Local environments, render caches, intermediate clips, and
superseded exports are excluded.

The Pages workflow runs on pushes to `main` and can also be started from the
Actions tab. It packages the committed gallery and media; no Manim render is
needed during deployment. To check the same static bundle locally:

```bash
python tools/build_site.py
python -m http.server 8000 --directory _site
```

Open `http://localhost:8000/`. The generated `_site` folder is not committed.
After changing lessons, render and inspect them, rebuild the gallery and
validation manifest, then commit the updated sources and exports together.

In the repository's **Settings → Pages**, select **GitHub Actions** as the
publishing source. The workflow follows the
[GitHub Pages deployment guide](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

## Installation

To install in a fresh environment with Cairo/Pango available:

```bash
python -m venv .venv
.venv/bin/python -m pip install -e .
```

## Keep the visual language consistent

Read [the visual contract](docs/visual_language.md) before adding a method.
Warm white, graphite, restrained machinery and dedicated label lanes frame
the molecular action. Bases use green A, amber T/U, blue C and violet G;
letters remain visible. Gray templates, charcoal new DNA and copper primers
separate strand roles. Sequencing signals reuse base identity colors.

Use `dna_animations/core.py` for typography, bases, strands, captions and
framing. Register a new lesson in `dna_animations/catalog.py`; the Manim
entrypoint, export tool and gallery share this catalogue. Each implementation
must have its own precise scope and verified source notes.

## Scientific scope and review

Scenes retain polarity, complementary pairing, primer identity, backbone
continuity and the origin of measured signals. Frame review includes both
held states and transitions. The text audit alone cannot detect every
text/shape collision or a misleading molecular transformation.

Some mechanisms are specific examples: classic bridge/four-color Illumina,
reversibly blocked TdT synthesis, a cytosine base editor, a prime-editing point
substitution, and short-patch base-excision repair. The named DNA repair lesson
does not cover every cellular repair pathway. Synthetic qPCR/current traces,
shortened sequences and non-atomic geometries are explicitly documented.

The new consensus-shuffling lesson follows Binkowski et al. (2005): strand
reassortment, fragmentation, immobilized-MutS filtering and overlap reassembly.
It is distinct from diversity-generating DNA shuffling and from the separate
MutS capture lesson. Error reduction is enrichment, not a guarantee of an
error-free molecule.
