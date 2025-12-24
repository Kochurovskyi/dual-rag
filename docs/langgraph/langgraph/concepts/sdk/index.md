<!-- Source: https://docs.langchain.com/langsmith/sdk -->

LangSmith provides both a Python SDK for interacting with [Agent Server](/langsmith/agent-server).

**Python SDK reference** For detailed information about the Python SDK, see [Python SDK reference docs](/langsmith/langgraph-python-sdk).



Installation

You can install the packages using the appropriate package manager for your language:

  * Python

  * JS

Copy

    pip install langgraph-sdk

Copy

    yarn add @langchain/langgraph-sdk



Python sync vs. async

The Python SDK provides both synchronous (`get_sync_client`) and asynchronous (`get_client`) clients for interacting with Agent Server:

  * Sync

  * Async

Copy

    from langgraph_sdk import get_sync_client

    client = get_sync_client(url=..., api_key=...)
    client.assistants.search()

Copy

    from langgraph_sdk import get_client

    client = get_client(url=..., api_key=...)
    await client.assistants.search()



Learn more

  * [Python SDK Reference](/langsmith/langgraph-python-sdk)
  * [LangGraph CLI API Reference](/langsmith/cli)
  * [JS/TS SDK Reference](/langsmith/langgraph-js-ts-sdk)

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/sdk.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.