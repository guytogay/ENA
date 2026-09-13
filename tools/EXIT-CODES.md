# Reference-tool exit codes

Use exit codes as machine contracts, not as a substitute for reading the tool-specific result.

```text
0    successful reference-tool operation
2    controlled ENA refusal / invalid caller state or input after CLI parsing
124  validate_change.py timed out while running the wrapped command
127  validate_change.py could not start the wrapped command
```

Argument-parser usage errors also use exit `2`.

`124` and `127` are deliberate semantic result codes of `validate_change.py`. They must not be normalized to the generic controlled-refusal code. Other tools may define their own documented semantic result codes; for example, `freshness_scan.py` uses `3` for stale records and `4` for unparseable records when the corresponding fail options are enabled.

Unexpected implementation defects are not controlled refusals. Do not catch arbitrary exceptions merely to turn them into exit `2`; expected boundary failures should be handled explicitly and concisely instead.
