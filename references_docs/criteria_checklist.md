# Submission Checklist — L2_Case05_Open_Choice_Agent

You chose this case, so you own the scope. Everything below is required
regardless of what you built.

## Define

- [ ] Problem statement: the domain, the user, and the decision the agent takes on their behalf.
- [ ] Justification that an agent is warranted — what makes this require runtime decision-making rather than a deterministic script.
- [ ] Data provenance note: source or generation method, what it represents, whether it includes the awkward cases that expose agent failure, and how you handled anything sensitive.

## Build

- [ ] Working agent, demonstrable end to end, where the model decides what to do at runtime rather than following a hardcoded sequence.
- [ ] At least two tools the agent invokes.
- [ ] A memory component, with a stated reason for the tier you chose.
- [ ] An explicit human validation gate before anything irreversible.
- [ ] Failure handling: output validated rather than trusted, the specific failure reason fed back on retry, and escalation with full context after repeated failure.

## Prove

- [ ] Evaluation against criteria you defined and defend, not by inspection.
- [ ] The cases it gets wrong, with at least two explained mechanistically.
- [ ] A deliberate failure injection and the recovery or escalation it triggered.
- [ ] `pytest-asyncio` suite covering the agent loop, tool mocking, and the recovery path, with passing output.
- [ ] Observability evidence: Portkey traces, LangSmith step traces, or equivalent.

## Communicate

- [ ] `REFLECTION.md`, 600-1000 words: what was built · why · what failed · how you fixed it · what you'd do differently · business impact. The failure sections carry the most weight.
- [ ] One slide pitching the solution to client stakeholders.
- [ ] A demo showing both a normal run and a failure being handled.
- [ ] Declared-effort statement: approximate hours and what you cut.

## Evidence standard

Every claim cites a specific input, tool call, trace, or measured number. "The
agent recovers from failures" scores nothing. "When the pricing tool returned a
string instead of a float, validation rejected it, the retry included the schema
mismatch, and the second attempt succeeded — trace attached" scores.

If you concluded during the build that your problem did not actually need an
agent, say so in your reflection. That finding, honestly reported and evidenced,
scores better than an agent nobody needed.

## Before you submit — challenge your own work

- [ ] Is the problem I chose narrow enough that I have actually solved it, rather than gestured at it?
- [ ] Can I explain every significant decision and the alternatives I rejected?
- [ ] Would my solution survive being pointed at data I did not choose?
- [ ] Have I named specific inputs where it fails, or only described failure in general terms?
- [ ] Does my write-up let the work speak for itself, without guessing at how it will be scored?

## How this will be assessed

There is no answer key for this case, because you defined the problem. You are
scored against the criteria for your level and against your own stated definition
of success — so a vague definition of success is not a safe choice, it is an
unscoreable one.

Two things carry disproportionate weight:

1. **Your data.** Where it came from, what it does and does not represent, and
   whether it contains cases that genuinely stress your solution. Data selected
   to flatter the prototype is a finding against you, not a neutral choice.
2. **Your failure analysis.** Specific inputs, specific wrong outputs, specific
   causes. "It sometimes struggles with ambiguous cases" is not a failure
   analysis.

You will answer several questions about your own submission at submission time.
They are generated from what you submitted — your stated problem, your data
decisions, your architecture — so they cannot be prepared in advance.
