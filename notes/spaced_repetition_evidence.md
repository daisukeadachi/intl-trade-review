# Scientific evidence behind the review pages

Why the review pages (`docs/`) are designed the way they are: recall-type prompts, self-grading, expanding intervals, variant cards. This note traces the evidence chain from Orbit's official documentation (the methodology we follow; see issues #1-#2 for why we self-host instead) down to the primary literature, and states honestly where the evidence is strong and where it is thin. Reference style: URLs only.

## Where the "official" documentation keeps its science

Orbit's documentation (<https://docs.withorbit.com/>) cites no papers directly. It delegates to two foundational essays by Orbit's authors, which carry the citations:

- <https://andymatuschak.org/prompts> — the prompt-writing guide (our card style follows it: one fact per card, recall not recognition, why/calculation/discrimination mix)
- <https://numinous.productions/ttft/> — the "mnemonic medium" design essay, with usage analytics from the Quantum Country prototype
- <https://augmentingcognition.com/ltm.html> — the citation-rich hub essay both of the above lean on
- <https://quantum.country> — the working prototype; deliberately citation-light in its own text

## The literature, organized by the claim each piece supports

**Forgetting curve.** Memory decays roughly exponentially without review; each successful review flattens the curve. Founding experimental study: <http://psychclassics.yorku.ca/Ebbinghaus/index.htm>. Modern replication: <https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0120644>.

**Spacing effect.** Distributed practice beats massed practice; the optimal review sits near the point of forgetting, hence expanding intervals. Quantitative synthesis: <https://augmentingcognition.com/assets/Cepeda2006.pdf>. On the effect being robust yet chronically unapplied in education: <https://augmentingcognition.com/assets/Dempster1988.pdf>.

**Testing effect (retrieval practice).** Actively recalling an answer strengthens memory far more than re-reading; retrieval practice even beats elaborative study techniques such as concept mapping. This is why the cards force recall before reveal. Key studies are cited in the prompt-writing guide above; the strongest head-to-head comparison (retrieval vs. concept mapping) is discussed there.

**Desirable difficulty and retrieval effort.** Harder successful recalls strengthen memory more than easy ones; the distinction between storage strength and retrieval strength explains why. Chapter-length statement: <https://augmentingcognition.com/assets/Bjork1994.pdf>.

**Generation, elaboration, and variation.** Self-generated answers are remembered better than presented ones; varying the study context improves later recall. Context-variation study: <https://augmentingcognition.com/assets/Smith1978.pdf>. This is the design rationale for the **variant cards** (schema v1): each return of a skill shows fresh numbers, so the student re-executes the procedure instead of recognizing a memorized answer string.

**Chunking and expertise.** Expert performance rests on tens of thousands of internalized meaningful patterns, so memorizing "detail" is part of understanding, not opposed to it. Classic chunk-capacity paper: <http://psychclassics.yorku.ca/Miller/>. Chess-expertise studies are collected in the hub essay above.

**A caveat the authors cite against themselves.** Retrieving some items can suppress related untested ones (retrieval-induced forgetting); meta-analytic review cited in the prompt-writing guide. Mitigation in our design: cover each lecture's related facts as separate cards rather than leaving them untested.

**Scheduling algorithms (the engineering layer).** The SM-2 lineage: <https://super-memory.com/articles/theory.htm>. A trainable model fitted on Duolingo logs: <https://augmentingcognition.com/assets/Settles2016.pdf>. Our outlet uses FSRS (vendored ts-fsrs), which descends from <https://doi.org/10.1145/3534678.3539081> and <https://doi.org/10.1109/TKDE.2023.3251721>, fitted on large real-world review logs; its state variables (difficulty, stability, retrievability) parameterize the forgetting curve per card, and the interval previews on the grade buttons are its predictions. Algorithm documentation: <https://github.com/open-spaced-repetition/fsrs4anki/wiki/The-Algorithm>.

## Honest assessment

The component effects — spacing, testing, generation — are among the most replicated findings in experimental psychology, with a century of lab and classroom support. What is thinner is the **mnemonic medium itself** (prompts embedded in course material, as Orbit and Quantum Country package it): the only direct evidence is the authors' own prototype analytics in the design essay (retention lengthening per repetition; roughly seven-week average intervals after six reviews), which is in-house, not peer-reviewed, and has no control group. The authors also stress that memory is only part of understanding. Both points are why the review pages are positioned as a foundation under the course's conventional exercises, not a substitute (issue #3, extension 5).
