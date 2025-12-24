# Cost tracking

Building agents at scale introduces non-trivial, usage-based costs that can be difficult to track. LangSmith automatically records LLM token usage and costs for major providers, and also allows you to submit custom cost data for any additional components.

This gives you a single, unified view of costs across your entire application, which makes it easy to monitor, understand, and debug your spend.

This guide covers:

* [Viewing costs in the LangSmith UI](#viewing-costs-in-the-langsmith-ui)
* [How cost tracking works](#cost-tracking)
* [How to send custom cost data](#send-custom-cost-data)

## Viewing costs in the LangSmith UI

In the [LangSmith UI](https://smith.langchain.com), you can explore usage and spend in three main ways: first by understanding how tokens and costs are broken down, then by viewing those details within individual traces, and finally by inspecting aggregated metrics in project stats and dashboards.

### Token and cost breakdowns

Token usage and costs are broken down into three categories:

* **Input**: Tokens in the prompt sent to the model. Subtypes include: cache reads, text tokens, image tokens, etc
* **Output**: Tokens generated in the response from the model. Subtypes include: reasoning tokens, text tokens, image tokens, etc
* **Other**: Costs from tool calls, retrieval steps or any custom runs.

You can view detailed breakdowns by hovering over cost sections in the UI. When available, each section is further categorized by subtype.

<img className="block dark:hidden" src="https://mintcdn.com/langchain-5e9cc07a/S029Harmw-iSrSVw/langsmith/images/cost-tooltip-light.png?fit=max&auto=format&n=S029Harmw-iSrSVw&q=85&s=49971715854df465e81e53ad6b7b297c" alt="Cost tooltip" data-og-width="894" width="894" data-og-height="400" height="400" data-path="langsmith/images/cost-tooltip-light.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/S029Harmw-iSrSVw/langsmith/images/cost-tooltip-light.png?w=280&fit=max&auto=format&n=S029Harmw-iSrSVw&q=85&s=0eefe6caadcf4d9a7a93c6c378122476 280w, https://mintcdn.com/langchain-5e9cc07a/S029Harmw-iSrSVw/langsmith/images/cost-tooltip-light.png?w=560&fit=max&auto=format&n=S029Harmw-iSrSVw&q=85&s=24a18c4afc2274abd598238598dfdf7d 560w, https://mintcdn.com/langchain-5e9cc07a/S029Harmw-iSrSVw/langsmith/images/cost-tooltip-light.png?w=840&fit=max&auto=format&n=S029Harmw-iSrSVw&q=85&s=fb04f0d82dbdb3e26a3fd58b4bcdc895 840w, https://mintcdn.com/langchain-5e9cc07a/S029Harmw-iSrSVw/langsmith/images/cost-tooltip-light.png?w=1100&fit=max&auto=format&n=S029Harmw-iSrSVw&q=85&s=6740a97c3545dc0df28415d2d7c67f6e 1100w, https://mintcdn.com/langchain-5e9cc07a/S029Harmw-iSrSVw/langsmith/images/cost-tooltip-light.png?w=1650&fit=max&auto=format&n=S029Harmw-iSrSVw&q=85&s=e7a8c02294dc5dbf08461118e820af11 1650w, https://mintcdn.com/langchain-5e9cc07a/S029Harmw-iSrSVw/langsmith/images/cost-tooltip-light.png?w=2500&fit=max&auto=format&n=S029Harmw-iSrSVw&q=85&s=d83617c271e7b701794589caa5964ba4 2500w" />

<img className="hidden dark:block" src="https://mintcdn.com/langchain-5e9cc07a/S029Harmw-iSrSVw/langsmith/images/cost-tooltip-dark.png?fit=max&auto=format&n=S029Harmw-iSrSVw&q=85&s=a51c9bc7bbd1836231b80d7d5a8db735" alt="Cost tooltip" data-og-width="900" width="900" data-og-height="394" height="394" data-path="langsmith/images/cost-tooltip-dark.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/S029Harmw-iSrSVw/langsmith/images/cost-tooltip-dark.png?w=280&fit=max&auto=format&n=S029Harmw-iSrSVw&q=85&s=55e6e557896671cf177be070b53853ca 280w, https://mintcdn.com/langchain-5e9cc07a/S029Harmw-iSrSVw/langsmith/images/cost-tooltip-dark.png?w=560&fit=max&auto=format&n=S029Harmw-iSrSVw&q=85&s=5aacd2afe8bb68d48f1b8718b04b337e 560w, https://mintcdn.com/langchain-5e9cc07a/S029Harmw-iSrSVw/langsmith/images/cost-tooltip-dark.png?w=840&fit=max&auto=format&n=S029Harmw-iSrSVw&q=85&s=b18555fd40e07821742940bcf23776f4 840w, https://mintcdn.com/langchain-5e9cc07a/S029Harmw-iSrSVw/langsmith/images/cost-tooltip-dark.png?w=1100&fit=max&auto=format&n=S029Harmw-iSrSVw&q=85&s=f5ba1370e3dd595cfc0af949ffe454f4 1100w, https://mintcdn.com/langchain-5e9cc07a/S029Harmw-iSrSVw/langsmith/images/cost-tooltip-dark.png?w=1650&fit=max&auto=format&n=S029Harmw-iSrSVw&q=85&s=f25ef24cc27cc01c3da8e76f402aeb12 1650w, https://mintcdn.com/langchain-5e9cc07a/S029Harmw-iSrSVw/langsmith/images/cost-tooltip-dark.png?w=2500&fit=max&auto=format&n=S029Harmw-iSrSVw&q=85&s=0a1d6251fbab47105ca63b4dfe6ef809 2500w" />

You can inspect these breakdowns throughout the LangSmith UI, described in the following section.

### Where to view token and cost breakdowns

<AccordionGroup>
  <Accordion title="In the trace tree">
    The trace tree shows the most detailed view of token usage and cost (for a single trace).  It displays the total usage for the entire trace, aggregated values for each parent run and token and cost breakdowns for each child run.

    Open any run inside a tracing project to view its trace tree.

    <img className="block dark:hidden" src="https://mintcdn.com/langchain-5e9cc07a/GpRpLUps9-PFSAXx/langsmith/images/trace-tree-costs-light.png?fit=max&auto=format&n=GpRpLUps9-PFSAXx&q=85&s=a25bf30084d96292ba00ca84c07653d6" alt="Cost tooltip" data-og-width="2062" width="2062" data-og-height="1530" height="1530" data-path="langsmith/images/trace-tree-costs-light.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/GpRpLUps9-PFSAXx/langsmith/images/trace-tree-costs-light.png?w=280&fit=max&auto=format&n=GpRpLUps9-PFSAXx&q=85&s=e8a79cea1a5bb04adcbf1ee0e62533e7 280w, https://mintcdn.com/langchain-5e9cc07a/GpRpLUps9-PFSAXx/langsmith/images/trace-tree-costs-light.png?w=560&fit=max&auto=format&n=GpRpLUps9-PFSAXx&q=85&s=3af7a8b874fcd58778412d260f1ab586 560w, https://mintcdn.com/langchain-5e9cc07a/GpRpLUps9-PFSAXx/langsmith/images/trace-tree-costs-light.png?w=840&fit=max&auto=format&n=GpRpLUps9-PFSAXx&q=85&s=4697febea4d4ece0924f34dc87ddba8f 840w, https://mintcdn.com/langchain-5e9cc07a/GpRpLUps9-PFSAXx/langsmith/images/trace-tree-costs-light.png?w=1100&fit=max&auto=format&n=GpRpLUps9-PFSAXx&q=85&s=5b306c9a32e9ce77bc2f92eaac315c2e 1100w, https://mintcdn.com/langchain-5e9cc07a/GpRpLUps9-PFSAXx/langsmith/images/trace-tree-costs-light.png?w=1650&fit=max&auto=format&n=GpRpLUps9-PFSAXx&q=85&s=d5145faa36dd98b6f0442cb0bfaa4fa7 1650w, https://mintcdn.com/langchain-5e9cc07a/GpRpLUps9-PFSAXx/langsmith/images/trace-tree-costs-light.png?w=2500&fit=max&auto=format&n=GpRpLUps9-PFSAXx&q=85&s=238b220a634d50adcf0a2754c167cee6 2500w" />

    <img className="hidden dark:block" src="https://mintcdn.com/langchain-5e9cc07a/GpRpLUps9-PFSAXx/langsmith/images/trace-tree-costs-dark.png?fit=max&auto=format&n=GpRpLUps9-PFSAXx&q=85&s=e2037cd8309e754f8753278d334c8344" alt="Cost tooltip" data-og-width="2052" width="2052" data-og-height="1490" height="1490" data-path="langsmith/images/trace-tree-costs-dark.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/GpRpLUps9-PFSAXx/langsmith/images/trace-tree-costs-dark.png?w=280&fit=max&auto=format&n=GpRpLUps9-PFSAXx&q=85&s=9f273466040d5f3178a1f32903b23578 280w, https://mintcdn.com/langchain-5e9cc07a/GpRpLUps9-PFSAXx/langsmith/images/trace-tree-costs-dark.png?w=560&fit=max&auto=format&n=GpRpLUps9-PFSAXx&q=85&s=4848270e7454f48070aa7a3585d9cafa 560w, https://mintcdn.com/langchain-5e9cc07a/GpRpLUps9-PFSAXx/langsmith/images/trace-tree-costs-dark.png?w=840&fit=max&auto=format&n=GpRpLUps9-PFSAXx&q=85&s=da0f8036b96015eb75b8721dc0c10425 840w, https://mintcdn.com/langchain-5e9cc07a/GpRpLUps9-PFSAXx/langsmith/images/trace-tree-costs-dark.png?w=1100&fit=max&auto=format&n=GpRpLUps9-PFSAXx&q=85&s=4ee69aee2b0dfae76923f09528a10977 1100w, https://mintcdn.com/langchain-5e9cc07a/GpRpLUps9-PFSAXx/langsmith/images/trace-tree-costs-dark.png?w=1650&fit=max&auto=format&n=GpRpLUps9-PFSAXx&q=85&s=0fc6303cc3c060aa35db962d6cfcb211 1650w, https://mintcdn.com/langchain-5e9cc07a/GpRpLUps9-PFSAXx/langsmith/images/trace-tree-costs-dark.png?w=2500&fit=max&auto=format&n=GpRpLUps9-PFSAXx&q=85&s=3e9abf61bc4da61f930fd923bec0bcfb 2500w" />
  </Accordion>

  <Accordion title="In project stats">
    The project stats panel shows the total token usage and cost for all traces in a project.

    <img className="block dark:hidden" src="https://mintcdn.com/langchain-5e9cc07a/yIWcej3jR6iH0nDR/langsmith/images/stats-pane-cost-tracking-light.png?fit=max&auto=format&n=yIWcej3jR6iH0nDR&q=85&s=c9168cc335b0d9ccdde0ebe6ab1abd91" alt="Cost tracking chart" data-og-width="1257" width="1257" data-og-height="544" height="544" data-path="langsmith/images/stats-pane-cost-tracking-light.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/yIWcej3jR6iH0nDR/langsmith/images/stats-pane-cost-tracking-light.png?w=280&fit=max&auto=format&n=yIWcej3jR6iH0nDR&q=85&s=72360ffba7901bae6a32dccffbc8098a 280w, https://mintcdn.com/langchain-5e9cc07a/yIWcej3jR6iH0nDR/langsmith/images/stats-pane-cost-tracking-light.png?w=560&fit=max&auto=format&n=yIWcej3jR6iH0nDR&q=85&s=9876ac6aa567436835c169cd416320ce 560w, https://mintcdn.com/langchain-5e9cc07a/yIWcej3jR6iH0nDR/langsmith/images/stats-pane-cost-tracking-light.png?w=840&fit=max&auto=format&n=yIWcej3jR6iH0nDR&q=85&s=fb2ac554cae4b7634d73872df0be735d 840w, https://mintcdn.com/langchain-5e9cc07a/yIWcej3jR6iH0nDR/langsmith/images/stats-pane-cost-tracking-light.png?w=1100&fit=max&auto=format&n=yIWcej3jR6iH0nDR&q=85&s=44027849f87a5644bc0c791be2c21ffe 1100w, https://mintcdn.com/langchain-5e9cc07a/yIWcej3jR6iH0nDR/langsmith/images/stats-pane-cost-tracking-light.png?w=1650&fit=max&auto=format&n=yIWcej3jR6iH0nDR&q=85&s=e9a7ea651c412dd20cea34c7b91e15e4 1650w, https://mintcdn.com/langchain-5e9cc07a/yIWcej3jR6iH0nDR/langsmith/images/stats-pane-cost-tracking-light.png?w=2500&fit=max&auto=format&n=yIWcej3jR6iH0nDR&q=85&s=b35b55da99133863bb1bf80c57b15fc7 2500w" />

    <img className="hidden dark:block" src="https://mintcdn.com/langchain-5e9cc07a/yIWcej3jR6iH0nDR/langsmith/images/stats-pane-cost-tracking-dark.png?fit=max&auto=format&n=yIWcej3jR6iH0nDR&q=85&s=e0be66ec244c134421af0475f83c3b1d" alt="Cost tracking chart" data-og-width="1253" width="1253" data-og-height="546" height="546" data-path="langsmith/images/stats-pane-cost-tracking-dark.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/yIWcej3jR6iH0nDR/langsmith/images/stats-pane-cost-tracking-dark.png?w=280&fit=max&auto=format&n=yIWcej3jR6iH0nDR&q=85&s=a87ee7f1da026cd212eadda5616c9e76 280w, https://mintcdn.com/langchain-5e9cc07a/yIWcej3jR6iH0nDR/langsmith/images/stats-pane-cost-tracking-dark.png?w=560&fit=max&auto=format&n=yIWcej3jR6iH0nDR&q=85&s=506dae4c2035c37fd846b4b96575130e 560w, https://mintcdn.com/langchain-5e9cc07a/yIWcej3jR6iH0nDR/langsmith/images/stats-pane-cost-tracking-dark.png?w=840&fit=max&auto=format&n=yIWcej3jR6iH0nDR&q=85&s=0883314216050e125bb733953b506a4e 840w, https://mintcdn.com/langchain-5e9cc07a/yIWcej3jR6iH0nDR/langsmith/images/stats-pane-cost-tracking-dark.png?w=1100&fit=max&auto=format&n=yIWcej3jR6iH0nDR&q=85&s=1781f3039d06b932a126d403b5060f99 1100w, https://mintcdn.com/langchain-5e9cc07a/yIWcej3jR6iH0nDR/langsmith/images/stats-pane-cost-tracking-dark.png?w=1650&fit=max&auto=format&n=yIWcej3jR6iH0nDR&q=85&s=6a2ebfeeb609516d33eec4affe08af2d 1650w, https://mintcdn.com/langchain-5e9cc07a/yIWcej3jR6iH0nDR/langsmith/images/stats-pane-cost-tracking-dark.png?w=2500&fit=max&auto=format&n=yIWcej3jR6iH0nDR&q=85&s=f9490ee9b5dc79060f6ef8cb072a2c73 2500w" />
  </Accordion>

  <Accordion title="In dashboards">
    Dashboards help you explore cost and token usage trends over time. The [prebuilt dashboard](/langsmith/dashboards/#prebuilt-dashboards) for a tracing project shows total costs and a cost breakdown by input and output tokens.

    You may also configure custom cost tracking charts in [custom dashboards](https://docs.langchain.com/langsmith/dashboards#custom-dashboards).

    <img className="block dark:hidden" src="https://mintcdn.com/langchain-5e9cc07a/S029Harmw-iSrSVw/langsmith/images/cost-tracking-chart-light.png?fit=max&auto=format&n=S029Harmw-iSrSVw&q=85&s=18b74d9ee26db0fe17877b3dc3c2c120" alt="Cost tracking chart" data-og-width="1206" width="1206" data-og-height="866" height="866" data-path="langsmith/images/cost-tracking-chart-light.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/S029Harmw-iSrSVw/langsmith/images/cost-tracking-chart-light.png?w=280&fit=max&auto=format&n=S029Harmw-iSrSVw&q=85&s=1f8119ffc4dbe3647884e83b9e600b2a 280w, https://mintcdn.com/langchain-5e9cc07a/S029Harmw-iSrSVw/langsmith/images/cost-tracking-chart-light.png?w=560&fit=max&auto=format&n=S029Harmw-iSrSVw&q=85&s=35fc237732844199920fe48c16c06c68 560w, https://mintcdn.com/langchain-5e9cc07a/S029Harmw-iSrSVw/langsmith/images/cost-tracking-chart-light.png?w=840&fit=max&auto=format&n=S029Harmw-iSrSVw&q=85&s=2697b4965b63dfaebdff1604fb509abd 840w, https://mintcdn.com/langchain-5e9cc07a/S029Harmw-iSrSVw/langsmith/images/cost-tracking-chart-light.png?w=1100&fit=max&auto=format&n=S029Harmw-iSrSVw&q=85&s=19a096bc55c074465060e6d7f1c0a5b3 1100w, https://mintcdn.com/langchain-5e9cc07a/S029Harmw-iSrSVw/langsmith/images/cost-tracking-chart-light.png?w=1650&fit=max&auto=format&n=S029Harmw-iSrSVw&q=85&s=0d524ec464b630a04312873f3847887a 1650w, https://mintcdn.com/langchain-5e9cc07a/S029Harmw-iSrSVw/langsmith/images/cost-tracking-chart-light.png?w=2500&fit=max&auto=format&n=S029Harmw-iSrSVw&q=85&s=d27dcf301e56083dfefb5d1f1b06baa6 2500w" />

    <img className="hidden dark:block" src="https://mintcdn.com/langchain-5e9cc07a/S029Harmw-iSrSVw/langsmith/images/cost-tracking-chart-dark.png?fit=max&auto=format&n=S029Harmw-iSrSVw&q=85&s=134115cab7e741a5b7f6d784f9d51b76" alt="Cost tracking chart" data-og-width="1202" width="1202" data-og-height="920" height="920" data-path="langsmith/images/cost-tracking-chart-dark.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/S029Harmw-iSrSVw/langsmith/images/cost-tracking-chart-dark.png?w=280&fit=max&auto=format&n=S029Harmw-iSrSVw&q=85&s=ad9e895cdf72d959bce04ec03321a78f 280w, https://mintcdn.com/langchain-5e9cc07a/S029Harmw-iSrSVw/langsmith/images/cost-tracking-chart-dark.png?w=560&fit=max&auto=format&n=S029Harmw-iSrSVw&q=85&s=e8c0d349174089891b2cd20d13be7d41 560w, https://mintcdn.com/langchain-5e9cc07a/S029Harmw-iSrSVw/langsmith/images/cost-tracking-chart-dark.png?w=840&fit=max&auto=format&n=S029Harmw-iSrSVw&q=85&s=a0cc08bf1d4aaff36f11f906c6b19729 840w, https://mintcdn.com/langchain-5e9cc07a/S029Harmw-iSrSVw/langsmith/images/cost-tracking-chart-dark.png?w=1100&fit=max&auto=format&n=S029Harmw-iSrSVw&q=85&s=268a4acd73f13045ff8de90733a50cde 1100w, https://mintcdn.com/langchain-5e9cc07a/S029Harmw-iSrSVw/langsmith/images/cost-tracking-chart-dark.png?w=1650&fit=max&auto=format&n=S029Harmw-iSrSVw&q=85&s=21c6c9d062c67e9f6900ac3deb7825d2 1650w, https://mintcdn.com/langchain-5e9cc07a/S029Harmw-iSrSVw/langsmith/images/cost-tracking-chart-dark.png?w=2500&fit=max&auto=format&n=S029Harmw-iSrSVw&q=85&s=ac2d88cf00ccf7daf7d367433bbf6d62 2500w" />
  </Accordion>
</AccordionGroup>

## Cost tracking

You can track costs in two ways:

1. Costs for LLM calls can be **automatically derived from token counts and model prices**
2. Cost for LLM calls or any other run type can be **manually specified as part of the run data**

The approach you use will depend on on what you're tracking and how your model pricing is structured:

| Method            | Run type: LLM                                                                                                                                                                                                                                                                                                                                                                                                                                                    | Run type: Other                                                |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| **Automatically** | <ul><li>Calling LLMs with [LangChain](/oss/python/langchain/overview)</li><li>Tracing LLM calls to OpenAI, Anthropic or models that follow an OpenAI-compliant format with `@traceable`</li><li> Using LangSmith wrappers for [OpenAI](/langsmith/trace-openai) or [Anthropic](/langsmith/trace-anthropic)</li><li>For other model providers, read the [token and cost information guide](/langsmith/log-llm-trace#provide-token-and-cost-information)</li></ul> | Not applicable.                                                |
| **Manually**      | If LLM call costs are non-linear (eg. follow a custom cost function)                                                                                                                                                                                                                                                                                                                                                                                             | Send costs for any run types, e.g. tool calls, retrieval steps |

### LLM calls: Automatically track costs based on token counts

To compute cost automatically from token usage, you need to provide **token counts**, the **model and provider** and the **model price**.

<Note>
  Follow the instructions below if you’re using model providers whose responses don’t follow the same patterns as one of OpenAI or Anthropic.

  These steps are **only required** if you are *not*:

  * Calling LLMs with [LangChain](/oss/python/langchain/overview)
  * Using `@traceable` to trace LLM calls to OpenAI, Anthropic or models that follow an OpenAI-compliant format
  * Using LangSmith wrappers for [OpenAI](/langsmith/trace-openai) or [Anthropic](/langsmith/trace-anthropic).
</Note>

**1. Send token counts**

Many models include token counts as part of the response. You must extract this information and include it in your run using one of the following methods:

<Accordion title="A. Set a `usage_metadata` field on the run’s metadata">
  Set a `usage_metadata` field on the run's metadata. The advantage of this approach is that you do not need to change your traced function’s runtime outputs

  <CodeGroup>
    ```python Python theme={null}
    from langsmith import traceable, get_current_run_tree

    inputs = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "I'd like to book a table for two."},
    ]

    @traceable(
        run_type="llm",
        metadata={"ls_provider": "my_provider", "ls_model_name": "my_model"}
    )
    def chat_model(messages: list):
        # Imagine this is the real model output format your application expects
        assistant_message = {
            "role": "assistant",
            "content": "Sure, what time would you like to book the table for?"
        }

        # Token usage you compute or receive from the provider
        token_usage = {
            "input_tokens": 27,
            "output_tokens": 13,
            "total_tokens": 40,
            "input_token_details": {"cache_read": 10}
        }

        # Attach token usage to the LangSmith run
        run = get_current_run_tree()
        run.set(usage_metadata=token_usage)

        return assistant_message

    chat_model(inputs)
    ```

    ```typescript TypeScript theme={null}
    import { traceable, getCurrentRunTree } from "langsmith/traceable";

    const inputs = [
      { role: "system", content: "You are a helpful assistant." },
      { role: "user", content: "I'd like to book a table for two." },
    ];

    const chatModel = traceable(
      async ({ messages }) => {
        // The output your application expects
        const assistantMessage = {
          role: "assistant",
          content: "Sure, what time would you like to book the table for?",
        };

        // Token usage you compute or receive from the provider
        const tokenUsage = {
          input_tokens: 27,
          output_tokens: 13,
          total_tokens: 40,
          input_token_details: { cache_read: 10 },
        };

        // Attach usage to the LangSmith run
        const runTree = getCurrentRunTree();
        runTree.metadata.usage_metadata = tokenUsage;

        return assistantMessage;
      },
      {
        run_type: "llm",
        name: "chat_model",
        metadata: {
          ls_provider: "my_provider",
          ls_model_name: "my_model",
        },
      }
    );

    await chatModel({ messages: inputs });
    ```
  </CodeGroup>
</Accordion>

<Accordion title="B. Return a `usage_metadata` field in your traced function's outputs.">
  Include the `usage_metadata` key directly within the object returned by your traced function. LangSmith will extract it from the output.

  <CodeGroup>
    ```python Python theme={null}
    from langsmith import traceable

    inputs = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "I'd like to book a table for two."},
    ]
    output = {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "Sure, what time would you like to book the table for?"
                }
            }
        ],
        "usage_metadata": {
            "input_tokens": 27,
            "output_tokens": 13,
            "total_tokens": 40,
            "input_token_details": {"cache_read": 10}
        },
    }

    @traceable(
        run_type="llm",
        metadata={"ls_provider": "my_provider", "ls_model_name": "my_model"}
    )
    def chat_model(messages: list):
        return output

    chat_model(inputs)
    ```

    ```typescript TypeScript theme={null}
    import { traceable } from "langsmith/traceable";

    const messages = [
        { role: "system", content: "You are a helpful assistant." },
        { role: "user", content: "I'd like to book a table for two." }
    ];
    const output = {
        choices: [
            {
                message: {
                    role: "assistant",
                    content: "Sure, what time would you like to book the table for?",
                },
            },
        ],
        usage_metadata: {
            input_tokens: 27,
            output_tokens: 13,
            total_tokens: 40,
        },
    };

    const chatModel = traceable(
        async ({
            messages,
        }: {
            messages: { role: string; content: string }[];
            model: string;
        }) => {
            return output;
        },
        {
            run_type: "llm",
            name: "chat_model",
            metadata: {
                ls_provider: "my_provider",
                ls_model_name: "my_model"
            }
        }
    );

    await chatModel({ messages });
    ```
  </CodeGroup>
</Accordion>

In either case, the usage metadata should contain a subset of the following LangSmith-recognized fields:

<Accordion title="Usage Metadata Schema and Cost Calculation">
  The following fields in the `usage_metadata` dict are recognized by LangSmith. You can view the full [Python types](https://github.com/langchain-ai/langsmith-sdk/blob/e705fbd362be69dd70229f94bc09651ef8056a61/python/langsmith/schemas.py#L1196-L1227) or [TypeScript interfaces](https://github.com/langchain-ai/langsmith-sdk/blob/e705fbd362be69dd70229f94bc09651ef8056a61/js/src/schemas.ts#L637-L689) directly.

  <ParamField path="input_tokens" type="number">
    Number of tokens used in the model input. Sum of all input token types.
  </ParamField>

  <ParamField path="output_tokens" type="number">
    Number of tokens used in the model response. Sum of all output token types.
  </ParamField>

  <ParamField path="total_tokens" type="number">
    Number of tokens used in the input and output. Optional, can be inferred. Sum of input\_tokens + output\_tokens.
  </ParamField>

  <ParamField path="input_token_details" type="object">
    Breakdown of input token types. Keys are token-type strings, values are counts. Example `{"cache_read": 5}`.

    Known fields include: `audio`, `text`, `image`, `cache_read`, `cache_creation`. Additional fields are possible depending on the model or provider.
  </ParamField>

  <ParamField path="output_token_details" type="object">
    Breakdown of output token types. Keys are token-type strings, values are counts. Example `{"reasoning": 5}`.

    Known fields include: `audio`, `text`, `image`, `reasoning`. Additional fields are possible depending on the model or provider.
  </ParamField>

  <ParamField path="input_cost" type="number">
    Cost of the input tokens.
  </ParamField>

  <ParamField path="output_cost" type="number">
    Cost of the output tokens.
  </ParamField>

  <ParamField path="total_cost" type="number">
    Cost of the tokens. Optional, can be inferred.  Sum of input\_cost + output\_cost.
  </ParamField>

  <ParamField path="input_cost_details" type="object">
    Details of the input cost. Keys are token-type strings, values are cost amounts.
  </ParamField>

  <ParamField path="output_cost_details" type="object">
    Details of the output cost. Keys are token-type strings, values are cost amounts.
  </ParamField>

  **Cost Calculations**

  The cost for a run is computed greedily from most-to-least specific token type. Suppose you set a price of \$2 per 1M input tokens with a detailed price of \$1 per 1M `cache_read` input tokens, and \$3 per 1M output tokens. If you uploaded the following usage metadata:

  ```python  theme={null}
  {
    "input_tokens": 20,
    "input_token_details": {"cache_read": 5},
    "output_tokens": 10,
    "total_tokens": 30,
  }
  ```

  Then, the token costs would be computed as follows:

  ```python  theme={null}
  # Notice that LangSmith computes the cache_read cost and then for any
  # remaining input_tokens, the default input price is applied.
  input_cost = 5 * 1e-6 + (20 - 5) * 2e-6  # 3.5e-5
  output_cost = 10 * 3e-6  # 3e-5
  total_cost = input_cost + output_cost  # 6.5e-5
  ```
</Accordion>

**2. Specify model name**

When using a custom model, the following fields need to be specified in a [run's metadata](/langsmith/add-metadata-tags) in order to associate token counts with costs. It's also helpful to provide these metadata fields to identify the model when viewing traces and when filtering.

* `ls_provider`: The provider of the model, e.g., “openai”, “anthropic”
* `ls_model_name`: The name of the model, e.g., “gpt-4o-mini”, “claude-3-opus-20240229”

**3. Set model prices**

A model pricing map is used to map model names to their per-token prices to compute costs from token counts. LangSmith's [model pricing table](https://smith.langchain.com/settings/workspaces/models) is used for this.

<Note>
  The table comes with pricing information for most OpenAI, Anthropic, and Gemini models. You can [add prices for other models](/langsmith/cost-tracking#create-a-new-model-price-entry), or [overwrite pricing for default models](/langsmith/cost-tracking#update-an-existing-model-price-entry) if you have custom pricing.
</Note>

For models that have different pricing for different token types (e.g., multimodal or cached tokens), you can specify a breakdown of prices for each token type. Hovering over the `...` next to the input/output prices shows you the price breakdown by token type.

<img className="block dark:hidden" src="https://mintcdn.com/langchain-5e9cc07a/PYCacG42leg3Zt_8/langsmith/images/model-price-map-light.png?fit=max&auto=format&n=PYCacG42leg3Zt_8&q=85&s=ae82f1ff59cfc57923d63869cb0608c0" alt="Model price map" data-og-width="1256" width="1256" data-og-height="494" height="494" data-path="langsmith/images/model-price-map-light.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/PYCacG42leg3Zt_8/langsmith/images/model-price-map-light.png?w=280&fit=max&auto=format&n=PYCacG42leg3Zt_8&q=85&s=ed5d4889252f7a890b8b86705a07aa31 280w, https://mintcdn.com/langchain-5e9cc07a/PYCacG42leg3Zt_8/langsmith/images/model-price-map-light.png?w=560&fit=max&auto=format&n=PYCacG42leg3Zt_8&q=85&s=5a801e45f2f628bbb5565b240a1060a3 560w, https://mintcdn.com/langchain-5e9cc07a/PYCacG42leg3Zt_8/langsmith/images/model-price-map-light.png?w=840&fit=max&auto=format&n=PYCacG42leg3Zt_8&q=85&s=5c43622f4b5259a41b911c1a1a686d1e 840w, https://mintcdn.com/langchain-5e9cc07a/PYCacG42leg3Zt_8/langsmith/images/model-price-map-light.png?w=1100&fit=max&auto=format&n=PYCacG42leg3Zt_8&q=85&s=73bfe48bbbc86df27b3c2705eb3ec850 1100w, https://mintcdn.com/langchain-5e9cc07a/PYCacG42leg3Zt_8/langsmith/images/model-price-map-light.png?w=1650&fit=max&auto=format&n=PYCacG42leg3Zt_8&q=85&s=a37f360aa7b50e29e984daf69a969be5 1650w, https://mintcdn.com/langchain-5e9cc07a/PYCacG42leg3Zt_8/langsmith/images/model-price-map-light.png?w=2500&fit=max&auto=format&n=PYCacG42leg3Zt_8&q=85&s=81a6f4ce7a883d757bd35d80ed950de4 2500w" />

<img className="hidden dark:block" src="https://mintcdn.com/langchain-5e9cc07a/PYCacG42leg3Zt_8/langsmith/images/model-price-map-dark.png?fit=max&auto=format&n=PYCacG42leg3Zt_8&q=85&s=739bb0123e9a238944452048578a4c49" alt="Model price map" data-og-width="1265" width="1265" data-og-height="486" height="486" data-path="langsmith/images/model-price-map-dark.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/PYCacG42leg3Zt_8/langsmith/images/model-price-map-dark.png?w=280&fit=max&auto=format&n=PYCacG42leg3Zt_8&q=85&s=3ef5d46c55b6d2a5a697bec31a908db4 280w, https://mintcdn.com/langchain-5e9cc07a/PYCacG42leg3Zt_8/langsmith/images/model-price-map-dark.png?w=560&fit=max&auto=format&n=PYCacG42leg3Zt_8&q=85&s=92cdeb0a4009cd7fb8f942ba28242571 560w, https://mintcdn.com/langchain-5e9cc07a/PYCacG42leg3Zt_8/langsmith/images/model-price-map-dark.png?w=840&fit=max&auto=format&n=PYCacG42leg3Zt_8&q=85&s=96100a58c8821063940522dd24758305 840w, https://mintcdn.com/langchain-5e9cc07a/PYCacG42leg3Zt_8/langsmith/images/model-price-map-dark.png?w=1100&fit=max&auto=format&n=PYCacG42leg3Zt_8&q=85&s=6e1e6a811ff7a28cf316b712deb62cd9 1100w, https://mintcdn.com/langchain-5e9cc07a/PYCacG42leg3Zt_8/langsmith/images/model-price-map-dark.png?w=1650&fit=max&auto=format&n=PYCacG42leg3Zt_8&q=85&s=61748722943b6fb76b5a45af10caabbc 1650w, https://mintcdn.com/langchain-5e9cc07a/PYCacG42leg3Zt_8/langsmith/images/model-price-map-dark.png?w=2500&fit=max&auto=format&n=PYCacG42leg3Zt_8&q=85&s=badfe7dda009e8c5ec675228331b3ed9 2500w" />

<Note>
  Updates to the model pricing map are not reflected in the costs for traces already logged. We do not currently support backfilling model pricing changes.
</Note>

<Accordion title="Create a new or modify an existing model price entry">
  To modify the default model prices, create a new entry with the same model, provider and match pattern as the default entry.

  To create a *new entry* in the model pricing map, click on the `+ Model` button in the top right corner.

  <img className="block dark:hidden" src="https://mintcdn.com/langchain-5e9cc07a/PYCacG42leg3Zt_8/langsmith/images/new-price-map-entry-light.png?fit=max&auto=format&n=PYCacG42leg3Zt_8&q=85&s=63dbd6e59b279a1f4ae692c892223af9" alt="New price map entry interface" data-og-width="467" width="467" data-og-height="854" height="854" data-path="langsmith/images/new-price-map-entry-light.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/PYCacG42leg3Zt_8/langsmith/images/new-price-map-entry-light.png?w=280&fit=max&auto=format&n=PYCacG42leg3Zt_8&q=85&s=0553163c010622eeb61af856cc6c41c4 280w, https://mintcdn.com/langchain-5e9cc07a/PYCacG42leg3Zt_8/langsmith/images/new-price-map-entry-light.png?w=560&fit=max&auto=format&n=PYCacG42leg3Zt_8&q=85&s=95cb41aa3695ea32e701f6a620cb778e 560w, https://mintcdn.com/langchain-5e9cc07a/PYCacG42leg3Zt_8/langsmith/images/new-price-map-entry-light.png?w=840&fit=max&auto=format&n=PYCacG42leg3Zt_8&q=85&s=37c244bfcfbf969a717dac9b7a01c58f 840w, https://mintcdn.com/langchain-5e9cc07a/PYCacG42leg3Zt_8/langsmith/images/new-price-map-entry-light.png?w=1100&fit=max&auto=format&n=PYCacG42leg3Zt_8&q=85&s=ca82285f5323216bb59b1be9b6cf1a2e 1100w, https://mintcdn.com/langchain-5e9cc07a/PYCacG42leg3Zt_8/langsmith/images/new-price-map-entry-light.png?w=1650&fit=max&auto=format&n=PYCacG42leg3Zt_8&q=85&s=a92a5257db7e1323b3301e5ed1aef7b0 1650w, https://mintcdn.com/langchain-5e9cc07a/PYCacG42leg3Zt_8/langsmith/images/new-price-map-entry-light.png?w=2500&fit=max&auto=format&n=PYCacG42leg3Zt_8&q=85&s=537332d988ad5b674bf5e5bd1f5584cc 2500w" />

  <img className="hidden dark:block" src="https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/new-price-map-entry.png?fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=2df87e349db00b8560f3d44824f2df13" alt="New price map entry interface" data-og-width="958" width="958" data-og-height="1762" height="1762" data-path="langsmith/images/new-price-map-entry.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/new-price-map-entry.png?w=280&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=4c49d72012424c80dc831b7f19125206 280w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/new-price-map-entry.png?w=560&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=ce3f75b14759e43c35723726933177a8 560w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/new-price-map-entry.png?w=840&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=2fb82f3bc83ee9dcecfad5243edb0844 840w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/new-price-map-entry.png?w=1100&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=57aebbd5b56a0ccbf91a664f7e930bef 1100w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/new-price-map-entry.png?w=1650&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=fbd6624fff7cf22139e022491e3188c3 1650w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/new-price-map-entry.png?w=2500&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=9ced4164e44f666c9e3dba0a9be9a188 2500w" />

  Here, you can specify the following fields:

  * **Model Name**: The human-readable name of the model.
  * **Input Price**: The cost per 1M input tokens for the model. This number is multiplied by the number of tokens in the prompt to calculate the prompt cost.
  * **Input Price Breakdown** (Optional): The breakdown of price for each different type of input token, e.g. `cache_read`, `video`, `audio`
  * **Output Price**: The cost per 1M output tokens for the model. This number is multiplied by the number of tokens in the completion to calculate the completion cost.
  * **Output Price Breakdown** (Optional): The breakdown of price for each different type of output token, e.g. `reasoning`, `image`, etc.
  * **Model Activation Date** (Optional): The date from which the pricing is applicable. Only runs after this date will apply this model price.
  * **Match Pattern**: A regex pattern to match the model name. This is used to match the value for `ls_model_name` in the run metadata.
  * **Provider** (Optional): The provider of the model. If specified, this is matched against `ls_provider` in the run metadata.

  Once you have set up the model pricing map, LangSmith will automatically calculate and aggregate the token-based costs for traces based on the token counts provided in the LLM invocations.
</Accordion>

### LLM calls: Sending costs directly

If your model follows a non-linear pricing scheme, we recommend calculating costs client-side and sending them to LangSmith as `usage_metadata`.

<Note>
  Gemini 3 Pro Preview and Gemini 2.5 Pro follow a pricing scheme with a stepwise cost function. We support this pricing scheme for Gemini by default. For any other models with non-linear pricing, you will need to follow these instructions to calculate costs.
</Note>

<CodeGroup>
  ```python Python theme={null}
  from langsmith import traceable, get_current_run_tree

  inputs = [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "I'd like to book a table for two."},
  ]

  @traceable(
      run_type="llm",
      metadata={"ls_provider": "my_provider", "ls_model_name": "my_model"}
  )
  def chat_model(messages: list):
      llm_output = {
          "choices": [
              {
                  "message": {
                      "role": "assistant",
                      "content": "Sure, what time would you like to book the table for?"
                  }
              }
          ],
          "usage_metadata": {
              # Specify cost (in dollars) for the inputs and outputs
              "input_cost": 1.1e-6,
              "input_cost_details": {"cache_read": 2.3e-7},
              "output_cost": 5.0e-6,
          },
      }
      run = get_current_run_tree()
      run.set(usage_metadata=llm_output["usage_metadata"])
      return llm_output["choices"][0]["message"]

  chat_model(inputs)
  ```

  ```typescript TypeScript theme={null}
  import { traceable, getCurrentRunTree } from "langsmith/traceable";

  const messages = [
    { role: "system", content: "You are a helpful assistant." },
    { role: "user", content: "I'd like to book a table for two." }
  ];

  const chatModel = traceable(
    async (messages: { role: string; content: string }[]) => {
      const llmOutput = {
        choices: [
          {
            message: {
              role: "assistant",
              content: "Sure, what time would you like to book the table for?",
            },
          },
        ],
        // Specify cost (in dollars) for the inputs and outputs
        usage_metadata: {
          input_cost: 1.1e-6,
          input_cost_details: { cache_read: 2.3e-7 },
          output_cost: 5.0e-6,
        },
      };

      // Attach usage metadata to the run
      const runTree = getCurrentRunTree();
      runTree.metadata.usage_metadata = llmOutput.usage_metadata;

      // Return only the assistant message
      return llmOutput.choices[0].message;
    },
    {
      run_type: "llm",
      name: "chat_model",
      metadata: {
        ls_provider: "my_provider",
        ls_model_name: "my_model",
      },
    }
  );

  await chatModel(messages);
  ```
</CodeGroup>

### Other runs: Sending costs

You can also send cost information for any non-LLM runs, such as tool calls.The cost must be specified in the `total_cost` field under the runs `usage_metadata`.

<Accordion title="A. Set a `total_cost` field on the run’s usage_metadata">
  Set a `total_cost` field on the run’s `usage_metadata`. The advantage of this approach is that you do not need to change your traced function’s runtime outputs

  <CodeGroup>
    ```python Python theme={null}
    from langsmith import traceable, get_current_run_tree

    # Example tool: get_weather
    @traceable(run_type="tool", name="get_weather")
    def get_weather(city: str):
        # Your tool logic goes here
        result = {
            "temperature_f": 68,
            "condition": "sunny",
            "city": city,
        }

        # Cost for this tool call (computed however you like)
        tool_cost = 0.0015

        # Attach usage metadata to the LangSmith run
        run = get_current_run_tree()
        run.set(usage_metadata={"total_cost": tool_cost})

        # Return only the actual tool result (no usage info)
        return result

    tool_response = get_weather("San Francisco")
    ```

    ```typescript TypeScript theme={null}
    import { traceable, getCurrentRunTree } from "langsmith/traceable";

    // Example tool: get_weather
    const getWeather = traceable(
      async ({ city }) => {
        // Your tool logic goes here
        const result = {
          temperature_f: 68,
          condition: "sunny",
          city,
        };

        // Cost for this tool call (computed however you like)
        const toolCost = 0.0015;

        // Attach usage metadata to the LangSmith run
        const runTree = getCurrentRunTree();
        runTree.metadata.usage_metadata = {
          total_cost: toolCost,
        };

        // Return only the actual tool result (no usage info)
        return result;
      },
      {
        run_type: "tool",
        name: "get_weather",
      }
    );

    const toolResponse = await getWeather({ city: "San Francisco" });
    ```
  </CodeGroup>
</Accordion>

<Accordion title="B. Return a `total_cost` field in your traced function's outputs.">
  Include the `usage_metadata` key directly within the object returned by your traced function. LangSmith will extract it from the output.

  <CodeGroup>
    ```python Python theme={null}
    from langsmith import traceable

    # Example tool: get_weather
    @traceable(run_type="tool", name="get_weather")
    def get_weather(city: str):
        # Your tool logic goes here
        result = {
            "temperature_f": 68,
            "condition": "sunny",
            "city": city,
        }

        # Attach tool call costs here
        return {
            **result,
            "usage_metadata": {
                "total_cost": 0.0015,   # <-- cost for this tool call
            },
        }

    tool_response = get_weather("San Francisco")
    ```

    ```typescript TypeScript theme={null}
    import { traceable } from "langsmith/traceable";

    // Example tool: get_weather
    const getWeather = traceable(
      async ({ city }) => {
        // Your tool logic goes here
        const result = {
          temperature_f: 68,
          condition: "sunny",
          city,
        };

        // Attach tool call costs here
        return {
          ...result,
          usage_metadata: {
            total_cost: 0.0015,  // <-- cost for this tool call
          },
        };
      },
      {
        run_type: "tool",
        name: "get_weather",
      }
    );

    const toolResponse = await getWeather({ city: "San Francisco" });
    ```
  </CodeGroup>
</Accordion>

***

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/cost-tracking.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.langchain.com/llms.txt