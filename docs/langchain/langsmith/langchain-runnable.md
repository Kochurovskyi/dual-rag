# How to evaluate a runnable

<Info>
  * `langchain`: [Python](https://python.langchain.com) and [JS/TS](https://js.langchain.com)
  * Runnable: [Python](https://python.langchain.com/docs/concepts/runnables/) and [JS/TS](https://js.langchain.com/docs/concepts/runnables/)
</Info>

`langchain` [Runnable](https://python.langchain.com/docs/concepts/runnables/) objects (such as chat models, retrievers, chains, etc.) can be passed directly into `evaluate()` / `aevaluate()`.

## Setup

Let's define a simple chain to evaluate. First, install all the required packages:

<CodeGroup>
  ```bash Python theme={null}
  pip install -U langsmith langchain[openai]
  ```

  ```bash TypeScript theme={null}
  yarn add langsmith @langchain/openai
  ```
</CodeGroup>

Now define a chain:

<CodeGroup>
  ```python Python theme={null}
  from langchain.chat_models import init_chat_model
  from langchain_core.prompts import ChatPromptTemplate
  from langchain_core.output_parsers import StrOutputParser

  instructions = (
      "Please review the user query below and determine if it contains any form "
      "of toxic behavior, such as insults, threats, or highly negative comments. "
      "Respond with 'Toxic' if it does, and 'Not toxic' if it doesn't."
  )

  prompt = ChatPromptTemplate(
      [("system", instructions), ("user", "{text}")],
  )

  model = init_chat_model("gpt-4o")
  chain = prompt | model | StrOutputParser()
  ```

  ```typescript TypeScript theme={null}
  import { ChatOpenAI } from "@langchain/openai";
  import { ChatPromptTemplate } from "@langchain/core/prompts";
  import { StringOutputParser } from "@langchain/core/output_parsers";

  const prompt = ChatPromptTemplate.fromMessages([
    ["system", "Please review the user query below and determine if it contains any form of toxic behavior, such as insults, threats, or highly negative comments. Respond with 'Toxic' if it does, and 'Not toxic' if it doesn't."],
    ["user", "{text}"]
  ]);

  const chatModel = new ChatOpenAI();
  const outputParser = new StringOutputParser();
  const chain = prompt.pipe(chatModel).pipe(outputParser);
  ```
</CodeGroup>

## Evaluate

To evaluate our chain we can pass it directly to the `evaluate()` / `aevaluate()` method. Note that the input variables of the chain must match the keys of the example inputs. In this case, the example inputs should have the form `{"text": "..."}`.

<CodeGroup>
  ```python Python theme={null}
  from langsmith import aevaluate, Client

  client = Client()

  # Clone a dataset of texts with toxicity labels.
  # Each example input has a "text" key and each output has a "label" key.
  dataset = client.clone_public_dataset(
      "https://smith.langchain.com/public/3d6831e6-1680-4c88-94df-618c8e01fc55/d"
  )

  def correct(outputs: dict, reference_outputs: dict) -> bool:
      # Since our chain outputs a string not a dict, this string
      # gets stored under the default "output" key in the outputs dict:
      actual = outputs["output"]
      expected = reference_outputs["label"]
      return actual == expected

  results = await aevaluate(
      chain,
      data=dataset,
      evaluators=[correct],
      experiment_prefix="gpt-4o, baseline",
  )
  ```

  ```typescript TypeScript theme={null}
  import { evaluate } from "langsmith/evaluation";
  import { Client } from "langsmith";

  const langsmith = new Client();

  const dataset = await client.clonePublicDataset(
    "https://smith.langchain.com/public/3d6831e6-1680-4c88-94df-618c8e01fc55/d"
  )

  await evaluate(chain, {
    data: dataset.name,
    evaluators: [correct],
    experimentPrefix: "gpt-4o, baseline",
  });
  ```
</CodeGroup>

The runnable is traced appropriately for each output.

<img src="https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/runnable-eval.png?fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=b9dac41dafb9a1cbb3b90fc508f212f7" alt="Runnable Evaluation" data-og-width="2288" width="2288" data-og-height="1052" height="1052" data-path="langsmith/images/runnable-eval.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/runnable-eval.png?w=280&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=39f7bda57df5d29c72729390065342c2 280w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/runnable-eval.png?w=560&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=2bbfa58f877541adff85056d2d4910c7 560w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/runnable-eval.png?w=840&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=198967ebb494d0577fac294f879f348c 840w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/runnable-eval.png?w=1100&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=dd0758a55517d6899d445bd203bc7d03 1100w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/runnable-eval.png?w=1650&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=6fa8f6a044a0b978ef727390f18f5ce3 1650w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/runnable-eval.png?w=2500&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=40dad8febfdaf0756c90b6326e2c4415 2500w" />

## Related

* [How to evaluate a `langgraph` graph](/langsmith/evaluate-on-intermediate-steps)

***

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/langchain-runnable.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.langchain.com/llms.txt