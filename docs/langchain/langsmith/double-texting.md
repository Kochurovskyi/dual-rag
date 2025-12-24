# Double texting

<Info>
  **Prerequisites**

  * [Agent Server](/langsmith/agent-server)
</Info>

Many times users might interact with your graph in unintended ways.
For instance, a user may send one message and before the graph has finished running send a second message.
More generally, users may invoke the graph a second time before the first run has finished.
We call this "double texting".

[Enqueue](#enqueue-default) is the default double texting (multi-tasking) strategy when creating runs in the [Agent Server](/langsmith/agent-server).

<Note>
  Double texting is a feature of LangSmith Deployment. It is not available in the [LangGraph open source framework](/oss/python/langgraph/overview).
</Note>

<img src="https://mintcdn.com/langchain-5e9cc07a/Hucw5hmCzWXDanL-/langsmith/images/double-texting.png?fit=max&auto=format&n=Hucw5hmCzWXDanL-&q=85&s=1cae1e8cd4920872e7992460b081f76d" alt="Double-text strategies across first vs. second run: Reject keeps only the first; Enqueue runs the second afterward; Interrupt halts the first to run the second; Rollback reverts the first and reruns with the second." data-og-width="1886" width="1886" data-og-height="648" height="648" data-path="langsmith/images/double-texting.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/Hucw5hmCzWXDanL-/langsmith/images/double-texting.png?w=280&fit=max&auto=format&n=Hucw5hmCzWXDanL-&q=85&s=67fc4d3817141da00d0f0e0b5c6de093 280w, https://mintcdn.com/langchain-5e9cc07a/Hucw5hmCzWXDanL-/langsmith/images/double-texting.png?w=560&fit=max&auto=format&n=Hucw5hmCzWXDanL-&q=85&s=2c9cf620db602c51a7e3804cb0815058 560w, https://mintcdn.com/langchain-5e9cc07a/Hucw5hmCzWXDanL-/langsmith/images/double-texting.png?w=840&fit=max&auto=format&n=Hucw5hmCzWXDanL-&q=85&s=7e16e946f3c616476fd99b40aa731a3c 840w, https://mintcdn.com/langchain-5e9cc07a/Hucw5hmCzWXDanL-/langsmith/images/double-texting.png?w=1100&fit=max&auto=format&n=Hucw5hmCzWXDanL-&q=85&s=98032b626677cf73744a3922112abda4 1100w, https://mintcdn.com/langchain-5e9cc07a/Hucw5hmCzWXDanL-/langsmith/images/double-texting.png?w=1650&fit=max&auto=format&n=Hucw5hmCzWXDanL-&q=85&s=2537ca1524e871001cd454f41dca6597 1650w, https://mintcdn.com/langchain-5e9cc07a/Hucw5hmCzWXDanL-/langsmith/images/double-texting.png?w=2500&fit=max&auto=format&n=Hucw5hmCzWXDanL-&q=85&s=d37e7e8cd1c4a5bad8cc399d0b878382 2500w" />

## Enqueue (default)

This option allows the current run to finish before processing any new input. Incoming requests are queued and executed sequentially once prior runs complete.

For configuring the enqueue double text option, refer to the [how-to guide](/langsmith/enqueue-concurrent).

## Reject

This option rejects any additional incoming runs while a current run is in progress and prevents concurrent execution or double texting.

For configuring the reject double text option, refer to the [how-to guide](/langsmith/reject-concurrent).

## Interrupt

This option halts the current execution and preserves the progress made up to the interruption point. The new user input is then inserted, and execution continues from that state.

When using this option, your graph must account for potential edge cases. For example, a tool call may have been initiated but not yet completed at the time of interruption. In these cases, handling or removing partial tool calls may be necessary to avoid unresolved operations.

For configuring the interrupt double text option, refer to the [how-to guide](/langsmith/interrupt-concurrent).

## Rollback

This option halts the current execution and reverts all progress—including the initial run input—before processing the new user input. The new input is treated as a fresh run, starting from the initial state.

For configuring the rollback double text option, refer to the [how-to guide](/langsmith/rollback-concurrent).

***

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/double-texting.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.langchain.com/llms.txt