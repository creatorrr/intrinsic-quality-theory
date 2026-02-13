# RFC-0001: Experimental Framing & Locus-Dependence Clarification

**Status:** Draft (proposed edits to IQT Draft v1.8; intended for v1.8.1 or v1.9)

**Files in scope:**
- `iqt.md` (full paper)
- `INTRODUCTION.md` (gentle intro)

**Non-goal:** introduce or litigate “direct vs indirect observation” as a philosophical distinction. This RFC removes/avoids that framing entirely.

---

## 1) Why change anything?

### 1.1 Optics / seriousness risk
Right now the gentle intro opens with psychedelics and time phenomenology. Even with the “not trip reports” disclaimer, leading with psychedelics can prime a reviewer (or casual reader) to treat the whole program as vibe-y rather than as a constrained, falsifiable physics-to-neuro program.

**Desired read:** IQT is a geometric identity thesis with multiple orthogonal empirical wedges. Psychedelics are one wedge, not the flagship.

### 1.2 Empirical breadth is a feature (but not surfaced)
The core temporal-geometry mapping is not inherently “about psychedelics.” It’s about *interventions that reshape effective integration windows / correlator families*.

So: keep Protocol 3, but explicitly frame it as *one member* of a larger intervention class that also includes perturbation (TMS), therapeutic stimulation (ECT), targeted clinical stimulation (iEEG/SEEG), and imaging correlates (fMRI/PET) as readouts.

### 1.3 Locus-dependence is core (and ontological), but its empirical bite is underplayed
IQT already commits to perspectival relativity / “no view from nowhere.” The missing piece (for some readers) is that this is not merely *epistemic hygiene* (“our instruments are limited”). It is an *ontological feature of quality itself*:

- a quality is defined **per bounded region** (per diamond);
- adding an instrument is not a passive “readout” — it enlarges/changes the region and therefore changes the algebra;
- the quality of **brain-only** and **brain+instrument** are genuinely different because they are qualities of different diamonds.

This reframes a known headache in consciousness science — cross-modal disagreement between markers (e.g., EEG vs fMRI) — as a predicted feature: two instruments that “measure the same brain state” are, in IQT terms, probing **two different effective diamonds**. The question becomes whether the *pattern* of disagreement is geometry-predictable, not whether disagreement is “noise.”

We should make this explicit without dragging in “direct vs indirect.”

---

## 2) Proposed edits (by file)

### 2.1 `INTRODUCTION.md`

#### Change A — Replace the psychedelic-first opening hook
**Current:** opens with “Psilocybin stretches your sense of time…”

**Proposed replacement (example text):**
```markdown
## What is this paper about?

Anesthesia can erase experience. Split-brain surgery can fracture it. Brain stimulation can perturb it. And certain compounds can radically reshape the felt structure of time.

Intrinsic Quality Theory (IQT) claims these aren’t disconnected curiosities: they are predictable consequences of a single geometric fact — the shape of the bounded spacetime region over which your brain integrates information.

IQT is an attempt to solve the Hard Problem by an identity thesis: the intrinsic physical state of a bounded region *is* its phenomenal quality. The pay-off is that this identity yields concrete, pre-registerable experiments with explicit failure conditions.
```

Notes:
- Psychedelics still appear, but as one item in a list of standard interventions.
- Tone stays concrete and scientific.

#### Change B — Rename “Protocol 3: The Psychedelics Test” to a mechanism-first label
**Proposed:**
- “Protocol 3: Temporal Integration Modulation”
- or “Protocol 3: Temporal Window Modulation”

Under that heading, keep the current substance-specific predictions (psilocybin/ketamine/DMT/midazolam), but position them as a *pharmacological arm*.

#### Change C — Add a short “Other intervention families” paragraph (no new protocol needed)
Add a short paragraph either:
- at the start of “How will it be tested?”, or
- as a sub-bullet under Protocol 3.

Example:
```markdown
Beyond pharmacology, the same geometric quantities can be pushed (or read out) with perturbation and clinical stimulation: TMS-EEG (causal perturbation), intracranial stimulation in epilepsy monitoring (precise local perturbation), and disconnection cases such as split brain (structural removal of cross-boundary correlators).
```

