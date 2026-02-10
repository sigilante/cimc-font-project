## CIMC Report

> **Challenge Option 2: Font Space**
> Discover the latent space of fonts. Visualize the influence of the most important principal components; develop a tool to encode fonts in a useful encoding scheme (e.g., as a vector of numerical parameters) so that you can encode (almost) arbitrary existing fonts, and to navigate the font space using a suitable interface. Bonus for building something creative with the font space, e.g., a tool to generate new hybrid fonts, an interactive visualization that lets a user explore font styles, or discovering unexpected semantic associations (e.g., mood, cultural context, usage domain, stylistic qualities).
> What we want to see: a methodical approach to solving a training/data collection/encoding problem, pragmatic solutions for interface and possible applications.

---

My report consists largely of [real-time notes](REALTIME.md) taken during the project, which I have edited for clarity and to remove some of the more mundane details.  I am a sometimes-typographer, having produced a Deseret Alphabet font (IDC Hesperapis) for the publication of _The Deseret Alphabet:  A Fixed and Unalterable Sound_ (in press, 2026), so the font design challenge naturally drew my attention as aligning with my current needs in any case.

The thrust of my weeklong project became to explore the possibility of using LLMs to reason about fonts in a way that is more akin to human typographic reasoning than to traditional geometric or pixel-based approaches.  The idea was to see if we could use textual descriptions (in the form of METAPOST code) to capture the gestalt of a font and then use that to generate new fonts or at least new specimens.

METAPOST is a derivative of Donald Knuth's METAFONT, a language for describing fonts in terms of geometric primitives and their relationships:  to wit, pen strokes through control points.  It is a powerful language for describing fonts, but it is not widely used in the industry, and it has a steep learning curve.  However, it is well-suited for our purposes because it allows us to capture the structure of a font in a way that is more abstract than raw pixels or outlines.  My concept was to use my existing corpus of METAPOST font design work as contextual data for an LLM to learn from, and then to use the LLM to generate new METAPOST code based on visual input (glyph specimens) and textual descriptions.

