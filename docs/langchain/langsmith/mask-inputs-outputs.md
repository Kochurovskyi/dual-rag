# Prevent logging of sensitive data in traces

In some situations, you may need to prevent the inputs and outputs of your traces from being logged for privacy or security reasons. LangSmith provides a way to filter the inputs and outputs of your traces before they are sent to the LangSmith backend.

If you want to completely hide the inputs and outputs of your traces, you can set the following environment variables when running your application:

```bash  theme={null}
LANGSMITH_HIDE_INPUTS=true
LANGSMITH_HIDE_OUTPUTS=true
```

This works for both the LangSmith SDK (Python and TypeScript) and LangChain.

You can also customize and override this behavior for a given `Client` instance. This can be done by setting the `hide_inputs` and `hide_outputs` parameters on the `Client` object (`hideInputs` and `hideOutputs` in TypeScript).

For the example below, we will simply return an empty object for both `hide_inputs` and `hide_outputs`, but you can customize this to your needs.

<CodeGroup>
  ```python Python theme={null}
  import openai
  from langsmith import Client
  from langsmith.wrappers import wrap_openai

  openai_client = wrap_openai(openai.Client())
  langsmith_client = Client(
      hide_inputs=lambda inputs: {}, hide_outputs=lambda outputs: {}
  )

  # The trace produced will have its metadata present, but the inputs will be hidden
  openai_client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
          {"role": "system", "content": "You are a helpful assistant."},
          {"role": "user", "content": "Hello!"},
      ],
      langsmith_extra={"client": langsmith_client},
  )

  # The trace produced will not have hidden inputs and outputs
  openai_client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
          {"role": "system", "content": "You are a helpful assistant."},
          {"role": "user", "content": "Hello!"},
      ],
  )
  ```

  ```typescript TypeScript theme={null}
  import OpenAI from "openai";
  import { Client } from "langsmith";
  import { wrapOpenAI } from "langsmith/wrappers";

  const langsmithClient = new Client({
      hideInputs: (inputs) => ({}),
      hideOutputs: (outputs) => ({}),
  });

  // The trace produced will have its metadata present, but the inputs will be hidden
  const filteredOAIClient = wrapOpenAI(new OpenAI(), {
      client: langsmithClient,
  });
  await filteredOAIClient.chat.completions.create({
      model: "gpt-4o-mini",
      messages: [
          { role: "system", content: "You are a helpful assistant." },
          { role: "user", content: "Hello!" },
      ],
  });

  const openaiClient = wrapOpenAI(new OpenAI());
  // The trace produced will not have hidden inputs and outputs
  await openaiClient.chat.completions.create({
      model: "gpt-4o-mini",
      messages: [
          { role: "system", content: "You are a helpful assistant." },
          { role: "user", content: "Hello!" },
      ],
  });
  ```
</CodeGroup>

## Rule-based masking of inputs and outputs

<Info>
  This feature is available in the following LangSmith SDK versions:

  * Python: 0.1.81 and above
  * TypeScript: 0.1.33 and above
</Info>

To mask specific data in inputs and outputs, you can use the `create_anonymizer` / `createAnonymizer` function and pass the newly created anonymizer when instantiating the client. The anonymizer can be either constructed from a list of regex patterns and the replacement values or from a function that accepts and returns a string value.

The anonymizer will be skipped for inputs if `LANGSMITH_HIDE_INPUTS = true`. Same applies for outputs if `LANGSMITH_HIDE_OUTPUTS = true`.

However, if inputs or outputs are to be sent to client, the `anonymizer` method will take precedence over functions found in `hide_inputs` and `hide_outputs`. By default, the `create_anonymizer` will only look at maximum of 10 nesting levels deep, which can be configured via the `max_depth` parameter.

