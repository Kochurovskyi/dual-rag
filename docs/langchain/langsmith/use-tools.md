# Use tools in a prompt

Tools allow language models to interact with external systems and perform actions beyond just generating text. In the LangSmith playground, you can use two types of tools:

1. **Built-in tools**: Pre-configured tools provided by model providers (like OpenAI and Anthropic) that are ready to use. These include capabilities like web search, code interpretation, and more.

2. **Custom tools**: Functions you define to perform specific tasks. These are useful when you need to integrate with your own systems or create specialized functionality. When you define custom tools within the LangSmith Playground, you can verify that the model correctly identifies and calls these tools with the correct arguments. Soon we plan to support executing these custom tool calls directly.

## When to use tools

* Use **built-in tools** when you need common capabilities like web search or code interpretation. These are built and maintained by the model providers.

* Use **custom tools** when you want to test and validate your own tool designs, including:

  * Validating which tools the model chooses to use and seeing the specific arguments it provides in tool calls
  * Simulating tool interactions

## Built-in tools

The LangSmith Playground has native support for a variety of tools from OpenAI and Anthropic. If you want to use a tool that isn't explicitly listed in the Playground, you can still add it by manually specifying its `type` and any required arguments.

### OpenAI Tools

* **Web search**: [Search the web for real-time information](https://platform.openai.com/docs/guides/tools-web-search?api-mode=responses)
* **Image generation**: [Generate images based on a text prompt](https://platform.openai.com/docs/guides/tools-image-generation)
* **MCP**: [Gives the model access to tools hosted on a remote MCP server](https://platform.openai.com/docs/guides/tools-remote-mcp)
* [View all OpenAI tools](https://platform.openai.com/docs/guides/tools?api-mode=responses)

### Anthropic Tools

* **Web search**: [Search the web for up-to-date information](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool)
* [View all Anthropic tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)

## Adding and using tools

### Add a tool

To add a tool to your prompt, click the `+ Tool` button at the bottom of the prompt editor. <img src="https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/add-tool.png?fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=b922d9b219cff1bbc726bc2f6b82d6b6" alt="Add tool" data-og-width="753" width="753" data-og-height="351" height="351" data-path="langsmith/images/add-tool.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/add-tool.png?w=280&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=d08cf08da323465b8340f5395f93cb94 280w, https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/add-tool.png?w=560&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=c54feb8a827ef4d7858061f252200fc1 560w, https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/add-tool.png?w=840&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=59fbdea1f87fc501812417a5457ff249 840w, https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/add-tool.png?w=1100&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=f850e2a4dacb21cba0939bd017ce2106 1100w, https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/add-tool.png?w=1650&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=5b40ff17dd48d154c83b5063bab9f673 1650w, https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/add-tool.png?w=2500&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=6c48a7e9d6c921f206fc9ff777d94ed6 2500w" />

### Use a built-in tool

1. In the tool section, select the built-in tool you want to use. You'll only see the tools that are compatible with the provider and model you've chosen.
2. When the model calls the tool, the playground will display the response

<img src="https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/web-search-tool.gif?s=2fb882f785abc26d0e5412557cc982ca" alt="Web search tool" data-og-width="1036" width="1036" data-og-height="720" height="720" data-path="langsmith/images/web-search-tool.gif" data-optimize="true" data-opv="3" />

### Create a custom tool

To create a custom tool, you'll need to provide:

* Name: A descriptive name for your tool
* Description: Clear explanation of what the tool does
* Arguments: The inputs your tool requires

<img src="https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/custom-tool.gif?s=69638e515cd7c5be413cf13348e10974" alt="Custom tool" data-og-width="1028" width="1028" data-og-height="720" height="720" data-path="langsmith/images/custom-tool.gif" data-optimize="true" data-opv="3" />

Note: When running a custom tool in the playground, the model will respond with a JSON object containing the tool name and the tool call. Currently, there's no way to connect this to a hosted tool via MCP.

<img src="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tool-call.png?fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=44458ff5a2790122ffd7e8b62bf14032" alt="Tool call" data-og-width="1488" width="1488" data-og-height="747" height="747" data-path="langsmith/images/tool-call.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tool-call.png?w=280&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=add552eba8c2254b2b8631420e8a92ee 280w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tool-call.png?w=560&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=807f9c730d6386d884a8b263d07de8c3 560w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tool-call.png?w=840&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=6190625854497044bea5a486f155c1ab 840w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tool-call.png?w=1100&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=eeee3567477764d44857923ff49d4d75 1100w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tool-call.png?w=1650&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=ec4aaf0657a0b200d8822b346762d443 1650w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tool-call.png?w=2500&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=1c6b56541dd156fdc5c06f3d9fb79648 2500w" />

## Tool choice settings

Some models provide control over which tools are called. To configure this:

1. Go to prompt settings
2. Navigate to tool settings
3. Select tool choice

To understand the available tool choice options, check the documentation for your specific provider. For example, [OpenAI's documentation on tool choice](https://platform.openai.com/docs/guides/function-calling/function-calling-behavior?api-mode=responses#tool-choice).

<img src="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tool-choice.png?fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=8685dbafdab37ed9529f8dbeceab72e6" alt="Tool choice" data-og-width="942" width="942" data-og-height="867" height="867" data-path="langsmith/images/tool-choice.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tool-choice.png?w=280&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=4d040577bbfae3816d23de7d16b2017d 280w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tool-choice.png?w=560&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=e8b1220627a1dd668a6c7e66bb8881b2 560w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tool-choice.png?w=840&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=f99a56b4e513d33c4595b9665e5a3d0e 840w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tool-choice.png?w=1100&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=c62de52814917a4d6f65a05c9b44a670 1100w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tool-choice.png?w=1650&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=6d4ff53eb7fa66b94c24e285dc89ba5f 1650w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/tool-choice.png?w=2500&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=591da66f1402ffa38645cec70ba12e0a 2500w" />

***

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/use-tools.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.langchain.com/llms.txt