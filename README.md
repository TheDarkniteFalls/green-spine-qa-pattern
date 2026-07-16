# Green-Spine QA Pattern

<!-- toolkit-trust-card:start -->
> **Public contract:** Stable pattern · about 5 min · Python 3 · no model · no network
>
> **Operation:** Read-only check; examples may use temporary files
>
> **A pass establishes:** One representative synthetic path and its known-bad cases satisfy the named checkpoint.
>
> **It does not establish:** A green spine deliberately does not prove every feature, path, or experience quality.
>
> **First check:** `python3 spine_green.py`
<!-- toolkit-trust-card:end -->

A tiny example of one named command that proves an important workflow still
works.

The demo does not call a model. It checks one synthetic assistant workflow:
structured output must parse, cite supplied sources, stay read-only, answer the
happy path, and reject known-bad outputs.

## Why It Exists

Large projects often collect many tests but still need one compact command that
answers a practical question: is the important path still healthy?

This repo shows the small version of that pattern.

## Run

```sh
python3 spine_green.py
```

Expected result:

```text
PASS happy_path_contract
PASS happy_path_answer
PASS known_bad_outputs
PASS green_spine
```

You can also pass a fixture path:

```sh
python3 spine_green.py examples/spine_case.json
```

## What The Spine Checks

- The happy-path output is valid JSON.
- Citations use only supplied source IDs.
- The workflow stays read-only.
- The answer contains the expected user-visible result.
- Known-bad outputs still fail.

## Browser QA Without Brittle Text Matching

`browser_structure_check.py` shows the same idea for browser-facing work. It
checks stable structure in a saved HTML fixture instead of matching exact page
copy:

- durable `data-testid` anchors for the workflow and form
- a submit button identified by action and type
- a status region identified by role and live-region attributes
- a known-bad fixture that must fail

```sh
python3 browser_structure_check.py
python3 browser_structure_check.py --self-test
```

## Choosing A Green Spine

Pick one path that would make the project feel broken if it regressed. Keep the
command boring, named, and fast enough to run before publishing or handing work
to a reviewer.

Good green spines usually combine a few existing focused checks. They should not
try to prove everything.

## How These Fit Together

This repo is one piece of a small public toolkit:

- [Public Repo Safety Kit](https://github.com/TheDarkniteFalls/public-repo-safety-kit)
  checks a public-candidate repo before publishing.
- [EvidenceGate](https://github.com/TheDarkniteFalls/evidencegate) records the
  evidence and checks behind an AI-assisted change.
- [Local Model Reliability Example](https://github.com/TheDarkniteFalls/local-model-reliability-example)
  validates structured model output and protected-path boundaries before
  trusting it.
- [Context Boundary Examples](https://github.com/TheDarkniteFalls/context-boundary-examples)
  checks whether an answer stays inside supplied evidence.
- Green-Spine QA Pattern shows how to bundle the important path behind one
  repeatable command.
- [Codex Project Instructions Starter](https://github.com/TheDarkniteFalls/codex-project-instructions-starter)
  gives coding agents clear project rules before they work.

## Public Data Notice

All examples are synthetic. Do not add private prompts, real assistant logs,
connector exports, credentials, or personal data.

## Scope

This is a pattern, not a framework. Start with one command. Add structure only
when the command becomes too hard to read or too slow to run.

## Quality Checks

```sh
python3 spine_green.py
python3 spine_green.py examples/spine_case.json
python3 browser_structure_check.py
python3 browser_structure_check.py --self-test
python3 -m py_compile spine_green.py
python3 -m py_compile browser_structure_check.py
```
