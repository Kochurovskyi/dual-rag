# How to use prebuilt evaluators

LangSmith integrates with the open-source openevals package to provide a suite of prebuilt evaluators that you can use as starting points for evaluation.

<Note>
  This how-to guide will demonstrate how to set up and run one type of evaluator (LLM-as-a-judge). For a complete list of prebuilt evaluators with usage examples, refer to the [openevals](https://github.com/langchain-ai/openevals) and [agentevals](https://github.com/langchain-ai/agentevals) repos.
</Note>

## Setup

You'll need to install the `openevals` package to use the pre-built LLM-as-a-judge evaluator.

<CodeGroup>
  ```bash Python theme={null}
  pip install -U openevals
  ```

  ```bash TypeScript theme={null}
  yarn add openevals @langchain/core
  ```
</CodeGroup>

You'll also need to set your OpenAI API key as an environment variable, though you can choose different providers too:

```bash  theme={null}
export OPENAI_API_KEY="your_openai_api_key"
```

We'll also use LangSmith's [pytest](/langsmith/pytest) integration for Python and [Vitest/Jest](/langsmith/vitest-jest) for TypeScript to run our evals. `openevals` also integrates seamlessly with the [`evaluate`](https://docs.smith.langchain.com/reference/python/evaluation/langsmith.evaluation._runner.evaluate) method as well. See the [appropriate guides](/langsmith/pytest) for setup instructions.

## Running an evaluator

The general flow is simple: import the evaluator or factory function from `openevals`, then run it within your test file with inputs, outputs, and reference outputs. LangSmith will automatically log the evaluator's results as feedback.

Note that not all evaluators will require each parameter (the exact match evaluator only requires outputs and reference outputs, for example). Additionally, if your LLM-as-a-judge prompt requires additional variables, passing them in as kwargs will format them into the prompt.

Set up your test file like this:

<CodeGroup>
  ```python Python theme={null}
  import pytest
  from langsmith import testing as t
  from openevals.llm import create_llm_as_judge
  from openevals.prompts import CORRECTNESS_PROMPT

  correctness_evaluator = create_llm_as_judge(
      prompt=CORRECTNESS_PROMPT,
      feedback_key="correctness",
      model="openai:o3-mini",
  )

  # Mock standin for your application
  def my_llm_app(inputs: dict) -> str:
      return "Doodads have increased in price by 10% in the past year."

  @pytest.mark.langsmith
  def test_correctness():
      inputs = "How much has the price of doodads changed in the past year?"
      reference_outputs = "The price of doodads has decreased by 50% in the past year."
      outputs = my_llm_app(inputs)

      t.log_inputs({"question": inputs})
      t.log_outputs({"answer": outputs})
      t.log_reference_outputs({"answer": reference_outputs})

      correctness_evaluator(
          inputs=inputs,
          outputs=outputs,
          reference_outputs=reference_outputs
      )
  ```

  ```typescript TypeScript theme={null}
  import * as ls from "langsmith/vitest";
  // import * as ls from "langsmith/jest";
  import { createLLMAsJudge, CORRECTNESS_PROMPT } from "openevals";

  const correctnessEvaluator = createLLMAsJudge({
      prompt: CORRECTNESS_PROMPT,
      feedbackKey: "correctness",
      model: "openai:o3-mini",
  });

  // Mock standin for your application
  const myLLMApp = async (_inputs: Record<string, unknown>) => {
      return "Doodads have increased in price by 10% in the past year.";
  };

  ls.describe("Correctness", () => {
      ls.test("incorrect answer", {
          inputs: {
              question: "How much has the price of doodads changed in the past year?"
          },
          referenceOutputs: {
              answer: "The price of doodads has decreased by 50% in the past year."
          }
      }, async ({ inputs, referenceOutputs }) => {
          const outputs = await myLLMApp(inputs);
          ls.logOutputs({ answer: outputs });
          await correctnessEvaluator({
              inputs,
              outputs,
              referenceOutputs,
          });
      });
  });
  ```
</CodeGroup>

The `feedback_key`/`feedbackKey` parameter will be used as the name of the feedback in your experiment.

Running the eval in your terminal will result in something like the following:

<img src="https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prebuilt-eval-result.png?fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=c2351acb065520c3cef3c374bd762982" alt="Prebuilt evaluator terminal result" data-og-width="2114" width="2114" data-og-height="614" height="614" data-path="langsmith/images/prebuilt-eval-result.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prebuilt-eval-result.png?w=280&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=5a091195ae1351d5b16b2ebe53632e1e 280w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prebuilt-eval-result.png?w=560&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=1e7488bb77662f71e60f01b9fa9609d6 560w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prebuilt-eval-result.png?w=840&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=7e491cd83accabc3a56153a6c12d84fe 840w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prebuilt-eval-result.png?w=1100&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=2fbc03b560b082ae5f6de8d17d4ae626 1100w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prebuilt-eval-result.png?w=1650&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=20f6023215721383019659a0b99f3de5 1650w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/prebuilt-eval-result.png?w=2500&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=af97fb8ec7343f536704719294560dd0 2500w" />

You can also pass prebuilt evaluators directly into the `evaluate` method if you have already created a dataset in LangSmith. If using Python, this requires `langsmith>=0.3.11`:

<CodeGroup>
  ```python Python theme={null}
  from langsmith import Client
  from openevals.llm import create_llm_as_judge
  from openevals.prompts import CONCISENESS_PROMPT

  client = Client()
  conciseness_evaluator = create_llm_as_judge(
      prompt=CONCISENESS_PROMPT,
      feedback_key="conciseness",
      model="openai:o3-mini",
  )

  experiment_results = client.evaluate(
      # This is a dummy target function, replace with your actual LLM-based system
      lambda inputs: "What color is the sky?",
      data="Sample dataset",
      evaluators=[
          conciseness_evaluator
      ]
  )
  ```

  ```typescript TypeScript theme={null}
  import { evaluate } from "langsmith/evaluation";
  import { createLLMAsJudge, CONCISENESS_PROMPT } from "openevals";

  const concisenessEvaluator = createLLMAsJudge({
      prompt: CONCISENESS_PROMPT,
      feedbackKey: "conciseness",
      model: "openai:o3-mini",
  });

  await evaluate((inputs) => "What color is the sky?", {
      data: datasetName,
      evaluators: [concisenessEvaluator],
  });
  ```
</CodeGroup>

For a complete list of available evaluators, see the [openevals](https://github.com/langchain-ai/openevals) and [agentevals](https://github.com/langchain-ai/agentevals) repos.

***

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/prebuilt-evaluators.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.langchain.com/llms.txt