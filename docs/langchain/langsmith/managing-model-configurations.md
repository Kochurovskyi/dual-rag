# Configure prompt settings

The LangSmith [playground](/langsmith/prompt-engineering-concepts#prompt-playground) enables you to control various settings for your prompts. The **Prompt Settings** window contains:

* [Model configuration](#model-configurations)
* [Tool settings](#tool-settings)
* [Prompt formatting](#prompt-formatting)

To access **Prompt Settings**:

1. Navigate to the **Playground** in the left sidebar.
2. Under the **Prompts** heading select the gear <Icon icon="gear" iconType="solid" /> icon next to the model name, which will launch the **Prompt Settings** window.

   <div style={{ textAlign: 'center' }}>
     <img className="block dark:hidden" src="https://mintcdn.com/langchain-5e9cc07a/6r3GRtwWCl4ozaHW/langsmith/images/model-config-light.png?fit=max&auto=format&n=6r3GRtwWCl4ozaHW&q=85&s=6c0f7d7012b1e5295fe545149f955e6b" alt="Model Configuration window in the LangSmith UI, settings for Provider, Model, Temperature, Max Output Tokens, Top P, Presence Penalty, Frequency Penalty, Reasoning Effort, etc." data-og-width="886" width="886" data-og-height="689" height="689" data-path="langsmith/images/model-config-light.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/6r3GRtwWCl4ozaHW/langsmith/images/model-config-light.png?w=280&fit=max&auto=format&n=6r3GRtwWCl4ozaHW&q=85&s=4e3b9ad92f6f14f4e0523bef50199318 280w, https://mintcdn.com/langchain-5e9cc07a/6r3GRtwWCl4ozaHW/langsmith/images/model-config-light.png?w=560&fit=max&auto=format&n=6r3GRtwWCl4ozaHW&q=85&s=e538eb740495a8afa8bfc552b13ae294 560w, https://mintcdn.com/langchain-5e9cc07a/6r3GRtwWCl4ozaHW/langsmith/images/model-config-light.png?w=840&fit=max&auto=format&n=6r3GRtwWCl4ozaHW&q=85&s=ebe73264e977153c869fd04d1552d09b 840w, https://mintcdn.com/langchain-5e9cc07a/6r3GRtwWCl4ozaHW/langsmith/images/model-config-light.png?w=1100&fit=max&auto=format&n=6r3GRtwWCl4ozaHW&q=85&s=2eeb01882056046bc73cc019d674af7e 1100w, https://mintcdn.com/langchain-5e9cc07a/6r3GRtwWCl4ozaHW/langsmith/images/model-config-light.png?w=1650&fit=max&auto=format&n=6r3GRtwWCl4ozaHW&q=85&s=8f28fe2fe8054cf0623fb9d17f91966f 1650w, https://mintcdn.com/langchain-5e9cc07a/6r3GRtwWCl4ozaHW/langsmith/images/model-config-light.png?w=2500&fit=max&auto=format&n=6r3GRtwWCl4ozaHW&q=85&s=cf9ad39be3623e73322d123699e73f19 2500w" />

     <img className="hidden dark:block" src="https://mintcdn.com/langchain-5e9cc07a/ppc8uxWc01j4q7Ia/langsmith/images/model-config-dark.png?fit=max&auto=format&n=ppc8uxWc01j4q7Ia&q=85&s=2e9da272c3fc8f7ac958c6e6d1da85e3" alt="Model Configuration window in the LangSmith UI, settings for Provider, Model, Temperature, Max Output Tokens, Top P, Presence Penalty, Frequency Penalty, Reasoning Effort, etc." data-og-width="881" width="881" data-og-height="732" height="732" data-path="langsmith/images/model-config-dark.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/ppc8uxWc01j4q7Ia/langsmith/images/model-config-dark.png?w=280&fit=max&auto=format&n=ppc8uxWc01j4q7Ia&q=85&s=652fb75a4682cfc813743a1260764e59 280w, https://mintcdn.com/langchain-5e9cc07a/ppc8uxWc01j4q7Ia/langsmith/images/model-config-dark.png?w=560&fit=max&auto=format&n=ppc8uxWc01j4q7Ia&q=85&s=02c980a8387f3d69a5870660b1668080 560w, https://mintcdn.com/langchain-5e9cc07a/ppc8uxWc01j4q7Ia/langsmith/images/model-config-dark.png?w=840&fit=max&auto=format&n=ppc8uxWc01j4q7Ia&q=85&s=ee633c06056fa7ad46ea58a179afa169 840w, https://mintcdn.com/langchain-5e9cc07a/ppc8uxWc01j4q7Ia/langsmith/images/model-config-dark.png?w=1100&fit=max&auto=format&n=ppc8uxWc01j4q7Ia&q=85&s=f62a35ed726b5f89c156a40c9ea76f2c 1100w, https://mintcdn.com/langchain-5e9cc07a/ppc8uxWc01j4q7Ia/langsmith/images/model-config-dark.png?w=1650&fit=max&auto=format&n=ppc8uxWc01j4q7Ia&q=85&s=18114575db8e6c7ce928763ddcb88c12 1650w, https://mintcdn.com/langchain-5e9cc07a/ppc8uxWc01j4q7Ia/langsmith/images/model-config-dark.png?w=2500&fit=max&auto=format&n=ppc8uxWc01j4q7Ia&q=85&s=ab24dc4975def52db55c4896ead5b77c 2500w" />
   </div>

## Model configurations

Model configurations define the parameters your prompt runs against. In the LangSmith Playground, you can save and manage these configurations, which allows you to reuse your preferred settings across prompts and sessions. For details on specific settings, refer to your model provider’s documentation (for example, [Anthropic](https://platform.claude.com/docs/en/api/messages), [OpenAI](https://platform.openai.com/docs/api-reference/responses/create)).

### Create saved configurations

1. In the **Model Configurations** tab, adjust the model configuration as needed—you can select a [saved configuration to edit](#edit-configurations).
2. Click the **Save As** button in the top bar.
3. Enter a name and optional description for your configuration and confirm.
4. Now that you've saved the configuration, anyone in your organization's [workspace](/langsmith/administration-overview#workspaces) can access it. All saved configurations are available in the **Model Configuration** dropdown.
5. Once you have created a saved configuration, you can set it as your default, so any new prompt you create will automatically use this configuration. To set a configuration as your default, click the **Set as default** <Icon icon="thumbtack" iconType="solid" /> icon next to the model name in the dropdown.

### Edit configurations

1. To rename a saved configuration, or update the description, select the configuration name or description and make the necessary changes.
2. Update the current configuration's parameters as needed and click the **Save** button at the top.

### Delete configurations

1. Select the configuration you want to remove.
2. Click the trash <Icon icon="trash" iconType="solid" /> icon to delete it.

### Extra parameters

The **Extra Parameters** field allows you to pass additional model parameters that aren't directly supported in the LangSmith interface. This is particularly useful in two scenarios:

1. When model providers release new parameters that haven't yet been integrated into the LangSmith interface. You can specify these parameters in JSON format to use them right away. For example:

   ```json  theme={null}
   {
       "reasoning_effort": "medium"
   }
   ```

2. When troubleshooting parameter-related errors in the playground, such as:

   ```
   TypeError: AsyncCompletions.create() got an unexpected keyword argument 'max_concurrency'
   ```

   If you receive an error about unnecessary parameters (which is more common when using [LangChain JS](/oss/python/langchain/overview) for run tracing), you can use this field to remove the extra parameters.

## Tool settings

[*Tools*](/langsmith/prompt-engineering-concepts#tools) enable your LLM to perform tasks like searching the web, looking up information, and so on. In the **Tools Settings** tab, you can manage the ways your LLM uses and accesses the tools you have defined in your prompt, including:

* **Parallel Tool Calls**: Calling multiple tools in parallel when appropriate. This allows the model to gather information from different sources simultaneously. (Dependent on model support for parallel execution.)
* **Tool Choice**: Select the tools that the model can access. For more details, refer to [Use tools in a prompt](/langsmith/use-tools).

## Prompt formatting

The **Prompt Format** tab allows you to specify:

* The **Prompt type**. For details on chat and completion prompts, refer to [Prompt engineering](/langsmith/prompt-engineering-concepts#chat-vs-completion) concepts.
* The **Template format**. For details on prompt templating and using variables, refer to [F-string vs. mustache](/langsmith/prompt-engineering-concepts##f-string-vs-mustache).

***

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/managing-model-configurations.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.langchain.com/llms.txt