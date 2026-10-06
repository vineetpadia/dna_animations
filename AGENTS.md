# Teaching animation contract

Read `docs/visual_language.md` before changing scenes. Use the shared
`dna_animations/core.py` drawing and scene API. Retain base identities, primer
segments, covalent backbone continuity, strand polarity, and object identity
as molecules move. A successful render is not sufficient validation.

Visual direction: Apple/Dieter Rams restraint. Warm white, graphite, fine
lines, muted functional accents. Colored nucleotides: A green, T/U amber,
C blue, G violet, with matching light tile fills. One title and one short
caption, with essential labels in dedicated lanes. No persistent subtitle,
legend or row of chapter names. Keep nucleotide identity colors consistent
with sequencing signal colors; backdrop, enzymes and backbones stay restrained.

Render changed scenes and inspect frames spanning every stage. Fix overlaps,
unreadable labels, misleading direction, and transformations that imply a
different molecular mechanism. Keep precise source references and deliberate
simplifications in each method's notes. Use minimal on-screen text; show the
causal step in the animation. Never claim a schematic is a full atomic model.

Keep exported GIF previews and the reusable render command working. Do not
replace genuine molecular actions with arbitrary circles, unrelated bars, or
whole-product crossfades.

Register lessons in `dna_animations/catalog.py`; `scenes.py`, the render CLI,
and gallery use that catalogue. Export the current collection to `previews/v5`
and retain `media/videos/scenes/720p30` as the canonical movie location.
Rebuild `previews/index.html` with `tools/build_gallery.py` after exports.