#### Change D — Make locus-dependence explicit (one paragraph)
Place this where “perspectival relativity” is introduced (democracy / diamonds section), phrased as:
- ontic claim: quality is defined *per region / locus*;
- epistemic corollary: any measurement pipeline picks an effective algebra defined by the instrument;
- no mention of “direct vs indirect.”

Suggested paragraph:
```markdown
A key consequence is locus-dependence: quality is defined for a bounded region (a diamond), and there is no “view from nowhere.” Any measurement is a *physical coupling* that effectively enlarges or reshapes the relevant region, changing the effective algebra. So “brain-only” and “brain+instrument” have genuinely different qualities because they are different diamonds.

Concretely, two instruments that “measure the same brain state” (e.g., EEG vs fMRI) are probing two different effective diamonds, and partial disagreement between their consciousness markers is not automatically “noise.” IQT predicts that the *pattern* of disagreement is geometry-dependent: modalities that trade temporal for spatial resolution should disagree most when temporal and spatial structure are dissociated — precisely the regimes targeted by temporal-integration modulation and perturbational protocols.
```

---

### 2.2 `iqt.md`

#### Change E — Abstract / Plain-English summary: lead mechanism-first *without* hiding specificity
Right now the abstract flags three protocols, with Protocol 3 described as psychedelic modulation. Keep the substance-specificity (it signals “this is pre-specifiable”), but ensure the first impression is “three orthogonal protocols” rather than “psychedelics are the headline.”

Minimal edit options:
- reorder the protocol list (anesthesia, overlap, temporal integration modulation), and in the temporal integration clause list interventions in a *second beat*:  
  “...temporal integration modulation via pharmacological (psilocybin, ketamine, DMT), perturbational (TMS‑EEG), and clinical (intracranial stimulation) interventions.”
- keep drug names, but avoid leading the abstract with them (no “Psilocybin does X” as the opener); instead, treat them as concrete examples inside a mechanism-first sentence.
- if space is tight, keep the mechanism-first label in the abstract and move the full list of example interventions to the first paragraph of §5.3 (but keep at least one named example in the abstract to signal specificity).

#### Change F — §2.6 (temporal phenomenology): generalize language from “compounds” to “interventions”
Current phrasing (paraphrase): “Crucially, compounds that alter effective integration timescales…”

Proposed:
- “Crucially, **interventions** that alter effective integration timescales — pharmacological, electrical, or magnetic — reshape the effective diamond…”
- Include 1–2 citations showing TMS-EEG perturbation is already used to track loss/recovery of consciousness via complexity/effective connectivity.

#### Change G — §5.3 Protocol 3: make “psychedelics” a sub-arm
Keep the existing substance predictions as **Arm 3A (Pharmacological modulation)**.

Add brief, optional arms (no need to over-specify; these can be marked “extensions”):

- **Arm 3B (Perturbational modulation; TMS-EEG):**
  - Use TMS pulse trains / paired-pulse paradigms to alter effective temporal depth, then measure the same multi-scale persistence peak shift.
  - This slots naturally into IQT because it is explicitly about perturbing a bounded region and reading out propagation / complexity.

- **Arm 3C (Clinical stimulation / ECT as a coarse lever):**
  - ECT is a strong, global perturbation; the claim is not that it gives fine control, but that it is another “shape shock” with measurable pre/post changes in integration window proxies.
  - Mark as a “high variance / low precision” lever (useful for falsification if the directionality is wrong, not for fine parameter fits).

- **Readout adjuncts (MRI/PET):**
  - Not primary tests of the identity thesis, but useful to constrain which networks / hubs change when the temporal window shifts.

#### Change H — Add a short “Additional empirical avenues” subsection (either end of §5 or in §7 Open Problems)
Three additions requested in discussion:

1) **Synesthesia epidemiology as a potentially primary geometric prediction**
- Strong form (promotable to a primary test *if* the geometry yields sharp constraints): derive a **rank-ordering** (and possible impossibility claims) over cross-modal pairings *from the allowed/disallowed correlator geometries alone* — e.g. “grapheme→color common,” “taste→sound rare,” “(say) proprioception→smell effectively impossible” — and compare to population prevalence / phenotype catalogs.
- Weak form (cross-check, until the strong form is actually derived): “observed distributions should be biased toward the allowed set” and away from disallowed geometries.
- Implementation note: to avoid story-time, the paper should be explicit about what would count as a win (pre-registered rank-order match) vs a loss (systematic inversions), and should acknowledge confounds (diagnostic criteria, reporting bias, cultural effects, heterogeneity across synesthesia types).

