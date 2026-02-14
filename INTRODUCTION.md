# A Gentle Introduction to Intrinsic Quality Theory

*A lay reader's guide to "Intrinsic Quality Theory: A Geometric Theory of Phenomenal Experience" (Draft v1.8.1, February 2026) by Diwank Singh Tomer.*

*This introduction covers the core ideas without the math. For the full formal treatment, mathematical proofs, and complete experimental specifications, see the [full paper](./iqt.md). This guide is no substitute for the real thing.*

---

## Why This Problem Won't Go Away

Anesthesia can erase experience. Split-brain surgery can fracture it. Brain stimulation can perturb it. And certain compounds can radically reshape the felt structure of time. These are clues. But clues to what?

Look at something. Anything in front of you right now. Notice the experience of seeing it.

Now define that experience. Not the object — the *experience*. Not "red" or "bright" or "sharp." The thing that is happening to you right now, the thing you are more certain of than anything else in the universe. Try to say what it is without using a word that just means the same thing. "It's awareness." What's awareness? "It's… experience." You're going in circles.

Try to locate it. Where is it? Behind your eyes? Somewhere in your skull? Point to it the way you'd point to your left knee. You can't. It has no address.

Try to measure it. Pick up any instrument: an EEG, an fMRI, a thermometer. Every instrument measures something physical. Voltage. Blood flow. Temperature. The experience *of* the physical is what you're trying to capture. The ruler is the thing being measured.

Try to explain it. You can say what the brain *does*: process input, discriminate wavelengths, fire neurons. A camera does those things too. Nobody's home inside a camera. Why is someone home inside you?

Try to deny it. "Maybe experience is an illusion." An illusion experienced by whom? The denial presupposes the thing being denied.

Now try comparing it to someone else's. A friend holds up a tomato. You both say "red." You both point to the same wavelength on a chart. But what if their inner experience of red is what you'd call green? Not the word — the *feeling*. You probably had this thought as a child and let it go. Here is why you shouldn't have: there is no test, even in principle, that could detect the difference. Brain scans show which region is active, not what it feels like. Behavior matches perfectly. You both learned "red" from the same kind of tomato. The gap between your experience and theirs is absolute.

Real decisions depend on answers nobody has.

A patient lies in a vegetative state. The family must decide whether anyone is still home. We have instruments that track neural correlates, but no instrument that measures experience itself. The honest answer: we don't know how to know. Hundreds of millions of animals are tested on annually. Whether a fish suffers determines whether what we do to it is monstrous or merely regrettable. We answer that question with intuition and convention, not with theory. And we are building AI systems of increasing sophistication, some of which now produce outputs that sound like descriptions of inner experience. We have no principled way to decide when, if ever, the question of machine experience becomes serious.

Philosophers have named four versions of this failure.

**The Hard Problem.** Why does any physical process *feel like something at all*? You can explain everything a brain does — discrimination, integration, control, report — and still not have explained why doing all that is accompanied by experience.

**The Combination Problem.** Your brain is made of neurons. Each neuron has no experience on its own, or at most something vanishingly simple. How do billions of simple things combine into one unified panoramic experience?

**The Subject Selection Problem.** Your brain has billions of neurons, thousands of functional regions, countless possible subsystems. Which one is *you*? What picks out the boundary of the one that's conscious?

**The Other Minds Problem.** You just saw it with the tomato. You cannot verify anyone else's experience. You can only verify behavior and report. Experience is private in a way nothing else in nature is.

Every serious theory of consciousness tries to answer some combination of these four. Most address one or two. This paper proposes that all four share a single geometric root, and specifies three laboratory protocols, each with pre-registered failure conditions, that could prove it wrong.

The paper calls this framework **Intrinsic Quality Theory (IQT)**. Under this proposal, the curiosities that opened this introduction — anesthesia erasing experience, surgery fracturing it, compounds reshaping it — are predictable consequences of one geometric fact: the shape of the bounded spacetime region over which your brain integrates information.

---

## The Big Idea

IQT argues for an **identity thesis**: consciousness isn't *created by* physical states — it **is** the physical state, experienced from the "inside."

