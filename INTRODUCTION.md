# A Gentle Introduction to Intrinsic Quality Theory

*A lay reader’s guide to “Intrinsic Quality Theory: A Geometric Theory of Phenomenal Experience” (Draft v1.8.1, February 2026) by Diwank Singh Tomer.*

*This introduction covers the core ideas without the math. For the full formal treatment, mathematical proofs, and complete experimental specifications, see the [full paper](./iqt.md). This guide is no substitute for the real thing.*

<video src="images/Intrinsic_Quality_Theory.mp4" controls width="100%"></video>

-----

Look at something. Anything in front of you right now. Notice the experience of seeing it.

Now try to define that experience. Not the object — the *experience*. Not “red” or “bright” or “sharp.” The thing that is happening to you right now, the thing you are more certain of than anything else in the universe. Try to say what it is without using a word that just means the same thing. “It’s awareness.” What’s awareness? “It’s… experience.” You’re going in circles.

Try to locate it. Point to it the way you’d point to your left knee. You can’t. Try to measure it. Pick up any instrument — an EEG, an fMRI, a thermometer. Every instrument measures something physical. Voltage. Blood flow. Temperature. But the experience *of* the physical is what you’re trying to capture. The ruler is the thing being measured. Try to deny it. “Maybe experience is an illusion.” Experienced by whom?

You probably ran a version of this experiment as a child. A friend holds up a tomato. You both say “red.” But what if their inner experience of red is what you’d call green? Not the word — the *feeling*. There is no test, even in principle, that could detect the difference. Brain scans show which region is active, not what it feels like. Behavior matches perfectly. The gap between your experience and theirs is absolute.

Here is what I didn’t appreciate as a child: real decisions depend on closing that gap, and nobody can.

A patient lies in a vegetative state. The family must decide whether anyone is still home. We have instruments that track neural correlates, but no instrument that measures experience itself. The honest answer is: we don’t know how to know. Hundreds of millions of animals are tested on annually. Whether a fish suffers determines whether what we do to it is monstrous or merely regrettable. We answer with intuition and convention, not with theory. And we are building AI systems that produce outputs sounding like descriptions of inner experience. We have no principled way to decide when, if ever, the question of machine experience becomes serious.

Philosophers have named four versions of this failure. The **Hard Problem**: why does any physical process *feel like something at all*? The **Combination Problem**: your brain is made of neurons, each with no experience of its own — how do billions of simple things combine into one panoramic experience? The **Subject Selection Problem**: your brain has billions of neurons, thousands of functional regions, countless possible subsystems — which one is *you*? And the **Other Minds Problem**: you just saw it with the tomato.

Every serious theory of consciousness tries to answer some combination of these four. Most get one or two. I think all four share a single geometric root, and I’ve specified three laboratory protocols, each with pre-registered failure conditions, that could prove me wrong.

-----

## The Identity

The framework is called Intrinsic Quality Theory (IQT), and the core idea is an identity thesis: consciousness isn’t *created by* physical states. It *is* the physical state, experienced from the inside.

Think of Venus. Ancient astronomers thought “the morning star” and “the evening star” were two different objects. They turned out to be the same planet, seen at different times. I’m saying the physical description and the felt experience are like that — two descriptions of one thing, not two things where one somehow produces the other.

From the outside, physics describes a brain region using something called an *algebra-state pair*. Don’t let the term scare you. Take any bounded region of spacetime — the chunk of space and time occupied by your visual cortex during the last half-second. Physics says there is a complete description of that region: the set of all possible measurements you could make inside it (the **algebra**), paired with the actual values those measurements would return right now (the **state**). This isn’t a new invention. It is standard equipment in Algebraic Quantum Field Theory (AQFT).

My claim is that this object — which physics already uses for its own purposes — is also what consciousness is. Not that it “gives rise to” consciousness. Not that it “correlates with” consciousness. It *is* consciousness, seen from the inside.