2) **Disconnection and split-brain style cases**
- Treat split brain as a naturally occurring “correlator cut”: remove cross-hemisphere correlators; predict multi-locus persistence changes and altered unity metrics.

3) **Harmless electrode stimulation protocols**
- Explicitly position the overlap protocol’s perturbational arm as a standard clinical research modality (epilepsy monitoring) with known safety/ethics constraints.

#### Change I — Add one boxed clarification: “Instrument-relative diamonds (measurement changes the locus)”
Place near the effective-theory bridge discussion:

- The effective algebra is instrument-defined (spatial resolution, temporal bandwidth, parcellation, sampling), *but* the deeper point is ontological: coupling an instrument does not merely reveal a pre-existing “brain quality.” It creates a larger **brain+instrument** diamond with a different algebra-state pair, hence a different quality.
- Pre-registration is the guardrail against post-hoc redefinition of the effective locus / algebra (“moving the diamond” to chase significance).
- This is the operational face of perspectival relativity: different loci → different qualities; measurement is just controlled locus-extension.

#### Change J — Promote cross-modal marker disagreement from “problem” to “prediction”
Add a short paragraph (either in the boxed clarification or immediately after) making the concrete consequence legible:

- Two instruments aimed at the “same” brain condition (EEG vs fMRI; iEEG vs MEG) are, in IQT terms, measuring **different effective diamonds**.
- Therefore, *systematic* disagreement between their “consciousness markers” is expected in some regimes — not as a methodological embarrassment but as perspectival relativity applied to measurement.
- Falsifiable add-on: the **pattern** of disagreement should be predictable from the geometry of the respective instrument diamonds. A concrete target is EEG (high temporal, low spatial) vs fMRI (low temporal, high spatial): they should diverge most when the temporal and spatial structure of quality are dissociated — precisely the sort of dissociation the temporal-integration modulation and perturbational protocols are designed to induce.

---

## 3) Rationale (why these changes preserve the theory)

### 3.1 We are not weakening Protocol 3 — we’re strengthening its positioning
Leading with psychedelics is rhetorically risky; treating them as one arm of a general “temporal integration modulation” mechanism is rhetorically safer and conceptually cleaner.

### 3.2 The locus point is already inside IQT; we’re just making it legible
IQT’s “no view from nowhere” is not an optional philosophical flourish — it’s directly tied to:
- democracy of diamonds (many loci),
- restriction maps (nested loci),
- effective-theory bridge (instrument-defined loci).

Making that explicit reduces misunderstanding without changing any math.

### 3.3 Avoiding “direct vs indirect” is correct hygiene
That distinction is:
- philosophically noisy,
- easy to derail into epistemology wars,
- unnecessary for IQT’s core commitments.

We keep the useful content (“every operationalization is from some locus using some interface”) and drop the distracting label.

---

## 4) Background notes / implementation guidance

### 4.1 Wording guidance: “psychedelics” vs “pharmacological modulation”
- In `INTRODUCTION.md`, avoid opening with drug names.
- In `iqt.md`, allow drug names in §5.3 (where experimental details live), but keep abstract language mechanism-first.

### 4.2 Guardrail: don’t promise precision where the lever is crude
- TMS / intracranial stimulation = good precision, good falsifiability.
- ECT = blunt instrument; include as optional extension, explicitly high-variance.
- fMRI/PET = readout adjuncts; not direct measures of “quality,” but useful constraints on bridge hypotheses.

### 4.3 Ethics and safety framing
When adding stimulation-related language, keep it clearly within:
- standard clinical monitoring contexts,
- standard stimulation-mapping practice,
- explicit pre-registered thresholds and stopping criteria.

### 4.4 Synesthesia note (how to avoid overclaiming while keeping the upside)
Default framing should be conservative *until* the math delivers something sharp:

