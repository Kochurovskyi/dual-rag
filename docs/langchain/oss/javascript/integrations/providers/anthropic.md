# Overview

All functionality related to Anthropic models..

[Anthropic](https://www.anthropic.com/) is an AI safety and research company, and is the creator of Claude.
This page covers all integrations between Anthropic models and LangChain.

## Prompting Best Practices

Anthropic models have several prompting best practices compared to OpenAI models.

**System Messages may only be the first message**

Anthropic models require any system messages to be the first one in your prompts.

## `ChatAnthropic`

`ChatAnthropic` is a subclass of LangChain's `ChatModel`, meaning it works best with `ChatPromptTemplate`.
You can import this wrapper with the following code:

<Tip>
  See [this section for general instructions on installing LangChain packages](/oss/javascript/langchain/install).
</Tip>

```bash npm theme={null}
npm install @langchain/anthropic @langchain/core
```

```typescript  theme={null}
import { ChatAnthropic } from "@langchain/anthropic";
const model = new ChatAnthropic({});
```

When working with ChatModels, it is preferred that you design your prompts as `ChatPromptTemplate`s.
Here is an example below of doing that:

```typescript  theme={null}
import { ChatPromptTemplate } from "@langchain/classic/prompts";

const prompt = ChatPromptTemplate.fromMessages([
  ["system", "You are a helpful chatbot"],
  ["human", "Tell me a joke about {topic}"],
]);
```

You can then use this in a chain as follows:

```typescript  theme={null}
const chain = prompt.pipe(model);
await chain.invoke({ topic: "bears" });
```

See the [chat model integration page](/oss/javascript/integrations/chat/anthropic/) for more examples, including multimodal inputs.

***

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/javascript/integrations/providers/anthropic.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.langchain.com/llms.txt