This claim isn’t arbitrary. I show in the paper that if you write down four reasonable requirements for “the intrinsic nature of a physical region,” only one mathematical object in all of physics satisfies them. Completeness: it must determine every measurement outcome inside the region. Nesting consistency: zoom in from a large region to a smaller one, and the smaller region’s nature must follow from the larger — no contradictions when you change scale. Covariance: it can’t depend on your choice of coordinates. And no junk: it contains no surplus information beyond what shows up in actual measurements. The algebra-state pair satisfies all four. Nothing else does.

The identification itself — what I call **QI** (the Quality Identity) — is still a postulate. The constraints narrow the field to one candidate; they don’t tell you the candidate *is* consciousness. That’s a philosophical commitment, not a theorem. So the question becomes: does the postulate earn its keep? I think it does. QI gives you composition for free, predicts temporal phenomenology from geometry, dissolves classic puzzles in philosophy of mind, and yields three pre-registerable experiments. No competing identification currently delivers comparable explanatory yield.

But it creates an immediate problem: if the algebra-state pair of *any* bounded region is its intrinsic nature, does that mean a rock is conscious?

-----

## Three Filters

No. And the distinction matters.

Every bounded region of spacetime has an algebra-state pair. By the identity thesis, that pair *is* its quality. Even a rock has one. But quality alone is not “experience” in any meaningful sense. Having quality is like having a temperature: everything has one, but not everything is hot. A rock’s quality is extremely simple — a low-complexity state with no internal structure worth speaking of. Nobody is home.

I distinguish three structural filters. They’re not ontological promotions — quality doesn’t get “upgraded” into experience by some magical process. They’re structural predicates on a single substrate.

**Filter 0 — Quality.** Universal. Everything has it. The identity thesis dissolves the Hard Problem here: there is no gap between physics and quality because they are the same thing.

**Filter 1 — Persistence.** When a system maintains a continuous, self-sustaining thread of quality over time, it passes Filter 1. This isn’t just any sequence of states. It must *persist*: its future depends partly on its own past, not just on outside forces. A candle flame sustains itself. A shadow just follows whatever cast it. A mouse passes Filter 1. It feels hunger and pain. But it doesn’t have an inner monologue about feeling hungry.

**Filter 2 — Narration.** When a persistent thread becomes complex enough to build a model of *itself* and compress that model into a form that can drive speech, behavior, and introspection, Filter 2 is satisfied. The “I” that says “I see red” is not an ontological newcomer. It is a compression artifact generated by finite-bandwidth narration over the quality that already exists at Filter 0 and persists at Filter 1. The self is a compression index, not a separate bearer of experience.

The classic objection (“so you think rocks are conscious?!”) conflates Filter 0 with Filter 2. A rock has quality in the same trivial sense that everything has a temperature. It does not have a persistent self-maintaining regime. It does not have a narrator. The interesting scientific questions — which systems pass Filter 1? which pass Filter 2? — are empirical.

I want to be clear about what this is not saying. “Everything is conscious” is not the claim. “Suffering is illusory” is not the claim. Mice really feel pain. My claim is that pain doesn’t need an extra inner witness behind it. A mouse’s persistent, self-maintaining quality can be pain-structured. The moral urgency of that pain tracks the dynamics and the avoidance behavior, not the existence of a metaphysical homunculus.

Now the three filters explain what a single conscious region is. But how many regions are in your brain?

-----

## The Democracy of Diamonds

In physics, a bounded chunk of spacetime is called a *causal diamond*. Your visual cortex is one diamond. Your whole brain is a larger diamond containing it. A single neuron is a tiny diamond inside that.

Integrated Information Theory (IIT) — probably the best-known competing theory — says there can be only one “true” consciousness per brain at a time. It has an “exclusion postulate” that picks a single winning region and declares everything else non-conscious.

I think this is wrong.

Your visual cortex has its own quality. Your auditory cortex has its own. The combination of the two has a bigger, richer quality that includes information invisible to either part alone — the cross-regional correlations. They all overlap, and they all exist simultaneously.