- Baseline: “distributional constraints consistent with IQT geometry” (a cross-check).
- But explicitly flag the upside: if the allowed/disallowed geometry becomes sharp enough to yield **pre-registered rank-orderings** (or impossibility claims) over synesthetic pairings, then synesthesia becomes a **primary test** — a novel prediction about the human phenomenological possibility space derived from geometry and checked by epidemiology.
- Guardrail: don’t promise this in prose unless the paper can actually write down the constraint → ranking pipeline in a way that is hard to fudge post hoc.

---

## 5) Suggested citations to add (minimal but high-signal)

**TMS-EEG perturbation & consciousness metrics**
- Casali, A. G., et al. (2013). *A theoretically based index of consciousness independent of sensory processing and behavior.* **Science Translational Medicine**. DOI: 10.1126/scitranslmed.3006294
- Ferrarelli, F., et al. (2010). *Breakdown in cortical effective connectivity during midazolam-induced loss of consciousness.* **PNAS**. (PMC open access)
- Sarasso, S., et al. (2014). *Quantifying cortical EEG responses to TMS in (un)consciousness.* **Clinical EEG and Neuroscience**

**Cross-modal NCC dissociation / method-relativity (EEG vs fMRI)**
- Dellert, T., et al. (2021). *Dissociating the Neural Correlates of Consciousness and Task Relevance in Face Perception Using Simultaneous EEG-fMRI.* **The Journal of Neuroscience** 41(37):7864–7875. DOI: 10.1523/JNEUROSCI.2799-20.2021
- Koch, C., Massimini, M., Boly, M., & Tononi, G. (2016). *Neural correlates of consciousness: progress and problems.* **Nature Reviews Neuroscience** 17:307–321. DOI: 10.1038/nrn.2016.22

**Psychedelic imaging / EEG anchors (for readout adjunct framing)**
- Carhart-Harris, R. L., et al. (2012). *Neural correlates of the psychedelic state as determined by fMRI studies with psilocybin.* **PNAS**. DOI: 10.1073/pnas.1119598109
- Timmermann, C., et al. (2019). *Neural correlates of the DMT experience assessed with multivariate EEG.* **Scientific Reports**

**Synesthesia prevalence as a distributional constraint source**
- Simner, J., et al. (2006). *Synaesthesia: The prevalence of atypical cross-modal experiences.* **Perception**. (PubMed)

**Split brain as correlator-cut motivation**
- de Haan, E. H. F., et al. (2020). *Split-Brain: What We Know Now and Why This is Important for Understanding Consciousness.* (PMC)

**Intracranial stimulation mapping / safety context**
- Grande, K. M., & Milham, M. P. (2020). *Electrical Stimulation Mapping of Brain Function.* **Frontiers in Human Neuroscience**
- Goldstein, H. E., et al. (2019). *Risk of seizures induced by intracranial research stimulation.* (PMC)

**ECT as “coarse lever” (if included)**
- Kadiyala, P. K., & Kadiyala, L. D. (2017). *Anaesthesia for electroconvulsive therapy: An overview…* (PMC)

---

## 6) Acceptance criteria (what “done” looks like)

1. `INTRODUCTION.md` no longer leads with psychedelics; it introduces IQT via a multi-intervention framing (anesthesia, stimulation, disconnection, pharmacology).
2. `iqt.md` abstract / plain-English summary is **mechanism-first** but does not hide specificity: it can name concrete interventions (e.g., psilocybin/ketamine/DMT) *without* letting them be the opener.
3. “Protocol 3” is mechanism-first in both documents (“Temporal Integration/Window Modulation”); psychedelics become Arm 3A rather than the header.
4. Both documents include a short, explicit locus-dependence paragraph **without** mentioning “direct vs indirect,” and it does real theoretical work (instrument coupling changes the effective diamond; cross-modal marker disagreement is framed as an expected perspectival feature).
5. If synesthesia is mentioned, it is framed with a clear gating: cross-check by default, but explicitly promotable to a **primary** test if the theory yields pre-registrable rank-orderings / impossibility claims over synesthetic pairings.
6. `iqt.md` includes at least one citation anchoring perturbational approaches (TMS-EEG / PCI / effective connectivity) and one anchoring synesthesia prevalence (if that avenue is kept).
7. Tone: empirically serious; no vibe-y phrasing; no extra metaphysical ballast.
