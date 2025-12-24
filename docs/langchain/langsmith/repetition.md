# How to evaluate with repetitions

Running multiple repetitions can give a more accurate estimate of the performance of your system since LLM outputs are not deterministic. Outputs can differ from one repetition to the next. Repetitions are a way to reduce noise in systems prone to high variability, such as agents.

## Configuring repetitions on an experiment

Add the optional `num_repetitions` param to the `evaluate` / `aevaluate` function ([Python](https://docs.smith.langchain.com/reference/python/evaluation/langsmith.evaluation._runner.evaluate), [TypeScript](https://docs.smith.langchain.com/reference/js/interfaces/evaluation.EvaluateOptions#numrepetitions)) to specify how many times to evaluate over each example in your dataset. For instance, if you have 5 examples in the dataset and set `num_repetitions=5`, each example will be run 5 times, for a total of 25 runs.

<CodeGroup>
  ```python Python theme={null}
  from langsmith import evaluate

  results = evaluate(
      lambda inputs: label_text(inputs["text"]),
      data=dataset_name,
      evaluators=[correct_label],
      experiment_prefix="Toxic Queries",
      num_repetitions=3,
  )
  ```

  ```typescript TypeScript theme={null}
  import { evaluate } from "langsmith/evaluation";

  await evaluate((inputs) => labelText(inputs["input"]), {
    data: datasetName,
    evaluators: [correctLabel],
    experimentPrefix: "Toxic Queries",
    numRepetitions: 3,
  });
  ```
</CodeGroup>

## Viewing results of experiments run with repetitions

If you've run your experiment with [repetitions](/langsmith/evaluation-concepts#repetitions), there will be arrows in the output results column so you can view outputs in the table. To view each run from the repetition, hover over the output cell and click the expanded view. When you run an experiment with repetitions, LangSmith displays the average for each feedback score in the table. Click on the feedback score to view the feedback scores from individual runs, or to view the standard deviation across repetitions.

<img src="https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/repetitions.png?fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=60962de04e5533d7718ca60fa9c7dcce" alt="Repetitions" data-og-width="1636" width="1636" data-og-height="959" height="959" data-path="langsmith/images/repetitions.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/repetitions.png?w=280&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=8be83801a53f2544883faf173bc16ef1 280w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/repetitions.png?w=560&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=7a924559be193efcc2c77dba3fea1231 560w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/repetitions.png?w=840&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=25cbd580d06bda48419b83401c268c2d 840w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/repetitions.png?w=1100&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=9da3908c81d1c8fd44dde6d3ec7dfe1d 1100w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/repetitions.png?w=1650&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=775af0be371e662bea7ba7e29c2f21fd 1650w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/repetitions.png?w=2500&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=4d593460688be852a64638f092cba9f3 2500w" />

***

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/repetition.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.langchain.com/llms.txt