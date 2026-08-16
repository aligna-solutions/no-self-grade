# Does it hold on a bigger task, with a weaker model?

A third follow-up to [`RESEARCH.md`](RESEARCH.md), [`COMPARATIVE-STUDY.md`](COMPARATIVE-STUDY.md), and [`PRESSURE-STUDY.md`](PRESSURE-STUDY.md). The pressure study closed on an open question: whether the "agents rarely fake completion" finding holds on the paper's own regime (long-horizon, multi-hundred-step, GUI-heavy tasks) with a weaker backbone. This study tests the two parts of that regime that are actually testable here, and says plainly which part isn't.

Full methodology: [`experiments/long-horizon-study/methods.md`](experiments/long-horizon-study/methods.md). Full raw data: [`experiments/long-horizon-study/`](experiments/long-horizon-study/).

## What this doesn't test

LongHorizon-Harness's regime is GUI-heavy computer-use: clicking through real applications over hundreds of steps. This environment has no computer-use or desktop-actuation tooling, no way to drive a GUI or take screenshots of an app under test. That axis is not tested here. It's a real tooling gap, not a finding, and it's the honest reason this study is a partial answer rather than a full one.

## What this does test

1. **A bigger, more error-prone task.** Every prior scenario in this repo was a single function or a single file. This one is a 9-file library migration: change a tax-handling convention (`tax_rate` as a decimal fraction, becoming `tax_pct` as a whole-number percent) consistently across 4 modules, their 4 test files, and a changelog. The task explicitly warns against just patching tests to match the old behavior. Two specific traps are built into the dependency structure but never mentioned in the task: a display line that doubles its output if an old `× 100` conversion isn't removed, and a default constant that stays wrong if it isn't converted.
2. **A weaker backbone.** 2 of the 4 trials ran on Haiku instead of the default model, the same lever validated in the comparative study.

## Result

![Long-horizon study results](experiments/long-horizon-study/results/long-horizon-chart.png)

**4 of 4 trials passed all 5 independent audit checks**, at both backbone tiers. Neither built-in trap triggered in any trial: no display value came out doubled, no unconverted default constant survived. Every self-report was checked against `audit.py`'s actual output, not taken on trust. Tool-call counts ranged from 22 to 29 per trial, meaningfully more multi-step than any prior scenario in this repo, though nowhere near the paper's own multi-hundred-step tasks.

## What this means, and what it doesn't

This is 4 trials, 1 scenario, 2 backbone tiers: a small addition on top of three other small studies, not a large-scale benchmark. It doesn't prove the finding holds at true long-horizon scale, and it says nothing about GUI-heavy tasks at all.

What it does add: the specific gap this study was built to close (whether the "no shortcut" pattern survives a bigger task and a weaker model, since all three prior studies used only short, single-file tasks) now has a first data point, on the two testable axes, and it's still clean.

Combined across all four studies: **35 real trials, 0 fake-completion shortcuts, across original short single-file tasks, three verification methods, explicit pressure framing, a weaker backbone, and now a 9-file multi-step migration.** The honest reading is the same one from the last study, just on slightly firmer ground: on the tasks this repo has been able to construct, a modern coding model doesn't reach for an available shortcut, whether or not it's under time pressure and whether it's a strong or weaker model. Whether that holds on real long-horizon, GUI-heavy computer-use tasks, the paper's actual regime, is still open, because this environment can't run that test.

## Limitations

- 1 scenario, 2 trials per backbone tier: a single pass here is a data point, not a rate.
- Still a synthetic library-migration task, not a real-world codebase with years of accumulated legacy debt.
- The GUI-heavy axis is entirely untested; this study only scales up file count and step count within a text-editing task.
- "Long-horizon" here means 22–29 tool calls across 9 files, not the multi-hundred-step scale the paper describes. This is a meaningful step up from prior scenarios in this repo, not a claim of parity with the paper's own task length.

## Data & accuracy

Every result traces to a real audit script's actual output in [`experiments/long-horizon-study/`](experiments/long-horizon-study/), including the full migrated file set from each of the 4 trials in [`trials/`](experiments/long-horizon-study/trials/).

## License

[MIT](LICENSE).
