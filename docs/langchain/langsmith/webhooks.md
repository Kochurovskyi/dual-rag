# Configure webhook notifications for rules

When you add a webhook URL on an automation action, we will make a POST request to your webhook endpoint any time the rules you defined match any new runs.

<img src="https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/webhook.png?fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=da310e976aa8824071d65b8fb44b9123" alt="Webhook" data-og-width="872" width="872" data-og-height="991" height="991" data-path="langsmith/images/webhook.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/webhook.png?w=280&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=6f30f7cd2de82b0ccb826d257b933f12 280w, https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/webhook.png?w=560&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=0fce81ff2661e8944ebfb781a07017fe 560w, https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/webhook.png?w=840&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=5799cf7458a15ac99579ba273d0b875e 840w, https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/webhook.png?w=1100&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=aa958b944f848f3a64ce068a64bc8433 1100w, https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/webhook.png?w=1650&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=a3e94463ac9d8fa498accb27124785ab 1650w, https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/webhook.png?w=2500&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=6a5db18db5cf7097fdba6d6b7162ba6d 2500w" />

## Webhook payload

The payload we send to your webhook endpoint contains:

* `"rule_id"`: this is the ID of the automation that sent this payload
* `"start_time"` and `"end_time"`: these are the time boundaries where we found matching runs
* `"runs"`: this is an array of runs, where each run is a dictionary. If you need more information about each run we suggest using our SDK in your endpoint to fetch it from our API.
* `"feedback_stats"`: this is a dictionary with the feedback statistics for the runs. An example payload for this field is shown below.

```json  theme={null}
"feedback_stats": {
    "about_langchain": {
        "n": 1,
        "avg": 0.0,
        "show_feedback_arrow": true,
        "values": {}
    },
    "category": {
        "n": 0,
        "avg": null,
        "show_feedback_arrow": true,
        "values": {
            "CONCEPTUAL": 1
        }
    },
    "user_score": {
        "n": 2,
        "avg": 0.0,
        "show_feedback_arrow": false,
        "values": {}
    },
    "vagueness": {
        "n": 1,
        "avg": 0.0,
        "show_feedback_arrow": true,
        "values": {}
    }
}
```

<Note>
  **fetching from S3 URLs**

  Depending on how recent your runs are, the `inputs_s3_urls` and `outputs_s3_urls` fields may contain S3 URLs to the actual data instead of the data itself.

  The `inputs` and `outputs` can be fetched by the `ROOT.presigned_url` provided in `inputs_s3_urls` and `outputs_s3_urls` respectively.
</Note>

This is an example of the entire payload we send to your webhook endpoint:

```json  theme={null}
{
  "rule_id": "d75d7417-0c57-4655-88fe-1db3cda3a47a",
  "start_time": "2024-04-05T01:28:54.734491+00:00",
  "end_time": "2024-04-05T01:28:56.492563+00:00",
  "runs": [
    {
      "status": "success",
      "is_root": true,
      "trace_id": "6ab80f10-d79c-4fa2-b441-922ed6feb630",
      "dotted_order": "20230505T051324571809Z6ab80f10-d79c-4fa2-b441-922ed6feb630",
      "run_type": "tool",
      "modified_at": "2024-04-05T01:28:54.145062",
      "tenant_id": "2ebda79f-2946-4491-a9ad-d642f49e0815",
      "end_time": "2024-04-05T01:28:54.085649",
      "name": "Search",
      "start_time": "2024-04-05T01:28:54.085646",
      "id": "6ab80f10-d79c-4fa2-b441-922ed6feb630",
      "session_id": "6a3be6a2-9a8c-4fc8-b4c6-a8983b286cc5",
      "parent_run_ids": [],
      "child_run_ids": null,
      "direct_child_run_ids": null,
      "total_tokens": 0,
      "completion_tokens": 0,
      "prompt_tokens": 0,
      "total_cost": null,
      "completion_cost": null,
      "prompt_cost": null,
      "first_token_time": null,
      "app_path": "/o/2ebda79f-2946-4491-a9ad-d642f49e0815/projects/p/6a3be6a2-9a8c-4fc8-b4c6-a8983b286cc5/r/6ab80f10-d79c-4fa2-b441-922ed6feb630?trace_id=6ab80f10-d79c-4fa2-b441-922ed6feb630&start_time=2023-05-05T05:13:24.571809",
      "in_dataset": false,
      "last_queued_at": null,
      "inputs": null,
      "inputs_s3_urls": null,
      "outputs": null,
      "outputs_s3_urls": null,
      "extra": null,
      "events": null,
      "feedback_stats": null,
      "serialized": null,
      "share_token": null
    }
  ]
}
```

## Security

We strongly recommend you add a secret query string parameter to the webhook URL, and verify it on any incoming request. This ensures that if someone discovers your webhook URL you can distinguish those calls from authentic webhook notifications.

An example would be

```
https://api.example.com/langsmith_webhook?secret=38ee77617c3a489ab6e871fbeb2ec87d
```

### Webhook custom HTTP headers

If you'd like to send any specific headers with your webhook, this can be configured per URL. To set this up, click on the `Headers` option next to the URL field and add your headers.

<Note>
  Headers are stored in encrypted format.
</Note>