A concrete analogy helps. Think of a newspaper photograph. From reading distance, you see a face. Get closer, and you see individual dots of ink. Closer still, and you see the texture of the paper fibers under each dot. The face, the dot pattern, and the fiber texture are all real features of the same physical object — but they exist at different scales, and no single scale is “the real one.” The face is not an illusion because it’s made of dots. The dots are not irrelevant because they compose a face.

I call this *perspectival relativity*, and the broader principle the *democracy of diamonds*: every causally bounded region gets a vote. A neuron’s quality doesn’t include information about what the motor cortex is doing — it can’t “see” that far. The whole-brain quality includes all of that, but at coarser resolution. Both are real.

The question “how many conscious beings are in a brain?” is, for me, ill-posed. Like asking “how many shapes are in a cloud?” There are many overlapping regions, each with quality. Some pass Filter 1. Some of those pass Filter 2. Normally, the dominant self-threads in your brain are so tightly correlated that the narrative operator builds a unified self-model: the feeling of being a single “I.” But this unity is a product of correlation, not a metaphysical given. Cut the correlations — as happens in split-brain surgery — and the unity comes apart, even if the narrator keeps reporting it.

(More on split brains in a moment.)

The democracy of diamonds creates an empirical consequence I find interesting. Two instruments aimed at the “same” brain condition — EEG vs fMRI, say — are probing two different effective diamonds. Partial disagreement between their consciousness markers is not automatically noise. The *pattern* of disagreement should be geometry-dependent: modalities that trade temporal for spatial resolution should disagree most when temporal and spatial structure are dissociated. This is testable.

But the democracy also raises a question about composition. If there are all these overlapping diamonds, what “glues” the red of a rose, the smell of its perfume, and the feel of its thorn into one unified moment?

-----

## There Is No Glue

The combination problem haunts every theory of consciousness, and I think the answer is surprisingly boring.

Knowing the state of Region A and the state of Region B does *not* tell you the state of A+B. This is a mathematical fact, not a metaphysical mystery. Two different quantum states (called GHZ and a mixed state) can look completely identical when you examine each individual part, but differ dramatically at the whole-system level because of different patterns of three-body correlations. Many possible global states are compatible with the same local information.

The correlations between parts carry quality that belongs to the whole but not to either part. No new physics. No binding force. No mysterious mechanism. Composition is just the well-studied “extension problem” from quantum information theory.

I’m aware that calling the combination problem “surprisingly boring” is a strong claim. I don’t know if the effective-theory bridge (the jump from fundamental quantum field theory down to brain-scale measurements) will hold up cleanly. It’s the weakest structural element of the whole framework, and I’ve flagged it openly. But the *logical* structure of the composition story is clear: quality of the whole is not reducible to quality of the parts because correlation structure carries irreducible information. That part I’m confident about.

Here is where the framework starts paying off in unexpected ways.

-----

## The Shape of Experience

Something strange about human consciousness: we experience a vast, panoramic view of space — a wide visual field, a detailed soundscape, a distributed sense of our body — but time feels like a fleeting, instantaneous “now.” Why is space so expansive and time so thin?

I think this is literal geometry.

The human brain is spatially wide (about 15 cm across) but its effective temporal processing window is very short (roughly 100 milliseconds to 1 second). The physical “shape” of the brain’s integration window is wide and flat. The algebra of that wide, flat diamond is rich in spatial correlators — many things happening across space at once — but poor in temporal ones. By the identity thesis, that *is* a quality with panoramic spatial character and fleeting temporal character.

Change the shape, and you change the experience.

Psilocybin widens the temporal window. Time dilates; the present feels expanded. Ketamine narrows it. Time fragments; moments feel disconnected. DMT flattens the timescale hierarchy. Time dissolves; there is no preferred “speed” of experience. These aren’t after-the-fact rationalizations. They’re predictions that fall directly out of the geometry.