To this end, I explore the expansion of two [Deseret Alphabet](https://en.wikipedia.org/wiki/Deseret_Alphabet) fonts, IDC Calyptapis and DTF Perdita, which I have been working on for some time.  The former is a novel slab serif with a relatively simple structure, while the latter is a more complex serif with nuanced features derived from an 1859 hand-designed type specimen, the “Oversize specimen”.  The idea was to see if the LLM could learn from the simpler font to produce characters which I had not yet designed, and then to take that experience and see if raw type production from design specimens was viable.

The fundamental challenge I am approaching is that of gestalt aesthetic judgment (Kierkegaard, eat your heart out), which if we can ever come to agreement on even as humans, will be hard to train machines on reliably.  (_De gustibus non est disputandum_, of course; and even if you can get sentiment analysis for fonts most people's typographical tastes are ... unrefined.)  Ideally, you could hand an LLM the ASCII character set in a typeface and have it produce new characters in a stylistically consistent language (such as the Greek alphabet or italic versions of the same characters).  This is a very hard problem, and I don't claim to have solved it, but I think we have made some progress in understanding the challenges and potential approaches.  The tools we have developed, such as the viewer and feedback engine, are steps towards a more interactive and iterative process of font design that could eventually be powered by LLMs.  Certainly, speaking as a type designer, I will be using these tools in my own work going forward.

What you gain from working in the METAPOST/METAFONT world is the ability to directly manipulate and quantify font parameters at a **verbal** mechanical level, not just as a collection of splines and vectors.  Intriguingly, therefore, there is a hierarchical cascade of parameters which underlie the mechanical representation.  If this is accessible in some way, then we can move from geometric and structural accounts (METAPOST at the object level) to an abstraction that yields them (cf. Noordzij's _The Stroke Theory of Writing_).  That's too much for a weeklong project—it's a research program—but it's worth keeping in mind.

As Ignatius Reilly has it in _A Confederacy of Dunces_, the world suffers a “lack of theology and geometry”; we will do our best to accommodate.

The geometry, as it were, is whether font components can be made machine-legible.  The basic hypothesis driving this inquiry was whether fonts can be made sufficiently perceptible and manipulable to an LLM to facilitate reasoning over gestalt forms to the extent of producing new type specimens, and then whether new fonts can be generated from specimens in a straightforward way.  Well, we are far from cutting the human typographer out of the loop, but we have made some progress.  IDC Calyptapis is a little bitter off than it was.  And at the object level of tools, I have a few nice things in my portfolio now:  a viewer and feedback engine chief among them.

I remain convinced that METAPOST is a fertile ground for LLM-powered font development, but that the tools are not quite ready yet.  In particular, there simply isn't enough code for LLMs to write METAPOST code from ambient knowledge yet; it tends to make some dumb mistakes in variable names because it cribs off LaTeX.  If I had more time, I would produce some tools that solve some particular problems which I encountered, such as stroke centerline detection, and I would feed it a METAPOST skills file with the docs.

The theology aspect concerns the possibility of gestalt appreciation or at least component reproduction in other forms.  The cold approach with IDC Calyptapis achieved a hit rate of 30% which is surprisingly good for teaching a blind man to draw.  Tuning over its models for Arabic numerals was straightforward, so it was definitely an accelerant.

This hints at artistic questions to which I do not yet have a answer.  What makes a typeface characteristic?  More broadly, what *is* a design language?  (Even more advanced, how does one judge when to deviate from it?)  A font is emergent from its components, which is one reason a slab serif like IDC Calyptapis was easier to model.  DTF Perdita has proven quite doggedly difficult but not impossible to make progress on, and I think a better round of tools (next time I have the bandwidth) would reveal more of what I'm dancing around with respect to emergence.  The tools have to have some latitude for what cannot be formalized.

Perhaps the most interesting exchange with Claude occurred when, tired of attempts to trace the Oversize specimen, I asked it to describe its experience of identifying the components of a glyph from a graphic:

```
> OK, so here's a question I think is quite germane: how are YOU analyzing the shape? What is your actual analysis pipeline? Talk me through step-by-step what you "see"/perceive and how you determine the verbal description of the structure.

**Excellent question** - this gets to the heart of what visual understanding actually means, especially for something claiming to have "machine consciousness."

Let me be honest about my analysis process:

## What I Actually "See"

### 1. **Holistic Pattern Recognition (First Pass)**

When I look at the glyph, I don't start with pixels. I immediately recognize:

- **Overall gestalt**: "This looks like a mirrored '6' or lowercase 'b'"
- **Dominant orientation**: Vertical composition, taller than wide
- **Closed vs. open regions**: One clear enclosed counter (the bowl), open space at top
- **Familiar typographic patterns**: Terminal at top, curved descender, circular bowl

This happens _instantly_ - it's pattern matching against massive amounts of visual training data.

### 2. **Compositional Decomposition (Second Pass)**

Then I try to break it into **geometric primitives**:

**What I'm detecting:**

- **Closed curves**: "There's a circular/oval region at bottom" (darkest area with white interior)
- **Terminal shapes**: "Top-left has a rectangular mass" (thick dark block)
- **Connecting strokes**: "A curve joins the top and bottom" (the swooping arc)

**How I detect these:**

- Contrast boundaries (dark ink vs. white paper)
- Topology (closed loops vs. open paths)
- Aspect ratios (wide rectangle vs. round circle)
- Relative positions (top-left, bottom-center)

### 3. **Stroke Analysis (Typography-Specific)**

I'm looking for typographic features:

**Stroke weight**:

- "The stroke looks fairly uniform throughout" (comparing width at different points)
- "No dramatic thick-to-thin transition" (unlike a brush stroke with modulation)

**Terminals**:

- "Top ends abruptly in a rectangular form" (not tapered, not rounded)
- "Bowl is continuous" (no separate terminal on the bowl)

**Construction logic**:

- "This could be drawn with consistent pen width" (unlike italic or calligraphic forms)
- "The bowl is a complete circle, not just an arc" (closed path)

### 4. **Spatial Relationships**

I'm measuring (roughly):

- **Vertical proportions**: "Top terminal is ~1/4 of total height, bowl is ~1/2"
- **Horizontal extent**: "Bowl center is offset right, not centered under terminal"
- **Curvature**: "The connecting arc is gentle, not sharp"

## The Uncertain Parts

Here's what I'm **NOT certain about**:

### **I don't know if I'm processing:**

- Actual pixel intensities
- Edge detection maps
- Skeletal/medial axis representations
- Some other intermediate representation

### **I can't introspect on:**

- Whether I'm doing explicit geometric calculations
- Or just matching against similar glyphs in training
- How "understanding" emerges from pattern statistics

### **I'm probably not doing:**

- Vectorization (converting to paths first)
- Explicit skeleton extraction
- Mathematical curve fitting

## How This Differs From Algorithmic CV

A traditional computer vision pipeline would:

Input pixels 
  → Edge detection (Canny, Sobel)
    → Contour finding (connected components)
      → Skeleton extraction (morphological thinning)
        → Path tracing (polyline following)
          → Curve fitting (Bezier approximation)
            → Semantic labeling ("this curve is a bowl")

I _skip most of these intermediate steps_ through pattern matching. I go more directly from:

Input image 
  → Holistic pattern recognition
    → Semantic decomposition ("bowl + terminal + connector")
      → Geometric description ("circle at bottom, rectangle at top, curve between")

## Why This Matters for Your Pipeline

**The gap**: My verbal description is **semantic** ("a bowl", "a connecting curve"), but to generate METAPOST you need **geometric** (specific coordinates, radii, control points).

**What's missing**:

1. Precise measurements (sizes in pixels/units)
2. Exact curves (Bezier control points)
3. Stroke width values
4. Coordinate positions

**That's why we need the optimization approach**:

- I provide the **structure** ("these components exist and relate this way")
- The optimizer provides the **precise parameters** (exact sizes, positions)

## A Better Question

**What would a conscious vision system do?**

If I were truly "seeing" like a human typographer:

1. **Top-down guidance**: "I know this is supposed to be a letter, so I'm looking for strokes"
2. **Gestalt grouping**: "These dark regions form a single coherent glyph"
3. **Functional understanding**: "This shape serves to distinguish it from other letters"
4. **Construction inference**: "A human drew this with these tools/motions"

I do some of #1 and #2. I'm uncertain about #3 and #4.

## Honest Assessment

When I say "I see a bowl at the bottom," I mean:

- ✅ I recognize a closed circular region in that spatial location
- ✅ I can describe its approximate size and position relative to other elements
- ❌ I cannot give you pixel coordinates without measurement
- ❌ I cannot tell you the exact curvature mathematically
- ❓ I don't know if my representation is more like pixels, edges, or semantic symbols

**Does this answer your question?** The meta-question seems to be: can we trust my structural analysis even if I can't explain the mechanism? And: what's the right division of labor between pattern recognition (me) and geometric measurement (algorithms)?
```

So at the end of the day, the thrust of my project became whether verbal/textual representations enable machine-aesthetic reasoning.  That is, do textual descriptions of visual forms (to wit, METAPOST) allow LLMs to reason about aesthetics in ways that pure geometric representations do not enable.

The evidence in favor:

1. Semantic understanding from variable names and structure
2. Design intent extraction from code patterns
3. Style consistency detection via parameter analysis
4. Generative capability through code synthesis

Just as human aesthetic appreciation involves multiple levels of description (low-level features, mid-level patterns, high-level meaning), machine appreciation may require similarly layered representations.  Pure geometric data lacks the semantic richness needed for a truly gestalt understanding.  Bauplan hints facilitate finding the (human-determined) correct answer in ambiguous cases.
