# Green-Spine QA Pattern

Put the checks for one important workflow behind a command you can run again.
That is the “green spine”: a small set of checks for the path you most need to
keep working. Green means those checks passed, not that every part of the
project has been tested.

This example checks a made-up assistant answer. It must be readable JSON,
refer to supplied sources, stay read-only and contain the expected answer.
The command also checks that deliberately bad answers are rejected. It calls
no model and uses no network.

## Why It Exists

If your project has many separate tests, it can be hard to know which ones to
run before handing over a change. Start by naming one important path and the
few checks that cover it. This repository gives you a small example to try
before adapting that idea to your own project.

## Run

From this repository’s folder, run the example with Python 3:

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

These four passes mean the example answer met its rules and the known-bad
answers were rejected. A fixture is a saved test input; you can name the
supplied one explicitly:

```sh
python3 spine_green.py examples/spine_case.json
```

<!-- toolkit-trust-card:placement -->

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

## What The Spine Checks

- The expected successful answer (the “happy path”) is valid JSON.
- Citations use only supplied source IDs.
- The workflow stays read-only.
- The answer contains the expected user-visible result.
- Known-bad outputs still fail.

## Browser QA Without Brittle Text Matching

Try `browser_structure_check.py` for the same idea applied to a saved web
page. It reads an HTML fixture and checks for elements a test can identify
even when the wording changes:

- `data-testid` labels that identify the workflow and form
- a submit button identified by action and type
- a status message region with a role and attributes for announcing updates
- a known-bad fixture that must fail

```sh
python3 browser_structure_check.py
python3 browser_structure_check.py --self-test
```

The first command checks the saved page. The self-test also confirms that the
fixture with missing elements fails. Neither command opens a browser or clicks
the form: use a rendered browser test to check actual interaction, layout and
keyboard access.

## Choosing A Green Spine

Choose one path you want to protect. For a form, that might be entering valid
data, submitting it and seeing confirmation. Name what success looks like,
then include a bad-input case so you can check that failures are caught too.

Combine existing focused checks where you can. Keep the command small enough
to run before handing over a change, and list what it leaves untested. A pass
does not give permission to publish or establish that people find the result useful.

## How These Fit Together

Choose a related tool if you need a different check:

- [Public Repo Safety Kit](https://github.com/TheDarkniteFalls/public-repo-safety-kit)
  checks a repository you intend to publish.
- [EvidenceGate](https://github.com/TheDarkniteFalls/evidencegate) records the
  evidence and checks behind an AI-assisted change.
- [Local Model Reliability Example](https://github.com/TheDarkniteFalls/local-model-reliability-example)
  validates structured model output and protected-path boundaries.
- [Context Boundary Examples](https://github.com/TheDarkniteFalls/context-boundary-examples)
  checks whether an answer stays inside supplied evidence.
- [Codex Project Instructions Starter](https://github.com/TheDarkniteFalls/codex-project-instructions-starter)
  gives coding agents clear project rules before they work.

## Public Data Notice

All examples are synthetic. Do not add private prompts, real assistant logs,
connector exports, credentials, or personal data.

## Scope

Start with one command and adapt the checks to the workflow you chose. Add
structure only when the command becomes too hard to read or too slow to run.
The supplied synthetic examples do not establish coverage for your own project.

## Quality Checks

```sh
python3 spine_green.py
python3 spine_green.py examples/spine_case.json
python3 browser_structure_check.py
python3 browser_structure_check.py --self-test
python3 -m py_compile spine_green.py
python3 -m py_compile browser_structure_check.py
```
