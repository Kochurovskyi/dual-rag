# Trace with Instructor

LangSmith provides a convenient integration with [Instructor](https://python.useinstructor.com/), a popular open-source library for generating structured output with LLMs.

In order to use, you first need to set your LangSmith API key.

```shell  theme={null}
export LANGSMITH_API_KEY=<your-api-key>
# For LangSmith API keys linked to multiple workspaces, set the LANGSMITH_WORKSPACE_ID environment variable to specify which workspace to use.
export LANGSMITH_WORKSPACE_ID=<your-workspace-id>
```

Next, you will need to install the LangSmith SDK:

<CodeGroup>
  ```bash pip theme={null}
  pip install -U langsmith
  ```

  ```bash uv theme={null}
  uv add langsmith
  ```
</CodeGroup>

Wrap your OpenAI client with `langsmith.wrappers.wrap_openai`

```python  theme={null}
from openai import OpenAI
from langsmith import wrappers

client = wrappers.wrap_openai(OpenAI())
```

After this, you can patch the wrapped OpenAI client using `instructor`:

```python  theme={null}
import instructor

client = instructor.patch(client)
```

Now, you can use `instructor` as you normally would, but now everything is logged to LangSmith!

```python  theme={null}
from pydantic import BaseModel


class UserDetail(BaseModel):
    name: str
    age: int


user = client.chat.completions.create(
    model="gpt-4o-mini",
    response_model=UserDetail,
    messages=[
        {"role": "user", "content": "Extract Jason is 25 years old"},
    ]
)
```

Oftentimes, you use `instructor` inside of other functions.
You can get nested traces by using this wrapped client and decorating those functions with `@traceable`.
Please see [this guide](./annotate-code) for more information on how to annotate your code for tracing with the `@traceable` decorator.

```python {highlight={2}} theme={null}
# You can customize the run name with the `name` keyword argument
@traceable(name="Extract User Details")
def my_function(text: str) -> UserDetail:
    return client.chat.completions.create(
        model="gpt-4o-mini",
        response_model=UserDetail,
        messages=[
            {"role": "user", "content": f"Extract {text}"},
        ]
    )

my_function("Jason is 25 years old")
```

***

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/trace-with-instructor.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.langchain.com/llms.txt