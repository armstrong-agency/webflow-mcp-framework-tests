# Advocate reports

Three Claude agents were each assigned one framework and asked to make its strongest honest case for AI-agent work through the Webflow MCP. They read the first-round probe results and the framework docs, and they looked for where my argument would fail. They are not statements from Finsweet, No-Code Supply Co., or Timothy Ricks.

| Report | Framework |
| --- | --- |
| [client-first.md](client-first.md) | Client-First |
| [mast.md](mast.md) | Mast |
| [lumos.md](lumos.md) | Lumos |

## How to read them

Each agent was told that I believed Client-First wins and planned to argue that publicly. That is why the reports speak to "Emmett" and list arguments to avoid. They are published unedited.

All three were written on 2026-11-02, before rounds 2 to 4 and the model evals, so some of their claims are out of date:

- **`calc()` claims.** Statements that a `calc()` value was silently corrupted or could render content invisible are wrong. Round 4 showed that this is a read-back bug only. See [round 4](../probes/round-4-rendered.md).
- **Mast's model priors and drift.** The expectation that Mast would score highest on zero-shot writing and drift least did not hold. See [the eval results](../evals/results.md).
- **Client-First responsive claims.** The reports predate the 200% text test and Client-First v3. See [round 4](../probes/round-4-rendered.md) and [the v3 notes](../probes/client-first-v3.md).
- **Test proposals.** The proposed experiments are ideas, and not all of them were run.

`lumos-naming.md`, mentioned in the Lumos report, was a local copy of Lumos's class naming docs. It is not republished here.
