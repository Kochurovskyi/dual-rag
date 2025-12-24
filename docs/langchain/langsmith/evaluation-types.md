# Evaluation types

LangSmith supports various evaluation types for different stages of development and deployment. Understanding when to use each helps build a comprehensive evaluation strategy.

## Offline evaluation types

Offline evaluation tests applications on curated datasets before deployment. By running evaluations on examples with reference outputs, teams can compare versions, validate functionality, and build confidence before exposing changes to users.

Run offline evaluations client-side using the LangSmith SDK ([Python](https://docs.smith.langchain.com/reference/python/reference) and [TypeScript](https://docs.smith.langchain.com/reference/js)) or server-side via the [Prompt Playground](/langsmith/observability-concepts#prompt-playground) or [automations](/langsmith/rules).

<img src="https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/offline.png?fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=879e4ee3616cecd7cff39879cfc6ec7b" alt="Offline" data-og-width="1581" width="1581" data-og-height="477" height="477" data-path="langsmith/images/offline.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/offline.png?w=280&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=ba01953933bebf30c6dc5d8112a3b3db 280w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/offline.png?w=560&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=3424f1efa82db871cba04c9a4bcac188 560w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/offline.png?w=840&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=ad0eca755f778a844465976b00a3efb6 840w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/offline.png?w=1100&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=cddc86584ad7d9e82a60fc219cff886b 1100w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/offline.png?w=1650&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=e8cf5a07175523921ee1595e36ea1d73 1650w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/offline.png?w=2500&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=0f94c55d22273e06d6cde301b4a0a3f3 2500w" />

### Benchmarking

*Benchmarking* compares multiple application versions on a curated dataset to identify the best performer. This process involves creating a dataset of representative inputs, defining performance metrics, and testing each version.

Benchmarking requires dataset curation with gold-standard reference outputs and well-designed comparison metrics. Examples:

* **RAG Q\&A bot**: Dataset of questions and reference answers, with an LLM-as-judge evaluator checking semantic equivalence between actual and reference answers.
* **ReACT agent**: Dataset of user requests and reference tool calls, with a heuristic evaluator verifying all expected tool calls were made.

### Unit tests

*Unit tests* verify the correctness of individual system components. In LLM contexts, [unit tests are often rule-based assertions](https://hamel.dev/blog/posts/evals/#level-1-unit-tests) on inputs or outputs (e.g., verifying LLM-generated code compiles, JSON loads successfully) that validate basic functionality.

Unit tests typically expect consistent passing results, making them suitable for CI pipelines. When running in CI, configure caching to minimize LLM API calls and associated costs.

### Regression tests

*Regression tests* measure performance consistency across application versions over time. They ensure new versions do not degrade performance on cases the current version handles correctly, and ideally demonstrate improvements over the baseline. These tests typically run when making updates expected to affect user experience (e.g., model or architecture changes).

LangSmith's comparison view highlights regressions (red) and improvements (green) relative to the baseline, enabling quick identification of changes.

<img src="https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/comparison-view.png?fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=c4ed751dc3e74f5ad16634dff061bd77" alt="Comparison view" data-og-width="3018" width="3018" data-og-height="1532" height="1532" data-path="langsmith/images/comparison-view.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/comparison-view.png?w=280&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=4b6c96f4480262f4db39b7a06a971ca8 280w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/comparison-view.png?w=560&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=568b65404d8bbe7444d742fbf131bb4d 560w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/comparison-view.png?w=840&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=36c750c22fcc302d617f1e6e8a5014a0 840w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/comparison-view.png?w=1100&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=fe9225cdcf381e2b6ef17c0bf99b3004 1100w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/comparison-view.png?w=1650&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=ac42818b24a858252bb320a23e06b1c2 1650w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/comparison-view.png?w=2500&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=bd4214772a68d401b48b704b56a35e4a 2500w" />

### Backtesting

*Backtesting* evaluates new application versions against historical production data. Production logs are converted into a dataset, then newer versions process these examples to assess performance on past, realistic user inputs.

This approach is commonly used for evaluating new model releases. For example, when a new model becomes available, test it on the most recent production runs and compare results to actual production outcomes.

### Pairwise evaluation

*Pairwise evaluation* compares outputs from two versions by determining relative quality rather than assigning absolute scores. For some tasks, [determining "version A is better than B"](https://www.oreilly.com/radar/what-we-learned-from-a-year-of-building-with-llms-part-i/) is easier than scoring each version independently.

This approach proves particularly useful for LLM-as-judge evaluations on subjective tasks. For example, in summarization, determining "Which summary is clearer and more concise?" is often simpler than assigning numeric clarity scores.

Learn [how run pairwise evaluations](/langsmith/evaluate-pairwise).

## Online evaluation types

Online evaluation assesses production application outputs in near real-time. Without reference outputs, these evaluations focus on detecting issues, monitoring quality trends, and identifying edge cases that inform future offline testing.

Online evaluators typically run server-side. LangSmith provides built-in [LLM-as-judge evaluators](/langsmith/llm-as-judge) for configuration, and supports custom code evaluators that run within LangSmith.

<img src="https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/online.png?fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=8d6c1b932e5487c4c01d84ae4f984240" alt="Online" data-og-width="1474" width="1474" data-og-height="521" height="521" data-path="langsmith/images/online.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/online.png?w=280&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=fd658bcfa1357196dd87ab6263a4896d 280w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/online.png?w=560&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=371e394c68e91e93efe1c80fb85d5484 560w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/online.png?w=840&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=5c65ce1c6487a959ce54bffcf8155bb8 840w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/online.png?w=1100&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=b8e1815f6df4419f65294d2a658bc9f0 1100w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/online.png?w=1650&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=f737a486fdb5232e8db121a760075dd8 1650w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/online.png?w=2500&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=0ad2d3d938b8048c21f23f0052904940 2500w" />

### Real-time monitoring

Monitor application quality continuously as users interact with the system. Online evaluations run automatically on production traffic, providing immediate feedback on each interaction. This enables detection of quality degradation, unusual patterns, or unexpected behaviors before they impact significant user populations.

### Anomaly detection

Identify outliers and edge cases that deviate from expected patterns. Online evaluators can flag runs with unusual characteristics—extremely long or short responses, unexpected error rates, or outputs that fail safety checks—for human review and potential addition to offline datasets.

### Production feedback loop

Use insights from production to improve offline evaluation. Online evaluations surface real-world issues and usage patterns that may not appear in curated datasets. Failed production runs become candidates for dataset examples, creating an iterative cycle where production experience continuously refines testing coverage.

***

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/evaluation-types.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.langchain.com/llms.txt