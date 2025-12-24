# Log multimodal traces

LangSmith supports logging and rendering images as part of traces. This is currently supported for multimodal LLM runs.

In order to log images, use `wrap_openai`/ `wrapOpenAI` in Python or TypeScript respectively and pass an image URL or base64 encoded image as part of the input.

<CodeGroup>
  ```python Python theme={null}
  from openai import OpenAI
  from langsmith.wrappers import wrap_openai
  client = wrap_openai(OpenAI())
  response = client.chat.completions.create(
      model="gpt-4-turbo",
      messages=[
        {
          "role": "user",
          "content": [
            {"type": "text", "text": "What's in this image?"},
            {
              "type": "image_url",
              "image_url": {
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
              },
            },
          ],
        }
      ],
  )
  print(response.choices[0])
  ```

  ```typescript TypeScript theme={null}
  import OpenAI from "openai";
  import { wrapOpenAI } from "langsmith/wrappers";
  // Wrap the OpenAI client to automatically log traces
  const wrappedClient = wrapOpenAI(new OpenAI());
  const response = await wrappedClient.chat.completions.create({
    model: "gpt-4-turbo",
    messages: [
      {
        role: "user",
        content: [
          { type: "text", text: "What's in this image?" },
          {
            type: "image_url",
            image_url: {
              "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
            },
          },
        ],
      },
    ],
  });
  console.log(response.choices[0]);
  ```
</CodeGroup>

The image will be rendered as part of the trace in the LangSmith UI.

<img src="https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/multimodal.png?fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=ff41711a0992c77f86cbc9f523e2ae93" alt="Multimodal" data-og-width="1600" width="1600" data-og-height="1216" height="1216" data-path="langsmith/images/multimodal.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/multimodal.png?w=280&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=d1119193b53a405869cbda1d17c88544 280w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/multimodal.png?w=560&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=147037549a28d87622e4c7d4d15ccc2b 560w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/multimodal.png?w=840&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=145003b20883ea39001adaf0eaf45529 840w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/multimodal.png?w=1100&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=01cc9ca22bca3312a5d4c1b356e5b8fc 1100w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/multimodal.png?w=1650&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=047b36000ced498139fa793c1815440a 1650w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/multimodal.png?w=2500&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=f7868994ae8fd23e9239b4b8d77ee4a0 2500w" />

***

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/log-multimodal-traces.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.langchain.com/llms.txt