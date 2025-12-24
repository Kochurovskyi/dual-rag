# Log retriever traces

<Note>
  Nothing will break if you don't log retriever traces in the correct format and data will still be logged. However, the data will not be rendered in a way that is specific to retriever steps.
</Note>

Many LLM applications require looking up documents from vector databases, knowledge graphs, or other types of indexes. Retriever traces are a way to log the documents that are retrieved by the retriever. LangSmith provides special rendering for retrieval steps in traces to make it easier to understand and diagnose retrieval issues. In order for retrieval steps to be rendered correctly, a few small steps need to be taken.

1. Annotate the retriever step with `run_type="retriever"`.

2. Return a list of Python dictionaries or TypeScript objects from the retriever step. Each dictionary should contain the following keys:

   * `page_content`: The text of the document.
   * `type`: This should always be "Document".
   * `metadata`: A python dictionary or TypeScript object containing metadata about the document. This metadata will be displayed in the trace.

The following code snippets show how to log a retrieval steps in Python and TypeScript.

<CodeGroup>
  ```python Python theme={null}
  from langsmith import traceable

  def _convert_docs(results):
      return [
          {
              "page_content": r,
              "type": "Document",
              "metadata": {"foo": "bar"}
          }
          for r in results
      ]

  @traceable(run_type="retriever")
  def retrieve_docs(query):
      # Foo retriever returning hardcoded dummy documents.
      # In production, this could be a real vector datatabase or other document index.
      contents = ["Document contents 1", "Document contents 2", "Document contents 3"]
      return _convert_docs(contents)

  retrieve_docs("User query")
  ```

  ```typescript TypeScript theme={null}
  import { traceable } from "langsmith/traceable";

  interface Document {
      page_content: string;
      type: string;
      metadata: { foo: string };
  }

  function convertDocs(results: string[]): Document[] {
      return results.map((r) => ({
          page_content: r,
          type: "Document",
          metadata: { foo: "bar" }
      }));
  }

  const retrieveDocs = traceable((query: string): Document[] => {
      // Foo retriever returning hardcoded dummy documents.
      // In production, this could be a real vector database or other document index.
      const contents = ["Document contents 1", "Document contents 2", "Document contents 3"];
      return convertDocs(contents);
  },{
      name: "retrieveDocs",
      run_type: "retriever"
  } // Configuration for traceable
  );

  await retrieveDocs("User query");
  ```
</CodeGroup>

The following image shows how a retriever step is rendered in a trace. The contents along with the metadata are displayed with each document.

<img src="https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/retriever-trace.png?fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=786c74f63e4c94d35535aa46ac9f38f4" alt="Retriever trace" data-og-width="1614" width="1614" data-og-height="736" height="736" data-path="langsmith/images/retriever-trace.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/retriever-trace.png?w=280&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=c2e2720a208cc2402e869e214609ec21 280w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/retriever-trace.png?w=560&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=8949f5484519221d159191e9437a862f 560w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/retriever-trace.png?w=840&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=7f376f3ca4575ffc08eb7fc6bdc0db4c 840w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/retriever-trace.png?w=1100&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=06ac1c1dfa24dab91376f2d641fe9aa2 1100w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/retriever-trace.png?w=1650&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=5046d388f4583d270740adfbd1e58539 1650w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/retriever-trace.png?w=2500&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=aa3aae9c839dd00ca450cfeb7b285371 2500w" />

***

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/log-retriever-trace.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.langchain.com/llms.txt