<img src="https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/webhook-headers.png?fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=8d6fde711d74784b803c13aba4b38837" alt="Webhook headers" data-og-width="848" width="848" data-og-height="1004" height="1004" data-path="langsmith/images/webhook-headers.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/webhook-headers.png?w=280&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=1d6c9f67920f0de5bc4b440593b87116 280w, https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/webhook-headers.png?w=560&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=a62d07be3f38e9c659faadb091f8a23e 560w, https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/webhook-headers.png?w=840&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=5a6c128eb91f899f9213fd0f8999a11f 840w, https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/webhook-headers.png?w=1100&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=6a9dd4e7f434f2f2806df60232f34ac3 1100w, https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/webhook-headers.png?w=1650&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=315d0e900bd0c65dd5264869bd545351 1650w, https://mintcdn.com/langchain-5e9cc07a/1RIJxfRpkszanJLL/langsmith/images/webhook-headers.png?w=2500&fit=max&auto=format&n=1RIJxfRpkszanJLL&q=85&s=31ce3f7628c5c3ba3916b77d906ff0c5 2500w" />

### Webhook Delivery

When delivering events to your webhook endpoint we follow these guidelines

* If we fail to connect to your endpoint, we retry the transport connection up to 2 times, before declaring the delivery failed.
* If your endpoint takes longer than 5 seconds to reply we declare the delivery failed and do not .
* If your endpoint returns a 5xx status code in less than 5 seconds we retry up to 2 times with exponential backoff.
* If your endpoint returns a 4xx status code, we declare the delivery failed and do not retry.
* Anything your endpoint returns in the body will be ignored

## Example with Modal

### Setup

For an example of how to set this up, we will use [Modal](https://modal.com/). Modal provides autoscaling GPUs for inference and fine-tuning, secure containerization for code agents, and serverless Python web endpoints. We'll focus on the web endpoints here.

First, create a Modal account. Then, locally install the Modal SDK:

<CodeGroup>
  ```bash pip theme={null}
  pip install modal
  ```

  ```bash uv theme={null}
  uv add modal
  ```
</CodeGroup>

To finish setting up your account, run the command:

```shell  theme={null}
modal setup
```

and follow the instructions

### Secrets

Next, you will need to set up some secrets in Modal.

First, LangSmith will need to authenticate to Modal by passing in a secret.
The easiest way to do this is to pass in a secret in the query parameters.
To validate this secret, we will need to add a secret in *Modal* to validate it.
We will do that by creating a Modal secret.
You can see instructions for secrets [here](https://modal.com/docs/guide/secrets).
For this purpose, let's call our secret `ls-webhook` and have it set an environment variable with the name `LS_WEBHOOK`.

We can also set up a LangSmith secret - luckily there is already an integration template for this!

<img src="https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/modal-langsmith-secret.png?fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=0c3209b59cb36273d82fb44383efa1d5" alt="LangSmith Modal Template" data-og-width="1229" width="1229" data-og-height="779" height="779" data-path="langsmith/images/modal-langsmith-secret.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/modal-langsmith-secret.png?w=280&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=c2ff70b647c04bb6a45a08de537b4d22 280w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/modal-langsmith-secret.png?w=560&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=02181b882935f45339d31f48adeed1e9 560w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/modal-langsmith-secret.png?w=840&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=52119f475cca739369cebb71bfefafae 840w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/modal-langsmith-secret.png?w=1100&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=aa8a1fc73b2e0b7f27c3186732e3bde9 1100w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/modal-langsmith-secret.png?w=1650&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=91d36950d22b86f7ad790a61957cbad7 1650w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/modal-langsmith-secret.png?w=2500&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=efcdfe7d54ca30079b147e00a0d9e934 2500w" />

### Service

After that, you can create a Python file that will serve as your endpoint.
An example is below, with comments explaining what is going on:

```python  theme={null}
from fastapi import HTTPException, status, Request, Query
from modal import Secret, Stub, web_endpoint, Image

stub = Stub("auth-example", image=Image.debian_slim().pip_install("langsmith"))


@stub.function(
    secrets=[Secret.from_name("ls-webhook"), Secret.from_name("my-langsmith-secret")]
)
# We want this to be a `POST` endpoint since we will post data here
@web_endpoint(method="POST")
# We set up a `secret` query parameter
def f(data: dict, secret: str = Query(...)):
    # You can import dependencies you don't have locally inside Modal functions
    from langsmith import Client

    # First, we validate the secret key we pass
    import os

    if secret != os.environ["LS_WEBHOOK"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # This is where we put the logic for what should happen inside this webhook
    ls_client = Client()
    runs = data["runs"]
    ids = [r["id"] for r in runs]
    feedback = list(ls_client.list_feedback(run_ids=ids))
    for r, f in zip(runs, feedback):
        try:
            ls_client.create_example(
                inputs=r["inputs"],
                outputs={"output": f.correction},
                dataset_name="classifier-github-issues",
            )
        except Exception:
            raise ValueError(f"{r} and {f}")
    # Function body
    return "success!"
```

We can now deploy this easily with `modal deploy ...` (see docs [here](https://modal.com/docs/guide/managing-deployments)).

You should now get something like:

```
✓ Created objects.
├── 🔨 Created mount /Users/harrisonchase/workplace/langsmith-docs/example-webhook.py
├── 🔨 Created mount PythonPackage:langsmith
└── 🔨 Created f => https://hwchase17--auth-example-f.modal.run
✓ App deployed! 🎉

View Deployment: https://modal.com/apps/hwchase17/auth-example
```

The important thing to remember is `https://hwchase17--auth-example-f.modal.run` - the function we created to run.
NOTE: this is NOT the final deployment URL, make sure not to accidentally use that.

### Hooking it up

We can now take the function URL we create above and add it as a webhook.
We have to remember to also pass in the secret key as a query parameter.
Putting it all together, it should look something like:

```
https://hwchase17--auth-example-f-dev.modal.run?secret={SECRET}
```

Replace `{SECRET}` with the secret key you created to access the Modal service.

***

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/webhooks.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.langchain.com/llms.txt