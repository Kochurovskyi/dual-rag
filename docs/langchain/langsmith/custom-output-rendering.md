# Custom output rendering

Custom output rendering allows you to visualize run outputs and dataset reference outputs using your own custom HTML pages. This is particularly useful for:

* **Domain-specific formatting**: Display medical records, legal documents, or other specialized data types in their native format.
* **Custom visualizations**: Create charts, graphs, or diagrams from numeric or structured output data.

In this page you'll learn how to:

* **[Configure custom rendering](#configure-custom-output-rendering)** in the LangSmith UI.
* **[Build a custom renderer](#build-a-custom-renderer)** to display output data.
* **[Understand where custom rendering appears](#where-custom-rendering-appears)** in LangSmith.

## Configure custom output rendering

Configure custom rendering at two levels:

* **For datasets**: Apply custom rendering to all runs associated with that dataset, wherever they appear—in experiments, run detail panes, or annotation queues.
* **For annotation queues**: Apply custom rendering to all runs within a specific annotation queue, regardless of which dataset they come from. This takes precedence over dataset-level configuration.

### For tracing projects

To configure custom output rendering for a tracing project:

<img src="https://mintcdn.com/langchain-5e9cc07a/oyRHf9tRXOU-EPbv/langsmith/images/tracing-project-custom-output-rendering-settings.png?fit=max&auto=format&n=oyRHf9tRXOU-EPbv&q=85&s=034f982fa3174c1649e5188bbb11ca03" alt="Tracing project settings showing custom output rendering configuration" data-og-width="1325" width="1325" data-og-height="1207" height="1207" data-path="langsmith/images/tracing-project-custom-output-rendering-settings.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/oyRHf9tRXOU-EPbv/langsmith/images/tracing-project-custom-output-rendering-settings.png?w=280&fit=max&auto=format&n=oyRHf9tRXOU-EPbv&q=85&s=9192b74a8df6dac268f17acee40817ab 280w, https://mintcdn.com/langchain-5e9cc07a/oyRHf9tRXOU-EPbv/langsmith/images/tracing-project-custom-output-rendering-settings.png?w=560&fit=max&auto=format&n=oyRHf9tRXOU-EPbv&q=85&s=106cf65662788e212505ac39d46d60ab 560w, https://mintcdn.com/langchain-5e9cc07a/oyRHf9tRXOU-EPbv/langsmith/images/tracing-project-custom-output-rendering-settings.png?w=840&fit=max&auto=format&n=oyRHf9tRXOU-EPbv&q=85&s=247529f2b0a3326a346145b9476cb709 840w, https://mintcdn.com/langchain-5e9cc07a/oyRHf9tRXOU-EPbv/langsmith/images/tracing-project-custom-output-rendering-settings.png?w=1100&fit=max&auto=format&n=oyRHf9tRXOU-EPbv&q=85&s=efcd6238cd47a17055a7ebcc214b3b30 1100w, https://mintcdn.com/langchain-5e9cc07a/oyRHf9tRXOU-EPbv/langsmith/images/tracing-project-custom-output-rendering-settings.png?w=1650&fit=max&auto=format&n=oyRHf9tRXOU-EPbv&q=85&s=4e0a42d7a9d939b0cd2731814116cba9 1650w, https://mintcdn.com/langchain-5e9cc07a/oyRHf9tRXOU-EPbv/langsmith/images/tracing-project-custom-output-rendering-settings.png?w=2500&fit=max&auto=format&n=oyRHf9tRXOU-EPbv&q=85&s=2519e4389455995b458e317fc23caa83 2500w" />

1. Navigate to the **Tracing Projects** page.
2. Click on an existing tracing project or create a new one.
3. In the edit tracing project pane, scroll to the **Custom Output Rendering** section.
4. Toggle **Enable custom output rendering**.
5. Enter the webpage URL in the **URL** field.
6. Click **Save**.

### For datasets

To configure custom output rendering for a dataset:

<img src="https://mintcdn.com/langchain-5e9cc07a/l7rhdSRpjWBkaCke/langsmith/images/custom-output-rendering-menu.png?fit=max&auto=format&n=l7rhdSRpjWBkaCke&q=85&s=7daf042ebae80eec20cd90a25c1d6087" alt="Dataset page with three-dot menu showing Custom Output Rendering option" data-og-width="3456" width="3456" data-og-height="2156" height="2156" data-path="langsmith/images/custom-output-rendering-menu.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/l7rhdSRpjWBkaCke/langsmith/images/custom-output-rendering-menu.png?w=280&fit=max&auto=format&n=l7rhdSRpjWBkaCke&q=85&s=432f6a5bb6c79797c17fa8faa74169b1 280w, https://mintcdn.com/langchain-5e9cc07a/l7rhdSRpjWBkaCke/langsmith/images/custom-output-rendering-menu.png?w=560&fit=max&auto=format&n=l7rhdSRpjWBkaCke&q=85&s=c77ec3be9ea681180d5c82d2588814b5 560w, https://mintcdn.com/langchain-5e9cc07a/l7rhdSRpjWBkaCke/langsmith/images/custom-output-rendering-menu.png?w=840&fit=max&auto=format&n=l7rhdSRpjWBkaCke&q=85&s=3f8fdb966f809ad049585efe3271182b 840w, https://mintcdn.com/langchain-5e9cc07a/l7rhdSRpjWBkaCke/langsmith/images/custom-output-rendering-menu.png?w=1100&fit=max&auto=format&n=l7rhdSRpjWBkaCke&q=85&s=3bdd2738b8dc1d17eeea3951536dedc8 1100w, https://mintcdn.com/langchain-5e9cc07a/l7rhdSRpjWBkaCke/langsmith/images/custom-output-rendering-menu.png?w=1650&fit=max&auto=format&n=l7rhdSRpjWBkaCke&q=85&s=5428362058ab8e8f4f71009779e3134f 1650w, https://mintcdn.com/langchain-5e9cc07a/l7rhdSRpjWBkaCke/langsmith/images/custom-output-rendering-menu.png?w=2500&fit=max&auto=format&n=l7rhdSRpjWBkaCke&q=85&s=a31530b7bd16f2fe6f8c6b622f55d9de 2500w" />

1. Navigate to your dataset in the **Datasets & Experiments** page.
2. Click **⋮** (three-dot menu) in the top right corner.
3. Select **Custom Output Rendering**.
4. Toggle **Enable custom output rendering**.
5. Enter the webpage URL in the **URL** field.
6. Click **Save**.

<img src="https://mintcdn.com/langchain-5e9cc07a/l7rhdSRpjWBkaCke/langsmith/images/custom-output-rendering-modal.png?fit=max&auto=format&n=l7rhdSRpjWBkaCke&q=85&s=bffd3b40ca14bbebc05c998d1cb5fa7e" alt="Custom Output Rendering modal with fields filled in" data-og-width="3456" width="3456" data-og-height="2156" height="2156" data-path="langsmith/images/custom-output-rendering-modal.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/l7rhdSRpjWBkaCke/langsmith/images/custom-output-rendering-modal.png?w=280&fit=max&auto=format&n=l7rhdSRpjWBkaCke&q=85&s=2fd8bdfcce6fdf5e9bd865590a8e0f79 280w, https://mintcdn.com/langchain-5e9cc07a/l7rhdSRpjWBkaCke/langsmith/images/custom-output-rendering-modal.png?w=560&fit=max&auto=format&n=l7rhdSRpjWBkaCke&q=85&s=c110a35a03909e146be961ac5386c888 560w, https://mintcdn.com/langchain-5e9cc07a/l7rhdSRpjWBkaCke/langsmith/images/custom-output-rendering-modal.png?w=840&fit=max&auto=format&n=l7rhdSRpjWBkaCke&q=85&s=1959a6a045a04e0d3290de4379a358bc 840w, https://mintcdn.com/langchain-5e9cc07a/l7rhdSRpjWBkaCke/langsmith/images/custom-output-rendering-modal.png?w=1100&fit=max&auto=format&n=l7rhdSRpjWBkaCke&q=85&s=4a154ab114547ff7e243acb36c9bd9a3 1100w, https://mintcdn.com/langchain-5e9cc07a/l7rhdSRpjWBkaCke/langsmith/images/custom-output-rendering-modal.png?w=1650&fit=max&auto=format&n=l7rhdSRpjWBkaCke&q=85&s=c2eae83b1d6ec160a37fd998511e9794 1650w, https://mintcdn.com/langchain-5e9cc07a/l7rhdSRpjWBkaCke/langsmith/images/custom-output-rendering-modal.png?w=2500&fit=max&auto=format&n=l7rhdSRpjWBkaCke&q=85&s=025b243cf994c130439ef55f6dc5e856 2500w" />

### For annotation queues

To configure custom output rendering for an annotation queue:

<img src="https://mintcdn.com/langchain-5e9cc07a/optUJrLvYf4z4j5I/langsmith/images/annotation-queue-custom-output-rendering-settings.png?fit=max&auto=format&n=optUJrLvYf4z4j5I&q=85&s=579aad04fa6990b220514280eef799f4" alt="Annotation queue settings showing custom output rendering configuration" data-og-width="3456" width="3456" data-og-height="1914" height="1914" data-path="langsmith/images/annotation-queue-custom-output-rendering-settings.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/optUJrLvYf4z4j5I/langsmith/images/annotation-queue-custom-output-rendering-settings.png?w=280&fit=max&auto=format&n=optUJrLvYf4z4j5I&q=85&s=525d5f11afb5bf8a5fd86f5de5063d72 280w, https://mintcdn.com/langchain-5e9cc07a/optUJrLvYf4z4j5I/langsmith/images/annotation-queue-custom-output-rendering-settings.png?w=560&fit=max&auto=format&n=optUJrLvYf4z4j5I&q=85&s=0d58600ddf45ff1e7bbad5cc31489f24 560w, https://mintcdn.com/langchain-5e9cc07a/optUJrLvYf4z4j5I/langsmith/images/annotation-queue-custom-output-rendering-settings.png?w=840&fit=max&auto=format&n=optUJrLvYf4z4j5I&q=85&s=d5aaa11700f5f58bcf157dc0fd32877a 840w, https://mintcdn.com/langchain-5e9cc07a/optUJrLvYf4z4j5I/langsmith/images/annotation-queue-custom-output-rendering-settings.png?w=1100&fit=max&auto=format&n=optUJrLvYf4z4j5I&q=85&s=51794d75925516c728177e91689dbdcd 1100w, https://mintcdn.com/langchain-5e9cc07a/optUJrLvYf4z4j5I/langsmith/images/annotation-queue-custom-output-rendering-settings.png?w=1650&fit=max&auto=format&n=optUJrLvYf4z4j5I&q=85&s=cf7c47a38a18a548f627dc56e94abfde 1650w, https://mintcdn.com/langchain-5e9cc07a/optUJrLvYf4z4j5I/langsmith/images/annotation-queue-custom-output-rendering-settings.png?w=2500&fit=max&auto=format&n=optUJrLvYf4z4j5I&q=85&s=bcd50a9547635188f2e7e458af0baa46 2500w" />

1. Navigate to the **Annotation Queues** page.
2. Click on an existing annotation queue or create a new one.
3. In the annotation queue settings pane, scroll to the **Custom Output Rendering** section.
4. Toggle **Enable custom output rendering**.
5. Enter the webpage URL in the **URL** field.
6. Click **Save** or **Create**.

<Info>When custom rendering settings are applied at multiple levels, the precedence is as follows: annotation queue > dataset > tracing project.</Info>

## Build a custom renderer

### Understand the message format

Your HTML page will receive output data via the [postMessage API](https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage). LangSmith sends messages with the following structure:

```typescript  theme={null}
{
  type: "output" | "reference",
  data: {
    // The outputs (actual output or reference output)
    // Structure varies based on your application
  },
  metadata: {
    inputs: {
      // The inputs that generated this output
      // Structure varies based on your application
    }
  }
}
```

* `type`: Indicates whether this is an actual output (`"output"`) or a reference output (`"reference"`).
* `data`: The output data itself.
* `metadata.inputs`: The input data that generated this output, provided for context.

<Note>**Message delivery timing**: LangSmith uses an exponential backoff retry mechanism to ensure your page receives the data even if it loads slowly. Messages are sent up to 6 times with increasing delays (100ms, 200ms, 400ms, 800ms, 1600ms, 3200ms).</Note>

### Example implementation

This example listens for incoming postMessage events and displays them on the page. Each message is numbered and formatted as JSON, making it easy to inspect the data structure LangSmith sends to your renderer.

```html  theme={null}
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8" />
        <title>PostMessage Echo</title>
        <link rel="stylesheet" href="https://unpkg.com/sakura.css/css/sakura.css" />
    </head>
    <body>
        <h1>PostMessage Messages</h1>
        <div id="messages"></div>
        <script>
            let count = 0;
            window.addEventListener("message", (event) => {
                count++;
                const header = document.createElement("h3");
                header.appendChild(document.createTextNode(`Message ${count}`));
                const code = document.createElement("code");
                code.appendChild(document.createTextNode(JSON.stringify(event.data, null, 2)));
                const pre = document.createElement("pre");
                pre.appendChild(code);
                document.getElementById("messages").appendChild(header);
                document.getElementById("messages").appendChild(pre);
            });
        </script>
    </body>
</html>
```

## Where custom rendering appears

When enabled, your custom rendering will replace the default output view in:

* **Experiment comparison view**: When comparing outputs across multiple experiments:

<img src="https://mintcdn.com/langchain-5e9cc07a/l7rhdSRpjWBkaCke/langsmith/images/custom-output-rendering-experiment-comparison.png?fit=max&auto=format&n=l7rhdSRpjWBkaCke&q=85&s=6f1fd9d3ca4be55aa9a0b40140771e08" alt="Experiment comparison view showing custom rendering" data-og-width="3456" width="3456" data-og-height="2156" height="2156" data-path="langsmith/images/custom-output-rendering-experiment-comparison.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/l7rhdSRpjWBkaCke/langsmith/images/custom-output-rendering-experiment-comparison.png?w=280&fit=max&auto=format&n=l7rhdSRpjWBkaCke&q=85&s=4010749197ec99216b6cbc004f8e2aed 280w, https://mintcdn.com/langchain-5e9cc07a/l7rhdSRpjWBkaCke/langsmith/images/custom-output-rendering-experiment-comparison.png?w=560&fit=max&auto=format&n=l7rhdSRpjWBkaCke&q=85&s=3eb5a8825d76c92f531c34912c476fb5 560w, https://mintcdn.com/langchain-5e9cc07a/l7rhdSRpjWBkaCke/langsmith/images/custom-output-rendering-experiment-comparison.png?w=840&fit=max&auto=format&n=l7rhdSRpjWBkaCke&q=85&s=1977c3020b1b2150beefc4980db857f9 840w, https://mintcdn.com/langchain-5e9cc07a/l7rhdSRpjWBkaCke/langsmith/images/custom-output-rendering-experiment-comparison.png?w=1100&fit=max&auto=format&n=l7rhdSRpjWBkaCke&q=85&s=2f8f86c1ad7ff02b65f78cd43bead446 1100w, https://mintcdn.com/langchain-5e9cc07a/l7rhdSRpjWBkaCke/langsmith/images/custom-output-rendering-experiment-comparison.png?w=1650&fit=max&auto=format&n=l7rhdSRpjWBkaCke&q=85&s=979e5426ee86673cd088aef614c52a6e 1650w, https://mintcdn.com/langchain-5e9cc07a/l7rhdSRpjWBkaCke/langsmith/images/custom-output-rendering-experiment-comparison.png?w=2500&fit=max&auto=format&n=l7rhdSRpjWBkaCke&q=85&s=292b4ac1322414a059b2ba5a4285caf3 2500w" />

* **Run detail panes**: When viewing runs that are associated with a dataset:

<img src="https://mintcdn.com/langchain-5e9cc07a/l7rhdSRpjWBkaCke/langsmith/images/custom-output-rendering-run-details.png?fit=max&auto=format&n=l7rhdSRpjWBkaCke&q=85&s=abec759e27bb3dfa827354d13746cf61" alt="Run detail pane showing custom rendering" data-og-width="3456" width="3456" data-og-height="2156" height="2156" data-path="langsmith/images/custom-output-rendering-run-details.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/l7rhdSRpjWBkaCke/langsmith/images/custom-output-rendering-run-details.png?w=280&fit=max&auto=format&n=l7rhdSRpjWBkaCke&q=85&s=9d4d8e9e4d3e2f9e856d9da23e16d805 280w, https://mintcdn.com/langchain-5e9cc07a/l7rhdSRpjWBkaCke/langsmith/images/custom-output-rendering-run-details.png?w=560&fit=max&auto=format&n=l7rhdSRpjWBkaCke&q=85&s=1adfc78a0ba06a3b9b18433fc2e1f82c 560w, https://mintcdn.com/langchain-5e9cc07a/l7rhdSRpjWBkaCke/langsmith/images/custom-output-rendering-run-details.png?w=840&fit=max&auto=format&n=l7rhdSRpjWBkaCke&q=85&s=a882e8fb03c81526070c0e9f49de157b 840w, https://mintcdn.com/langchain-5e9cc07a/l7rhdSRpjWBkaCke/langsmith/images/custom-output-rendering-run-details.png?w=1100&fit=max&auto=format&n=l7rhdSRpjWBkaCke&q=85&s=39d6a85d5578c58cf2c6853ce1d5e704 1100w, https://mintcdn.com/langchain-5e9cc07a/l7rhdSRpjWBkaCke/langsmith/images/custom-output-rendering-run-details.png?w=1650&fit=max&auto=format&n=l7rhdSRpjWBkaCke&q=85&s=d9c37910f147b76685b018a620aa9d40 1650w, https://mintcdn.com/langchain-5e9cc07a/l7rhdSRpjWBkaCke/langsmith/images/custom-output-rendering-run-details.png?w=2500&fit=max&auto=format&n=l7rhdSRpjWBkaCke&q=85&s=24538e055a2363976a7f3ce5d0111356 2500w" />

* **Annotation queues**: When reviewing runs in annotation queues:

<img src="https://mintcdn.com/langchain-5e9cc07a/l7rhdSRpjWBkaCke/langsmith/images/custom-output-rendering-annotation-queue.png?fit=max&auto=format&n=l7rhdSRpjWBkaCke&q=85&s=8d1b66541ea7dcd0246354fca1568719" alt="Annotation queue showing custom rendering" data-og-width="3456" width="3456" data-og-height="2156" height="2156" data-path="langsmith/images/custom-output-rendering-annotation-queue.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/l7rhdSRpjWBkaCke/langsmith/images/custom-output-rendering-annotation-queue.png?w=280&fit=max&auto=format&n=l7rhdSRpjWBkaCke&q=85&s=a42373180e5ab88ee80c3a670102f290 280w, https://mintcdn.com/langchain-5e9cc07a/l7rhdSRpjWBkaCke/langsmith/images/custom-output-rendering-annotation-queue.png?w=560&fit=max&auto=format&n=l7rhdSRpjWBkaCke&q=85&s=47be4504dd9d4a0c191cc426d7eaa7c4 560w, https://mintcdn.com/langchain-5e9cc07a/l7rhdSRpjWBkaCke/langsmith/images/custom-output-rendering-annotation-queue.png?w=840&fit=max&auto=format&n=l7rhdSRpjWBkaCke&q=85&s=36eda0a27d923057fbb4f0fc661e311e 840w, https://mintcdn.com/langchain-5e9cc07a/l7rhdSRpjWBkaCke/langsmith/images/custom-output-rendering-annotation-queue.png?w=1100&fit=max&auto=format&n=l7rhdSRpjWBkaCke&q=85&s=82593a5f663686eb61d9b90d9b1b8c39 1100w, https://mintcdn.com/langchain-5e9cc07a/l7rhdSRpjWBkaCke/langsmith/images/custom-output-rendering-annotation-queue.png?w=1650&fit=max&auto=format&n=l7rhdSRpjWBkaCke&q=85&s=dec8e45c1c77bd1cdd9b3aec093bf566 1650w, https://mintcdn.com/langchain-5e9cc07a/l7rhdSRpjWBkaCke/langsmith/images/custom-output-rendering-annotation-queue.png?w=2500&fit=max&auto=format&n=l7rhdSRpjWBkaCke&q=85&s=a8a978b3ec3d119fb16002d1a432c91a 2500w" />

***

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/custom-output-rendering.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.langchain.com/llms.txt