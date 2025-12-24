# How to audit evaluator scores

LLM-as-a-judge evaluators don't always get it right. Because of this, it is often useful for a human to manually audit the scores left by an evaluator and correct them where necessary. LangSmith allows you to make corrections on evaluator scores in the UI or SDK.

## In the comparison view

In the comparison view, you may click on any feedback tag to bring up the feedback details. From there, click the "edit" icon on the right to bring up the corrections view. You may then type in your desired score in the text box under "Make correction". If you would like, you may also attach an explanation to your correction. This is useful if you are using a [few-shot evaluator](/langsmith/create-few-shot-evaluators) and will be automatically inserted into your few-shot examples in place of the `few_shot_explanation` prompt variable.

<img src="https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/corrections-comparison-view.png?fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=5b815b771c18f291a9ef1b7defb9feb3" alt="Audit Evaluator Comparison View" data-og-width="3426" width="3426" data-og-height="1878" height="1878" data-path="langsmith/images/corrections-comparison-view.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/corrections-comparison-view.png?w=280&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=4840ceb8c340713fef6a7999c5d9c6cb 280w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/corrections-comparison-view.png?w=560&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=08b128d085701f17e20fdc6d314253a8 560w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/corrections-comparison-view.png?w=840&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=7d6300071894c9ff3f1fc80c6954c13d 840w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/corrections-comparison-view.png?w=1100&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=ffe472be6a4b33d741782a1bc3269c60 1100w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/corrections-comparison-view.png?w=1650&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=454422187b095a4ad0ec3ad9074d4301 1650w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/corrections-comparison-view.png?w=2500&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=93b0585577eb98e6d76db3cba6868473 2500w" />

## In the runs table

In the runs table, find the "Feedback" column and click on the feedback tag to bring up the feedback details. Again, click the "edit" icon on the right to bring up the corrections view.

<img src="https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/corrections-runs-table.png?fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=5e64530681ac9125751af2383b67ba35" alt="Audit Evaluator Runs Table" data-og-width="1734" width="1734" data-og-height="1002" height="1002" data-path="langsmith/images/corrections-runs-table.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/corrections-runs-table.png?w=280&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=46a1a8328ad238d876d3b003a7ab836a 280w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/corrections-runs-table.png?w=560&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=60183b8a46938ccfe97a694cb941e7e3 560w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/corrections-runs-table.png?w=840&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=7a2b5008a78d18d283e81eae9a8e23c0 840w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/corrections-runs-table.png?w=1100&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=e58f3c26472e5e78209927d662ab72c1 1100w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/corrections-runs-table.png?w=1650&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=eeb374392b18fa613e43564269cd8ff8 1650w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/corrections-runs-table.png?w=2500&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=117673d7c311c45f0b954313a35efb32 2500w" />

## In the SDK

Corrections can be made via the SDK's `update_feedback` function, with the `correction` dict. You must specify a `score` key which corresponds to a number for it to be rendered in the UI.

<CodeGroup>
  ```python Python theme={null}
  import langsmith

  client = langsmith.Client()

  client.update_feedback(
      my_feedback_id,
      correction={
          "score": 1,
      },
  )
  ```

  ```typescript TypeScript theme={null}
  import { Client } from 'langsmith';

  const client = new Client();

  await client.updateFeedback(
      myFeedbackId,
      {
          correction: {
              score: 1,
          }
      }
  )
  ```
</CodeGroup>

***

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/audit-evaluator-scores.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.langchain.com/llms.txt