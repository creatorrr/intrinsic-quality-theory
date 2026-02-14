# Review: RFC-0002 (Revise the IQT Gentle Introduction)

**Reviewer:** Claude
**Date:** February 14, 2026
**Status:** Review of Draft

---

## Verdict

The RFC gets the diagnosis right. The current introduction hands the reader an answer before they've felt the question. The proposed fix — make them try to grab consciousness and watch them fail — is the correct structural move. The section arc (fail, compare, stakes, names, pivot) earns the theory's entrance.

The details below are mostly about tightening the spec so the implementer doesn't have to guess.

---

## What works

**The five failures are genuinely distinct.** Circularity, unlocatability, measurement collapse, function/experience gap, self-reference trap. Each fails differently. This isn't five ways of saying "consciousness is hard." It's five walls, each made of different material.

**The example draft text (Section 3.1) is good.** It does what it promises: second-person, present-tense, no jargon, no setup. The reader is the experiment. If the final version holds this tone across all five failures, the section will work.

**The anti-pattern lists (Sections 5 and 6) are precise enough to be useful.** They aren't vague instructions to "write clearly." They name specific failure modes ("don't use the word consciousness more than necessary," "don't preview solutions") and explain why each one matters. An implementer can run these as a literal checklist.

---

## Problems

### 1. The word budget probably doesn't hold

The example draft of the first two failures runs ~120 words. The RFC budgets 150–250 for all five. That leaves ~30–40 words per failure for the remaining three. Possible, but only if those three are noticeably shorter than the first two, which would create an awkward taper.

**Fix:** Write all five before committing to a word count. The budget should follow the draft, not the other way around. 250–350 may be more honest.

### 2. The splice point is unspecified

Section 4.2 says to "trim or cut" overlapping sentences in the current "What is this paper about?" section, but doesn't say which ones. Specifically:

Lines 15–16 of the current INTRODUCTION.md read:

> How does the physical matter inside your skull generate the invisible, private feeling of *having an experience*? Why does seeing red *feel* like something?

The five failures cover this ground better and more viscerally. If the new section goes in, these lines are redundant. The RFC should say so explicitly: cut lines 15–17 (the whole "IQT is an attempt to solve the Hard Problem" paragraph), or merge its one useful piece of information (the name "Hard Problem of Consciousness") into the Named Problems subsection where it belongs.

The splice point itself: the new material should go after line 11 ("And certain compounds can radically reshape the felt structure of time.") and before what is currently line 13 ("**Intrinsic Quality Theory (IQT)** claims these are not disconnected curiosities."). The IQT-claims paragraph becomes post-pivot material.

### 3. Sections 4.3 and 6 contradict each other

Section 4.3 suggests adding forward references at each named problem: "IQT addresses this in Section X." Section 6 says: "Don't preview the solutions. The problems accumulate. The reader feels the weight."

These can't both be the instruction. The subtler option already mentioned in 4.3 (echoing the exact language from the problem statement when presenting the solution later) is the right call. Drop the explicit forward references. Let the language do the linking.

### 4. The tomato shows up twice

Section 3.2 uses a tomato for qualia inversion. The existing Mary's Room section (INTRODUCTION.md lines 183–184) also uses a red tomato. This could be a nice echo or a distracting repetition. Either way, it should be a deliberate choice, noted in the RFC, not an accident the implementer discovers mid-draft.

### 5. The pivot's strong claim needs a hedge note

The example pivot text says: "None has addressed all four within a single formal framework that also generates concrete, falsifiable experiments."

That's a strong sentence. It may also be the sentence external reviewers attack first. IIT's adversarial collaboration with GNW produced pre-registered experiments, and IIT does address multiple problems (Hard Problem, combination, exclusion). The claim is defensible if scoped carefully ("all four" plus "single formal framework" does exclude IIT, which doesn't address temporal phenomenology or the other minds problem in its current form). But the RFC should flag this sentence as one that needs verification against the current state of competing theories, not just approval as draft text.

---

## On the open questions

**Q1: Heading or no heading?**
Heading. The new section is 500–700 words. Dropping that much material in without a heading punishes anyone who re-reads or skims. The "sneaking up" effect sounds appealing but trades away navigation for atmosphere. Not worth it.

**Q2: Tomato or something else?**
Tomato. Section 6 says "don't be clever." The tomato is the standard example. Zero cognitive overhead.

**Q3: Bold labels or prose for the named problems?**
Bold labels. The whole point of Section 3.4 is to plant anchors. Anchors should be visible. Prose buries them.

**Q4: Splice point?**
Answered above (Problem #2).

**Q5: Carry forward existing language?**
No. "How does the physical matter inside your skull generate the invisible, private feeling of having an experience?" is the question the five failures demonstrate without asking. Asking it explicitly after the reader has already lived it would be the kind of throat-clearing the RFC warns against.

---

## Minor notes

- The RFC title says "Opening with the Problem" but the existing opening hook (anesthesia, split-brain, compounds) is retained before the problem section. The section doesn't open with the problem; it opens with the hook, then moves to the problem. Not a real issue, but a more accurate title would be something like "Earning the Problem Before the Answer."

- Section 3.3 says "No domain gets a full paragraph." But the AI domain example is already three sentences and reads as a paragraph. The constraint is overspecified. "Keep each domain tight" is sufficient.

- The RFC estimates a 7–10% increase in document length. That's fine. The concern isn't length but pacing. The new section needs to move fast enough that the reader doesn't lose momentum before reaching the pivot. The five-failure structure handles this naturally if each failure stays short.
