# Test multi-turn conversations

This how-to guide walks you through the various ways you can set up the playground for multi-turn conversations, which will allow you to test different tool configurations and system prompts against longer threads of messages.

<img src="https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/multiturn-diagram.png?fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=8d468f069fe0ee6eac2e95c8942990aa" alt="Multiturn diagram" data-og-width="963" width="963" data-og-height="552" height="552" data-path="langsmith/images/multiturn-diagram.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/multiturn-diagram.png?w=280&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=ee61b9e81315c0b78ca5de6edb93f303 280w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/multiturn-diagram.png?w=560&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=ae0c7a1b4e68b46ef29469a2dc04610e 560w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/multiturn-diagram.png?w=840&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=9ce886cc977da99e442bf0ffeb82b683 840w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/multiturn-diagram.png?w=1100&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=b4365db9abb545cf507c7d3333404ffa 1100w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/multiturn-diagram.png?w=1650&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=fd3ff5634b263980b0f9b9d97756d2b8 1650w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/multiturn-diagram.png?w=2500&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=c28271d3bc0988362e988a64c1f1b396 2500w" />

## From an existing run

First, ensure you have properly [traced](/langsmith/observability) a multi-turn conversation, and then navigate to your tracing project. Once you get to your tracing project simply open the run, select the LLM call, and open it in the playground as follows:

<img src="https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/multiturn-from-run.gif?s=b4918bc6c6fac9c71859d962495db053" alt="Multiturn from run" data-og-width="1632" width="1632" data-og-height="1080" height="1080" data-path="langsmith/images/multiturn-from-run.gif" data-optimize="true" data-opv="3" />

You can then edit the system prompt, tweak the tools and/or output schema and observe how the output of the multi-turn conversation changes.

## From a dataset

Before starting, make sure you have [set up your dataset](/langsmith/manage-datasets-in-application). Since you want to evaluate multi-turn conversations, make sure there is a key in your inputs that contains a list of messages.

Once you have created your dataset, head to the playground and [load your dataset](/langsmith/manage-datasets-in-application#from-the-prompt-playground) to evaluate.

Then, add a messages list variable to your prompt, making sure to name it the same as the key in your inputs that contains the list of messages:

<img src="https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/multiturn-from-dataset.gif?s=42e2f11a348f50a7d2a0c8b6630c57e9" alt="Multiturn from dataset" data-og-width="1632" width="1632" data-og-height="1080" height="1080" data-path="langsmith/images/multiturn-from-dataset.gif" data-optimize="true" data-opv="3" />

When you run your prompt, the messages from each example will be added as a list in place of the 'Messages List' variable.

## Manually

There are two ways to manually create multi-turn conversations. The first way is by simply appending messages to the prompt:

<img src="https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/multiturn-manual.gif?s=1278a29854a66ee3dec92cc6f5059da0" alt="Multiturn manual" data-og-width="1632" width="1632" data-og-height="1080" height="1080" data-path="langsmith/images/multiturn-manual.gif" data-optimize="true" data-opv="3" />

This is helpful for quick iteration, but is rigid since the multi-turn conversation is hardcoded. Instead, if you want your prompt to work with any multi-turn conversation you can add a 'Messages List' variable and add your multi-turn conversation there:

<img src="https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/multiturn-manual-list.gif?s=12458af5558482bdfe40855c3117c02b" alt="Multiturn manual list" data-og-width="1632" width="1632" data-og-height="1080" height="1080" data-path="langsmith/images/multiturn-manual-list.gif" data-optimize="true" data-opv="3" />

This allows you to just tweak the system prompt or the tools, while allowing any multi-turn conversation to take the place of the `Messages List` variable, allowing you to reuse this prompt across various runs.

## Next steps

Now that you know how to set up the playground for multi-turn interactions, you can either manually inspect and judge the outputs, or you can [add evaluators](/langsmith/code-evaluator) to classify results.

You can also read [these how-to guides](/langsmith/create-a-prompt) to learn more about how to use the playground to run evaluations.

***

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/multiple-messages.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.langchain.com/llms.txt