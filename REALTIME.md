## Immediate Reactions (~2026.2.4..10.35.00)

What does this prompt mean?  Of the options, it obviously resonates the most with me:  I've designed fonts, I have ambitions to do much more font work, I'm stuck on a thorny problem in encoding mid-19th century phonetic alphabets, and I am a possessor of Opinions on Typography™.  It's the obvious vein to mine.

So the key concepts to explore here are evidently:

> latent space

Presumably this is simply the configuration space over the kinds of things one can categorize or know about fonts.  There are very spiky edges to this problem:
* Fonts aren't simple rasters, and can even have different behavior at different sizes.
* Fonts can be very baroque and unusual, like Zapfino.
* There are open questions about equivalence across symbol sets:  is a Roman “O” the same thing as a Cyrillic “О” the same thing as a Deseret “𐐄”?  Search engines _tend_ to say yes but not consistently; e.g. on many platforms “𝔤𝔬𝔱𝔥𝔦𝔠” will search as `gothic` despite being an entirely different set of letters.
* OpenType feature sets introduce all sorts of mapping wrinkles.  Is a slashed zero “Ø” the same as a regular zero “0” in the font?  What if they are separate characters, as also you see with small capitals?  Ligatures, too; Hoefler made much of these so there are some exotic cases.

> Visualize the influence of the most important principal components

Classically, this recalls diagrams from Rosen's _The Designer's Book of Type_ or Knuth's _The METAFONT Book_, which I should check if I have on hand or need to request from the library again.  _The Elements of Typographic Style_, too (how is this book still $60!? freaking graphic designers), and maybe pull some of the type specimens I have.

The phrase “most important” is a cute bit of question-begging that can lead to all sorts of rabbit holes.  Naïvely, you have the x-height, the kerning, the counter/aperture size, and other metrics.  Or you can go back to gestalt effects, like what ties a typeface together as such.  This is worth sticking a pin in to explore later.

> develop a tool to encode fonts in a useful encoding scheme (e.g., as a vector of numerical parameters) so that you can encode (almost) arbitrary existing fonts

There are a couple of different ways that immediately come to mind to do this, but it depends to some extent on whether we're talking about existing fonts (in which case METAFONT vs. TrueType/OpenType style vector descriptions) or exploring a space of novel fonts.  If the latter, then the Deseret and Cherokee are both testbeds I've been planning on working more in soon anyway.  (Greek could be more legible to a reviewer.)

> \[develop a tool] to navigate the font space using a suitable interface

Interfaces are more or less a solved problem, so I'm going to punt on thinking about this for now.  (Obviously it's quite easy to make a poor UI, but this is a different sort of problem that's dependent on the parameters of whatever I produce under the hood.)

> building something creative with the font space, e.g., a tool to generate new hybrid fonts, an interactive visualization that lets a user explore font styles, or discovering unexpected semantic associations (e.g., mood, cultural context, usage domain, stylistic qualities).

Miscellaneous thoughts:
* bits-per-glyph calculator (i.e. information density of language)
* ink economy
* automation vs. freeform design
* can LLMs do from-scratch work well in, say, METAPOST?  that'd be very interesting to explore; they “see” in 1D in some sense (data streams) but obviously can do 2D design well in certain cases
    * look at Sequoyah's proto-Cherokee script
    * or Mayan glyphs, pull my books back out and try my hand at those; the toki pona people likely have good resources for thinking about representation
