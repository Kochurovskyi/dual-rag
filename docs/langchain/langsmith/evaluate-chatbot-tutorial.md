# Evaluate a chatbot

In this guide we will set up evaluations for a chatbot. These allow you to measure how well your application is performing over a set of data. Being able to get this insight quickly and reliably will allow you to iterate with confidence.

At a high level, in this tutorial we will:

* *Create an initial golden dataset to measure performance*
* *Define metrics to use to measure performance*
* *Run evaluations on a few different prompts or models*
* *Compare results manually*
* *Track results over time*
* *Set up automated testing to run in CI/CD*

For more information on the evaluation workflows LangSmith supports, check out the [how-to guides](/langsmith/evaluation), or see the reference docs for [evaluate](https://docs.smith.langchain.com/reference/python/evaluation/langsmith.evaluation._runner.evaluate) and its asynchronous [aevaluate](https://docs.smith.langchain.com/reference/python/evaluation/langsmith.evaluation._arunner.aevaluate) counterpart.

Lots to cover, let's dive in!

## Setup

First install the required dependencies for this tutorial. We happen to use OpenAI, but LangSmith can be used with any model:

<CodeGroup>
  ```bash pip theme={null}
  pip install -U langsmith openai
  ```

  ```bash uv theme={null}
  uv add langsmith openai
  ```
</CodeGroup>

And set environment variables to enable LangSmith tracing:

```bash  theme={null}
export LANGSMITH_TRACING="true"
export LANGSMITH_API_KEY="<Your LangSmith API key>"
export OPENAI_API_KEY="<Your OpenAI API key>"
```

## Create a dataset

The first step when getting ready to test and evaluate your application is to define the datapoints you want to evaluate. There are a few aspects to consider here:

* What should the schema of each datapoint be?
* How many datapoints should I gather?
* How should I gather those datapoints?

**Schema:** Each datapoint should consist of, at the very least, the inputs to the application. If you are able, it is also very helpful to define the expected outputs - these represent what you would expect a properly functioning application to output. Often times you cannot define the perfect output - that's okay! Evaluation is an iterative process. Sometimes you may also want to define more information for each example - like the expected documents to fetch in RAG, or the expected steps to take as an agent. LangSmith datasets are very flexible and allow you to define arbitrary schemas.

**How many:** There's no hard and fast rule for how many you should gather. The main thing is to make sure you have proper coverage of edge cases you may want to guard against. Even 10-50 examples can provide a lot of value! Don't worry about getting a large number to start - you can (and should) always add over time!

**How to get:** This is maybe the trickiest part. Once you know you want to gather a dataset... how do you actually go about it? For most teams that are starting a new project, we generally see them start by collecting the first 10-20 datapoints by hand. After starting with these datapoints, these datasets are generally *living* constructs and grow over time. They generally grow after seeing how real users will use your application, seeing the pain points that exist, and then moving a few of those datapoints into this set. There are also methods like synthetically generating data that can be used to augment your dataset. To start, we recommend not worrying about those and just hand labeling \~10-20 examples.

Once you've got your dataset, there are a few different ways to upload them to LangSmith. For this tutorial, we will use the client, but you can also upload via the UI (or even create them in the UI).

For this tutorial, we will create 5 datapoints to evaluate on. We will be evaluating a question-answering application. The input will be a question, and the output will be an answer. Since this is a question-answering application, we can define the expected answer. Let's show how to create and upload this dataset to LangSmith!

```python  theme={null}
from langsmith import Client

client = Client()

# Define dataset: these are your test cases
dataset_name = "QA Example Dataset"
dataset = client.create_dataset(dataset_name)

client.create_examples(
    dataset_id=dataset.id,
    examples=[
        {
            "inputs": {"question": "What is LangChain?"},
            "outputs": {"answer": "A framework for building LLM applications"},
        },
        {
            "inputs": {"question": "What is LangSmith?"},
            "outputs": {"answer": "A platform for observing and evaluating LLM applications"},
        },
        {
            "inputs": {"question": "What is OpenAI?"},
            "outputs": {"answer": "A company that creates Large Language Models"},
        },
        {
            "inputs": {"question": "What is Google?"},
            "outputs": {"answer": "A technology company known for search"},
        },
        {
            "inputs": {"question": "What is Mistral?"},
            "outputs": {"answer": "A company that creates Large Language Models"},
        }
    ]
)
```

Now, if we go the LangSmith UI and look for `QA Example Dataset` in the `Datasets & Testing` page, when we click into it we should see that we have five new examples.

<img src="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-dataset.png?fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=9ab5110714d009d5865ba0e2d8ee0ffa" alt="Testing tutorial dataset" data-og-width="1251" width="1251" data-og-height="560" height="560" data-path="langsmith/images/testing-tutorial-dataset.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-dataset.png?w=280&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=e4b38ded6968e649ed8ab507f63f1f3e 280w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-dataset.png?w=560&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=f7aee5327f8058dd99684cd43e44c791 560w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-dataset.png?w=840&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=9e853ed05b0a2ad40f9e4d0403e7004c 840w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-dataset.png?w=1100&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=331654a31885b89a93924eaac4fa95da 1100w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-dataset.png?w=1650&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=833bf2a60b392323bba47fbe42655537 1650w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-dataset.png?w=2500&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=3410e4bc7ac5c28f8838fc5fb88026bd 2500w" />

## Define metrics

After creating our dataset, we can now define some metrics to evaluate our responses on. Since we have an expected answer, we can compare to that as part of our evaluation. However, we do not expect our application to output those **exact** answers, but rather something that is similar. This makes our evaluation a little trickier.

In addition to evaluating correctness, let's also make sure our answers are short and concise. This will be a little easier - we can define a simple Python function to measure the length of the response.

Let's go ahead and define these two metrics.

For the first, we will use an LLM to **judge** whether the output is correct (with respect to the expected output). This **LLM-as-a-judge** is relatively common for cases that are too complex to measure with a simple function. We can define our own prompt and LLM to use for evaluation here:

```python  theme={null}
import openai
from langsmith import wrappers

openai_client = wrappers.wrap_openai(openai.OpenAI())

eval_instructions = "You are an expert professor specialized in grading students' answers to questions."

def correctness(inputs: dict, outputs: dict, reference_outputs: dict) -> bool:
    user_content = f"""You are grading the following question:
{inputs['question']}
Here is the real answer:
{reference_outputs['answer']}
You are grading the following predicted answer:
{outputs['response']}
Respond with CORRECT or INCORRECT:
Grade:"""
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": eval_instructions},
            {"role": "user", "content": user_content},
        ],
    ).choices[0].message.content
    return response == "CORRECT"
```

For evaluating the length of the response, this is a lot easier! We can just define a simple function that checks whether the actual output is less than 2x the length of the expected result.

```python  theme={null}
def concision(outputs: dict, reference_outputs: dict) -> bool:
    return int(len(outputs["response"]) < 2 * len(reference_outputs["answer"]))
```

## Run Evaluations

Great! So now how do we run evaluations? Now that we have a dataset and evaluators, all that we need is our application! We will build a simple application that just has a system message with instructions on how to respond and then passes it to the LLM. We will build this using the OpenAI SDK directly:

```python  theme={null}
default_instructions = "Respond to the users question in a short, concise manner (one short sentence)."

def my_app(question: str, model: str = "gpt-4o-mini", instructions: str = default_instructions) -> str:
    return openai_client.chat.completions.create(
        model=model,
        temperature=0,
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": question},
        ],
    ).choices[0].message.content
```

Before running this through LangSmith evaluations, we need to define a simple wrapper that maps the input keys from our dataset to the function we want to call, and then also maps the output of the function to the output key we expect.

```python  theme={null}
def ls_target(inputs: str) -> dict:
    return {"response": my_app(inputs["question"])}
```

Great! Now we're ready to run an evaluation. Let's do it!

```python  theme={null}
experiment_results = client.evaluate(
    ls_target, # Your AI system
    data=dataset_name, # The data to predict and grade over
    evaluators=[concision, correctness], # The evaluators to score the results
    experiment_prefix="openai-4o-mini", # A prefix for your experiment names to easily identify them
)
```

This will output a URL. If we click on it, we should see results of our evaluation!

<img src="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-run.png?fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=9517dd9f9fc23062fcba7b061fe5cdda" alt="Testing tutorial run" data-og-width="3022" width="3022" data-og-height="1128" height="1128" data-path="langsmith/images/testing-tutorial-run.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-run.png?w=280&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=06b6a2a70ea3f85929dca6f03653be68 280w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-run.png?w=560&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=3ddae16867d89b93f0155dc654dede93 560w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-run.png?w=840&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=5ba93e0b10423be56081602f65ec41bc 840w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-run.png?w=1100&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=2088e69be2ee5efdf949296ea3c74652 1100w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-run.png?w=1650&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=b6fa551b7edab188da50ccc63dbd9769 1650w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-run.png?w=2500&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=0b79a1b6f5a351ed986810f53d14d9d9 2500w" />

If we go back to the dataset page and select the `Experiments` tab, we can now see a summary of our one run!

<img src="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-one-run.png?fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=4c30f7474727d2f537c75e5f80ae1298" alt="Testing tutorial one run" data-og-width="3022" width="3022" data-og-height="1532" height="1532" data-path="langsmith/images/testing-tutorial-one-run.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-one-run.png?w=280&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=4886dc0021394767078872237779a8f3 280w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-one-run.png?w=560&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=cd111a19a463ed45fabe53caa2fc08be 560w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-one-run.png?w=840&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=25363336afaecae0198f7c55f5bfe739 840w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-one-run.png?w=1100&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=42473dfcfad36f26ad7cfea316dbb458 1100w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-one-run.png?w=1650&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=4317ea45ce5de4f3917a902d84b3e2e3 1650w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-one-run.png?w=2500&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=0b0371997a45b936b37c8f44539fd1aa 2500w" />

Let's now try it out with a different model! Let's try `gpt-4-turbo`

```python  theme={null}
def ls_target_v2(inputs: str) -> dict:
    return {"response": my_app(inputs["question"], model="gpt-4-turbo")}

experiment_results = client.evaluate(
    ls_target_v2,
    data=dataset_name,
    evaluators=[concision, correctness],
    experiment_prefix="openai-4-turbo",
)
```

And now let's use GPT-4 but also update the prompt to be a bit more strict in requiring the answer to be short.

```python  theme={null}
instructions_v3 = "Respond to the users question in a short, concise manner (one short sentence). Do NOT use more than ten words."

def ls_target_v3(inputs: str) -> dict:
    response = my_app(
        inputs["question"],
        model="gpt-4-turbo",
        instructions=instructions_v3
    )
    return {"response": response}

experiment_results = client.evaluate(
    ls_target_v3,
    data=dataset_name,
    evaluators=[concision, correctness],
    experiment_prefix="strict-openai-4-turbo",
)
```

If we go back to the `Experiments` tab on the datasets page, we should see that all three runs now show up!

<img src="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-three-runs.png?fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=9d74c18991c33d4fbd5180dbb12a4f91" alt="Testing tutorial three runs" data-og-width="3020" width="3020" data-og-height="1540" height="1540" data-path="langsmith/images/testing-tutorial-three-runs.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-three-runs.png?w=280&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=11a8a19c576760e949137952786ad325 280w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-three-runs.png?w=560&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=dedd52ea55db2e7c886bdbddab19bcf4 560w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-three-runs.png?w=840&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=d10e4b9efd6dbea2c50859fde066afb7 840w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-three-runs.png?w=1100&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=bc78ab5c6cad42ee2aa0aaf5350329ac 1100w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-three-runs.png?w=1650&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=84edcc8ea892ac534009c9a05212bf26 1650w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-three-runs.png?w=2500&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=aefc9019026a0c38b5a92c2aa5ac3462 2500w" />

## Comparing results

Awesome, we've evaluated three different runs. But how can we compare results? The first way we can do this is just by looking at the runs in the `Experiments` tab. If we do that, we can see a high level view of the metrics for each run:

<img src="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-compare-metrics.png?fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=224acfbea78b8b1d0e08ce59d06b5088" alt="Testing tutorial compare metrics" data-og-width="3020" width="3020" data-og-height="1540" height="1540" data-path="langsmith/images/testing-tutorial-compare-metrics.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-compare-metrics.png?w=280&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=abf04bbd16675f00a4a3941c27e21ac7 280w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-compare-metrics.png?w=560&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=40893fc5274fb96ea5a1bd26919604a7 560w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-compare-metrics.png?w=840&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=3ebe594101ccb3c8efcf3d9cf0e8d906 840w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-compare-metrics.png?w=1100&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=6a934bbb56ebf268636db8f3c775d73d 1100w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-compare-metrics.png?w=1650&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=178412fa63f8011046cd44d5e4411f68 1650w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-compare-metrics.png?w=2500&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=8f893b4d545e6723dc2efe8d76c4da9f 2500w" />

Great! So we can tell that GPT-4 is better than GPT-3.5 at knowing who companies are, and we can see that the strict prompt helped a lot with the length. But what if we want to explore in more detail?

In order to do that, we can select all the runs we want to compare (in this case all three) and open them up in a comparison view. We immediately see all three tests side by side. Some of the cells are color coded - this is showing a regression of *a certain metric* compared to *a certain baseline*. We automatically choose defaults for the baseline and metric, but you can change those yourself. You can also choose which columns and which metrics you see by using the `Display` control. You can also automatically filter to only see the runs that have improvements/regressions by clicking on the icons at the top.

<img src="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-compare-runs.png?fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=de5575b837cdf97d479e5c91aff9dc78" alt="Testing tutorial compare runs" data-og-width="3022" width="3022" data-og-height="1548" height="1548" data-path="langsmith/images/testing-tutorial-compare-runs.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-compare-runs.png?w=280&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=09d73536620b794bab530f1c154ca1cd 280w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-compare-runs.png?w=560&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=3cc976e3066b5a1777bd76ef367e5cd9 560w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-compare-runs.png?w=840&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=8fa9010ec69b095f97094ea3f1322b7c 840w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-compare-runs.png?w=1100&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=03f984b970ffeceafa30bc6b242dd468 1100w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-compare-runs.png?w=1650&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=9d7ba0782fdf722b27ff1382a8156ea9 1650w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-compare-runs.png?w=2500&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=64ff5b28a56fcffedb5d0daaa2c87e33 2500w" />

If we want to see more information, we can also select the `Expand` button that appears when hovering over a row to open up a side panel with more detailed information:

<img src="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-side-panel.png?fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=a72c4924a0ad9bebceae2da9518c56cc" alt="Testing tutorial side panel" data-og-width="2824" width="2824" data-og-height="1546" height="1546" data-path="langsmith/images/testing-tutorial-side-panel.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-side-panel.png?w=280&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=f10bab81b285ece30e110570962caeaf 280w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-side-panel.png?w=560&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=ced32c31ada87af7f81ca78ee4d9b1a5 560w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-side-panel.png?w=840&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=282ab40f9b90b46589a92fb9cd1da680 840w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-side-panel.png?w=1100&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=b584cee17dd93e0e121b7a30ccdc1d3f 1100w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-side-panel.png?w=1650&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=b2b51c2aaf8e582eedae0586b0a08031 1650w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-side-panel.png?w=2500&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=fc077628c53f5684d16bb309df8fc84a 2500w" />

## Set up automated testing to run in CI/CD

Now that we've run this in a one-off manner, we can set it to run in an automated fashion. We can do this pretty easily by just including it as a pytest file that we run in CI/CD. As part of this, we can either just log the results OR set up some criteria to determine if it passes or not. For example, if I wanted to ensure that we always got at least 80% of generated responses passing the `length` check, we could set that up with a test like:

```python  theme={null}
def test_length_score() -> None:
    """Test that the length score is at least 80%."""
    experiment_results = evaluate(
        ls_target, # Your AI system
        data=dataset_name, # The data to predict and grade over
        evaluators=[concision, correctness], # The evaluators to score the results
    )
    # This will be cleaned up in the next release:
    feedback = client.list_feedback(
        run_ids=[r.id for r in client.list_runs(project_name=experiment_results.experiment_name)],
        feedback_key="concision"
    )
    scores = [f.score for f in feedback]
    assert sum(scores) / len(scores) >= 0.8, "Aggregate score should be at least .8"
```

## Track results over time

Now that we've got these experiments running in an automated fashion, we want to track these results over time. We can do this from the overall `Experiments` tab in the datasets page. By default, we show evaluation metrics over time (highlighted in red). We also automatically track git metrics, to easily associate it with the branch of your code (highlighted in yellow).

<img src="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-over-time.png?fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=a5961747b6ea92bb2f838d025ca5e3d5" alt="Testing tutorial over time" data-og-width="3020" width="3020" data-og-height="1544" height="1544" data-path="langsmith/images/testing-tutorial-over-time.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-over-time.png?w=280&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=e0dc96840d39b210e1ae957e8dfb5fb2 280w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-over-time.png?w=560&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=8f56098392ba5b2c0670ceb16e29ac0c 560w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-over-time.png?w=840&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=df47e336e15b6d23f36b20915db7192d 840w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-over-time.png?w=1100&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=e6e38b84ee80b1df85ee926a16e3b654 1100w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-over-time.png?w=1650&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=8ef1345d6b299b41399a1a60fbef2219 1650w, https://mintcdn.com/langchain-5e9cc07a/ImHGLQW1HnQYwnJV/langsmith/images/testing-tutorial-over-time.png?w=2500&fit=max&auto=format&n=ImHGLQW1HnQYwnJV&q=85&s=679f95e97b7ac941e3380f658b158ef5 2500w" />

## Conclusion

That's it for this tutorial!

We've gone over how to create an initial test set, define some evaluation metrics, run experiments, compare them manually, set up CI/CD, and track results over time. Hopefully this can help you iterate with confidence.

This is just the start. As mentioned earlier, evaluation is an ongoing process. For example - the datapoints you will want to evaluate on will likely continue to change over time. There are many types of evaluators you may wish to explore. For information on this, check out the [how-to guides](/langsmith/evaluation).

Additionally, there are other ways to evaluate data besides in this "offline" manner (e.g. you can evaluate production data). For more information on online evaluation, check out [this guide](/langsmith/online-evaluations).

## Reference code

<Accordion title="Click to see a consolidated code snippet">
  ```python  theme={null}
  import openai
  from langsmith import Client, wrappers

  # Application code
  openai_client = wrappers.wrap_openai(openai.OpenAI())

  default_instructions = "Respond to the users question in a short, concise manner (one short sentence)."

  def my_app(question: str, model: str = "gpt-4o-mini", instructions: str = default_instructions) -> str:
      return openai_client.chat.completions.create(
          model=model,
          temperature=0,
          messages=[
              {"role": "system", "content": instructions},
              {"role": "user", "content": question},
          ],
      ).choices[0].message.content

  client = Client()

  # Define dataset: these are your test cases
  dataset_name = "QA Example Dataset"
  dataset = client.create_dataset(dataset_name)

  client.create_examples(
      dataset_id=dataset.id,
      examples=[
          {
              "inputs": {"question": "What is LangChain?"},
              "outputs": {"answer": "A framework for building LLM applications"},
          },
          {
              "inputs": {"question": "What is LangSmith?"},
              "outputs": {"answer": "A platform for observing and evaluating LLM applications"},
          },
          {
              "inputs": {"question": "What is OpenAI?"},
              "outputs": {"answer": "A company that creates Large Language Models"},
          },
          {
              "inputs": {"question": "What is Google?"},
              "outputs": {"answer": "A technology company known for search"},
          },
          {
              "inputs": {"question": "What is Mistral?"},
              "outputs": {"answer": "A company that creates Large Language Models"},
          }
      ]
  )

  # Define evaluators
  eval_instructions = "You are an expert professor specialized in grading students' answers to questions."

  def correctness(inputs: dict, outputs: dict, reference_outputs: dict) -> bool:
      user_content = f"""You are grading the following question:
  {inputs['question']}
  Here is the real answer:
  {reference_outputs['answer']}
  You are grading the following predicted answer:
  {outputs['response']}
  Respond with CORRECT or INCORRECT:
  Grade:"""
      response = openai_client.chat.completions.create(
          model="gpt-4o-mini",
          temperature=0,
          messages=[
              {"role": "system", "content": eval_instructions},
              {"role": "user", "content": user_content},
          ],
      ).choices[0].message.content
      return response == "CORRECT"

  def concision(outputs: dict, reference_outputs: dict) -> bool:
      return int(len(outputs["response"]) < 2 * len(reference_outputs["answer"]))

  # Run evaluations
  def ls_target(inputs: str) -> dict:
      return {"response": my_app(inputs["question"])}

  experiment_results_v1 = client.evaluate(
      ls_target, # Your AI system
      data=dataset_name, # The data to predict and grade over
      evaluators=[concision, correctness], # The evaluators to score the results
      experiment_prefix="openai-4o-mini", # A prefix for your experiment names to easily identify them
  )

  def ls_target_v2(inputs: str) -> dict:
      return {"response": my_app(inputs["question"], model="gpt-4-turbo")}

  experiment_results_v2 = client.evaluate(
      ls_target_v2,
      data=dataset_name,
      evaluators=[concision, correctness],
      experiment_prefix="openai-4-turbo",
  )

  instructions_v3 = "Respond to the users question in a short, concise manner (one short sentence). Do NOT use more than ten words."

  def ls_target_v3(inputs: str) -> dict:
      response = my_app(
          inputs["question"],
          model="gpt-4-turbo",
          instructions=instructions_v3
      )
      return {"response": response}

  experiment_results_v3 = client.evaluate(
      ls_target_v3,
      data=dataset_name,
      evaluators=[concision, correctness],
      experiment_prefix="strict-openai-4-turbo",
  )
  ```
</Accordion>

***

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/evaluate-chatbot-tutorial.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.langchain.com/llms.txt