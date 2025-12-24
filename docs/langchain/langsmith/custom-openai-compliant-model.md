# Connect to an OpenAI compliant model provider/proxy

The LangSmith playground allows you to use any model that is compliant with the OpenAI API. You can utilize your model by setting the Proxy Provider for  in the playground.

## Deploy an OpenAI compliant model

Many providers offer OpenAI compliant models or proxy services. Some examples of this include:

* [LiteLLM Proxy](https://github.com/BerriAI/litellm?tab=readme-ov-file#quick-start-proxy---cli)
* [Ollama](https://ollama.com/)

You can use these providers to deploy your model and get an API endpoint that is compliant with the OpenAI API.

Take a look at the full [specification](https://platform.openai.com/docs/api-reference/chat) for more information.

## Use the model in the LangSmith Playground

Once you have deployed a model server, you can use it in the LangSmith [Playground](/langsmith/prompt-engineering-concepts#prompt-playground).

To access the **Prompt Settings** menu:

1. Under the **Prompts** heading select the gear <Icon icon="gear" iconType="solid" /> icon next to the model name.
2. In the **Model Configuration** tab, select the model to edit in the dropdown.
3. For the **Provider** dropdown, select **OpenAI Compatible Endpoint**.
4. Add your OpenAI Compatible Endpoint to the **Base URL** input.

   <div style={{ textAlign: 'center' }}>
     <img className="block dark:hidden" src="https://mintcdn.com/langchain-5e9cc07a/cemWY9w7h0W8uMbk/langsmith/images/openai-compatible-endpoint.png?fit=max&auto=format&n=cemWY9w7h0W8uMbk&q=85&s=fdbe548e512ed40fb512578d02986b45" alt="Model Configuration window in the LangSmith UI with a model selected and the Provider dropdown with OpenAI Compatible Endpoint selected." data-og-width="897" width="897" data-og-height="572" height="572" data-path="langsmith/images/openai-compatible-endpoint.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/cemWY9w7h0W8uMbk/langsmith/images/openai-compatible-endpoint.png?w=280&fit=max&auto=format&n=cemWY9w7h0W8uMbk&q=85&s=75921e7b30edbac5263ee10178977383 280w, https://mintcdn.com/langchain-5e9cc07a/cemWY9w7h0W8uMbk/langsmith/images/openai-compatible-endpoint.png?w=560&fit=max&auto=format&n=cemWY9w7h0W8uMbk&q=85&s=468265c2ad0a6c1740eb18590dab27a5 560w, https://mintcdn.com/langchain-5e9cc07a/cemWY9w7h0W8uMbk/langsmith/images/openai-compatible-endpoint.png?w=840&fit=max&auto=format&n=cemWY9w7h0W8uMbk&q=85&s=9f9c3f68df77205264eb9221373790f2 840w, https://mintcdn.com/langchain-5e9cc07a/cemWY9w7h0W8uMbk/langsmith/images/openai-compatible-endpoint.png?w=1100&fit=max&auto=format&n=cemWY9w7h0W8uMbk&q=85&s=ccb9820653e1e57b529bc46ac7d20e40 1100w, https://mintcdn.com/langchain-5e9cc07a/cemWY9w7h0W8uMbk/langsmith/images/openai-compatible-endpoint.png?w=1650&fit=max&auto=format&n=cemWY9w7h0W8uMbk&q=85&s=c320b3f4051643b71fba4faa350daf9b 1650w, https://mintcdn.com/langchain-5e9cc07a/cemWY9w7h0W8uMbk/langsmith/images/openai-compatible-endpoint.png?w=2500&fit=max&auto=format&n=cemWY9w7h0W8uMbk&q=85&s=e9d1be7c69021b7fa575a2a466dbfe58 2500w" />

     <img className="hidden dark:block" src="https://mintcdn.com/langchain-5e9cc07a/cemWY9w7h0W8uMbk/langsmith/images/openai-compatible-endpoint-dark.png?fit=max&auto=format&n=cemWY9w7h0W8uMbk&q=85&s=97459563da21d17228a1bb94a1b9edf3" alt="Model Configuration window in the LangSmith UI with a model selected and the Provider dropdown with OpenAI Compatible Endpoint selected." data-og-width="896" width="896" data-og-height="552" height="552" data-path="langsmith/images/openai-compatible-endpoint-dark.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/cemWY9w7h0W8uMbk/langsmith/images/openai-compatible-endpoint-dark.png?w=280&fit=max&auto=format&n=cemWY9w7h0W8uMbk&q=85&s=c3e8e46813ec673fbc3ac4e4748a4ab6 280w, https://mintcdn.com/langchain-5e9cc07a/cemWY9w7h0W8uMbk/langsmith/images/openai-compatible-endpoint-dark.png?w=560&fit=max&auto=format&n=cemWY9w7h0W8uMbk&q=85&s=381a567b022c71ed6f74abbb7e3cecbd 560w, https://mintcdn.com/langchain-5e9cc07a/cemWY9w7h0W8uMbk/langsmith/images/openai-compatible-endpoint-dark.png?w=840&fit=max&auto=format&n=cemWY9w7h0W8uMbk&q=85&s=7df617e39d5bd098f4e80d523ef85778 840w, https://mintcdn.com/langchain-5e9cc07a/cemWY9w7h0W8uMbk/langsmith/images/openai-compatible-endpoint-dark.png?w=1100&fit=max&auto=format&n=cemWY9w7h0W8uMbk&q=85&s=06408cd348f56fcc409af8273c799a97 1100w, https://mintcdn.com/langchain-5e9cc07a/cemWY9w7h0W8uMbk/langsmith/images/openai-compatible-endpoint-dark.png?w=1650&fit=max&auto=format&n=cemWY9w7h0W8uMbk&q=85&s=6b79b55e2868ed11e9d2c2eb396b004f 1650w, https://mintcdn.com/langchain-5e9cc07a/cemWY9w7h0W8uMbk/langsmith/images/openai-compatible-endpoint-dark.png?w=2500&fit=max&auto=format&n=cemWY9w7h0W8uMbk&q=85&s=4e0439d889aa2175c0802e9bf5db399b 2500w" />
   </div>

If everything is set up correctly, you should see the model's response in the playground. You can also use this functionality to invoke downstream pipelines as well.

For information on how to store your model configuration , refer to [Configure prompt settings](/langsmith/managing-model-configurations).

***

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/custom-openai-compliant-model.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.langchain.com/llms.txt