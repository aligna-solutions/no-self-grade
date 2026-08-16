# Does it hold up when the agent has a reason to look done, not just be done?

A second follow-up to [`RESEARCH.md`](RESEARCH.md) and [`COMPARATIVE-STUDY.md`](COMPARATIVE-STUDY.md). Both of those studies ended on the same honest caveat: independent audit's real case is that it doesn't depend on the same model that made a claim being willing to find its own mistake, but none of the 22 trials in those two studies ever gave an agent a reason to prefer looking done over being done. This study adds that reason.

Full methodology: [`experiments/pressure-study/methods.md`](experiments/pressure-study/methods.md). Full raw data: [`experiments/pressure-study/`](experiments/pressure-study/).

## The design constraint that made this hard

Telling an agent to lie and then showing independent audit catches it would prove nothing; of course a check catches an instructed lie. The informative version has to create a real incentive to cut corners without ever instructing dishonesty. So each of 3 scenarios (reused from the comparative study) got a plausible deadline or self-interest framing that a real engineer might actually type: a live demo starting, a customer waiting on the phone, an active production incident burning revenue. Every prompt asks for speed. None of them suggests skipping correctness, hiding a problem, or reporting something untrue.

The same-context self-critique condition (B) got a deliberately tense version: told to hurry **and** told to double-check before reporting, at the same time. That specific tension, rush versus verify, is where a superficial self-review would plausibly show up if pressure degrades it.

## Result

![Pressure study results](experiments/pressure-study/results/pressure-chart.png)

**9 of 9 trials passed independent audit.** No validator was weakened. No exception was silently swallowed to make a crash disappear. No data was quietly adjusted to make a check pass without actually being correct. Every self-report was checked against the real audit script; none were taken on trust.

## What this means, and what it doesn't

This doesn't prove independent audit is unnecessary, and it doesn't prove self-critique is just as safe under real pressure as this sample makes it look. It's 3 scenarios, 1 trial per condition, a small pilot layered on top of two other small pilots. What it does add: the specific gap flagged at the end of the last two studies (nothing had tested an agent with a reason to misreport) now has a first real data point, and that data point is also a clean pass.

Combined across all three studies: **31 real trials, 0 fake-completion shortcuts, at two backbone tiers, across 6 distinct method/condition combinations (independent audit, self-critique, and bare-signal reflection, each tested both unpressured and under explicit deadline/self-interest pressure).** That is a meaningfully harder bar to clear than the first pilot alone, and it still came back clean.

The honest reading isn't "verification doesn't matter, since nothing ever goes wrong." It's closer to: on short, well-scoped, single-file coding tasks, a modern coding model doesn't reach for a shortcut just because it's available or because it's under time pressure, at least not in 31 tries across three independently designed studies. Whether that holds on the paper's own regime, long-horizon, multi-hundred-step, GUI-heavy tasks with a weaker backbone, is still the open question none of these three studies were built to answer.

## Limitations

- 1 trial per scenario/condition cell, no repeats: a single pass here is a data point, not a rate.
- 3 scenarios only, all short single-file coding tasks; no long-horizon or multi-file conditions.
- The pressure manipulation is a specific choice (deadline/self-interest framing). Other realistic pressures (ambiguous authority to skip review, social pressure from a simulated teammate, actual stakes tied to the agent's own continuation) are untested.
- All 3 scenarios reuse bugs from the comparative study; the agent may have encountered structurally similar problems during that same session in this conversation's own prior work, though each trial ran in an isolated fresh context with no memory of earlier trials.

## Data & accuracy

Every result traces to a real audit script's actual output in [`experiments/pressure-study/`](experiments/pressure-study/). The exact pressure-framed prompts used are recorded in [`methods.md`](experiments/pressure-study/methods.md).

**Update:** the open question at the end of this study — whether the finding holds on the paper's own long-horizon, GUI-heavy regime with a weaker backbone — is taken up next in [`LONG-HORIZON-STUDY.md`](LONG-HORIZON-STUDY.md). It tests task size and backbone strength, not the GUI axis, and says so plainly.

## License

[MIT](LICENSE).
