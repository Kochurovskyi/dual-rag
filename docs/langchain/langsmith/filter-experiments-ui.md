# How to filter experiments in the UI

LangSmith lets you filter your previous experiments by feedback scores and metadata to make it easy to find only the experiments you care about.

## Background: add metadata to your experiments

When you run an experiment in the SDK, you can attach metadata to make it easier to filter in UI. This is helpful if you know what axes you want to drill down into when running experiments.

In our example, we are going to attach metadata to our experiment around the model used, the model provider, and a known ID of the prompt:

```python  theme={null}
models = {
    "openai-gpt-4o": ChatOpenAI(model="gpt-4o", temperature=0),
    "openai-gpt-4o-mini": ChatOpenAI(model="gpt-4o-mini", temperature=0),
    "anthropic-claude-3-sonnet-20240229": ChatAnthropic(temperature=0, model_name="claude-3-sonnet-20240229")
}

prompts = {
    "singleminded": "always answer questions with the word banana.",
    "fruitminded": "always discuss fruit in your answers.",
    "basic": "you are a chatbot."
}

def answer_evaluator(run, example) -> dict:
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    answer_grader = hub.pull("langchain-ai/rag-answer-vs-reference") | llm
    score = answer_grader.invoke(
        {
            "question": example.inputs["question"],
            "correct_answer": example.outputs["answer"],
            "student_answer": run.outputs,
        }
    )
    return {"key": "correctness", "score": score["Score"]}

dataset_name = "Filterable Dataset"

for model_type, model in models.items():
    for prompt_type, prompt in prompts.items():
        def predict(example):
            return model.invoke(
                [("system", prompt), ("user", example["question"])]
            )

        model_provider = model_type.split("-")[0]
        model_name = model_type[len(model_provider) + 1:]

        evaluate(
            predict,
            data=dataset_name,
            evaluators=[answer_evaluator],
            # ADD IN METADATA HERE!!
            metadata={
                "model_provider": model_provider,
                "model_name": model_name,
                "prompt_id": prompt_type
            }
        )
```

## Filter experiments in the UI

In the UI, we see all experiments that have been run by default.

<img src="https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/filter-all-experiments.png?fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=0cb5b29f405286dadb8b6491709eb789" alt="Filter all experiments" data-og-width="2900" width="2900" data-og-height="1370" height="1370" data-path="langsmith/images/filter-all-experiments.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/filter-all-experiments.png?w=280&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=45a66945b4ca67d1dc3c29890b5d5feb 280w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/filter-all-experiments.png?w=560&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=1d8fdbdf637f750dcef092a49b45e0ae 560w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/filter-all-experiments.png?w=840&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=7177578edd6e6bcfef63d7a778ded723 840w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/filter-all-experiments.png?w=1100&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=f0c6bdae3afabe2b179a74450adbc508 1100w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/filter-all-experiments.png?w=1650&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=8dd72a9e30b093a58819d79f40f69b65 1650w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/filter-all-experiments.png?w=2500&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=e65610094b48a0f81ac75a49be573382 2500w" />

If we, say, have a preference for openai models, we can easily filter down and see scores within just openai models first:

<img src="https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/filter-openai.png?fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=e3a0c42e4eb37cae68d367dec75d0df1" alt="Filter openai" data-og-width="2910" width="2910" data-og-height="1130" height="1130" data-path="langsmith/images/filter-openai.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/filter-openai.png?w=280&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=96ef35ffdaf371b2819da5a3f4bdf7aa 280w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/filter-openai.png?w=560&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=b44c6d30e0e03560d26719facf1dfc0c 560w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/filter-openai.png?w=840&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=a737dceb8e7a2c89b9d0dfc008352afd 840w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/filter-openai.png?w=1100&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=cd3adf4b2d249bde3646810d3783b931 1100w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/filter-openai.png?w=1650&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=7dc39864577acc20bb9229de313cbe33 1650w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/filter-openai.png?w=2500&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=7d5392a8453b2f416f795834eb02cc6e 2500w" />

We can stack filters, allowing us to filter out low scores on correctness to make sure we only compare relevant experiments:

<img src="https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/filter-feedback.png?fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=c0e223bbe637a03a4c251896a5662f52" alt="Filter feedback" data-og-width="2912" width="2912" data-og-height="826" height="826" data-path="langsmith/images/filter-feedback.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/filter-feedback.png?w=280&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=476871f1d9569046084b380b3fa50ba3 280w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/filter-feedback.png?w=560&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=c8f24775e8f736a2cfd6b1092106a200 560w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/filter-feedback.png?w=840&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=c014f713cb651fa61d13dc8fe11055e2 840w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/filter-feedback.png?w=1100&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=f8c9ad41ba9ba73ee43df8c0c740b53e 1100w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/filter-feedback.png?w=1650&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=4e8105316812331bf3d865c15028e3e7 1650w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/filter-feedback.png?w=2500&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=45c2cd7461fde3670a814ae0915a3584 2500w" />

Finally, we can clear and reset filters. For example, if we see there is clear there's a winner with the `singleminded` prompt, we can change filtering settings to see if any other model providers' models work as well with it:

<img src="https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/filter-singleminded.png?fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=7a30d214745fcddc022e3c715267dfd2" alt="Filter singleminded" data-og-width="2904" width="2904" data-og-height="832" height="832" data-path="langsmith/images/filter-singleminded.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/filter-singleminded.png?w=280&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=bcf8d6a876b76137cc5682308f9e2f74 280w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/filter-singleminded.png?w=560&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=4c1e77dc12de1b65183d26877104a384 560w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/filter-singleminded.png?w=840&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=3aa8585e58f88e5e7eac344ae386808f 840w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/filter-singleminded.png?w=1100&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=613558759a127d7003d3ae653e83298b 1100w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/filter-singleminded.png?w=1650&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=2ba32a223d7012904c0eb63fe7c1fdb7 1650w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/filter-singleminded.png?w=2500&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=c643c61125d409c706ea607b1504740c 2500w" />

***

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/filter-experiments-ui.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.langchain.com/llms.txt