# Composite evaluators

*Composite evaluators* are a way to combine multiple evaluator scores into a single [score](/langsmith/evaluation-concepts#evaluator-outputs). This is useful when you want to evaluate multiple aspects of your application and combine the results into a single result.

## Create a composite evaluator using the UI

You can create composite evaluators on a [tracing project](/langsmith/observability-concepts#projects) (for [online evaluations](/langsmith/evaluation-concepts#online-evaluation)) or a [dataset](/langsmith/evaluation-concepts#datasets) (for [offline evaluations](/langsmith/evaluation-concepts#offline-evaluation)). With composite evaluators in the UI, you can compute a weighted average or weighted sum of multiple evaluator scores, with configurable weights.

<div style={{ textAlign: 'center' }}>
  <img className="block dark:hidden" src="https://mintcdn.com/langchain-5e9cc07a/cRRwi1N4-QohYC73/langsmith/images/create_composite_evaluator-light.png?fit=max&auto=format&n=cRRwi1N4-QohYC73&q=85&s=b3859ada8b576ebeaf5399ff15359b10" alt="LangSmith UI showing an LLM call trace called ChatOpenAI with a system and human input followed by an AI Output." data-og-width="756" width="756" data-og-height="594" height="594" data-path="langsmith/images/create_composite_evaluator-light.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/cRRwi1N4-QohYC73/langsmith/images/create_composite_evaluator-light.png?w=280&fit=max&auto=format&n=cRRwi1N4-QohYC73&q=85&s=9bab5ad812328acdd6ffe858f487262b 280w, https://mintcdn.com/langchain-5e9cc07a/cRRwi1N4-QohYC73/langsmith/images/create_composite_evaluator-light.png?w=560&fit=max&auto=format&n=cRRwi1N4-QohYC73&q=85&s=4637a2dc732f945d98b0214023266180 560w, https://mintcdn.com/langchain-5e9cc07a/cRRwi1N4-QohYC73/langsmith/images/create_composite_evaluator-light.png?w=840&fit=max&auto=format&n=cRRwi1N4-QohYC73&q=85&s=c3e7b24dde21ed45f481b7a513ecc256 840w, https://mintcdn.com/langchain-5e9cc07a/cRRwi1N4-QohYC73/langsmith/images/create_composite_evaluator-light.png?w=1100&fit=max&auto=format&n=cRRwi1N4-QohYC73&q=85&s=1310a99e2a8b37d68d78f794b8ce6606 1100w, https://mintcdn.com/langchain-5e9cc07a/cRRwi1N4-QohYC73/langsmith/images/create_composite_evaluator-light.png?w=1650&fit=max&auto=format&n=cRRwi1N4-QohYC73&q=85&s=6beb89dcc6ec734b2ad012bc46c58821 1650w, https://mintcdn.com/langchain-5e9cc07a/cRRwi1N4-QohYC73/langsmith/images/create_composite_evaluator-light.png?w=2500&fit=max&auto=format&n=cRRwi1N4-QohYC73&q=85&s=ba7fd7ba48a3e46d8701b6f64bb68f66 2500w" />

  <img className="hidden dark:block" src="https://mintcdn.com/langchain-5e9cc07a/cRRwi1N4-QohYC73/langsmith/images/create_composite_evaluator-dark.png?fit=max&auto=format&n=cRRwi1N4-QohYC73&q=85&s=ac13f4d2d4a5e3b67285284150b7d592" alt="LangSmith UI showing an LLM call trace called ChatOpenAI with a system and human input followed by an AI Output." data-og-width="761" width="761" data-og-height="585" height="585" data-path="langsmith/images/create_composite_evaluator-dark.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/cRRwi1N4-QohYC73/langsmith/images/create_composite_evaluator-dark.png?w=280&fit=max&auto=format&n=cRRwi1N4-QohYC73&q=85&s=bfc19d802f0327a579d90e519441cf9a 280w, https://mintcdn.com/langchain-5e9cc07a/cRRwi1N4-QohYC73/langsmith/images/create_composite_evaluator-dark.png?w=560&fit=max&auto=format&n=cRRwi1N4-QohYC73&q=85&s=23ab26db75e25795c17abf07e487ba5d 560w, https://mintcdn.com/langchain-5e9cc07a/cRRwi1N4-QohYC73/langsmith/images/create_composite_evaluator-dark.png?w=840&fit=max&auto=format&n=cRRwi1N4-QohYC73&q=85&s=7ce9597b62f3e68b2dc1afa5f17f0e8c 840w, https://mintcdn.com/langchain-5e9cc07a/cRRwi1N4-QohYC73/langsmith/images/create_composite_evaluator-dark.png?w=1100&fit=max&auto=format&n=cRRwi1N4-QohYC73&q=85&s=ee7058d60185a820fe23decf003bd2c1 1100w, https://mintcdn.com/langchain-5e9cc07a/cRRwi1N4-QohYC73/langsmith/images/create_composite_evaluator-dark.png?w=1650&fit=max&auto=format&n=cRRwi1N4-QohYC73&q=85&s=cff38ad541c55d6834edfa67f5650818 1650w, https://mintcdn.com/langchain-5e9cc07a/cRRwi1N4-QohYC73/langsmith/images/create_composite_evaluator-dark.png?w=2500&fit=max&auto=format&n=cRRwi1N4-QohYC73&q=85&s=0f85093799a489eff72dae01ed5b6d94 2500w" />
</div>

### 1. Navigate to the tracing project or dataset

To start configuring a composite evaluator, navigate to the **Tracing Projects** or **Dataset & Experiments** tab and select a project or dataset.

* From within a tracing project: **+ New** > **Evaluator** > **Composite score**
* From within a dataset: **+ Evaluator** > **Composite score**

### 2. Configure the composite evaluator

1. Name your evaluator.
2. Select an aggregation method, either **Average** or **Sum**.
   * **Average**: ∑(weight\*score) / ∑(weight).
   * **Sum**: ∑(weight\*score).
3. Add the feedback keys you want to include in the composite score.
4. Add the weights for the feedback keys. By default, the weights are equal for each feedback key. Adjust the weights to increase or decrease the importance of specific feedback keys in the final score.
5. Click **Create** to save the evaluator.

<Tip> If you need to adjust the weights for the composite scores, they can be updated after the evaluator is created. The resulting scores will be updated for all runs that have the evaluator configured. </Tip>

### 3. View composite evaluator results

Composite scores are attached to a run as **feedback**, similarly to feedback from a single evaluator. How you can view them depends on where the evaluation was run:

**On a tracing project**:

* Composite scores appear as feedback on runs.
* [Filter for runs](/langsmith/filter-traces-in-application) with a composite score, or where the composite score meets a certain threshold.
* [Create a chart](/langsmith/dashboards#custom-dashboards) to visualize trends in the composite score over time.

**On a dataset**:

* View the composite scores in the experiments tab. You can also filter and sort experiments based on the average composite score of their runs.
* Click into an experiment to view the composite score for each run.

<Note> If any of the constituent evaluators are not configured on the run, the composite score will not be calculated for that run. </Note>

## Create composite feedback with the SDK

This guide describes setting up an evaluation that uses multiple evaluators and combines their scores with a custom aggregation function.

<Note> Requires langsmith>=0.4.29 </Note>

### 1. Configure evaluators on a dataset

Start by configuring your evaluators. In this example, the application generates a tweet from a blog introduction and uses three evaluators — summary, tone, and formatting — to assess the output.

If you already have your own dataset with evaluators configured, you can skip this step.

<Accordion title="Configure evaluators on a dataset.">
  ```python  theme={null}
  import os
  from dotenv import load_dotenv
  from openai import OpenAI
  from langsmith import Client
  from pydantic import BaseModel
  import json

  # Load environment variables from .env file
  load_dotenv()

  # Access environment variables
  openai_api_key = os.getenv('OPENAI_API_KEY')
  langsmith_api_key = os.getenv('LANGSMITH_API_KEY')
  langsmith_project = os.getenv('LANGSMITH_PROJECT', 'default')


  # Create a dataset. Only need to do this once.
  client = Client()
  oai_client = OpenAI()

  examples = [
    {
      "inputs": {"blog_intro": "Today we’re excited to announce the general availability of LangSmith — our purpose-built infrastructure and management layer for deploying and scaling long-running, stateful agents. Since our beta last June, nearly 400 companies have used LangSmith to deploy their agents into production. Agent deployment is the next hard hurdle for shipping reliable agents, and LangSmith dramatically lowers this barrier with: 1-click deployment to go live in minutes, 30 API endpoints for designing custom user experiences that fit any interaction pattern, Horizontal scaling to handle bursty, long-running traffic, A persistence layer to support memory, conversational history, and async collaboration with human-in-the-loop or multi-agent workflows, Native Studio, the agent IDE, for easy debugging, visibility, and iteration "},
    },
    {
      "inputs": {"blog_intro": "Klarna has reshaped global commerce with its consumer-centric, AI-powered payment and shopping solutions. With over 85 million active users and 2.5 million daily transactions on its platform, Klarna is a fintech leader that simplifies shopping while empowering consumers with smarter, more flexible financial solutions. Klarna’s flagship AI Assistant is revolutionizing the shopping and payments experience. Built on LangGraph and powered by LangSmith, the AI Assistant handles tasks ranging from customer payments, to refunds, to other payment escalations. With 2.5 million conversations to date, the AI Assistant is more than just a chatbot; it’s a transformative agent that performs the work equivalent of 700 full-time staff, delivering results quickly and improving company efficiency."},
    },
  ]

  dataset = client.create_dataset(dataset_name="Blog Intros")

  client.create_examples(
    dataset_id=dataset.id,
    examples=examples,
  )

  # Define a target function. In this case, we're using a simple function that generates a tweet from a blog intro.
  def generate_tweet(inputs: dict) -> dict:
      instructions = (
        "Given the blog introduction, please generate a catchy yet professional tweet that can be used to promote the blog post on social media. Summarize the key point of the blog post in the tweet. Use emojis in a tasteful manner."
      )
      messages = [
          {"role": "system", "content": instructions},
          {"role": "user", "content": inputs["blog_intro"]},
      ]
      result = oai_client.responses.create(
          input=messages, model="gpt-5-nano"
      )
      return {"tweet": result.output_text}

  # Define evaluators. In this case, we're using three evaluators: summary, formatting, and tone.
  def summary(inputs: dict, outputs: dict) -> bool:
      """Judge whether the tweet is a good summary of the blog intro."""
      instructions = "Given the following text and summary, determine if the summary is a good summary of the text."

      class Response(BaseModel):
          summary: bool

      msg = f"Question: {inputs['blog_intro']}\nAnswer: {outputs['tweet']}"
      response = oai_client.responses.parse(
          model="gpt-5-nano",
          input=[{"role": "system", "content": instructions,}, {"role": "user", "content": msg}],
          text_format=Response
      )

      parsed_response = json.loads(response.output_text)
      return parsed_response["summary"]

  def formatting(inputs: dict, outputs: dict) -> bool:
      """Judge whether the tweet is formatted for easy human readability."""
      instructions = "Given the following text, determine if it is formatted well so that a human can easily read it. Pay particular attention to spacing and punctuation."

      class Response(BaseModel):
          formatting: bool

      msg = f"{outputs['tweet']}"
      response = oai_client.responses.parse(
          model="gpt-5-nano",
          input=[{"role": "system", "content": instructions,}, {"role": "user", "content": msg}],
          text_format=Response
      )

      parsed_response = json.loads(response.output_text)
      return parsed_response["formatting"]

  def tone(inputs: dict, outputs: dict) -> bool:
      """Judge whether the tweet's tone is informative, friendly, and engaging."""
      instructions = "Given the following text, determine if the tweet is informative, yet friendly and engaging."

      class Response(BaseModel):
          tone: bool

      msg = f"{outputs['tweet']}"
      response = oai_client.responses.parse(
          model="gpt-5-nano",
          input=[{"role": "system", "content": instructions,}, {"role": "user", "content": msg}],
          text_format=Response
      )
      parsed_response = json.loads(response.output_text)
      return parsed_response["tone"]

  # Calling evaluate() with the dataset, target function, and evaluators.
  results = client.evaluate(
      generate_tweet,
      data=dataset.name,
      evaluators=[summary, tone, formatting],
      experiment_prefix="gpt-5-nano",
  )

  # Get the experiment name to be used in client.get_experiment_results() in the next section
  experiment_name = results.experiment_name
  ```
</Accordion>

### 2. Create composite feedback

Create composite feedback that aggregates the individual evaluator scores using your custom function. This example uses a weighted average of the individual evaluator scores.

<Accordion title="Create a composite feedback.">
  ```python  theme={null}
  from typing import Dict
  import math
  from langsmith import Client
  from dotenv import load_dotenv

  load_dotenv()

  # TODO: Replace with your experiment name. Can be found in UI or from the above client.evaluate() result
  YOUR_EXPERIMENT_NAME = "placeholder_experiment_name"

  # Set weights for the individual evaluator scores
  DEFAULT_WEIGHTS: Dict[str, float] = {
      "summary": 0.7,
      "tone": 0.2,
      "formatting": 0.1,
  }
  WEIGHTED_FEEDBACK_NAME = "weighted_summary"

  # Pull experiment results
  client = Client()
  results = client.get_experiment_results(
      name=YOUR_EXPERIMENT_NAME,
  )

  # Calculate weighted score for each run
  def calculate_weighted_score(feedback_stats: dict) -> float:
      if not feedback_stats:
          return float("nan")

      # Check if all required metrics are present and have data
      required_metrics = set(DEFAULT_WEIGHTS.keys())
      available_metrics = set(feedback_stats.keys())

      if not required_metrics.issubset(available_metrics):
          return float("nan")

      # Calculate weighted score
      total_score = 0.0
      for metric, weight in DEFAULT_WEIGHTS.items():
          metric_data = feedback_stats[metric]
          if metric_data.get("n", 0) > 0 and "avg" in metric_data:
              total_score += metric_data["avg"] * weight
          else:
              return float("nan")

      return total_score

  # Process each run and write feedback
  # Note that experiment results need to finish processing before this should be called.
  for example_with_runs in results["examples_with_runs"]:
      for run in example_with_runs.runs:
          if run.feedback_stats:
              score = calculate_weighted_score(run.feedback_stats)
              if not math.isnan(score):
                  client.create_feedback(
                      run_id=run.id,
                      key=WEIGHTED_FEEDBACK_NAME,
                      score=float(score)
                  )
  ```
</Accordion>

***

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/composite-evaluators.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.langchain.com/llms.txt