* check my publishing toolchain doc too
* handwriting-to-font development (I've wanted to do this for the Bentley/Shelton handwriting with the Martineau ligature set if it can be salvaged)
* automatic font tuning, per-character kerning in particular (no reason to believe LLMs would be uniquely good at this vs. manually weighted tools like Marini's)
* build a tool to automatically fix the weight and space issues in IDC Calyptapis that I've been gumption-trapped on

I'd really like better tools for working with italics, which are fiendishly hard to make correctly.

> What we want to see: a methodical approach to solving a training/data collection/encoding problem, pragmatic solutions for interface and possible applications.

OK, presumably they want me to lean pretty hard into LLMs and other AI tools.  AI generative art tools are notoriously bad at text, and they particularly produce garbage when looking at anything non-Roman.  LLMs are good at tool construction once you have a good specification, however, 

At this point, what I need to do next is pull the resources I identified and sort this into an exploration.

Updates:
* ~2026.2.4..11.25.00 Leaning towards Greek not only because it's more legible to a potential reviewer but because it has two common modalities of use, in text and in mathematics. This stress-tests the properties of the typeface more generally than, say, Cyrillic would receive.
* ~2026.2.4..11.40.00 Literati-style dynamic equivalence for automatic translations?
* ~2026.2.4..11.50.00 “Design me a font that looks like a gypsy witch would write a spell in.”
* ~2026.2.4..12.25.00 “Visualize the influence of the most important principal components” wait, what does this mean?  if you do this naïvely then you need a figure of merit to measure influence (legibility, presumably, but also in/formality)
* ~2026.2.4.12.25.00 At this point I'm somewhat frustrated (in the formal sense) by the non-obvious utilization of AI in this particular challenge.  There are obvious ways to use the tools, of course, but I'm either missing something or they're mainly interested in what I do with the open-endedness (in which case I'm overthinking).
* ~2026.2.4..12.30.00 I'll feed the challenge and some context to Claude and see what it thinks before I tell it my own thoughts.
    * The strength of typography is that it is an incredibly honed art:  while there is still ample room for experimentation, we have learned by hard experience the attributes of effective and disastrous fonts.
* ~2026.2.4..13.00.00 “latent space” really implies a diagonalization or compressible description of fonts...
* ~2026.2.4..13.10.00 Actually, building a specimen-to-parametric font pipeline would be very helpful.  It uses LLMs where they are strong and humans where they are strong.

---

In that case, the project becomes (concretely) how to proceed from a nineteenth-century type design specimen to a parameterized font with export to a standard OpenType font; (abstractly) how to produce a parameterized font from an image.

This builds a pipeline from a JPEG input to a vectorized font to parameter extraction, a system to encode fonts in a learned parametric space that captures meaningful typographic variation.  As a bonus, we can attempt to use a partial parameterized type description as a basis to generate missing symbols that are stylistically consistent.  It's a clear inverse problem from observation to a generative model, moving between real-world data across multiple levels of representation and schemata.

(This also solves a specific ambition I've nursed for a couple of years now, to produce the DTF Perdita typeface from the Oversize specimen of Deseret from 1859, otherwise never used.)

---

## First Steps (~2026.2.5..09.45.00)

If this is the right approach—and the decision window is rapidly closing—then it's a matter of demonstrating problem-solving within this context, as well as elaborating a tentative theory of the praxis, rather than 

Now, as a contraindication to this solution as it is currently framed, CIMC does close by referring to “a methodical approach to solving a training/data collection/encoding problem, pragmatic solutions for interface and possible applications.”  That first part highlights training (as fine-tuning? expensive!), data collection (which could mean a lot of things including what is subtended by my current direction), and encoding (everything is encoding, man)—all this rather points to more than a conventional 2016 machine-learning tools scaffolded by a 2026 cyborg pipeline.

Plus there is the whole problem of gestalt judgment, which if we can ever come to agreement on even as humans, will be hard to train machines on reliably.  _De gustibus non est disputandum_, of course; and even if you can get sentiment analysis for fonts most people's tastes are trash.

What you gain from working in the METAPOST/METAFONT world is the ability to directly manipulate and quantify font parameters at a **verbal** mechanical level, not just a collection of splines and vectors.  Intriguingly, therefore, there is a hierarchical cascade of parameters which underlie the mechanical representation.  If this is accessible in some way, then we can move from geometric and structural accounts (METAPOST at the object level) to an abstraction that yields them (cf. Noordzij's _The Stroke Theory of Writing_).  That's too much for a weeklong project—it's a research program—but it's worth keeping in mind.

In any case, what we want concretely is a threefold production:
1. Measurement.  Extract all quantifiable parameters from a description.
    1. Intervention.  Which automatic metrics suggest problems vs. expert assessment, and can these be looped back in?  (Use IDC Calyptapis here.)
2. Generalization.  Use automated extraction and quantifiable parameters to get a new font 80% of the way complete.  (Use DTF Perdita here.)
    1. Capture.  Use expert judgment to tune the 20% that requires adjustment.
3. Analysis.  Which gestalt judgments were quantifiable, and which were idiosyncratic?  What feelings correlate with observables?  What does this reveal about the latent font space in the neighborhood of Calyptapis and Perdita?

* ~2026.2.5..10.15.00 METAPOST is actually my secret weapon.  Standard font machine learning runs a pipeline from raw input to a neural network to a raw output (all the way back to the Mark I Perceptron).  METAPOST gives us a legible intermediate representation, just like a programming language.  Our pipeline is longer, more legible, and yields more intervention points:  raw input to feature extraction to METAPOST parameterization to specimen rendering to (CV + heuristics) to vector font output.  We do have a training problem (predicting METAPOST parameters and expert corrections from visual input); a data collection problem (producing a dataset with known METAPOST characterizations); and an encoding problem (METAPOST parameters).  Then we can solve the gestalt problem with a sidestep:  don't try to learn the principles of universal aesthetics, but instead attack the problem as, “Given glyphs A, B, C from Font X, what should glyph D look like?”  I.e., “If these glyphs are Bodoni, what should other Bodoni glyphs look like?”  This has practical uses:  Greek from Roman, Cherokee from Roman, Italic from Roman, etc.  Call this “style transfer” or “few-shot generative modeling”.  In a way, we reduce font modeling to a Hofstadterian strange loop, in that a font is not the collection of glyph instantiations, it is the underlying process by which those instantiations reify.  If I extract the Oversize specimen letters into DTF Perdita, it's not merely a matter of curve fitting, but of “mind fitting”:  why did the designer work this way, consistent with the other evident design choices?  Cognitive archaeology, mental models reconstructed from concrete artifacts.  (I need to listen to some _musique concrète_ while I'm at this, or at least Sun Ra.)  Typography's irreducibility with respect to gestalt patterns makes it a better model for consciousness research precisely because of that difficulty.
* ~2026.2.5..10.25.00 I bet ink traps can be detected automatically.
* ~2026.2.5..10.30.00 IDC Calyptapis already exists as a regular font with six weights (hairline to black) in METAPOST.

I fired up Claude Code in the `idc-calyptapis/` folder with the context from the chat in a `docs/` file.

```
TODO include session here
```

It only took five minutes to go from a spec to a working glyph review tool suitable for (what I may as well call) sentiment analyis.

![[Pasted image 20260205113722.png]]
(The reason this is necessary isn't because current font tools can't give you this tabular overview—they can—it's because METAPOST outputs are SVGs not entries in a font file.)

Armed with the judgment, the first thing to do is to see if Claude can fix the font itself.  (I gave specific feedback on the flawed glyphs, not just an approval or disapproval.)  There were two glyphs across all weights that required serious attention, `Y` and `𐐔`.  The only feedback I gave Claude was the description of the serif flaws in the JSON feedback document.  It fixed `Y` with no trouble but `𐐔` required some rounds of feedback.  This helped me clean up a longstanding gumption trap with the implementation in about thirty minutes of total work.

IDC Calyptapis is a hand-designed font in METAPOST that has a lot of quirks of its unsystematic development across its files.  Although not in the original work plan, it seems like it may be worth asking it to try its hand at regularizing things before we start talking about parameterizing the font.  Thus, I prompt:

> IDC Calyptapis is a hand-designed font in METAPOST that has a lot of quirks
  of its unsystematic development across its files.  Although not in the original work plan, it seems like it may be worth asking you to review the   
  source glyph files and regularize them.  Because that's sensitive to a lot  of variables, you should plan and ultrathink the process.

It produced this plan:

```
 IDC Calyptapis METAPOST Source Regularization Plan                             

 Overview

 Regularize 47 METAPOST glyph source files to fix inconsistencies accumulated
 over years of hand-design, while preserving visual output.

 Key Issues Found

 Critical (Affect Rendering Across Weights)

 1. Pen-height dependent positioning - 17 files use pen_height in serif/bar
 calculations, causing misalignment at different weights
   - Example (U10408.mp line 9): bar := (Ox,
 -y_radius-0.375*pen_height+0.125*0.5*pen_height)
   - Should be: bar := (Ox, -y_radius) -- (Ox, y_radius) (like U10406.mp)

 Code Quality

 2. Dead/commented code - 8 files with large commented blocks
 3. Missing numeric keyword - 5 files with improper declarations
 4. Redundant arithmetic - 0.0*pen_height, (-0/3)*y_radius in 4 files
 5. Magic numbers - Unexplained values like 3.925, 2.875, 39.75/30
 6. TODO/XXX comments - 2 files with unresolved issues

 File Categorization
 ┌──────────────┬───────┬─────────────────────┬──────────────────┐
 │     Tier     │ Count │     Description     │      Action      │
 ├──────────────┼───────┼─────────────────────┼──────────────────┤
 │ A - Clean    │ 11    │ No issues           │ None needed      │
 ├──────────────┼───────┼─────────────────────┼──────────────────┤
 │ B - Minor    │ 13    │ Header/comment only │ Quick fixes      │
 ├──────────────┼───────┼─────────────────────┼──────────────────┤
 │ C - Moderate │ 6     │ Code cleanup needed │ Careful edits    │
 ├──────────────┼───────┼─────────────────────┼──────────────────┤
 │ D - Critical │ 17    │ Pen-height fixes    │ Test each weight │
 └──────────────┴───────┴─────────────────────┴──────────────────┘
 Implementation Phases

 Phase 1: Baseline (Before Any Changes)

 7. Generate SVGs for all glyphs across all 6 weights
 8. Document current state with review tool
 9. Git tag: pre-regularization

 Phase 2: Safe Fixes (Tier B - Headers/Comments)

 Files: U1040b, U1040c, U1040e, U10410, U10419, U1041a, U10421, U10427,
 Ue000-Ue003

 - Standardize headers to: % U+XXXXX DESERET CAPITAL LETTER NAME (char)
 - Remove obvious dead code
 - No functional changes

 Phase 3: Code Cleanup (Tier C)

 Files: U10400, U10417, U10418, U1041b, U1041c, U1041d

 - Add missing numeric keyword
 - Remove redundant arithmetic (0.0*pen_height etc.)
 - Clean up commented code blocks
 - Resolve or document TODO/XXX comments

 Phase 4: Critical Fixes (Tier D) - In Batches

 Batch 4A: Bar Calculation Pattern (5 files)
 - U10408, U10409, U10426, Ue004, Ue005
 - Fix: Change -y_radius-0.375*pen_height+0.125*0.5*pen_height to -y_radius
 - These all have identical pattern

 Batch 4B: Stem Overshoot (8 files) - KEEP AS-IS
 - U10412, U10414, U10415, U10416, U1041e, U1041f, U10420, U10423
 - Pattern: y_radius+0.375*pen_height or y_radius+0.5*pen_height
 - Decision: KEEP - This is intentional optical compensation (stems extend
 slightly beyond serif line)
 - Action: Leave stem overshoot intact; only fix unrelated issues in these
 files

 Batch 4C: Serif Positioning (4 files)
 - U1040d, U1040f, U10411, U10422
 - Various pen_height dependencies in serif calculations
 - Individual analysis required

 Key Files
 ┌──────────────────────────────────┬─────────────────────────────────────────┐
 │               File               │                  Role                   │
 ├──────────────────────────────────┼─────────────────────────────────────────┤
 │ calyptapis/src/letters/U10406.mp │ Reference template (cleanest structure) │
 ├──────────────────────────────────┼─────────────────────────────────────────┤
 │ calyptapis/src/letters/U10408.mp │ First fix target (simple bar pattern)   │
 ├──────────────────────────────────┼─────────────────────────────────────────┤
 │ calyptapis/src/letters/U10412.mp │ Test case for overshoot decision        │
 ├──────────────────────────────────┼─────────────────────────────────────────┤
 │ scripts/rebuild_glyphs.py        │ Selective rebuild tool                  │
 ├──────────────────────────────────┼─────────────────────────────────────────┤
 │ scripts/review_server.py         │ Visual verification                     │
 └──────────────────────────────────┴─────────────────────────────────────────┘
 Standard File Template

 % U+XXXXX DESERET CAPITAL LETTER NAME (char)
 beginfig(NNN);
   numeric x_diam, y_diam;
   x_diam := 2 * x_radius;
   y_diam := 2 * y_radius;

   pickup thin_pen;
   path bar;
   bar := (Ox, -y_radius) -- (Ox, y_radius);  % Absolute positions
   draw bar;

   pickup loz_pen;
   path serif;
   serif := (-(1/3) * x_radius, y_radius)
           -- ((1/3) * x_radius, y_radius);
   draw serif;
   draw serif shifted (0, -2*y_radius);

 endfig;

 Verification Process

 For each file modified:
 1. Run python3 scripts/rebuild_glyphs.py --glyphs NNN
 2. Check all 6 weights in review tool (http://localhost:5000)
 3. Criteria: No visible regression; improved alignment if fixing pen_height
 issue

 Design Decisions

 Stem overshoot (y_radius+0.375*pen_height): KEEP
 - This is intentional optical compensation
 - Stems extend slightly beyond serif line for clean visual appearance
 - Do NOT remove these patterns

 What TO fix:
 - Serif positions using pen_height (causes horizontal/vertical misalignment)
 - Bar endpoint calculations like
 -y_radius-0.375*pen_height+0.125*0.5*pen_height
 - Redundant arithmetic, dead code, missing keywords

 Estimated Scope

 - Phase 2: ~15 minutes (13 files, trivial changes)
 - Phase 3: ~30 minutes (6 files, careful review)
 - Phase 4A: ~20 minutes (5 files, identical pattern)
 - Phase 4B-C: ~60 minutes (12 files, individual testing)

 Total: ~2 hours of editing + verification time
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
```

Another issue in the font was evident after the first round of fixes, this one touchier and innate to METAPOST's handling of stroke paths.

```
 Fix Junction Gap in U10408 and U10409                                          
                                                                   
 Problem Statement
                                     
 Glyphs U10408 (Short A, 𐐈) and U10409 (Short Ah, 𐐉) have a visual defect: "
 chunk out of the lower right where the bottom sweep meets the vertical
 stroke." The problem is worse at heavier weights.

 Root Cause Analysis

 Current Geometry (U10408)

 % Vertical bar: lozenge pen rotated 90° (wide horizontally, thin vertically)
 pickup loz_pen rotated 90;
 bar := (Ox, -y_radius) -- (Ox, y_radius);
 draw bar;

 % Curved sweep: lozenge pen rotated -15°
 pickup loz_pen rotated -15;
 bar := (-0.75*x_radius,-1.0*y_radius)
         .. tension 0.9
         .. (Ox,-1.0*y_radius-0.25*pen_height)
         .. tension 0.9
         .. (0.75*x_radius,-1.0*y_radius);
 draw bar rotatedaround ((Ox,-y_radius),-15)
          shifted (...);

 The Gap

 The lozenge pen (loz_pen) is defined as:
 loz_pen = makepen(fullcircle xscaled (0.25*pen_height) yscaled pen_height);
 - Normal orientation: 0.25*pen_height wide, pen_height tall
 - Rotated 90°: pen_height wide, 0.25*pen_height tall

 When the vertical bar ends at (Ox, -y_radius):
 - The pen extends only ±0.125*pen_height vertically from center
 - Bottom edge of bar stroke: -y_radius - 0.125*pen_height

 The sweep, after rotation and shift, doesn't quite reach this bottom edge. The
  gap becomes more visible at heavier weights because pen_height is larger.

 Solution Options

 Option A: Extend Vertical Bar Downward (Recommended)

 Extend the bar past -y_radius so it overlaps with the sweep:
 bar := (Ox, -y_radius - 0.5*pen_height) -- (Ox, y_radius);
 - Simple, predictable
 - Ensures overlap at all weights
 - The extension is hidden behind the sweep

 Option B: Adjust Sweep Start Point

 Modify the sweep to reach higher into the bar region.
 - More complex transformation math
 - Risk of changing sweep's visual curve

 Option C: Use Round Pen for Bar

 Change loz_pen rotated 90 to thin_pen (round).
 - Would match U10407 (Short E) which has no gap
 - But changes the visual character of the glyph

 Recommended Approach: Option A

 Extend the vertical bar downward by 0.5*pen_height for both U10408 and U10409.

 Files to Modify
 File: calyptapis/src/letters/U10408.mp
 Figure: 408
 Change: Extend bar to -y_radius - 0.5*pen_height
 ────────────────────────────────────────
 File: calyptapis/src/letters/U10409.mp
 Figure: 409
 Change: Extend bar to -y_radius - 0.5*pen_height
 Exact Code Changes

 U10408.mp line 9:
 % Before:
 bar := (Ox, -y_radius) -- (Ox, y_radius);

 % After:
 bar := (Ox, -y_radius - 0.5*pen_height) -- (Ox, y_radius);

 U10409.mp line 9:
 % Before:
 bar := (Ox, -y_radius) -- (Ox, y_radius);

 % After:
 bar := (Ox, -y_radius - 0.5*pen_height) -- (Ox, y_radius);

 Related Files

 U10426 (Ew), Ue004, and Ue005 share similar structure but may or may not have
 the same gap issue. They should be checked after fixing 408/409.

 Verification

 1. Rebuild all 6 weights:
 cd calyptapis && mpost src/calyptapis.mp
 2. Then rebuild each weight directory.
 3. Visual inspection in review tool:
   - Focus on lower-right junction
   - Check UltraLight (baseline) through Black (worst case)
   - Verify no new artifacts introduced
 3. Acceptance criteria:
   - No visible gap at junction in any weight
   - Sweep still visually meets bar cleanly
   - No regression in overall glyph appearance
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
```

---

## Gumption Traps (~2026.2.6..12.25.00)

> OK, let's stick a pin in that action plan.  Yesterday I mostly fixed a font in METAPOST using Claude Code; it's not quite there but it's close, and I'll get it over the line.  I did use the specific feedback on the individual glyphs but haven't done the overall adjustment pending fixing a junction issue it's having trouble reasoning about.  What does it look like to extract parameters now?  The files look like this (with appropriate header for variables):

```metapost
% U+10408 DESERET CAPITAL LETTER SHORT A (𐐈)
beginfig(408) ;
  numeric x_diam, y_diam;
  x_diam := 2 * x_radius;
  y_diam := 2 * y_radius;

  pickup loz_pen rotated 90;
  path bar;
  bar := (Ox, -y_radius - 0.325*pen_height) -- (Ox, y_radius);
  draw bar;

  pickup loz_pen;
  path serif;
  serif := (-(1/3) * x_radius, y_radius)
          -- ((1/3) * x_radius, y_radius);
  draw serif;

  path sweep_base, sweep;
  sweep_base := (-0.75*x_radius,-1.0*y_radius)
          .. tension 0.9
          .. (Ox,-1.0*y_radius-0.25*pen_height)
          .. tension 0.9
          .. (0.75*x_radius,-1.0*y_radius);

  sweep := sweep_base rotatedaround ((Ox,-y_radius),-15)
           shifted (Ox-0.75*cosd(-15)*x_radius,Oy-0.75*sind(-15)*y_radius);

  rotatingdraw(sweep, -15, 0, 20, 0.6);
endfig;
```

From this basis, we devised a set of scripts to attempt to extract some parameters:
1. Level 1: Global Variables (description of pen, counter height, etc.)
2. Level 2: Per-Glyph Structure
3. Level 3: Semantic Analysis
4. Level 4: Cross-Glyph Pattern Recognition

Now, a caveat:  I am working with IDC Calyptapis, which is a slab serif font using a uniform stroke weight.  This is both good (in that it is fairly straightforward to model) and bad (in that it is less complicated than, say, Computer Modern would be).  But one has to start somewhere! and DTF Perdita will be more complex when we get to it.

I also circled back around and fixed the lingering junction issue at the lower right of five glyphs:
![[Pasted image 20260206140447.png]]
which now looks like:
![[Pasted image 20260206141209.png]]
(The tool to fix the curve was built by the LLM, but it still required hand-tuning to visually fix the parameters.)

Typography has irreducible gestalt properties which make it hard to quantify, but arguably this makes it better for consciousness research not worse. We need frameworks to lean into emergence, not try to abstract it out of existence. Typography has reasonably tight feedback loops, resists full formalization, and exhibits emergent properties to/effects on conscious minds.

So there are rather two incipient senses to this project:
1. Can typographical aesthetics be sufficiently parameterized to facilitate font creation or extension?  Kerning is an easy win but what about creating new target glyphs from scratch?
2. Can aesthetics be rendered amenable to “machine appreciation”?

Output from the parameter extraction first pass:
```
Parsed 47 glyphs
Found 5 pen definitions

Saving dataset to calyptapis/analysis/calyptapis_dataset.json

Analyzing construction patterns...
Saving analysis to calyptapis/analysis/construction_patterns.json

============================================================
SUMMARY
============================================================
Glyphs parsed: 47
Pens defined: 5
Global variables: 5

Path types used:
  serif: 48
  crossbar: 28
  loop: 25
  closed_path: 17
  straight_segment: 15
  curved_path: 6
  unknown: 3

Symmetry usage:
  vertical: 4
  horizontal: 1
  custom(0,0 to 0,y_radius): 3
  None: 1
  custom(0,0 to x_radius,0): 1

Complexity range: 1 - 5
Average complexity: 3.0
```

The weight are differentiated by stroke weight only.  (Some calculations like junctions depend slightly on the pen size, but in general this means the strokes from each weight sit directly on top of each other.)

Some observations about the parameter extraction:

1. It is still somewhat semantic rather than by shape.  (That is, whether it is recognized as a loop isn't because it draws a counter but because I named it a loop in the source.)
2. The complexity scale ranges from 1 to 5 and is a rather arbitrary bucket system rather than something more quantitative.  (In particular, it's not clear how it would be comparable across fonts.)
3. Still, it sort of understands the shapes because they are text descriptions rather than SVGs or vector OTFs.  This is potentially a big win, and it's somewhat exciting to me because I'm really the only person situated at the nexus of METAPOST fonts and LLM research right now.

Back to the earlier point about “machine appreciation”.  This doesn't mean that the machine experiences qualia or subjective experience (we're pending that question because it may be orthogonal).  What we want to know is if it can recognize coherence, detect violations, understand style, and generate consistently.  The basic hypothesis, then, is that verbal/textual representations like METAPOST enable a richer “appreciation” than a purely geometric representation fosters.  Text carries semantic information, encodes intent, reveals thinking by its structure (even if inconsistently), and exploits the deeply engrained associations that LLMs have trained into them between words, patterns, and concepts.

So we're going to run an experiment right now:  given only what we have in place right now, I am going to ask Claude to read my current glyphs and generate the simplest of symbols:  a zero.  I have some opinions about what this should look like, but I'll have a light touch for the first pass and guide if necessary.

> Examine the glyphs in calyptapis/src/letters and the summary data in scripts/analysis.  We need to prepare a set of Arabic numerals which correspond stylistically to the current letters of IDC Calyptapis.  First, give me a textual description of all ten digits (which do not exist yet).

(While that is spinning, let me write a ‘just-so’ story for why this may fail:  the training set of METAPOST files is too small; here there are only 47 different glyphs to compare to.)

```
⏺ Let me explore the existing glyphs and analysis data to understand the style
  of IDC Calyptapis.

⏺ Now let me read a few key glyphs to see specific constructions that would
  inform numeral design — especially the circle (Long O), bar forms, and more
  complex structures.

⏺ Let me read a few more to understand diagonal and crossbar treatments.

⏺ Now I have a thorough understanding of the design language. Here are my
  descriptions for all ten digits:

  ---
  Proposed Arabic Numerals for IDC Calyptapis

  The existing Deseret letters establish a clear vocabulary: uniform-weight
  strokes from thin_pen, discrete diamond-shaped (loz_pen) serifs at terminals,
  tension 0.9 curves built from circles and loops, and proportions governed by
  x_radius (0.45em) and y_radius (0.5em). The numerals should draw from this
  same kit of parts while remaining unmistakably recognizable as Arabic digits.

  0 — Zero

  A closed oval, slightly narrower than the full circle used for Long O
  (U+10404). Constructed as an outer_circle with the x-dimension scaled to
  approximately 3/4 of x_radius, preserving the full y_radius height. This
  compression distinguishes it from the letter O while remaining entirely native
   to the typeface's circular vocabulary. No serifs — the closed, unbroken
  contour is its own terminal. Drawn with thin_pen throughout.

  1 — One

  A vertical bar from baseline to cap height, drawn with thin_pen — structurally
   identical to the bar in Short I (U+10406). At the baseline, a horizontal
  loz_pen serif spanning 2/3 * x_radius, centered on the stroke. At the
  top-left, a short diagonal flag descending from the cap height toward the
  upper-left, roughly 1/3 x_radius long, angled approximately 45 degrees, drawn
  with thin_pen and capped with a small loz_pen rotated 45 tick. The flag gives
  the digit its identity without introducing any element foreign to the typeface
   — it echoes the serif-like articulations seen on Bee (U+10411) and Pe
  (U+10411).

  2 — Two

  An open S-curve reading top-to-bottom, terminating in a horizontal baseline
  stroke. Starting at upper-right with a loz_pen rotated 90 vertical serif tick,
   the stroke sweeps leftward across the top as a half-circle arc (tension 0.9,
  radius approximately 2/3 of the letter forms), curving down through the center
   and then rightward to the baseline. At the baseline, the curve meets a
  straight horizontal bar extending from approximately -0.75 * x_radius to 0.75
  * x_radius, drawn with thin_pen. The bar terminates at both ends with short
  loz_pen serif ticks. The overall profile is compact, fitting within the
  standard x_radius by y_radius bounding area.

  3 — Three

  Two open half-loops stacked vertically, both opening to the left — constructed
   from the same loop primitives used throughout the typeface (as in Long E,
  U+10401) but mirrored so the opening faces left rather than right. The upper
  loop is a half-circle arc from upper-left, sweeping right and back to center;
  the lower loop mirrors it below the midline. Both loops are scaled to 2/3 and
  shifted vertically by +/- 1/3 * y_radius, exactly as the double-loop letters
  are constructed. Where the two loops meet at the vertical center, the path
  passes through a shared junction point at the right edge. Each loop's free
  terminal (upper-left and lower-left) receives a horizontal loz_pen serif tick
  pointing inward.

  4 — Four

  A construction of two straight strokes and one crossbar. The primary vertical
  stroke descends from 2/3 * y_radius to -y_radius, positioned at 1/3 * x_radius
   right of center, drawn with thin_pen. A diagonal stroke runs from upper-left
  (approximately (-x_radius, 2/3 * y_radius)) down to the junction point at (1/3
   * x_radius, -1/6 * y_radius), also in thin_pen. A horizontal crossbar in
  thin_pen extends from (-x_radius, -1/6 * y_radius) through the junction and
  onward to (2/3 * x_radius, -1/6 * y_radius). At the top of the vertical
  stroke, a horizontal loz_pen serif; at the bottom, another. The diagonal's
  upper-left terminal gets a loz_pen rotated 45 tick. The open, airy
  construction with discrete serif accents is fully consistent with forms like
  Thee (U+1041C) and Kay (U+10417).

  5 — Five

  A horizontal bar at the top, a vertical descent on the left, and a lower bowl.
   The top bar extends from (-2/3 * x_radius, y_radius) to (2/3 * x_radius,
  y_radius), drawn with thin_pen, with loz_pen serif ticks at both ends. From
  the left end of this bar, a vertical stroke descends to the midline (-2/3 *
  x_radius, 0), where it smoothly transitions (tension 0.9) into a
  rightward-opening half-circle bowl occupying the lower half of the glyph,
  sweeping right, down, and back left to terminate near (-1/3 * x_radius,
  -y_radius). The bowl's terminal receives a loz_pen rotated 90 vertical serif
  tick. The combination of straight-to-curve transition recalls the construction
   of Chee (U+10415).

  6 — Six

  A sweeping arc descending from upper-right into a closed circular bowl at the
  bottom. The bowl is a full outer_circle scaled to 2/3, shifted downward by 1/3
   * y_radius — the same construction used for loops throughout the typeface.
  From the top of the bowl (approximately at its 12-o'clock position), a
  thin_pen arc continues upward and to the right with tension 0.9, terminating
  near (1/3 * x_radius, y_radius). This tail receives a loz_pen rotated 90
  vertical serif tick at its tip. The relationship between the open tail and the
   closed bowl echoes Long I (U+10400), where an open arc feeds into a closed
  circle.

  7 — Seven

  A horizontal bar at the top and a descending diagonal stroke — one of the
  simplest constructions, befitting this simple digit. The top bar spans from
  (-2/3 * x_radius, y_radius) to (2/3 * x_radius, y_radius), drawn with
  thin_pen, with loz_pen serif ticks at both ends. From the right end of the
  bar, a straight diagonal stroke descends to approximately (-1/6 * x_radius,
  -y_radius), drawn with thin_pen. The diagonal's lower terminal gets a loz_pen
  rotated 45 tick aligned with the stroke angle. No crossbar — the form is kept
  clean and minimal, consistent with the typeface's preference for economy.

  8 — Eight

  A figure-eight composed of two stacked closed loops, closely related to Ess
  (U+1041D) but without that letter's lateral extensions. The upper loop is a
  closed circle scaled to approximately 1/2, centered at (0, 1/2 * y_radius);
  the lower loop is a closed circle also scaled to 1/2, centered at (0, -1/2 *
  y_radius). Both are drawn with thin_pen at tension 0.9. The two loops share a
  tangent point at the vertical center, where the path crosses through (0, 0).
  The continuous crossing creates the figure-eight naturally. No serifs — like
  Zero, the closed contours are self-terminating. The lower loop may be made
  very slightly wider (scaled to 0.55 in x) for optical stability.

  9 — Nine

  The vertical inverse of Six. A closed circular bowl at the top — outer_circle
  scaled to 2/3, shifted upward by 1/3 * y_radius — with a thin_pen tail
  descending from the bowl's 6-o'clock position, curving slightly leftward with
  tension 0.9 to terminate near (-1/3 * x_radius, -y_radius). The tail's lower
  terminal receives a loz_pen rotated 90 vertical serif tick. The form is
  literally the 180-degree rotation of Six, honoring the typeface's deep
  commitment to rotational symmetry (as seen in the relationship between many
  Deseret letter pairs like Ay/H, Long I/Short I, etc.).

  ---
  Design principles maintained across all ten digits:
  - All primary strokes in thin_pen (uniform weight)
  - All terminal articulations in loz_pen (diamond serifs), rotated as
  appropriate to stroke direction
  - All curves at tension 0.9
  - All proportions expressed as fractions of x_radius and y_radius
  - Closed forms (0, 8) receive no serifs; open terminals always do
  - Loops and circles reuse the exact same path primitives as the existing
  letters
```

Not bad.  Let's proceed.

> Please prepare these ten glyphs.  The naming scheme is based on the Unicode code point so you'll want the ASCII code points as the file numbers.  You'll need to add them to the calyptapis.mp build file.

```
⏺ All done. Here's a summary of what was created:
  File: U0030.mp                                
  Fig: 30                                                                       
  Glyph: 0
  Construction: Closed oval (narrower than Long O — 0.75 x_radius width)        
  ────────────────────────────────────────                                      
  File: U0031.mp                                                                
  Fig: 31                                                                       
  Glyph: 1
  Construction: Vertical bar + top-left flag + baseline serif
  ────────────────────────────────────────
  File: U0032.mp
  Fig: 32
  Glyph: 2
  Construction: S-curve from upper-right descending to horizontal baseline bar
  ────────────────────────────────────────
  File: U0033.mp
  Fig: 33
  Glyph: 3
  Construction: Two half-loops stacked, opening left, with serif ticks
  ────────────────────────────────────────
  File: U0034.mp
  Fig: 34
  Glyph: 4
  Construction: Vertical bar + diagonal from upper-left + horizontal crossbar
  ────────────────────────────────────────
  File: U0035.mp
  Fig: 35
  Glyph: 5
  Construction: Top bar + left stem + lower bowl curving right
  ────────────────────────────────────────
  File: U0036.mp
  Fig: 36
  Glyph: 6
  Construction: Closed 2/3-circle bowl shifted down + ascending tail
  ────────────────────────────────────────
  File: U0037.mp
  Fig: 37
  Glyph: 7
  Construction: Top bar + descending diagonal + serif ticks
  ────────────────────────────────────────
  File: U0038.mp
  Fig: 38
  Glyph: 8
  Construction: Two stacked closed loops (upper slightly narrower for optical
    balance)
  ────────────────────────────────────────
  File: U0039.mp
  Fig: 39
  Glyph: 9
  Construction: Closed 2/3-circle bowl shifted up + descending tail (rotational
    inverse of 6)
  All files use the same parametric system (x_radius, y_radius, tension 0.9),
  thin_pen for primary strokes, loz_pen for serif articulations, and have been
  added to the build file.
```

Here's the first pass:
![[Pasted image 20260206153302.png]]

In a sense, not bad.  They generally do kind of match the style.

0. Fine.
1. Plausible.  Not nuts about it, but plausible.
2. Confused.
3. Barely plausible.  Look at 4015.
4. The stroke is the wrong direction.
5. The upper half is fine, the lower loop is confused.
6. ???
7. Plausible but needs a serif at the upper left.
8. Plausible.
9. ??? like 6

> There is a feedback file at ../scripts/glyph_reviews.json with details on    
  the Black version of the digits (which you just made).  Please review it and correct the glyphs based on its feedback.

```
Good — the feedback is specific.  Let me look at glyph 4015 (Ue003) which the reviewer references for the 3, and re-read my current files before fixing.

⏺ Now I have a clear picture of all the issues. Let me fix all seven glyphs:    
   
  - 2: The S-curve is a mess at Black weight. Simplify to arch + diagonal +     
  baseline.                                                                     
  - 3: Use the typeface's standard loop vocabulary (as in 4015) instead of      
  ad-hoc half-loops.                                                            
  - 4: The diagonal slants the wrong way (╲ instead of ╱). The high point should
   be at the vertical bar, not opposite.
  - 5: The bowl tries to loop back on itself. Simplify to a clean 3-node open
  arc.
  - 6: The tail goes {right} from the top of the bowl, creating a cusp. It
  should go {left}, flowing with the bowl's natural direction.
  - 7: Just needs a proper hanging serif at the left end of the top bar.
  - 9: Same tail direction problem as 6, inverted.
    
⏺ All seven glyphs corrected. Here's a summary of the changes:                  
  Digit: 2
  Problem: Complex 6-node S-curve collapsed at Black weight                     
  Fix: Replaced with 3 clean elements: half-circle arch + straight diagonal
    descent + baseline bar                                                      
  ────────────────────────────────────────                                      
  Digit: 3
  Problem: Ad-hoc half-loops didn't match typeface vocabulary
  Fix: Rebuilt using the standard loop construction from Ue003 (4015) — mirrored

    loops opening left, with a loz_pen rotated 90 connecting serif on the
    right spine
  ────────────────────────────────────────
  Digit: 4
  Problem: Diagonal slanted ╲ (high-left to low-right)
  Fix: Reversed to ╱ — diagonal now goes from crossbar height at the left up to
    the top of the vertical bar. Removed the extraneous top serif and
    diagonal-tip serif since the strokes now meet at clean junctions
  ────────────────────────────────────────
  Digit: 5
  Problem: 4-node bowl tried to loop back on itself
  Fix: Simplified to a clean 3-node open arc: stem → right side → bottom.
    Terminal serif changed to horizontal loz_pen at the bottom
  ────────────────────────────────────────
  Digit: 6
  Problem: Tail went {right} from bowl top, creating a cusp/reversal
  Fix: Tail now goes {left} from bowl top (matching the bowl's natural direction

    at point 0), curving up to a terminal at (-1/3*x_radius, y_radius)
  ────────────────────────────────────────
  Digit: 7
  Problem: Missing serif at upper left
  Fix: Replaced the tiny horizontal nub with a proper hanging loz_pen rotated
  -90
     serif (like Bee U+10411), descending from the left end of the top bar
  ────────────────────────────────────────
  Digit: 9
  Problem: Same cusp problem as 6, inverted
  Fix: Tail now goes {right} from bowl bottom (matching the bowl's direction at
    point 2), curving down to (1/3*x_radius, -y_radius) — the rotational
    inverse of 6
```

![[Pasted image 20260206155010.png]]

* 0, 1, 4, 6, 7, 8 all good enough to move forwards.
* We're not likely to improve on 2 or 3 much at this point without manual tuning.
* 6 and 9 are still very confused, like Phoenician _qop_ `𐤒`.
* 5 can likewise maybe be coaxed along with more wordcelery.

(At this rate, DTF Perdita is going to be a huge lift to get done in this time frame.)

After another round of feedback:

![[Pasted image 20260206160429.png]]
I know enough about METAPOST to know why Claude struggles with the loops on 5, 6, and 9:  circles define their extent by 8 points around the 360° and cannot go negative, so if you want something that extends past the starting point you either have to rotate the arc or you have to construct it from two separate curves.  That's teachable I think but I should probably model it to Claude instead of describing it in a prompt.  But these are very good for a cold intro like we did!

Now, aesthetically these aren't terrible, especially because they were designed by a blind man as it were.  I don't _like_ the 2, 3, 4, or 5 but they _match_ the font.  0, 1, 7, 8 are quite good; I like the baroque so personally I'd add a crossbar on the 7, and the upper right junction will need some spot tuning.  I prefer open 4s, and the top of the 2 should look more like the `𐐀`, as should 6 and 9.  There's not a great precedent for 5 in any case so it really is a human design problem at this point.  The 3 needs the notch at right but otherwise is great.

---

> The fact that typography has irreducible gestalt properties **makes it a better model for consciousness research**, not a worse one.
> 
> Consciousness isn't fully measurable either. We need frameworks that work with emergence, not against it.
> 
> Your submission could make the case: _"Here's a domain where we can study emergence concretely, with tight feedback loops, while acknowledging that some properties resist full formalization. The tools and insights from this work apply to any system with emergent properties - including minds."_

---

At this point, I have SVG outputs tuned by the machine.  The pipeline to produce an OTF file looks like this:

1. SVG files (by weight) →
2. FontForge Python script →
3. Map figure numbers to Unicode →
4. Import glyphs, set metadata →
5. Generate OTF per weight →
6. (Optional) Add kerning

Obviously there are a number of places that can break down and require intervention, but it's comprehensible.


IDC Calyptapis aside:  I asked for basic ASCII punctuation marks, and this was the first pass:
![[Pasted image 20260206205557.png]]
```
⏺ Done. Here's the full set with the mapping:                                   
  Char: .                                                                       
  File: U002e                                                                   
  Fig: 4023                                                                     
  Construction: drawdot at baseline                                    
  ────────────────────────────────────────                                    
  Char: ,                                                           
  File: U002c
  Fig: 4021
  Construction: drawdot + loz_pen tail descending left
  ────────────────────────────────────────
  Char: :
  File: U003a
  Fig: 4025
  Construction: Two drawdots at 1/3 y_radius and -y_radius
  ────────────────────────────────────────
  Char: ;
  File: U003b
  Fig: 4026
  Construction: Colon + comma tail on lower dot
  ────────────────────────────────────────
  Char: '
  File: U0027
  Fig: 27
  Construction: loz_pen rotated 90 tick, y_radius to 2/3 y_radius
  ────────────────────────────────────────
  Char: "
  File: U0022
  Fig: 22
  Construction: Two apostrophe ticks at ±1/4 x_radius
  ────────────────────────────────────────
  Char: ?
  File: U003f
  Fig: 4028
  Construction: Arch hook (4-node curve) + serif + dot below
  ────────────────────────────────────────
  Char: /
  File: U002f
  Fig: 4024
  Construction: Diagonal, lower-left to upper-right
  ────────────────────────────────────────
  Char: \
  File: U005c
  Fig: 4029
  Construction: Diagonal, upper-left to lower-right
  ────────────────────────────────────────
  Char: (
  File: U0028
  Fig: 28
  Construction: 3-node arc opening right, tension 0.9
  ────────────────────────────────────────
  Char: )
  File: U0029
  Fig: 29
  Construction: 3-node arc opening left, tension 0.9
  ────────────────────────────────────────
  Char: -
  File: U002d
  Fig: 4022
  Construction: Horizontal bar at Oy, ±1/3 x_radius
  ────────────────────────────────────────
  Char: +
  File: U002b
  Fig: 4020
  Construction: Crossing bars at center, ±1/2 x_radius / ±1/2 y_radius
  ────────────────────────────────────────
  Char: =
  File: U003d
  Fig: 4027
  Construction: Two horizontal bars at ±1/4 y_radius
  ────────────────────────────────────────
  Char: *
  File: U002a
  Fig: 4019
  Construction: Three strokes at 60° intervals, centered at 1/2 y_radius
  ────────────────────────────────────────
  Char: $
  File: U0024
  Fig: 24
  Construction: S-curve (cf. Es figure-eight) + vertical bar
  ────────────────────────────────────────
  Char: @
  File: U0040
  Fig: 40
  Construction: Outer arc (5/6 circle) + inner circle scaled 1/3
  Design notes:
  - Simple marks (.,:;'-") use drawdot and loz_pen ticks — the typeface's
  standard articulation vocabulary
  - Brackets () use the same tension-0.9 arc construction as the letter curves
  - Math operators (+-=) are centered at the origin with proportions relative to
   x_radius/y_radius
  - $ borrows the Es (U+1041D) S-curve construction, narrowed to 1/2 x_radius
  - @ will be the most weight-sensitive — the inner circle at 1/3 scale may
  merge at Black weight
```

![[Pasted image 20260206211736.png]]
```
⏺ Done. The new ? uses 416's (Jee) loop vocabulary directly: the same 5-node
  spiral loop scaled 2/3 and shifted to the upper portion, a bar descending from
   point 4, and the loz_pen rotated 90 serif extending upward from point 0. The 
  bottom serif is replaced with a dot at -(5/6)*y_radius to make it a question
  mark.                                                                         
```

![[Pasted image 20260206212021.png]]
Now, while I'm not nuts about `?` still (it's facing the wrong way at least), there's some consideration of form going into it by the LLM.

Like early computer art, the possibilities of this approach will probably have a hard ceiling for a long time.  You can conceive of interesting questions:  interpolate between a Bodoni and a Times New Roman, for example, or make a TNR-style Devanagari.

There won't be much work possible today due to family commitments but I'll try to squeeze a session or two in.  I've finally got the FontForge Python bindings working.

---

(no Day Five)

---

## Crunch Time (~2026.2.9..08.30.00)

If I want to validate the end of the pipeline then I need to get fonts building from the Calyptapis SVG glyph specimens today.  The difficulty with my previous attempts was that as the weights change, the strokes "stay still", that is, they grow visually thicker in each dimension but do not appear to move off their centerline.  SVGs once imported into FontForge do not do this well because they preserve the outline but not the source stroke.  Claude thinks that this should flow naturally from our arrangement thus far, but we'll see.

What I have in hand now:  some Python scripts designed to systematically extract the Deseret glyphs into font code points.

(Regarding minuscules:  classic Deseret typography never differentiated minuscules by form, only by size.  The Oversize specimen is the only 19th-century design I am aware of that employs different forms for some minuscules.  Jenkins, of course, started experimenting with other shapes in the Aughts.  WE only need to import and scale the letters appropriately; my guess as a typographer is that IDC Calyptapis minuscules will work if we supply the next weight up scaled down such that the stroke size is the same as the target; that is, use small versions of SemiBold for Regular and so forth.  In that case, we need a minuscule model that is heavier than Black.)

First pass:
![[Pasted image 20260209093713.png]]
The main issue here (which is common to FontForge and nothing I can lay at the feet of the LLM's attempt) is that the SVG directions lead to intersections being cut out.  This is touchy to handle even manually, so I'll try revisiting how the SVGs are produced by METAPOST (maybe I can preemptively reverse their direction in necessary cases).  The punctuation is being oddly sized because the scaling factor is currently pinned to the glyph height, which is clearly wrong for punctuation (we can use the internal `x_radius` parameter as a basis to tune this automatically).

(Typical of technology like MetaPost, there's a thorny mapping issue for code points, wherein I must use decimal code points because hexadecimal isn't supported—okay—but then I am limited to 32767 as my maximum number, whereas Deseret is far beyond that point.  Thus I MUST have a number mapping, sigh.  Fortunately, using modulo 32768 actually results in disjoint sets for everything we care about.)

ANYWAY, back to today's goals:
1. Get automatic OTF building, including kerning.
2. Start working on DTF Perdita automatic creation from the Oversize specimen.

Regarding the Oversize specimen:  my co-author informs me that the LDS Church History Library actually did a much higher-resolution scan than the cell phone snapshot I am using ([CHL MS 16662](https://catalog.churchofjesuschrist.org/assets/04c8ba76-37cb-4325-91b1-8eec3f086e56/0/2?lang=eng)).  (Notice that the first page has a different El `𐐢` than the specimen itself; I like the variant more than the original.)  It's also missing an exemplar of Thee `𐐜` but includes the only verified instance of the SQUARE vowel; I could go on (it's labeled 1852 but is clearly post-1859), but I'll refrain.  (Aside:  since it's missing Thee `𐐜` it's a perfect microcosmic case study for our LLM design experiment.  I have my own opinions, of course.)

So the current status:
1. We have an automatic MetaPost build script from MP files.
2. Claude can make a reasonably good pass at designing new characters from existing exemplars.

Our missing parts:
1. The resulting fonts have intersection/direction issues that we need to resolve.
2. We haven't looked at the development from image files yet (i.e. image to strokes in MetaPost).

Claude suggests trying to fix directions in METAPOST rather than in FontForge.  I'm skeptical of Claude's "quick path" because we are producing strokes not shapes. All strokes are "outside" in that sense: counters result from being interior to strokes not from being drawn as an explicit negative space.  That is, strokes outline where counters emerge from overlapping stroke geometry, not explicit negative space.  This is METAPOST's (and METAFONT's) secret weapon but it's very unconventional for digital font design.

So I'm going to pend this in favor of a more concrete research problem:  producing stroke descriptions from image files of glyph specimens.
1. Image preprocessing (crop, threshold, align)
2. Stroke skeleton extraction (_Bauplan_)
3. Width measurement along Bauplan
4. METAPOST parameter fitting
5. Code generation

There are two hypotheses we can make about the production of DTF Perdita:
1. METAPOST exemplars will be sufficient to design new glyphs because of digitally native production.
2. Human glyphs will be better because of semantic naming and organization.

I can make a case for either of these, because I don't really know yet which prevails.  Too much of a just-so-story for my tastes but it is what it is.

```
python3 ./scripts/extract_skeleton.py design/ --threshold 140 --blur 3 --smooth 2 --prune
Input: design/
Output: design/skeleton_output
Found 4 images
============================================================

Processing U10400.png...
  Parameters: threshold=140, kernel=3, blur=3, smooth=2
  Image size: (892, 581)
  Applied Gaussian blur (3x3)
  Binary pixels: 161209
  Computing skeleton...
  Smoothing skeleton (2 iterations)...
  Pruning spurs...
  Skeleton pixels: 347
  Saved: U10400_skeleton_viz.png
```
Et cetera.

That yields an extracted skeleton like this:
![[U10400_skeleton_viz.png]]

which is pretty good but I tuned it anyway because those are too fragmented still.

Really, though, this is a pain.  Machine vision algorithms like OpenCV kind of suck in practice.  Let's try [`autotrace`](https://github.com/autotrace/autotrace) which should be able to get us centerlines at least.
![[U10400_centerline.svg]]
(The face I'm making right now isn't very happy.)  That could be cleaned up, or maybe there are some parameters we can tune, but another idea occurs to me:  give Claude a basic METAPOST file and have the system tune the parameters to fit the base shape instead.  This really does situate the font-as-code approach at the front and center.  Structurally, we have a swirl and a serif.  The swirl could be a bit hard as a single stroke in METAPOST because of pen limitations, but we have the pen rotation macro now so perhaps we can adapt that to scale the pen as it travels.  Essentially, we have a left-facing `6` with two-stroke serif.

So I talked through a verbal description of the glyph with Claude (as above) then we co-constructed an optimization algorithm with 11 tunable parameters.

![[Pasted image 20260209200639.png]]
If I'm being bullish, then I say that the optimization successfully extracted a structurally correct parametric representation from the specimen.  It's not pixel-perfect but the parameters make further refinement tractable.  This demonstrates that METAPOST's tool-based representation is amenable to machine learning, unlike black-box geometric approaches.  If I'm being bearish, then I can focus on the inability to settle the thickness and the angular tension of the components.

The pitch at this point is essentially:
> We demonstrate an LLM-enabled pipeline to treat fonts as programs (METAPOST) rather than geometric data, which enables LLM reasoning about design intent. The specimen extraction has challenges (connectivity), but the parametric analysis and generation framework is novel and shows promise.

---

## Day Seven

But that's not good enough.  I want something a bit stronger.  And we're wandering a bit from the original vision of generative font work.  (We didn't necessarily abandon it—it was demonstrated to some extent with IDC Calyptapis—but we won't have time to run it again with DTF Perdita.)  So what I propose today is to make a constrained interactive fitting tool and using that as the basis for deriving DTF Perdita.  (Incidentally, I discovered that I had started a manual production of Perdita, which I have assiduously not used during this project.)

So we cooked up a tool to let me set fixed points (including directions) over the image.

![[Pasted image 20260210094237.png]]

which renders in METAPOST with default tensions as:
![[Pasted image 20260210092829.png]]
Not bad!  Let's try optimizing it.

```
python3 optimize_metapost.py design/U10403.png \
  --template generated_path_parameterized.mp \
  --metadata optimizer_metadata.json \
  --output optimized_output

Loaded 28 parameters
  28 are free to optimize
  0 are fixed

Validating template...
✓ Template validates successfully
Initial error: 0.8820
Saved initial render to: optimized_output/initial_render.png

Optimizing 28 free parameters...
============================================================
  Error: 0.8820
  ...
```

Oh no.  There are way too many free parameters to optimize over here and I am skeptical there's an algorithm good enough to do it in any reasonable amount of time.
![[Pasted image 20260210125833.png]]

Let's couple them so there are fewer to check:  there should only be two limiting pen sizes, and absolute $x$ and $y$ positions should instead be proportions within an overall vertical and horizontal scale.  That can reduce us to 10 or 12 parameters easily.



In this case, the development pipeline looks like this:
1. Manual image extraction (pretty much always a requirement)
2. Manual skeleton hinting (superior to any tool I had available in this time span but possibly not globally optimal)
3. Automatic production of METAPOST file
4. Automatic optimization of METAPOST file
5. Automatic production of SVGs
6. Automatic ingestment of SVGs to FontForge
7. Automatic production of OTF

There are a few good spots for manual intervention (back to our centaur thesis) such as between 6 and 7 if I can't figure out a better solution to the vector directionality and intersection gaps as with Calyptapis.
