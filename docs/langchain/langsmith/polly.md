# LangSmith Polly

<Callout color="#4F46E5">
  **Polly is in beta.** Your [feedback](https://forum.langchain.com) on Polly is invaluable as the team refines its capabilities.
</Callout>

**LangSmith Polly** is an AI assistant embedded directly in your LangSmith [workspace](/langsmith/administration-overview#workspaces) to help you analyze and understand your application data.

Polly helps you gain insight from your traces, conversation threads, and prompts without having to dig through data manually. By asking natural language questions, you can quickly understand agent performance, debug issues, and analyze user sentiment.

<img src="https://mintcdn.com/langchain-5e9cc07a/Ttks5oP9I9O2zjYP/langsmith/images/polly.png?fit=max&auto=format&n=Ttks5oP9I9O2zjYP&q=85&s=fa4a72becb05f414f053f06af4ce6afb" alt="LangSmith Polly icon" style={{float: 'left', marginRight: '20px', marginTop: '-1px', marginBottom: '20px', maxWidth: '100px'}} data-og-width="120" width="120" data-og-height="54" height="54" data-path="langsmith/images/polly.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/Ttks5oP9I9O2zjYP/langsmith/images/polly.png?w=280&fit=max&auto=format&n=Ttks5oP9I9O2zjYP&q=85&s=e0466a20faaeb2a5a89007aa07788cfb 280w, https://mintcdn.com/langchain-5e9cc07a/Ttks5oP9I9O2zjYP/langsmith/images/polly.png?w=560&fit=max&auto=format&n=Ttks5oP9I9O2zjYP&q=85&s=5ebe583f22eb955aade91c1d030a9c8f 560w, https://mintcdn.com/langchain-5e9cc07a/Ttks5oP9I9O2zjYP/langsmith/images/polly.png?w=840&fit=max&auto=format&n=Ttks5oP9I9O2zjYP&q=85&s=f8f45119dda87228e2d5d9f59de40025 840w, https://mintcdn.com/langchain-5e9cc07a/Ttks5oP9I9O2zjYP/langsmith/images/polly.png?w=1100&fit=max&auto=format&n=Ttks5oP9I9O2zjYP&q=85&s=d1c4e7b178aad853b49bcd74e1afac22 1100w, https://mintcdn.com/langchain-5e9cc07a/Ttks5oP9I9O2zjYP/langsmith/images/polly.png?w=1650&fit=max&auto=format&n=Ttks5oP9I9O2zjYP&q=85&s=865d3c5195858e7114b3ec2e5f9876ea 1650w, https://mintcdn.com/langchain-5e9cc07a/Ttks5oP9I9O2zjYP/langsmith/images/polly.png?w=2500&fit=max&auto=format&n=Ttks5oP9I9O2zjYP&q=85&s=725b2b5615c1248dd39959e16cac36d2 2500w" /> Polly appears in the right-hand bottom corner of the following locations within [LangSmith UI](https://smith.langchain.com), optimized for different use cases:

* [Trace pages](#tracing-page)
* [Thread views](#thread-views)
* [Prompt Playground](#prompt-playground)

### Tracing page

On an individual [trace](/langsmith/observability-concepts#traces), Polly pulls in the context of the page and analyzes the [run](/langsmith/observability-concepts#runs). Polly reads the run data and trajectory to help you understand what happened and identify areas for improvement.

To ask Polly about your tracing:

1. In your **Tracing Projects**, click on a trace to view its details page.
2. Select a run in the trace.
3. Open Polly in the right-hand corner of the page to ask questions relating to this run.
4. Ask Polly a question about your data. You can use the sample questions or you might ask questions like:

   * "Is there anything that the agent could have done better here?"
   * "Why did this run fail?"
   * "What took the most time in this trace?"
   * "What errors occurred during this run?"
   * "Summarize what happened in this trace"

When analyzing runs, Polly will examine the full trace context, including [run metadata](/langsmith/observability-concepts#metadata), inputs, outputs, intermediate steps, and configuration to provide actionable insights. This helps you diagnose issues without manually expanding each step in the trace tree or cross-referencing multiple runs.

### Thread view

Under the **Threads** tab, Polly analyzes conversation [threads](/langsmith/observability-concepts#threads) by pulling in relevant information about the user interaction. This helps you understand user sentiment and conversation outcomes.

To ask Polly about your threads:

1. Select a thread.
2. Open Polly in the right-hand corner of the page to ask questions relating to this thread.
3. Ask Polly a question about the conversation thread. You might ask questions like:

   * "Did the user seem frustrated?"
   * "What issues is the user experiencing?"
   * "How did this conversation resolve?"
   * "Was the user's problem solved?"
   * "What was the main topic of this thread?"

Use Polly in thread view to gain insights into how users are interacting with your application. Understand conversation outcomes and whether issues were resolved, identify common user pain points, and track user sentiment through thread analysis. This helps you improve user experience by understanding what's working and what needs improvement in your application's responses.

### Prompt Playground

When you open a [prompt](/langsmith/prompt-engineering-concepts#prompt-in-langsmith) in the [Playground](/langsmith/prompt-engineering-concepts#prompt-playground), Polly can help you edit and improve your prompts based on your instructions. Polly reads the prompt and makes suggested edits.

To ask Polly about your prompt:

1. Enter the **Playground** from the left-hand navigation or trace view.
2. Select a prompt to experiment with.
3. Open Polly in the right-hand corner of the page to work on this prompt.
4. You can use one of the automated options that Polly suggests:

   * <Icon icon="play" /> **Optimize prompt**: Polly will analyze the current prompt and make edits to the prompt with a summary of the changes.
   * <Icon icon="wrench" /> **Generate a tool**: Give details to Polly on the tool you would like to add. It will generate a tool for your prompt template. It can also help you modify existing tooling or system messages about tooling. Then, have Polly test tool configurations with reviews of sample output from the model using the tool.
   * <Icon icon="brackets-curly" /> **Generate an output schema**: Polly will create a JSON schema that defines the structure of the output you want the model to generate. This is useful when you need the model to return data in a specific format. Select this option, and then provide Polly with the type of data, fields/properties, and any other constraints you might need.

   Or, you might ask your own questions, like:

   * "Make it respond in Italian"
   * "Add more context about the user's role"
   * "Make the tone more professional"
   * "Simplify the instructions"
   * "Add examples to the prompt"

   <img className="block dark:hidden" src="https://mintcdn.com/langchain-5e9cc07a/Ttks5oP9I9O2zjYP/langsmith/images/polly-prompt-tool.png?fit=max&auto=format&n=Ttks5oP9I9O2zjYP&q=85&s=f99e532bc008d41a40808c8f2eb988d3" alt="Prompt Playground showing Polly chat in the sidebar with information on a generated tool." data-og-width="1520" width="1520" data-og-height="1151" height="1151" data-path="langsmith/images/polly-prompt-tool.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/Ttks5oP9I9O2zjYP/langsmith/images/polly-prompt-tool.png?w=280&fit=max&auto=format&n=Ttks5oP9I9O2zjYP&q=85&s=32813c69c4faf716649aafccb0fe8275 280w, https://mintcdn.com/langchain-5e9cc07a/Ttks5oP9I9O2zjYP/langsmith/images/polly-prompt-tool.png?w=560&fit=max&auto=format&n=Ttks5oP9I9O2zjYP&q=85&s=25d105f79090bea64897cd7a439b3ddb 560w, https://mintcdn.com/langchain-5e9cc07a/Ttks5oP9I9O2zjYP/langsmith/images/polly-prompt-tool.png?w=840&fit=max&auto=format&n=Ttks5oP9I9O2zjYP&q=85&s=259d26f4be950927a72acdc7b2070a68 840w, https://mintcdn.com/langchain-5e9cc07a/Ttks5oP9I9O2zjYP/langsmith/images/polly-prompt-tool.png?w=1100&fit=max&auto=format&n=Ttks5oP9I9O2zjYP&q=85&s=2b52a59e445e14388c66cc585cb34864 1100w, https://mintcdn.com/langchain-5e9cc07a/Ttks5oP9I9O2zjYP/langsmith/images/polly-prompt-tool.png?w=1650&fit=max&auto=format&n=Ttks5oP9I9O2zjYP&q=85&s=3fde3e574cab288f671cc0f2864e9a64 1650w, https://mintcdn.com/langchain-5e9cc07a/Ttks5oP9I9O2zjYP/langsmith/images/polly-prompt-tool.png?w=2500&fit=max&auto=format&n=Ttks5oP9I9O2zjYP&q=85&s=98f8ea9f62eace790f560e0563d4cc7b 2500w" />

   <img className="hidden dark:block" src="https://mintcdn.com/langchain-5e9cc07a/Ttks5oP9I9O2zjYP/langsmith/images/polly-prompt-tool-dark.png?fit=max&auto=format&n=Ttks5oP9I9O2zjYP&q=85&s=1b0b035d9ac5471b7fc4d536e66149a6" alt="Prompt Playground showing Polly chat in the sidebar with information on a generated tool." data-og-width="1523" width="1523" data-og-height="1152" height="1152" data-path="langsmith/images/polly-prompt-tool-dark.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/Ttks5oP9I9O2zjYP/langsmith/images/polly-prompt-tool-dark.png?w=280&fit=max&auto=format&n=Ttks5oP9I9O2zjYP&q=85&s=63b88b48b4c46acc691a8de870e29b56 280w, https://mintcdn.com/langchain-5e9cc07a/Ttks5oP9I9O2zjYP/langsmith/images/polly-prompt-tool-dark.png?w=560&fit=max&auto=format&n=Ttks5oP9I9O2zjYP&q=85&s=837158f3440dcf6e9e031d4426c712a0 560w, https://mintcdn.com/langchain-5e9cc07a/Ttks5oP9I9O2zjYP/langsmith/images/polly-prompt-tool-dark.png?w=840&fit=max&auto=format&n=Ttks5oP9I9O2zjYP&q=85&s=651982d8dc9d454ea7cc99dbbf23c454 840w, https://mintcdn.com/langchain-5e9cc07a/Ttks5oP9I9O2zjYP/langsmith/images/polly-prompt-tool-dark.png?w=1100&fit=max&auto=format&n=Ttks5oP9I9O2zjYP&q=85&s=98ead88299efdcee34f54dd05084ab7b 1100w, https://mintcdn.com/langchain-5e9cc07a/Ttks5oP9I9O2zjYP/langsmith/images/polly-prompt-tool-dark.png?w=1650&fit=max&auto=format&n=Ttks5oP9I9O2zjYP&q=85&s=5d79413aaf531d5cfe9881fec582140d 1650w, https://mintcdn.com/langchain-5e9cc07a/Ttks5oP9I9O2zjYP/langsmith/images/polly-prompt-tool-dark.png?w=2500&fit=max&auto=format&n=Ttks5oP9I9O2zjYP&q=85&s=fa2fb0268ae7784d6f733aa4020dd00f 2500w" />

## What's next

Learn more about the features that Polly helps you explore:

<CardGroup cols={2}>
  <Card title="Observability" icon="magnifying-glass" href="/langsmith/observability">
    Learn more about tracing and monitoring your LLM applications
  </Card>

  <Card title="Threads" icon="comments" href="/langsmith/threads">
    Understand how threads work in LangSmith
  </Card>

  <Card title="Prompt Engineering" icon="wand-magic-sparkles" href="/langsmith/prompt-engineering">
    Create and iterate on prompts in the playground
  </Card>

  <Card title="Evaluation" icon="clipboard-check" href="/langsmith/evaluation">
    Evaluate and test your applications systematically
  </Card>
</CardGroup>

***

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/polly.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.langchain.com/llms.txt