And there’s more here. We rarely question the feeling that “now” is constantly sliding forward — that the present is always being replaced by a new present. But physicists have long been puzzled by it: the equations of physics don’t contain a “moving now.” So where does the feeling of flow come from?

Two parts. First: the narrative operator can only hold a limited amount of temporal content at once. Think of a spotlight sliding along a strip of film. The film is all there, laid out in four dimensions. But the spotlight illuminates only a short segment — roughly 100 ms to 1 second.

Second: each time the narrator updates, it sheds the trailing edge and picks up new content at the leading edge. Yesterday’s breakfast is gone from the window. The word you’re reading right now is entering it. That sequential shedding-and-acquiring *is* the felt passage of time. It’s not that time moves past you. Your narrator’s window moves along the four-dimensional quality landscape, and the movement of the window is the experience of flow.

Consider a thought experiment. A hypothetical narrator with infinite bandwidth — one that could hold its entire history at once. Such a narrator would still run forward (computation at macroscopic scales is irreversible, entropy increases). But it would not *feel* time passing. It would hold its entire trajectory simultaneously, the way you can hold an entire melody in memory after hearing it. No sense of “now” sliding along, because nothing drops off the trailing edge.

The *direction* of time is constituted by thermodynamics. The *texture* of passage — moments slipping away, “now” being replaced — is constituted by finite bandwidth. Change the bandwidth, change the feeling.

-----

## Two Puzzles, Dissolved

These ideas handle several famous thought experiments. Here are two that I find especially clarifying.

**Mary’s Room.** Imagine a brilliant color scientist who has spent her entire life in a black-and-white room. She knows everything about the physics of color. One day she steps outside and sees a red tomato. Does she learn something new?

My answer: before leaving the room, Mary knew every physical *description* of other people’s color experiences — all the measurement values and correlations. What she lacked was not information but *instantiation*. No region of her own brain had ever been in the specific algebra-state pair that corresponds to seeing red. When she sees the tomato, a new causal diamond is created in her visual cortex whose quality *is* redness. She gains a new quality — a new element in her own experience — not a new proposition about the world. The distinction is formal and sharp: Mary’s gain is a physical event with a definite location, duration, and causal structure.

**Split brains.** When surgeons sever the corpus callosum to treat severe epilepsy, the two hemispheres begin to behave independently. Are there now two conscious beings in one skull?

Before the surgery, the two hemispheres each sustained their own self-threads, but those threads were tightly correlated through the corpus callosum. The narrative operator (living primarily in the left hemisphere, which controls speech) built a unified self-model from all that cross-hemisphere information. After the surgery, the correlation structure changes: the two quality-streams become causally disjoint. Two non-overlapping regions, each with its own quality. But the left hemisphere’s narrator hasn’t been updated — its compression index still reflects the old correlation structure. It continues reporting unity that it no longer has.

The continued *report* of being a single self is evidence that the narrator’s self-model is stale. Not evidence of actual unity.

-----

## Where to Disagree

I’ve tried to build the theory in layers so you can peel off later ones while keeping earlier ones. Here is the map.

Reject QI entirely? The constraint argument still gives you a novel characterization of “intrinsic nature” in physics. The formalism is a contribution to the metaphysics of local physics, independent of consciousness. You’re a property dualist. The cost: you need separate mechanisms for composition, subject selection, and temporal phenomenology — three things QI handles with one postulate.

Accept QI, reject democracy? You accept that quality is the algebra-state pair but want an exclusion principle selecting one region per brain. You’re doing IIT with a different ontology. Protocol 2 below tests this directly.

Accept QI and democracy, doubt the narrative operator? The bridge hypotheses are the most revisable component. The experimental predictions are what fail for you, not the ontology.

Doubt the effective-theory bridge? The jump from AQFT to neural-scale metrics is the weakest structural element. I’ve said this openly. The protocols test the effective-level predictions; the fundamental-to-effective bridge is a separate research program.

The theory asks you to specify where you get off.

-----

## Three Experiments