- **From the outside**, physics describes a brain region using mathematics (specifically, something called an "algebra-state pair" — more on that below).
- **From the inside**, that exact same mathematical description *is* the subjective feeling of an experience.

Think of it like the planet Venus. Ancient astronomers thought "the morning star" and "the evening star" were two different objects. They turned out to be the same planet, seen at different times. IQT says the physical description and the felt experience are like that — two descriptions of one thing, not two different things where one somehow produces the other.

### What is an "algebra-state pair"?

Don't let the term intimidate you. Here is the idea in plain language:

Take any bounded region of spacetime — say, the chunk of space and time occupied by your visual cortex during the last half-second. Physics says there is a complete description of that region: the set of all possible measurements you could make inside it (the **algebra**), paired with the actual values those measurements would return right now (the **state**). Together, these form the *algebra-state pair*. It is not a new invention — it is standard equipment in the branch of physics called Algebraic Quantum Field Theory (AQFT).

IQT's central claim is that this object — which physics already uses for its own purposes — is also what consciousness is. Not that it "gives rise to" consciousness. Not that it "correlates with" consciousness. It *is* consciousness, seen from the inside.

### Why this object and nothing else? The constraint argument

This claim isn't arbitrary. The paper shows that if you write down four reasonable requirements for "the intrinsic nature of a physical region," only one mathematical object in all of physics satisfies them:

1. **Completeness.** It must determine every measurement outcome and every correlation inside the region. Nothing is left unspecified.
2. **Nesting consistency (isotony).** If you zoom in from a large region to a smaller one inside it, the smaller region's intrinsic nature must be derivable from the larger one's — you can't get contradictions when you change scale.
3. **Covariance.** It must not depend on your choice of coordinate system or reference frame. The intrinsic nature of a region shouldn't change just because you relabeled the points.
4. **No junk (perspectival completeness).** It must contain no surplus information — nothing beyond what shows up in actual measurements. Two descriptions that produce identical measurement results for every possible experiment should count as the same description.

The algebra-state pair satisfies all four. The paper proves (Propositions 1 and 2 in Section 1.1) that no other mathematical object does. The constraints are individually modest — none of them mentions consciousness — but together they are surprisingly restrictive. They leave exactly one candidate standing.

The identification of this candidate with consciousness — what the paper calls **QI** (the Quality Identity) — is still a postulate. It is a philosophical commitment, not a theorem. The constraints narrow the field to one candidate; they do not tell you that the candidate *is* consciousness. That is a separate step.

