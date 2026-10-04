# Measured Narration Duration Fit

This skill checks whether measured narration fits approved shot budgets. Give it up to 30 segments with measured narration milliseconds, approved shot duration, start offset, allowed pause, and a cut version. Available time is shot duration minus start offset; the allowed post-segment pause consumes that budget and is included in required time. It returns per-segment available/required/overrun milliseconds, a total check, and concrete trim-copy or extend-approved-shot tasks.

It does not synthesize speech, rearrange shots, alter approved copy, or hide timing issues by speeding audio up. If only word count or estimated speaking rate is supplied, it asks for measured duration. Missing offsets or pauses means it cannot confirm a fit.

Install: `npx skills add xxjrq/video-narration-duration-fit-cn`

```sh
python3 scripts/check_duration.py fixtures/within-budget-input.json
sh scripts/self_test.sh
```


See [feasible copy reduction](fixtures/trim-feasible-input.json), [fixed pause overrun](fixtures/fixed-pause-overrun-input.json), [fixed offset overrun](fixtures/fixed-offset-overrun-input.json), and the [actual offline reports](fixtures/action-boundary-report.md). Copy reduction is suggested only when narration can remain; fixed offsets and pauses are not silently changed.

See the [successful fixture](fixtures/within-budget-input.json), [successful report](fixtures/within-budget-report.md), [post-pause overrun fixture](fixtures/success-input.json), and [failure fixture](fixtures/missing-measured-duration.json). The implementation is original; public Whisper project links are retained in the Chinese README as contextual sources.