<CodeGroup>
  ```python Python theme={null}
  from langsmith.anonymizer import create_anonymizer
  from langsmith import Client, traceable
  import re

  # create anonymizer from list of regex patterns and replacement values
  anonymizer = create_anonymizer([
      { "pattern": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}", "replace": "<email-address>" },
      { "pattern": r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}", "replace": "<UUID>" }
  ])

  # or create anonymizer from a function
  email_pattern = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}")
  uuid_pattern = re.compile(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")
  anonymizer = create_anonymizer(
      lambda text: email_pattern.sub("<email-address>", uuid_pattern.sub("<UUID>", text))
  )

  client = Client(anonymizer=anonymizer)

  @traceable(client=client)
  def main(inputs: dict) -> dict:
      ...
  ```

  ```typescript TypeScript theme={null}
  import { createAnonymizer } from "langsmith/anonymizer"
  import { traceable } from "langsmith/traceable"
  import { Client } from "langsmith"

  // create anonymizer from list of regex patterns and replacement values
  const anonymizer = createAnonymizer([
      { pattern: /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}/g, replace: "<email>" },
      { pattern: /[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}/g, replace: "<uuid>" }
  ])

  // or create anonymizer from a function
  const anonymizer = createAnonymizer((value) => value.replace("...", "<value>"))

  const client = new Client({ anonymizer })

  const main = traceable(async (inputs: any) => {
      // ...
  }, { client })
  ```
</CodeGroup>

Please note, that using the anonymizer might incur a performance hit with complex regular expressions or large payloads, as the anonymizer serializes the payload to JSON before processing.