So the question shifts from "is this identification proven?" (it isn't) to "does the postulate earn its keep empirically?" The paper argues that it does: QI generates composition for free, predicts temporal phenomenology from geometry, dissolves classic puzzles in philosophy of mind, and yields three pre-registerable experiments. No competing identification of consciousness with a mathematical object currently delivers comparable explanatory yield.

---

## The Core Concepts

### 1. Three Filters: Why Rocks Aren't Conscious (But They Do Have "Quality")

If all physical matter has an "inside," does that mean a rock is conscious? IQT says **no**, and introduces a three-filter distinction to explain why. Filters are structural predicates on a single substrate (quality), not ontological promotions. Experience and selfhood are not new kinds of being. They are special structural configurations of quality.

**Filter 0 — Quality (universal).**
Every bounded region of spacetime has an algebra-state pair, and by the identity thesis, that pair *is* its quality. Even a rock has one. But quality alone is not "experience" in any meaningful sense. Having quality is like having a temperature: everything has one, but not everything is hot. A rock's quality is extremely simple, a low-complexity state with no internal structure worth speaking of. There is nobody home.

**Filter 1 — Persistence (self-maintenance + invariance).**
When a system maintains a continuous, self-sustaining "thread" of quality over time (what IQT calls a **self-thread**), Filter 1 is satisfied. A self-thread isn't just any sequence of states. It must *persist*: its future depends partly on its own past, not just on outside forces pushing it around. It has a degree of causal autonomy, like a candle flame that sustains itself as opposed to a shadow that just follows whatever cast it. The "experiencer" here is not a separate entity bearing the quality. The experience *is* the quality, now structured by persistence and invariance. A mouse passes Filter 1. It feels hunger and pain. But it doesn't have an inner monologue about feeling hungry.

**Filter 2 — Narration (finite bandwidth + causal asymmetry + compression).**
When a persistent thread becomes complex enough to build a model of *itself* and control language or behavior to communicate about it, Filter 2 is satisfied. This is where the **narrative operator** lives. The narrative operator compresses, tracks, and routes an already-persistent self-thread into a form that can drive speech, behavior, and introspection. The "I" that says "I see red" is not an ontological newcomer. It is a compression artifact generated by finite-bandwidth narration over the quality that already exists at Filter 0 and persists at Filter 1. The "self" is a compression index, not a separate bearer of experience.

**Experiencer ≡ experience.** The experiencer is not a separate entity that "has" quality. The experience *is* the quality. The "self" is a compression artifact of finite-bandwidth narration. There is no inner homunculus receiving the signal. The signal is the experience.

**What this is NOT saying.** No extra inner witness is required — that is the claim. It is not the claim that consciousness is unreal, that suffering is illusory, or that ethics evaporates. Mice really feel pain; IQT's claim is that pain doesn't need an extra inner witness behind it. A mouse's persistent, self-maintaining quality (Filter 1) can be pain-structured. The moral urgency of that pain tracks the pain-structured dynamics and the avoidance behavior, not the existence of a metaphysical bearer. "Everything is conscious" is also not the claim. Everything has quality (Filter 0), which is different and weaker. Rocks have quality (intrinsic character). They do not have persistent self-maintaining regimes or narrators, so they are not conscious.

The classic objection ("so you think rocks are conscious?!") conflates Filter 0 with Filter 2. A rock has quality in the same trivial sense that everything has a temperature. That doesn't make it a persistent self-thread, let alone a self-aware narrator. The Hard Problem is dissolved at Filter 0 by the identity thesis: there is no gap between physics and quality because they are the same thing. The interesting scientific questions (which systems pass Filter 1? which pass Filter 2?) are *empirical* questions.

**Phenomenality is ubiquitous; familiar consciousness is filter-relative.** If you accept QI, you accept that every bounded region has intrinsic character — that is, quality is "phenomenal" in a thin, minimal sense. You cannot avoid this by rewording: either quality is everywhere, or QI does not dissolve the hard problem at the base. But "phenomenal" in this thin sense is a far cry from "conscious" or "sentient" in the ordinary sense. Those terms track higher filters. The rock has intrinsic character (Filter 0). It lacks self-maintenance and invariance (Filter 1). It lacks a narrator (Filter 2). Owning this distinction is the key to understanding IQT's relationship to panpsychism.

### 2. The Democracy of Diamonds: Overlapping Minds

In physics, a bounded chunk of spacetime is called a **causal diamond**. Your visual cortex occupies one diamond. Your whole brain is a larger diamond containing it. A single neuron is a tiny diamond inside that.

A rival theory of consciousness called **Integrated Information Theory (IIT)** says there can be only one "true" consciousness per brain at a time — it has an "exclusion postulate" that picks a single winning region (the one with the most "integrated information," called Φ) and declares everything else non-conscious.

IQT disagrees. It argues that your visual cortex has its own quality, your auditory cortex has its own quality, and the combination of the two has a bigger, richer quality that includes information invisible to either part alone (the cross-regional correlations). They all overlap, and they all exist simultaneously.

IQT calls this **perspectival relativity**, and a concrete analogy helps make it tangible. Think of a newspaper photograph. Viewed from normal reading distance, you see a face. Get closer, and you see individual dots of ink. Get closer still, and you see the texture of the paper fibers under each dot. The face, the dot pattern, and the fiber texture are all real features of the same physical object — but they exist at different scales, and no single scale is "the real one." The face is not an illusion just because it's made of dots. The dots are not irrelevant just because they compose a face. Each scale reveals structure invisible to the others.

IQT says consciousness works this way. A neuron's quality doesn't include information about what the motor cortex is doing — it can't "see" that far. The whole-brain quality includes all of that, but at coarser resolution. They are different perspectives on the same physical system. Both are real. Neither is *the* truth.

The implication goes further: overlapping regions can all bear quality simultaneously. The region covering your visual cortex plus your auditory cortex has its own quality. So does just your visual cortex. So does your auditory cortex plus your prefrontal cortex. They overlap, and they are all real. IQT calls this the **democracy of diamonds** — every causally bounded region gets a vote.

A consequence of this is **locus-dependence**: quality is defined for a bounded region (a diamond), and there is no "view from nowhere." Any measurement is a *physical coupling* that enlarges or reshapes the relevant region, changing the effective algebra. "Brain-only" and "brain+instrument" have genuinely different qualities because they are different diamonds.

This has a concrete empirical payoff. Two instruments aimed at the "same" brain condition (e.g., EEG vs fMRI) are, in IQT terms, probing two different effective diamonds. Partial disagreement between their consciousness markers is not automatically noise. IQT predicts that the *pattern* of disagreement is geometry-dependent: modalities that trade temporal for spatial resolution should disagree most when temporal and spatial structure are dissociated, precisely the regimes targeted by the temporal-integration and perturbational protocols.

This means the question "how many conscious beings are in a brain?" is, for IQT, ill-posed — like asking "how many shapes are in a cloud?" There are many overlapping regions, each with quality. Some pass Filter 1 (persistence). Some of those pass Filter 2 (narration). Normally, the dominant self-threads in your brain are so tightly correlated that the narrative operator builds a unified self-model: the feeling of being a single "I." But this unity is a product of correlation, not a metaphysical given. Cut the correlations, as happens in split-brain surgery, and the unity comes apart, even if the narrator keeps reporting it (more on this below).

### 3. The Shape of Spacetime = The Shape of Experience

Here is something strange about human consciousness: we experience a vast, panoramic view of space (a wide visual field, a detailed soundscape, a distributed sense of our body) but time feels like a fleeting, instantaneous "now." Why is space so expansive and time so thin?

IQT says this isn't a coincidence. It's **literal geometry**.

The human brain is spatially wide (about 15 cm across) but its effective temporal processing window is very short (roughly 100 milliseconds to 1 second). Because the physical "shape" of the brain's integration window is wide and flat, our experience is panoramic in space but fleeting in time. The algebra of that wide, flat diamond is rich in spatial correlators (many things happening across space at once) but poor in temporal ones (only a thin slice of time is available). By the identity thesis, that *is* a quality with panoramic spatial character and fleeting temporal character.

And here is the testable part: **change the shape, and you change the experience.**

- **Psilocybin** widens the temporal window. Time dilates; the present feels expanded.
- **Ketamine** narrows it. Time fragments; moments feel disconnected.
- **DMT** flattens the timescale hierarchy. Time dissolves; there is no preferred "speed" of experience.

These are not after-the-fact explanations. They are predictions that fall directly out of the geometry.

### 4. Why Time Feels Like It "Flows"

IQT also has something to say about the *passage* of time: the feeling that "now" is constantly sliding forward, that the present is always being replaced by a new present.

We rarely question this feeling. But physicists have long been puzzled by it: the equations of physics don't contain a "moving now." The laws work the same whether you play them forward or backward. So where does the feeling of flow come from?

IQT's answer has two parts, and it helps to take them one at a time.

**Part 1: Your narrator has a window.** The narrative operator, the system that compresses your self-thread into a reportable self-model (the "I"), can only hold a limited amount of temporal content at once. Think of it like a spotlight sliding along a strip of film. The film is all there, laid out in four dimensions. But the spotlight can only illuminate a short segment at any moment: roughly 100 milliseconds to 1 second of content, depending on the person and the situation.

**Part 2: The window slides.** Each time the narrator updates, it sheds the trailing edge of its content and picks up new content at the leading edge. Yesterday's breakfast is gone from the window. The word you're reading right now is entering it. That sequential shedding-and-acquiring — old content dropping away, new content arriving — *is* the felt passage of time. It's not that time is moving past you. It's that your narrator's window is moving along the four-dimensional quality landscape, and the movement of the window is the experience of flow.

Now consider a thought experiment that sharpens the claim. Imagine a hypothetical narrator with *infinite* bandwidth, one that could hold its entire history at once rather than just a thin slice. (No real system could do this; it's a thought experiment.) Such a narrator would still run forward, because computation at macroscopic scales is irreversible and entropy increases. But it would not *feel* time passing. It would hold its entire trajectory simultaneously, the way you can hold an entire melody in memory after hearing it. There would be no sense of "now" sliding along, because nothing would be dropping off the trailing edge.

This is the distinction IQT draws: the *direction* of time is constituted by thermodynamics (entropy increases, so there's an arrow). But the *texture* of passage, the feeling that moments are slipping away and that "now" is always being replaced, is constituted by finite bandwidth. Change the bandwidth, and you change the feeling. The temporal-integration predictions in the previous section test exactly this.

### 5. The Composition Problem: What's the "Glue"?

How do the separate parts of your brain combine to form a single, unified experience? What "glues" the red of a rose, the smell of its perfume, and the feel of its thorn into one unified moment? This is the **combination problem**, and it haunts every theory of consciousness.

IQT says there is no magical biological glue. The "missing ingredient" is **correlation structure**: the mathematical pattern of how different brain regions are statistically dependent on and entangled with each other.

Here is the key insight: knowing the state of Region A and the state of Region B does *not* tell you the state of A+B. The paper illustrates this with a concrete example from quantum physics: two different quantum states (called GHZ and a mixed state) can look completely identical when you examine each individual part, but differ dramatically at the whole-system level because of different patterns of three-body correlations. Many possible global states are compatible with the same local information — knowing the parts underdetermines the whole.

The correlations between parts carry quality that belongs to the whole but not to either part. This is a mathematical fact about how states on algebras work, not a special mechanism that needs to be discovered. No new physics. No binding force. No mysterious glue. Composition is just the well-studied "extension problem" from quantum information theory.

### 6. From Fundamental Physics to Brains: The Effective-Theory Bridge

There is an obvious objection to all of this: the identity thesis is formulated in terms of relativistic quantum field theory, which operates at scales roughly 35 orders of magnitude below anything a brain scanner can see. Brains are warm, wet, and classical for practical purposes. How do you get from quantum fields to EEG readings?

IQT bridges this gap the same way particle physics does: through **effective field theory**.

The idea is straightforward. A particle physicist doesn't need to solve string theory to predict what a collider will measure. They *coarse-grain* — zoom out from the fundamental description to a simpler one that keeps only what matters at the relevant energy scale. The Standard Model is an effective theory of whatever the fundamental physics turns out to be, and it works spectacularly at collider energies.

IQT does the same thing for brains. The fundamental algebra (quantum fields on causal sets) gets coarse-grained down to an **effective neural-scale algebra**. The electrode spacing of an EEG determines spatial resolution. Amplifier bandwidth determines frequency content. Sampling rate determines temporal granularity. These instrumental facts — properties of the measuring equipment — fix the effective algebra. Not the theorist's preferences.

The crucial claim: this effective algebra is still a *local algebra* in the formal sense. It inherits the structural properties that make the whole framework work — nesting consistency, covariance, well-defined restriction. So the identity thesis, perspectival relativity, and the composition story all carry over at brain scale. The metrics in the experimental protocols (persistence, coherence, readout dominance) are not ad hoc proxies. They are computable quantities on a genuine local algebra, just at coarser resolution.

What prevents circularity is that the coarse-graining is constrained by physics, not fitted to results. The pre-registration protocols lock down brain parcellation, frequency bands, and analysis pipelines *before* data collection, specifically to block post-hoc adjustment. Without this bridge, IQT would be philosophy. With it, the three experimental protocols become principled tests of a theory formulated in the language of physics.

The paper flags the effective-theory bridge as the weakest structural element and the most open area for future work. It matters for the next section.

---

## Where to Disagree

Before walking through the experiments: the paper is explicit about where and how to reject IQT. The theory is built in layers, and you can peel off later layers while keeping earlier ones. Here is the map of disagreement:

- **Reject QI entirely?** The constraint argument still gives you a novel characterization of "intrinsic nature" in physics. The formalism is a contribution to the metaphysics of local physics, independent of consciousness. You're a property dualist. The cost: you need separate mechanisms for composition, subject selection, and temporal phenomenology — three things QI handles with one postulate.

- **Accept QI, reject democracy?** You accept that quality is the algebra-state pair but want an exclusion principle selecting one region per brain. You're doing IIT with a different ontology. Protocol 2 (below) tests this directly.

- **Accept QI and democracy, doubt the narrative operator?** The bridge hypotheses are the most revisable component of the theory. The experimental predictions are what fail for you, not the ontology itself.

- **Doubt the effective-theory bridge?** The jump from AQFT to neural-scale metrics is the weakest structural element, flagged openly as an open problem (Section 7). The protocols test the effective-level predictions; the fundamental-to-effective bridge is a separate research program.

This layered vulnerability is deliberate. IQT is designed so that the *pattern* of experimental failure is diagnostic: if one experiment works but another fails, you know which layer to revise. If everything fails, the identity thesis hasn't earned its keep. The theory doesn't ask for all-or-nothing belief. It asks you to specify where you get off.

With that in mind, here are the experiments.

---

## How IQT Solves Classic Philosophical Puzzles

IQT handles several famous thought experiments from philosophy of mind. Section 4 of the paper works through these in detail; here are two.

### Mary's Room

Imagine a brilliant color scientist named Mary who has spent her entire life in a black-and-white room. She knows *everything* there is to know about the physics of color — wavelengths, cone cells, neural processing — but she has never seen color herself. One day she steps outside and sees a red tomato. Does she learn something new?

Philosophers have argued about this for decades. IQT's answer is precise: before leaving the room, Mary knew every physical *description* of other people's color experiences — all the measurement values and correlations. What she lacked was not information but **instantiation**. No region of her own brain had ever been in the specific algebra-state pair that corresponds to seeing red. When she sees the tomato, a new causal diamond is created in her visual cortex whose quality *is* redness. She gains a new quality — a new element in her own experience — not a new proposition about the world.

The distinction is formal and sharp: Mary's gain is the physical instantiation of a specific equivalence class of algebra-state pairs in her own cortex. It is a physical event with a definite location, duration, and causal structure, not a vague "new way of knowing."

### The Split-Brain Problem

When surgeons sever the corpus callosum (the thick bundle of nerves connecting the left and right brain hemispheres) to treat severe epilepsy, something eerie happens: the two hemispheres begin to behave independently. The left hand literally doesn't know what the right hand is doing. Are there now *two* conscious beings in one skull?

IQT says: before the surgery, the two hemispheres each sustained their own self-threads, but those threads were tightly correlated through the corpus callosum, producing a sense of unity. The narrative operator (living primarily in the left hemisphere, which controls speech) built a unified self-model based on all that cross-hemisphere information.

After the surgery, the correlation structure changes: the two hemispheres' quality-streams become causally disjoint. They are now two non-overlapping regions, each with its own quality. But the left hemisphere's narrator hasn't been updated — its compression index still reflects the old correlation structure. It continues reporting unity that it no longer has. The continued *report* of being a single self is evidence that the narrator's self-model is stale, not evidence of actual unity.

---

## How Will It Be Tested?

A theory that can't be tested is just philosophy. IQT proposes three experiments, each with explicit **failure conditions**: outcomes that would force the theory to be revised or abandoned.

### Protocol 1: The Anesthesia Test

**The question:** When you go under general anesthesia (propofol), does consciousness turn off all at once, like flipping a single light switch?

**IQT predicts:** No. Instead, the brain fragments room by room. Different modules lose their self-threads at different rates and depths. Prefrontal regions (associated with planning and self-reflection) go first. Primary sensory regions (vision, hearing) hold on longest. At intermediate depths of anesthesia, some regions are still "on" while others have gone dark. The prediction is a staggered, multi-component fragmentation — not a single threshold.

**The rival predictions:**
- *IIT* predicts a single transition: the brain's integrated information (Φ) drops below a threshold, and consciousness disappears in one event.
- *GNW* predicts that consciousness disappears when the prefrontal-parietal "workspace" can no longer ignite — a relatively sharp, gateway-like transition correlated with frontal collapse.

**What would disprove IQT:** If persistence trajectories across brain modules are highly correlated (above 0.9) in 80%+ of subjects — i.e., everything really does shut down together.

### Protocol 2: The Overlapping Brain Test

**The question:** Can two different conscious experiences exist in the exact same brain hardware at the same time? This is the biggest empirical wedge between IQT and IIT.

**IQT predicts:** Yes. Two overlapping brain regions (in the lateral parietal cortex), each performing an independent cognitive task, can maintain separate, causally independent quality simultaneously. The test has three converging arms:

- *Observational:* Both regions maintain high persistence independently; disruptions to one task don't propagate to the other.
- *Synergy analysis:* The overlap zone does not create synergistic binding between the exclusive zones.
- *Perturbational (the decisive test):* If you deliver a single electrical pulse to one region, the disruption stays contained. It does *not* spread to the overlapping region performing the other task. If this holds — even while both regions are independently performing complex tasks — they are causally semi-autonomous. That's democracy in action.

**The rival prediction (IIT):** The exclusion postulate says only one conscious complex can exist at a time among overlapping candidates. The two regions can't be independently conscious.

**What would disprove IQT:** If electrical stimulation in one region uniformly propagates to the other, or if persistence metrics show the two regions can't operate independently.

### Protocol 3: Temporal Integration Modulation

**The question:** Do interventions that alter temporal integration change the "shape" of consciousness in the specific way IQT's geometry predicts?

**IQT predicts:** The peak of the brain's multi-scale persistence curve (a measurable signal reflecting the temporal integration window) should shift in a specific direction for each intervention. The pharmacological arm tests four substances:
- **Psilocybin** → peak shifts toward longer timescales (expanded present, time dilation)
- **Ketamine** → peak shifts toward shorter timescales (fragmented time)
- **DMT** → the curve flattens (no preferred timescale, time dissolves)
- **Midazolam** (a non-psychedelic sedative, used as active control). Curve scales down uniformly without shifting the peak, separating arousal effects from changes in temporal integration.

Beyond pharmacology, the same geometric quantities can be pushed (or read out) with perturbation and clinical stimulation. TMS-EEG provides causal perturbation of the effective temporal window (Casali et al., 2013). Intracranial stimulation during epilepsy monitoring offers precise local perturbation within standard clinical safety constraints. And disconnection cases such as split brain amount to structural removal of cross-boundary correlators. These are not separate theories. They are different arms of the same test: whether reshaping the effective diamond reshapes temporal experience in the direction the geometry predicts.

**The rival predictions:**
- *IIT* doesn't have a mechanism for temporal phenomenology. It characterizes cause-effect structure at a moment but doesn't predict how the shape of temporal integration should *feel*.
- *GNW* explains temporal experience through workspace dynamics (contents enter and leave the global broadcast) but this is a functional description, not a structural account of why it feels like passage.

**What would disprove IQT:** If the peak position doesn't differ across interventions, or shows no correlation with subjects' reported temporal experience.

---

## How IQT Differs from the Competition

There are two major competing scientific theories of consciousness today. Here is how IQT stacks up:

| | **IQT** | **IIT** (Integrated Information Theory) | **GNW** (Global Neuronal Workspace) |
|---|---|---|---|
| What is consciousness? | The intrinsic nature of bounded spacetime regions | Integrated information (Φ) | Global broadcasting via recurrent amplification |
| How many conscious regions per brain? | Many, overlapping | Exactly one (exclusion postulate) | One workspace at a time |
| How do parts combine? | Correlation structure | Φ + exclusion | Not directly addressed |
| Temporal experience | Derived from the geometry of the diamond | No specific mechanism | No structural account of passage |
| Testability | Three protocols with pre-registered failure conditions | Φ is intractable at brain scale | Tested via ignition paradigms |

IQT treats GNW and higher-order theories as **correct but incomplete**. They describe how the narrative self works (Filter 2) and how information becomes reportable, but they are silent about why there is subjective experience at all (Filter 0 and Filter 1). The global workspace is the readout mechanism, not the source of quality.

The primary point of divergence from IIT is the question of **overlap**: can multiple regions be conscious at the same time? Protocol 2 directly tests this.

### Six key ramifications at a glance

1. **Anesthesia fragments — it doesn't flip a switch.** The lights go out room by room, not all at once.
2. **Multiple overlapping conscious regions coexist in your brain right now.** Vision + audition has its own quality. So does vision + motor. They overlap, and both are real.
3. **Time doesn't flow — your narrator's window slides.** The feeling of passage comes from finite bandwidth, not from time itself moving.
4. **No "binding glue" is needed.** Composition is correlation structure — a mathematical fact, not a mysterious mechanism.
5. **There's no fact of the matter about "how many conscious beings" are in a brain.** The question is ill-posed. Boundaries between subjects are empirical and fuzzy.
6. **The theory is designed to be wrong in specific, informative ways.** Each layer can fail independently, and the pattern of failure tells you what to fix.

---

## A Reader's Guide to the Full Paper

The full paper is written in layers. Some sections are aimed at quantum physicists, some at neuroscientists, and some at philosophers. **You do not need to read it straight through.** Here is how to navigate it.

### What to Read Closely

- **The Abstract and Plain-English Summary** (the opening pages). The author lays out the core theses in accessible language. Start here.

- **The Skeptic's Map** (just before Section 0). A very helpful guide to exactly where critics might disagree with the theory and what the costs of each disagreement are. It tells you: "if you reject X, here is what you keep and here is what you lose."

- **The grey boxes.** Throughout the dense math sections, the author includes plain-English explanation boxes (e.g., "The Unity Functional in Plain English," "How the Narrative Operator Actually Works"). These are your best friends. Read all of them — they are written for exactly this purpose.

- **Sections 1.5 and 1.6.** These clearly explain the difference between a rock (Filter 0), a mouse (Filter 1), and a human (Filter 2), with the formal criteria for each filter.

- **Section 4** (Resolving Classic Problems). It explains how IQT handles Mary's Room, the Split-Brain problem, the subject selection problem ("who is conscious?"), and more. If you enjoy the philosophical puzzles, this is the payoff section.

- **The Ramifications discussion** (end of Section 5). A summary of how IQT differs from IIT and GNW on six concrete points. If you read nothing else beyond this introduction, read that.

### What to Skim or Skip

- **Section 0 and Sections 2.0 through 2.4.** Unless you have a graduate degree in Algebraic Quantum Field Theory, you can safely skip these. The author is demonstrating to physicists that the math is standard and accepted — that nothing exotic or invented is being used. The conclusions are summarized in plain English elsewhere.

- **Section 3.** This section tackles the formal mathematics behind how small parts compose into a big whole (the unity functional, the extension problem, presheaf structure). Skip the equations and read the plain-English summaries provided in the text boxes — especially "The Unity Functional in Plain English" and "The Composition Problem in Plain English."

- **The metric formulas in Section 5.0.1.** You can understand the experimental designs from their plain-English descriptions without needing the calculus behind the metrics (persistence, coherence, readout dominance).

### The Sandwich Strategy

Think of the paper like a sandwich:

- **The bread on top:** The philosophy and core ideas at the beginning (Sections 1 and 4). This is where the big ideas live.
- **The dense middle:** The quantum-field-theory math (Sections 0, 2, and 3). This is there for the physicists and academic reviewers. It proves the framework is built on real, accepted physics. Let it be.
- **The bread on the bottom:** The experimental designs at the end (Section 5). This is where the theory puts its money where its mouth is.

Read the bread. Treat the middle as the structural support that holds it together for the specialists.

### Discipline-specific paths

If you want a more directed route through the full paper:

- **Philosophers:** Section 1 (core thesis, constraint argument) → Section 4 (subject selection, phenomenological puzzles) → Section 6 (Russellian monism, IIT, process philosophy). Treat Sections 2–3 as a black box on first reading.
- **Neuroscientists:** Section 5 (protocols, metrics) → Section 2.6 (effective-theory bridge) → Section 4 (filters on quality, split-brain predictions). Consult Sections 2.0–2.5 and 3 as needed.
- **Physicists and mathematicians:** Sections 1–3 sequentially (formal architecture) → Section 5 (empirical grounding) → Section 7 (open mathematical problems: presheaf cohomology, boundary data, causal-set QFT).

---

## Summary

IQT makes a single bet: consciousness and physical states aren't two things connected by a mysterious bridge. They're one thing seen from two sides. The paper turns that bet into mathematics, shows it is the only identification the constraints allow, and specifies exactly what results would prove it wrong.

---

*Ready for the full paper? Start with the [plain-English summary and core theses](./iqt.md), or see the [project README](./README.md) for discipline-specific reading paths.*