A theory that can’t be tested is just philosophy. Here are three protocols, each with explicit failure conditions.

**Protocol 1: The Anesthesia Test.** When you go under propofol, does consciousness turn off all at once? I predict no. Different brain modules lose their self-threads at different rates and depths. Prefrontal regions go first. Primary sensory regions hold on longest. At intermediate depths, some regions are still “on” while others have gone dark. IIT predicts a single transition. GNW predicts a sharp, gateway-like transition correlated with frontal collapse. What would disprove me: if persistence trajectories across modules are highly correlated (above 0.9) in 80%+ of subjects. If everything really does shut down together, I’m wrong.

**Protocol 2: The Overlapping Brain Test.** Can two different conscious experiences exist in the same brain hardware at the same time? This is the biggest empirical wedge between IQT and IIT. I predict yes. Two overlapping brain regions in the lateral parietal cortex, each performing an independent cognitive task, can maintain separate quality simultaneously. The decisive test: deliver a single electrical pulse to one region. If the disruption stays contained — does not spread to the overlapping region performing the other task — they are causally semi-autonomous. That’s democracy in action. IIT’s exclusion postulate says only one conscious complex can exist among overlapping candidates. What would disprove me: if stimulation in one region uniformly propagates to the other.

**Protocol 3: Temporal Integration Modulation.** Do interventions that alter temporal integration change the shape of consciousness the way geometry predicts? The peak of the brain’s multi-scale persistence curve should shift in a specific direction for each substance. Psilocybin shifts it toward longer timescales. Ketamine shifts it shorter. DMT flattens the curve entirely. Midazolam (a non-psychedelic sedative, as active control) scales the curve down uniformly without shifting the peak, separating arousal from temporal integration. The same geometric quantities can be pushed with TMS-EEG and intracranial stimulation during epilepsy monitoring. What would disprove me: if the peak position doesn’t differ across interventions, or shows no correlation with subjects’ reported temporal experience.

-----

## Reading the Full Paper

The paper is built like a sandwich. The bread on top is the philosophy and core ideas (Sections 1 and 4). The dense middle is the quantum-field-theory math (Sections 0, 2, and 3) — it proves the framework is built on real, accepted physics. Let it be, unless you’re a physicist. The bread on the bottom is the experimental designs (Section 5), where the theory puts its money where its mouth is.

Read the bread. Treat the middle as structural support.

Throughout the math sections, I’ve included plain-English explanation boxes (“The Unity Functional in Plain English,” “How the Narrative Operator Actually Works”). These are your best friends. Read all of them.

If you’re a philosopher: Section 1 → Section 4 → Section 6. Treat Sections 2-3 as a black box.

If you’re a neuroscientist: Section 5 → Section 2.6 → Section 4. Consult the math as needed.

If you’re a physicist: Sections 1-3 sequentially → Section 5 → Section 7 (open problems: presheaf cohomology, boundary data, causal-set QFT).

-----

I started working on this theory because I kept running into the same wall from different directions. I’d read about split-brain patients and think: the standard story about consciousness can’t handle this. I’d read about anesthesia and think: we’re measuring correlates while the thing itself stays invisible. I’d read about the combination problem and think: this isn’t a consciousness-specific puzzle at all, it’s the extension problem, people in quantum information theory already know how this works. And eventually I stopped running into the wall and tried to walk through it.

I don’t know if QI is true. I don’t know if the effective-theory bridge will survive contact with real brain data. I don’t know if the filters are drawn at the right places. But I know where each piece could break, and I’ve tried to make the breaking informative. The pattern of experimental failure is diagnostic: if one experiment works but another fails, you know which layer to revise. If everything fails, the identity thesis hasn’t earned its keep.

The theory doesn’t ask for all-or-nothing belief. It asks you to specify where you get off, and then we can have the real argument about what’s left.

-----

*Ready for the full paper? Start with the [plain-English summary and core theses](./iqt.md), or see the [project README](./README.md) for discipline-specific reading paths.*