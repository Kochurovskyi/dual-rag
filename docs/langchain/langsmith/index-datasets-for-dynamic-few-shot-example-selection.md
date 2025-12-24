# Dynamic few shot example selection

<Note>
  This feature is in open beta. It is only available to paid team plans. Please contact support via [support.langchain.com](https://support.langchain.com) if you have questions about enablement.
</Note>

Configure your datasets so that you can search for few shot examples based on an incoming request.

## Pre-conditions

1. Your dataset must use the KV store data type (we do not currently support chat model or LLM type datasets)
2. You must have an input schema defined for your dataset. See our docs on setting up schema validation [in our UI](/langsmith/manage-datasets-in-application#dataset-schema-validation) for details.
3. You must be on a paid team plan (e.g. Plus plan)
4. You must be on LangSmith cloud

## Index your dataset for few shot search

Navigate to the datasets UI, and click the new `Few-Shot search` tab. Hit the `Start sync` button, which will create a new index on your dataset to make it searchable.

<img src="https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-tab-unsynced.png?fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=7bc50f1a3d4ea7b9e7458f3ed9770179" alt="Few shot tab unsynced" data-og-width="3208" width="3208" data-og-height="1902" height="1902" data-path="langsmith/images/few-shot-tab-unsynced.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-tab-unsynced.png?w=280&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=c2ee3688a24b8d142d4a5dd89c8797c1 280w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-tab-unsynced.png?w=560&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=44a4d8b59948893b4bd20d4c1b62198c 560w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-tab-unsynced.png?w=840&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=16a303eab8e2aede574c12353f782789 840w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-tab-unsynced.png?w=1100&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=fbcf4566ec48c219bb7828bdc2cfe6b9 1100w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-tab-unsynced.png?w=1650&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=15da2b6b3e4a29ac3a2b4e139e2cf345 1650w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-tab-unsynced.png?w=2500&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=6bd99520313da2fedbbbaf388c956ba7 2500w" />

By default, we sync to the latest version of your dataset. That means when new examples are added to your dataset, they will automatically be added to your index. This process runs every few minutes, so there should be a very short delay for indexing new examples. You can see whether your index is up to date under `Few-shot index` on the lefthand side of the screen in the next section.

## Test search quality in the few shot playground

Now that you have turned on indexing for your dataset, you will see the new few shot playground.

<img src="https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-synced-empty-state.png?fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=b2b714b5a281ab8f39761566afd452f7" alt="Few shot synced empty state" data-og-width="3208" width="3208" data-og-height="1902" height="1902" data-path="langsmith/images/few-shot-synced-empty-state.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-synced-empty-state.png?w=280&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=b8e4e648ce36f12a141f98815fd2e63d 280w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-synced-empty-state.png?w=560&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=49044eef3af8c08b60bcfeabadde6d16 560w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-synced-empty-state.png?w=840&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=b0fb897716bfac9521d0490c11eb006e 840w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-synced-empty-state.png?w=1100&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=f21c2ad1fc5177af66c5f0c5ac59f660 1100w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-synced-empty-state.png?w=1650&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=dd9e2f9aa42366063ca14ad2b365e6fc 1650w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-synced-empty-state.png?w=2500&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=72158d44bcf916f2548bc5c7a6dabbce 2500w" />

You can type in a sample input, and check which results would be returned by our search API.

<img src="https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-search-results.png?fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=f64d39010f85b68d4d9ae3febc2b59d7" alt="Few shot search results" data-og-width="3208" width="3208" data-og-height="1902" height="1902" data-path="langsmith/images/few-shot-search-results.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-search-results.png?w=280&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=cbbd01172c4514eb3d775a4c0f3ca2e4 280w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-search-results.png?w=560&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=4a15ea167365f8d9105ab5aab50ed241 560w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-search-results.png?w=840&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=94ac208df6e860b9c194a646e3183779 840w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-search-results.png?w=1100&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=ec68d9679e4cc86eebe352a9364e8894 1100w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-search-results.png?w=1650&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=5650c218963b5e8bd8d56e0bf886cd3e 1650w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-search-results.png?w=2500&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=89e90c66c065bee2a728cd5dad69432a 2500w" />

Each result will have a score and a link to the example in the dataset. The scoring system works such that 0 is a completely random result, and higher scores are better. Results will be sorted in descending order according to score.

<Note>
  Search uses a BM25-like algorithm for keyword based similarity scores. The actual score is subject to change as we improve the search algorithm, so we recommend not relying on the scores themselves, as their meaning may evolve over time. They are simply used for convenience in vibe-testing outputs in the playground.
</Note>

## Adding few shot search to your application

Click the `Get Code Snippet` button in the previous diagram, you'll be taken to a screen that has code snippets from our LangSmith SDK in different languages.

<img src="https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-code-snippet.png?fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=015d9416ef4f2708a6f2dfedceb1ea07" alt="Few shot code snippet" data-og-width="3208" width="3208" data-og-height="1902" height="1902" data-path="langsmith/images/few-shot-code-snippet.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-code-snippet.png?w=280&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=a5b15cf813569f4f218d972f2dbe89a5 280w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-code-snippet.png?w=560&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=231a3aad9937aab1fa92e65839bb5869 560w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-code-snippet.png?w=840&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=8aa86a24694342bca8ab387c83338afe 840w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-code-snippet.png?w=1100&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=d92247c22e6fb2fd85e80713616b7fba 1100w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-code-snippet.png?w=1650&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=28f6e81c67c52687cd24431b83145675 1650w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/few-shot-code-snippet.png?w=2500&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=aeafca83ae2489c43aa38d24165e5d62 2500w" />

For code samples on using few shot search in LangChain python applications, please see our [how-to guide in the LangChain docs](https://python.langchain.com/v0.2/docs/how_to/example_selectors_langsmith/).

### Code snippets

<Note>
  Please ensure you are using the python SDK with version >= 1.101 or the typescript SDK with version >= 1.43
</Note>

For copy and paste convenience, you can find the similar code snippets to the ones shown in the screenshot above here:

<CodeGroup>
  ```python Python (Async) theme={null}
  import langsmith as ls
  # Copy this value from LangSmith UI
  dataset_id = "1c5e9c95-dfd4-4dc5-a4b8-df7ea921c913"
  async with ls.AsyncClient() as client:
    examples = await client.similar_examples(
        {"question": "knock knock"}, dataset_id=dataset_id, limit=1
    )
    print(examples[0].outputs)  # {"output": "Few shots'll do the trick."}
  ```

  ```python Python theme={null}
  from langsmith import Client
  client = Client()
  # Copy this value from LangSmith UI
  dataset_id = "1c5e9c95-dfd4-4dc5-a4b8-df7ea921c913"
  examples = client.similar_examples(
    {"question": "knock knock"}, dataset_id=dataset_id, limit=1
  )
  print(examples[0].outputs)
  # {"output": "Few shots'll do the trick."}
  ```

  ```typescript TypeScript theme={null}
  import { Client } from "langsmith";
  const client = new Client();
  // Copy this value from LangSmith UI
  const dataset_id = "1c5e9c95-dfd4-4dc5-a4b8-df7ea921c913";
  const examples = await client.similarExamples({question: "knock knock"}, dataset_id, 1);
  console.log(examples[0].outputs);
  // {output: "Few shots'll do the trick."}
  ```
</CodeGroup>

***

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/index-datasets-for-dynamic-few-shot-example-selection.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.langchain.com/llms.txt