<Note>
  Improving the performance of `anonymizer` API is on our roadmap! If you are encountering performance issues, please contact support via [support.langchain.com](https://support.langchain.com).
</Note>

<img src="https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/hide-inputs-outputs.png?fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=ac9ba9a6729029a7fa38da03e1466a1a" alt="Hide inputs outputs" data-og-width="1708" width="1708" data-og-height="717" height="717" data-path="langsmith/images/hide-inputs-outputs.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/hide-inputs-outputs.png?w=280&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=7ded12c0345f47d55e9802083c5032d0 280w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/hide-inputs-outputs.png?w=560&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=8cbe74d09660d8c65e8a75dd78cdb24e 560w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/hide-inputs-outputs.png?w=840&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=8cb8c0b5c926e46522b9539b0262ee7a 840w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/hide-inputs-outputs.png?w=1100&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=9b8ef244796fad943ec76b0aa5733f80 1100w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/hide-inputs-outputs.png?w=1650&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=87f35d63f42f05c49a220d5b8a87787a 1650w, https://mintcdn.com/langchain-5e9cc07a/0B2PFrFBMRWNccee/langsmith/images/hide-inputs-outputs.png?w=2500&fit=max&auto=format&n=0B2PFrFBMRWNccee&q=85&s=5173e30032c065646c13e9b9c6a95fb5 2500w" />

Older versions of LangSmith SDKs can use the `hide_inputs` and `hide_outputs` parameters to achieve the same effect. You can also use these parameters to process the inputs and outputs more efficiently as well.

<CodeGroup>
  ```python Python theme={null}
  import re
  from langsmith import Client, traceable

  # Define the regex patterns for email addresses and UUIDs
  EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}"
  UUID_REGEX = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"

  def replace_sensitive_data(data, depth=10):
      if depth == 0:
          return data
      if isinstance(data, dict):
          return {k: replace_sensitive_data(v, depth-1) for k, v in data.items()}
      elif isinstance(data, list):
          return [replace_sensitive_data(item, depth-1) for item in data]
      elif isinstance(data, str):
          data = re.sub(EMAIL_REGEX, "<email-address>", data)
          data = re.sub(UUID_REGEX, "<UUID>", data)
          return data
      else:
          return data

  client = Client(
      hide_inputs=lambda inputs: replace_sensitive_data(inputs),
      hide_outputs=lambda outputs: replace_sensitive_data(outputs)
  )

  inputs = {"role": "user", "content": "Hello! My email is user@example.com and my ID is 123e4567-e89b-12d3-a456-426614174000."}
  outputs = {"role": "assistant", "content": "Hi! I've noted your email as user@example.com and your ID as 123e4567-e89b-12d3-a456-426614174000."}

  @traceable(client=client)
  def child(inputs: dict) -> dict:
      return outputs

  @traceable(client=client)
  def parent(inputs: dict) -> dict:
      child_outputs = child(inputs)
      return child_outputs

  parent(inputs)
  ```

  ```typescript TypeScript theme={null}
  import { Client } from "langsmith";
  import { traceable } from "langsmith/traceable";

  // Define the regex patterns for email addresses and UUIDs
  const EMAIL_REGEX = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}/g;
  const UUID_REGEX = /[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}/g;

  function replaceSensitiveData(data: any, depth: number = 10): any {
      if (depth === 0) return data;
      if (typeof data === "object" && !Array.isArray(data)) {
          const result: Record<string, any> = {};
          for (const [key, value] of Object.entries(data)) {
              result[key] = replaceSensitiveData(value, depth - 1);
          }
          return result;
      } else if (Array.isArray(data)) {
          return data.map(item => replaceSensitiveData(item, depth - 1));
      } else if (typeof data === "string") {
          return data.replace(EMAIL_REGEX, "<email-address>").replace(UUID_REGEX, "<UUID>");
      } else {
          return data;
      }
  }

  const langsmithClient = new Client({
      hideInputs: (inputs) => replaceSensitiveData(inputs),
      hideOutputs: (outputs) => replaceSensitiveData(outputs)
  });

  const inputs = {
      role: "user",
      content: "Hello! My email is user@example.com and my ID is 123e4567-e89b-12d3-a456-426614174000."
  };
  const outputs = {
      role: "assistant",
      content: "Hi! I've noted your email as <email-address> and your ID as <UUID>."
  };

  const child = traceable(async (inputs: any) => {
      return outputs;
  }, { name: "child", client: langsmithClient });

  const parent = traceable(async (inputs: any) => {
      const childOutputs = await child(inputs);
      return childOutputs;
  }, { name: "parent", client: langsmithClient });

  await parent(inputs);
  ```
</CodeGroup>

## Processing Inputs & Outputs for a Single Function

<Info>
  The `process_outputs` parameter is available in LangSmith SDK version 0.1.98 and above for Python.
</Info>

In addition to client-level input and output processing, LangSmith provides function-level processing through the `process_inputs` and `process_outputs` parameters of the `@traceable` decorator.

These parameters accept functions that allow you to transform the inputs and outputs of a specific function before they are logged to LangSmith. This is useful for reducing payload size, removing sensitive information, or customizing how an object should be serialized and represented in LangSmith for a particular function.

Here's an example of how to use `process_inputs` and `process_outputs`:

```python  theme={null}
from langsmith import traceable

def process_inputs(inputs: dict) -> dict:
    # inputs is a dictionary where keys are argument names and values are the provided arguments
    # Return a new dictionary with processed inputs
    return {
        "processed_key": inputs.get("my_cool_key", "default"),
        "length": len(inputs.get("my_cool_key", ""))
    }

def process_outputs(output: Any) -> dict:
    # output is the direct return value of the function
    # Transform the output into a dictionary
    # In this case, "output" will be an integer
    return {"processed_output": str(output)}

@traceable(process_inputs=process_inputs, process_outputs=process_outputs)
def my_function(my_cool_key: str) -> int:
    # Function implementation
    return len(my_cool_key)

result = my_function("example")
```

In this example, `process_inputs` creates a new dictionary with processed input data, and `process_outputs` transforms the output into a specific format before logging to LangSmith.

<Warning>
  It's recommended to avoid mutating the source objects in the processor functions. Instead, create and return new objects with the processed data.
</Warning>

For asynchronous functions, the usage is similar:

```python  theme={null}
@traceable(process_inputs=process_inputs, process_outputs=process_outputs)
async def async_function(key: str) -> int:
    # Async implementation
    return len(key)
```

These function-level processors take precedence over client-level processors (`hide_inputs` and `hide_outputs`) when both are defined.

## Quick starts

You can combine rule-based masking with various anonymizers to scrub sensitive information from inputs and outputs. In this how-to-guide, we'll cover working with regex, Microsoft Presidio, and Amazon Comprehend.

### Regex

<Info>
  The implementation below is not exhaustive and may miss some formats or edge cases. Test any implementation thoroughly before using it in production.
</Info>

You can use regex to mask inputs and outputs before they are sent to LangSmith. The implementation below masks email addresses, phone numbers, full names, credit card numbers, and SSNs.

```python  theme={null}
import re
import openai
from langsmith import Client
from langsmith.wrappers import wrap_openai

# Define regex patterns for various PII
SSN_PATTERN = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')
CREDIT_CARD_PATTERN = re.compile(r'\b(?:\d[ -]*?){13,16}\b')
EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')
PHONE_PATTERN = re.compile(r'\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b')
FULL_NAME_PATTERN = re.compile(r'\b([A-Z][a-z]*\s[A-Z][a-z]*)\b')

def regex_anonymize(text):
    """
    Anonymize sensitive information in the text using regex patterns.
    Args:
        text (str): The input text to be anonymized.
    Returns:
        str: The anonymized text.
    """
    # Replace sensitive information with placeholders
    text = SSN_PATTERN.sub('[REDACTED SSN]', text)
    text = CREDIT_CARD_PATTERN.sub('[REDACTED CREDIT CARD]', text)
    text = EMAIL_PATTERN.sub('[REDACTED EMAIL]', text)
    text = PHONE_PATTERN.sub('[REDACTED PHONE]', text)
    text = FULL_NAME_PATTERN.sub('[REDACTED NAME]', text)
    return text

def recursive_anonymize(data, depth=10):
    """
    Recursively traverse the data structure and anonymize sensitive information.
    Args:
        data (any): The input data to be anonymized.
        depth (int): The current recursion depth to prevent excessive recursion.
    Returns:
        any: The anonymized data.
    """
    if depth == 0:
        return data
    if isinstance(data, dict):
        anonymized_dict = {}
        for k, v in data.items():
            anonymized_value = recursive_anonymize(v, depth - 1)
            anonymized_dict[k] = anonymized_value
        return anonymized_dict
    elif isinstance(data, list):
        anonymized_list = []
        for item in data:
            anonymized_item = recursive_anonymize(item, depth - 1)
            anonymized_list.append(anonymized_item)
        return anonymized_list
    elif isinstance(data, str):
        anonymized_data = regex_anonymize(data)
        return anonymized_data
    else:
        return data

openai_client = wrap_openai(openai.Client())

# Initialize the LangSmith client with the anonymization functions
langsmith_client = Client(
    hide_inputs=recursive_anonymize, hide_outputs=recursive_anonymize
)

# The trace produced will have its metadata present, but the inputs and outputs will be anonymized
response_with_anonymization = openai_client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "My name is John Doe, my SSN is 123-45-6789, my credit card number is 4111 1111 1111 1111, my email is john.doe@example.com, and my phone number is (123) 456-7890."},
    ],
    langsmith_extra={"client": langsmith_client},
)

# The trace produced will not have anonymized inputs and outputs
response_without_anonymization = openai_client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "My name is John Doe, my SSN is 123-45-6789, my credit card number is 4111 1111 1111 1111, my email is john.doe@example.com, and my phone number is (123) 456-7890."},
    ],
)
```

The anonymized run will look like this in LangSmith: <img src="https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/regex-anonymized.png?fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=d42154587a9440675d2d506e1124b3fe" alt="Anonymized run" data-og-width="3178" width="3178" data-og-height="1836" height="1836" data-path="langsmith/images/regex-anonymized.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/regex-anonymized.png?w=280&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=0d0da550b34ec564879292413f36b492 280w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/regex-anonymized.png?w=560&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=3160769f89669b892d97ce42b69d2e9b 560w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/regex-anonymized.png?w=840&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=22d315f029d39b4b2094551077455399 840w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/regex-anonymized.png?w=1100&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=3a949b36dd27bc4491177bb6020df5f9 1100w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/regex-anonymized.png?w=1650&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=101541bc73fff2c554e9922107119837 1650w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/regex-anonymized.png?w=2500&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=38ff424147bb73093b40d7a87767f41f 2500w" />

The non-anonymized run will look like this in LangSmith: <img src="https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/regex-not-anonymized.png?fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=98da1cf86195ebb3be2119cddbf1ae0d" alt="Non-anonymized run" data-og-width="3176" width="3176" data-og-height="1830" height="1830" data-path="langsmith/images/regex-not-anonymized.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/regex-not-anonymized.png?w=280&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=871939d7d51881a70cb8d9d6334d47cb 280w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/regex-not-anonymized.png?w=560&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=00c968ee9e50c1588e2dae1bc157e26c 560w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/regex-not-anonymized.png?w=840&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=b37c8e4de393f885634c24407bb26bbe 840w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/regex-not-anonymized.png?w=1100&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=90800846fe864309521405f18d918d76 1100w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/regex-not-anonymized.png?w=1650&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=f2b6161b2bbb45fcb3b1a02b55368fca 1650w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/regex-not-anonymized.png?w=2500&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=c01f709dba7c6ebbf3e28c2cdc94c2cc 2500w" />

### Microsoft Presidio

<Info>
  The implementation below provides a general example of how to anonymize sensitive information in messages exchanged between a user and an LLM. It is not exhaustive and does not account for all cases. Test any implementation thoroughly before using it in production.
</Info>

Microsoft Presidio is a data protection and de-identification SDK. The implementation below uses Presidio to anonymize inputs and outputs before they are sent to LangSmith. For up to date information, please refer to Presidio's [official documentation](https://microsoft.github.io/presidio/).

To use Presidio and its spaCy model, install the following:

<CodeGroup>
  ```bash pip theme={null}
  pip install presidio-analyzer
  pip install presidio-anonymizer
  python -m spacy download en_core_web_lg
  ```

  ```bash uv theme={null}
  uv add presidio-analyzer
  uv add presidio-anonymizer
  python -m spacy download en_core_web_lg
  ```
</CodeGroup>

Also, install OpenAI:

<CodeGroup>
  ```bash pip theme={null}
  pip install openai
  ```

  ```bash uv theme={null}
  uv add openai
  ```
</CodeGroup>

```python  theme={null}
import openai
from langsmith import Client
from langsmith.wrappers import wrap_openai
from presidio_anonymizer import AnonymizerEngine
from presidio_analyzer import AnalyzerEngine

anonymizer = AnonymizerEngine()
analyzer = AnalyzerEngine()

def presidio_anonymize(data):
    """
    Anonymize sensitive information sent by the user or returned by the model.
    Args:
        data (any): The data to be anonymized.
    Returns:
        any: The anonymized data.
    """
    message_list = (
        data.get('messages') or [data.get('choices', [{}])[0].get('message')]
    )
    if not message_list or not all(isinstance(msg, dict) and msg for msg in message_list):
        return data

    for message in message_list:
        content = message.get('content', '')
        if not content.strip():
            print("Empty content detected. Skipping anonymization.")
            continue

        results = analyzer.analyze(
            text=content,
            entities=["PERSON", "PHONE_NUMBER", "EMAIL_ADDRESS", "US_SSN"],
            language='en'
        )
        anonymized_result = anonymizer.anonymize(
            text=content,
            analyzer_results=results
        )
        message['content'] = anonymized_result.text

    return data

openai_client = wrap_openai(openai.Client())

# initialize the langsmith client with the anonymization functions
langsmith_client = Client(
  hide_inputs=presidio_anonymize, hide_outputs=presidio_anonymize
)

# The trace produced will have its metadata present, but the inputs and outputs will be anonymized
response_with_anonymization = openai_client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "My name is Slim Shady, call me at 313-666-7440 or email me at real.slim.shady@gmail.com"},
  ],
  langsmith_extra={"client": langsmith_client},
)

# The trace produced will not have anonymized inputs and outputs
response_without_anonymization = openai_client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "My name is Slim Shady, call me at 313-666-7440 or email me at real.slim.shady@gmail.com"},
  ],
)
```

The anonymized run will look like this in LangSmith: <img src="https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/presidio-anonymized.png?fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=100d741a3fb32d0c1f251186f57568ac" alt="Anonymized run" data-og-width="3174" width="3174" data-og-height="1830" height="1830" data-path="langsmith/images/presidio-anonymized.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/presidio-anonymized.png?w=280&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=3f2f159c048e309e5b78e85ca4dfa75f 280w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/presidio-anonymized.png?w=560&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=e78dc405ee0019523ffb150dc0b56eae 560w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/presidio-anonymized.png?w=840&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=edefbf42e4749b8d26fca7e87b627659 840w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/presidio-anonymized.png?w=1100&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=69a3b82526f4a31ce449322c100ece2f 1100w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/presidio-anonymized.png?w=1650&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=9de36ba2545c911c9908b5dbbb8b30c3 1650w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/presidio-anonymized.png?w=2500&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=ca15dafdf66dd0e7dd13eb898d76ee7f 2500w" />

The non-anonymized run will look like this in LangSmith: <img src="https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/presidio-not-anonymized.png?fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=2ef3e46591877ffdf23c0c240ec389c2" alt="Non-anonymized run" data-og-width="3176" width="3176" data-og-height="1684" height="1684" data-path="langsmith/images/presidio-not-anonymized.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/presidio-not-anonymized.png?w=280&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=7792f325a64b7f64ff78db535b275c61 280w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/presidio-not-anonymized.png?w=560&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=85d81aa5511eae3fc961b97a0e857e3c 560w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/presidio-not-anonymized.png?w=840&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=be4fceb44186435053c2e7eea51ceba5 840w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/presidio-not-anonymized.png?w=1100&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=6a29ce75afa17e6a7c09fb591e17aa97 1100w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/presidio-not-anonymized.png?w=1650&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=4acda7489155c3a97d732b6788243fa9 1650w, https://mintcdn.com/langchain-5e9cc07a/H9jA2WRyA-MV4-H0/langsmith/images/presidio-not-anonymized.png?w=2500&fit=max&auto=format&n=H9jA2WRyA-MV4-H0&q=85&s=a5f962c936c4dfe97bdb31fb0b51c445 2500w" />

### Amazon Comprehend

<Info>
  The implementation below provides a general example of how to anonymize sensitive information in messages exchanged between a user and an LLM. It is not exhaustive and does not account for all cases. Test any implementation thoroughly before using it in production.
</Info>

Comprehend is a natural language processing service that can detect personally identifiable information. The implementation below uses Comprehend to anonymize inputs and outputs before they are sent to LangSmith. For up to date information, please refer to Comprehend's [official documentation](https://docs.aws.amazon.com/comprehend/latest/APIReference/API_DetectPiiEntities.html).

To use Comprehend, install [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html):

<CodeGroup>
  ```bash pip theme={null}
  pip install boto3
  ```

  ```bash uv theme={null}
  uv add boto3
  ```
</CodeGroup>

Also, install OpenAI:

<CodeGroup>
  ```bash pip theme={null}
  pip install openai
  ```

  ```bash uv theme={null}
  uv add openai
  ```
</CodeGroup>

You will need to set up credentials in AWS and authenticate using the AWS CLI. Follow the instructions [here](https://docs.aws.amazon.com/comprehend/latest/dg/setting-up.html).

```python  theme={null}
import openai
import boto3
from langsmith import Client
from langsmith.wrappers import wrap_openai

comprehend = boto3.client('comprehend', region_name='us-east-1')

def redact_pii_entities(text, entities):
    """
    Redact PII entities in the text based on the detected entities.
    Args:
        text (str): The original text containing PII.
        entities (list): A list of detected PII entities.
    Returns:
        str: The text with PII entities redacted.
    """
    sorted_entities = sorted(entities, key=lambda x: x['BeginOffset'], reverse=True)
    redacted_text = text
    for entity in sorted_entities:
        begin = entity['BeginOffset']
        end = entity['EndOffset']
        entity_type = entity['Type']
        # Define the redaction placeholder based on entity type
        placeholder = f"[{entity_type}]"
        # Replace the PII in the text with the placeholder
        redacted_text = redacted_text[:begin] + placeholder + redacted_text[end:]
    return redacted_text

def detect_pii(text):
    """
    Detect PII entities in the given text using AWS Comprehend.
    Args:
        text (str): The text to analyze.
    Returns:
        list: A list of detected PII entities.
    """
    try:
        response = comprehend.detect_pii_entities(
            Text=text,
            LanguageCode='en',
        )
        entities = response.get('Entities', [])
        return entities
    except Exception as e:
        print(f"Error detecting PII: {e}")
        return []

def comprehend_anonymize(data):
    """
    Anonymize sensitive information sent by the user or returned by the model.
    Args:
        data (any): The input data to be anonymized.
    Returns:
        any: The anonymized data.
    """
    message_list = (
        data.get('messages') or [data.get('choices', [{}])[0].get('message')]
    )
    if not message_list or not all(isinstance(msg, dict) and msg for msg in message_list):
        return data

    for message in message_list:
        content = message.get('content', '')
        if not content.strip():
            print("Empty content detected. Skipping anonymization.")
            continue

        entities = detect_pii(content)
        if entities:
            anonymized_text = redact_pii_entities(content, entities)
            message['content'] = anonymized_text
        else:
            print("No PII detected. Content remains unchanged.")

    return data

openai_client = wrap_openai(openai.Client())

# initialize the langsmith client with the anonymization functions
langsmith_client = Client(
  hide_inputs=comprehend_anonymize, hide_outputs=comprehend_anonymize
)

# The trace produced will have its metadata present, but the inputs and outputs will be anonymized
response_with_anonymization = openai_client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "My name is Slim Shady, call me at 313-666-7440 or email me at real.slim.shady@gmail.com"},
  ],
  langsmith_extra={"client": langsmith_client},
)

# The trace produced will not have anonymized inputs and outputs
response_without_anonymization = openai_client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "My name is Slim Shady, call me at 313-666-7440 or email me at real.slim.shady@gmail.com"},
  ],
)
```

The anonymized run will look like this in LangSmith: <img src="https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/aws-comprehend-anonymized.png?fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=cea182d95ef02e614a6f1bbd7e3a2657" alt="Anonymized run" data-og-width="3180" width="3180" data-og-height="1616" height="1616" data-path="langsmith/images/aws-comprehend-anonymized.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/aws-comprehend-anonymized.png?w=280&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=d3c5a665e2ee726ad6dacf89ade8daea 280w, https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/aws-comprehend-anonymized.png?w=560&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=77bccbc4ba3bcde3bd771866e44ce535 560w, https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/aws-comprehend-anonymized.png?w=840&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=527a6563672cb66d28bf7ae3272c0c5e 840w, https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/aws-comprehend-anonymized.png?w=1100&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=108afc60434f26addae7525049850aac 1100w, https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/aws-comprehend-anonymized.png?w=1650&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=e0216a9846c6e7ff041bcccdb23ce98a 1650w, https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/aws-comprehend-anonymized.png?w=2500&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=cd4119b7e81420f54db86cad58db5426 2500w" />

The non-anonymized run will look like this in LangSmith: <img src="https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/aws-comprehend-not-anonymized.png?fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=ec61e5c8d78268b5b34b6b9c184871cc" alt="Non-anonymized run" data-og-width="3180" width="3180" data-og-height="1648" height="1648" data-path="langsmith/images/aws-comprehend-not-anonymized.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/aws-comprehend-not-anonymized.png?w=280&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=34ad34770c55fcea58caee9dfa7f856e 280w, https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/aws-comprehend-not-anonymized.png?w=560&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=089c86d993f3dc8a5998bfc2adc8a75d 560w, https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/aws-comprehend-not-anonymized.png?w=840&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=7fcd25c38a94d366762cf74629dd07c7 840w, https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/aws-comprehend-not-anonymized.png?w=1100&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=b82a670a0e25bc656475cccea5d1a50d 1100w, https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/aws-comprehend-not-anonymized.png?w=1650&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=c422ed47282a844783713e5dc291a7b0 1650w, https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/aws-comprehend-not-anonymized.png?w=2500&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=a5a62a5bd72b2cf49c9495d14d3059fa 2500w" />

***

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/mask-inputs-outputs.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.langchain.com/llms.txt