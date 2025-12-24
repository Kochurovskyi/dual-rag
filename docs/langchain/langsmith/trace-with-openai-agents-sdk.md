# Trace with OpenAI Agents SDK

The OpenAI Agents SDK allows you to build agentic applications powered by OpenAI's models.

Learn how to trace your LLM applications using the OpenAI Agents SDK with LangSmith.

## Installation

<Info>
  Requires Python SDK version `langsmith>=0.3.15`.
</Info>

Install LangSmith with OpenAI Agents support:

<CodeGroup>
  ```bash pip theme={null}
  pip install "langsmith[openai-agents]"
  ```

  ```bash uv theme={null}
  uv add "langsmith[openai-agents]"
  ```
</CodeGroup>

This will install both the LangSmith library and the OpenAI Agents SDK.

## Quick Start

You can integrate LangSmith tracing with the OpenAI Agents SDK by using the `OpenAIAgentsTracingProcessor` class.

```python  theme={null}
import asyncio
from agents import Agent, Runner, set_trace_processors
from langsmith.integrations.openai_agents_sdk import OpenAIAgentsTracingProcessor

async def main():
    agent = Agent(
        name="Captain Obvious",
        instructions="You are Captain Obvious, the world's most literal technical support agent.",
    )

    question = "Why is my code failing when I try to divide by zero? I keep getting this error message."
    result = await Runner.run(agent, question)
    print(result.final_output)

if __name__ == "__main__":
    set_trace_processors([OpenAIAgentsTracingProcessor()])
    asyncio.run(main())
```

The agent's execution flow, including all spans and their details, will be logged to LangSmith.

<img src="https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/agent-trace.png?fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=7544fc0deb9c6279a9848da17d70bf8b" alt="OpenAI Agents SDK Trace in LangSmith" data-og-width="2984" width="2984" data-og-height="1782" height="1782" data-path="langsmith/images/agent-trace.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/agent-trace.png?w=280&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=18b3ec39553d20f562c61e68120b5ed7 280w, https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/agent-trace.png?w=560&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=e278d9a842f33c876cf1bb6937edaa9d 560w, https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/agent-trace.png?w=840&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=cf1fd1047a4f61bfe3cb0917d64cb403 840w, https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/agent-trace.png?w=1100&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=6d98b5286390e19b818c82fa3dcdd3e8 1100w, https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/agent-trace.png?w=1650&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=a20187910934b3921b5cac30df0922cb 1650w, https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/agent-trace.png?w=2500&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=3434b20ed1dfef6fc3751a50bb49b062 2500w" />

***

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/trace-with-openai-agents-sdk.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.langchain.com/llms.txt