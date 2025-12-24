# Connect to a custom model

The LangSmith playground allows you to use your own custom models. You can deploy a model server that exposes your model's API via [LangServe](https://github.com/langchain-ai/langserve), an open source library for serving LangChain applications. Behind the scenes, the playground will interact with your model server to generate responses.

## Deploy a custom model server

For your convenience, we have provided a sample model server that you can use as a reference. You can find the sample model server [here](https://github.com/langchain-ai/langsmith-model-server) We highly recommend using the sample model server as a starting point.

Depending on your model is an instruct-style or chat-style model, you will need to implement either `custom_model.py` or `custom_chat_model.py` respectively.

## Adding configurable fields

It is often useful to configure your model with different parameters. These might include temperature, model\_name, max\_tokens, etc.

To make your model configurable in the LangSmith playground, you need to add configurable fields to your model server. These fields can be used to change model parameters from the playground.

You can add configurable fields by implementing the `with_configurable_fields` function in the `config.py` file. You can

```python  theme={null}
def with_configurable_fields(self) -> Runnable:
    """Expose fields you want to be configurable in the playground. We will automatically expose these to the
    playground. If you don't want to expose any fields, you can remove this method."""
    return self.configurable_fields(n=ConfigurableField(
        id="n",
        name="Num Characters",
        description="Number of characters to return from the input prompt.",
    ))
```

## Use the model in the LangSmith Playground

Once you have deployed a model server, you can use it in the LangSmith Playground. Enter the playground and select either the `ChatCustomModel` or the `CustomModel` provider for chat-style model or instruct-style models.

Enter the `URL`. The playground will automatically detect the available endpoints and configurable fields. You can then invoke the model with the desired parameters.

<img src="https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/playground-custom-model.png?fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=7a2889af5f55cc73661033837a50fad6" alt="ChatCustomModel in Playground" data-og-width="2816" width="2816" data-og-height="1676" height="1676" data-path="langsmith/images/playground-custom-model.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/playground-custom-model.png?w=280&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=c6509706fee0c85205e039f6868a5ead 280w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/playground-custom-model.png?w=560&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=deafe903353d9bec02143ebd578d5599 560w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/playground-custom-model.png?w=840&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=928818d42fc58d83e1b5a04ecaa36630 840w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/playground-custom-model.png?w=1100&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=552046bb4c04947154a2c8fa3457beca 1100w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/playground-custom-model.png?w=1650&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=2735d4eed015cafa0861079133c5220c 1650w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/playground-custom-model.png?w=2500&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=f59ef79d897acce3ae4835ce949d61b6 2500w" />

If everything is set up correctly, you should see the model's response in the playground as well as the configurable fields specified in the `with_configurable_fields`.

See how to store your model configuration for later use [here](/langsmith/managing-model-configurations).

***

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/custom-endpoint.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.langchain.com/llms.txt