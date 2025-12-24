# Configure threads

Many LLM applications have a chatbot-like interface in which the user and the LLM application engage in a multi-turn conversation. In order to track these conversations, you can use the `Threads` feature in LangSmith.

## Group traces into threads

A `Thread` is a sequence of traces representing a single conversation. Each response is represented as its own trace, but these traces are linked together by being part of the same thread.

To associate traces together, you need to pass in a special `metadata` key where the value is the unique identifier for that thread. The key name should be one of:

* `session_id`
* `thread_id`
* `conversation_id`.

The value can be any string you want, but we recommend using UUIDs, such as `f47ac10b-58cc-4372-a567-0e02b2c3d479`. Check out [this guide](./add-metadata-tags) for instructions on adding metadata to your traces.

### Example

This example demonstrates how to log and retrieve conversation history using a structured message format to maintain long-running chats.

<CodeGroup>
  ```python Python theme={null}
  import os
  from typing import List, Dict, Any, Optional

  import openai
  from langsmith import traceable, Client
  import langsmith as ls
  from langsmith.wrappers import wrap_openai

  # Initialize clients
  client = wrap_openai(openai.Client())
  langsmith_client = Client()

  # Configuration
  LANGSMITH_PROJECT = "project-with-threads"
  THREAD_ID = "thread-id-1"
  langsmith_extra={"project_name": LANGSMITH_PROJECT, "metadata":{"session_id": THREAD_ID}}

  # gets a history of all LLM calls in the thread to construct conversation history
  def get_thread_history(thread_id: str, project_name: str):
      # Filter runs by the specific thread and project
      filter_string = f'and(in(metadata_key, ["session_id","conversation_id","thread_id"]), eq(metadata_value, "{thread_id}"))'
      # Only grab the LLM runs
      runs = [r for r in langsmith_client.list_runs(project_name=project_name, filter=filter_string, run_type="llm")]

      # Sort by start time to get the most recent interaction
      runs = sorted(runs, key=lambda run: run.start_time, reverse=True)

      # Reconstruct the conversation state
      latest_run = runs[0]
      return latest_run.inputs['messages'] + [latest_run.outputs['choices'][0]['message']]


  @traceable(name="Chat Bot")
  def chat_pipeline(messages: list, get_chat_history: bool = False):
      # Whether to continue an existing thread or start a new one
      if get_chat_history:
          run_tree = ls.get_current_run_tree()
          # Get existing conversation history and append new messages
          history_messages = get_thread_history(run_tree.extra["metadata"]["session_id"], run_tree.session_name)
          all_messages = history_messages + messages
          # Include the complete conversation in the input for tracing
          input_messages = all_messages
      else:
          all_messages = messages
          input_messages = messages

      # Invoke the model
      chat_completion = client.chat.completions.create(
          model="gpt-4o-mini", messages=all_messages
      )

      # Return the complete conversation including input and response
      response_message = chat_completion.choices[0].message
      return {
          "messages": input_messages + [response_message]
      }

  # Format message
  messages = [
      {
          "content": "Hi, my name is Sally",
          "role": "user"
      }
  ]
  get_chat_history = False

  # Call the chat pipeline
  result = chat_pipeline(messages, get_chat_history, langsmith_extra=langsmith_extra)
  ```

  ```typescript TypeScript theme={null}
  import 'dotenv/config';
  import OpenAI from 'openai';
  import { traceable, getCurrentRunTree } from 'langsmith/traceable';
  import { Client } from 'langsmith';
  import { wrapOpenAI } from 'langsmith/wrappers';

  // Initialize clients
  const openai = new OpenAI();
  const client = wrapOpenAI(openai);
  const langsmithClient = new Client();

  // Configuration
  const LANGSMITH_PROJECT = "project-with-threads";
  const THREAD_ID = "thread-id-1";
  const langsmithExtra = {
    project_name: LANGSMITH_PROJECT,
    metadata: { session_id: THREAD_ID }
  };

  // Message type definition
  interface Message {
    role: 'user' | 'assistant' | 'system';
    content: string;
  }

  interface ChatResponse {
    messages: Message[];
  }

  interface ChatInput {
    get_chat_history: boolean;
    messages: Message[];
  }

  // gets a history of all LLM calls in the thread to construct conversation history
  async function getThreadHistory(threadId: string, projectName: string): Promise<Message[]> {
    // Filter runs by the specific thread and project
    const filterString = `and(in(metadata_key, ["session_id","conversation_id","thread_id"]), eq(metadata_value, "${threadId}"))`;

    // Only grab the LLM runs
    const runs: any[] = [];
    for await (const run of langsmithClient.listRuns({
      projectName: projectName,
      filter: filterString,
      runType: "llm"
    })) {
      if (run.run_type === "llm") {
        runs.push(run);
      }
    }

    // Sort by start time to get the most recent interaction
    runs.sort((a: any, b: any) => new Date(b.start_time).getTime() - new Date(a.start_time).getTime());

    // Check if we have any runs
    if (runs.length === 0) {
      return [];
    }

    // The current state of the conversation
    const latestRun = runs[0];
    const inputMessages = latestRun.inputs.messages as Message[];
    const outputMessage = latestRun.outputs.choices[0].message as Message;

    return [...inputMessages, outputMessage];
  }

  // Updated chat pipeline that accepts JSON input format
  const chatPipeline = traceable(async (input: ChatInput): Promise<ChatResponse> => {
    const { messages, get_chat_history } = input;
    let allMessages: Message[];
    let inputMessages: Message[];

    // Whether to continue an existing thread or start a new one
    if (get_chat_history) {
      const runTree = getCurrentRunTree();
      // Get existing conversation history and append new messages
      const sessionId = runTree.extra?.metadata?.session_id || THREAD_ID;
      const historyMessages = await getThreadHistory(
        sessionId,
        runTree.project_name
      );
      allMessages = historyMessages.concat(messages);
      // Include the complete conversation in the input for tracing
      inputMessages = allMessages;
    } else {
      allMessages = messages;
      inputMessages = messages;
    }

    // Invoke the model
    const chatCompletion = await client.chat.completions.create({
      model: "gpt-4o-mini",
      messages: allMessages
    });

    // Return the complete conversation including input and response
    const responseMessage = chatCompletion.choices[0].message as Message;
    return {
      messages: [...inputMessages, responseMessage]
    };
  }, { name: "Chat Bot" });

  // Example input in the requested JSON format
  const input: ChatInput = {
    get_chat_history: false,
    messages: [
      {
        content: "Hi, my name is Sally",
        role: "user"
      }
    ]
  };

  // Call the chat pipeline
  const result = await chatPipeline(input);
  ```
</CodeGroup>

After waiting a few seconds, you can make the following calls to continue the conversation. By passing `get_chat_history=True,`/`getChatHistory: true`,
you can continue the conversation from where it left off. This means that the LLM will receive the entire message history and respond to it,
instead of just responding to the latest message.

<CodeGroup>
  ```python Python theme={null}
  # Continue the conversation.
  messages = [
      {
          "content": "What is my name?",
          "role": "user"
      }
  ]
  get_chat_history = True

  chat_pipeline(messages, get_chat_history, langsmith_extra=langsmith_extra)
  ```

  ```typescript TypeScript theme={null}
  // Continue the conversation.
  const input: ChatInput = {
    get_chat_history: true,
    messages: [
      {
        content: "What is my name?",
        role: "user"
      }
    ]
  };

  await chatPipeline(input);
  ```
</CodeGroup>

Keep the conversation going. Since past messages are included, the LLM will remember the conversation.

<CodeGroup>
  ```python Python theme={null}
  # Continue the conversation.
  messages = [
      {
          "content": "What was the first message I sent you?",
          "role": "user"
      }
  ]
  get_chat_history = True

  chat_pipeline(messages, get_chat_history, langsmith_extra=langsmith_extra)
  ```

  ```typescript TypeScript theme={null}
  // Continue the conversation.
  const input: ChatInput = {
    get_chat_history: true,
    messages: [
      {
        content: "What was the first message I sent you?",
        role: "user"
      }
    ]
  };

  await chatPipeline(input);
  ```
</CodeGroup>

## View threads

You can view threads by clicking on the **Threads** tab in any project details page. You will then see a list of all threads, sorted by the most recent activity.

<div style={{ textAlign: 'center' }}>
  <img className="block dark:hidden" src="https://mintcdn.com/langchain-5e9cc07a/zLS2qlRr5r04zU3G/langsmith/images/threads-tab-light.png?fit=max&auto=format&n=zLS2qlRr5r04zU3G&q=85&s=45e1c11dce5eaaaf0cf8ae01057647b7" alt="LangSmith UI showing the threads table." data-og-width="1277" width="1277" data-og-height="762" height="762" data-path="langsmith/images/threads-tab-light.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/zLS2qlRr5r04zU3G/langsmith/images/threads-tab-light.png?w=280&fit=max&auto=format&n=zLS2qlRr5r04zU3G&q=85&s=cb5d147a58a3a9ecbb1c550a3308e871 280w, https://mintcdn.com/langchain-5e9cc07a/zLS2qlRr5r04zU3G/langsmith/images/threads-tab-light.png?w=560&fit=max&auto=format&n=zLS2qlRr5r04zU3G&q=85&s=a7cc6f9c8def1e15cc9c93382b82473d 560w, https://mintcdn.com/langchain-5e9cc07a/zLS2qlRr5r04zU3G/langsmith/images/threads-tab-light.png?w=840&fit=max&auto=format&n=zLS2qlRr5r04zU3G&q=85&s=23013f31edf91e66da89e102cb6ea302 840w, https://mintcdn.com/langchain-5e9cc07a/zLS2qlRr5r04zU3G/langsmith/images/threads-tab-light.png?w=1100&fit=max&auto=format&n=zLS2qlRr5r04zU3G&q=85&s=1bfbd6daad34b699553a30d8f9663540 1100w, https://mintcdn.com/langchain-5e9cc07a/zLS2qlRr5r04zU3G/langsmith/images/threads-tab-light.png?w=1650&fit=max&auto=format&n=zLS2qlRr5r04zU3G&q=85&s=d3fc20ddbe02630ac98a0c336a39caa7 1650w, https://mintcdn.com/langchain-5e9cc07a/zLS2qlRr5r04zU3G/langsmith/images/threads-tab-light.png?w=2500&fit=max&auto=format&n=zLS2qlRr5r04zU3G&q=85&s=cfa17b6f006faef0a6f8537eedab6532 2500w" />

  <img className="hidden dark:block" src="https://mintcdn.com/langchain-5e9cc07a/zLS2qlRr5r04zU3G/langsmith/images/threads-tab-dark.png?fit=max&auto=format&n=zLS2qlRr5r04zU3G&q=85&s=b0ec4964ee49a3ead3a1e8042e406abc" alt="LangSmith UI showing the threads table." data-og-width="1275" width="1275" data-og-height="761" height="761" data-path="langsmith/images/threads-tab-dark.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/zLS2qlRr5r04zU3G/langsmith/images/threads-tab-dark.png?w=280&fit=max&auto=format&n=zLS2qlRr5r04zU3G&q=85&s=98750a8129e2e8283871c096a642f8b8 280w, https://mintcdn.com/langchain-5e9cc07a/zLS2qlRr5r04zU3G/langsmith/images/threads-tab-dark.png?w=560&fit=max&auto=format&n=zLS2qlRr5r04zU3G&q=85&s=4be143312bdd90ab8318da304c0c1e91 560w, https://mintcdn.com/langchain-5e9cc07a/zLS2qlRr5r04zU3G/langsmith/images/threads-tab-dark.png?w=840&fit=max&auto=format&n=zLS2qlRr5r04zU3G&q=85&s=c7ace4e000b6a1c925d32b78983fadca 840w, https://mintcdn.com/langchain-5e9cc07a/zLS2qlRr5r04zU3G/langsmith/images/threads-tab-dark.png?w=1100&fit=max&auto=format&n=zLS2qlRr5r04zU3G&q=85&s=9ece1b058745be1c3b2dcfffd9a9af58 1100w, https://mintcdn.com/langchain-5e9cc07a/zLS2qlRr5r04zU3G/langsmith/images/threads-tab-dark.png?w=1650&fit=max&auto=format&n=zLS2qlRr5r04zU3G&q=85&s=0ab63a1b906fe2a559cfb5772c95dc47 1650w, https://mintcdn.com/langchain-5e9cc07a/zLS2qlRr5r04zU3G/langsmith/images/threads-tab-dark.png?w=2500&fit=max&auto=format&n=zLS2qlRr5r04zU3G&q=85&s=6093b81ee1f92978880e74a9630f451d 2500w" />
</div>

<Callout type="info" icon="bird">
  Use **[Polly](/langsmith/polly)** in thread views to analyze conversation threads, understand user sentiment, identify pain points, and track whether issues were resolved.
</Callout>

### View a thread

You can then click into a particular thread. This will open the history for a particular thread.

<div style={{ textAlign: 'center' }}>
  <img className="block dark:hidden" src="https://mintcdn.com/langchain-5e9cc07a/zLS2qlRr5r04zU3G/langsmith/images/thread-overview-light.png?fit=max&auto=format&n=zLS2qlRr5r04zU3G&q=85&s=f7af4c3904073d5f58f28c656603ca19" alt="LangSmith UI showing the threads table." data-og-width="1273" width="1273" data-og-height="757" height="757" data-path="langsmith/images/thread-overview-light.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/zLS2qlRr5r04zU3G/langsmith/images/thread-overview-light.png?w=280&fit=max&auto=format&n=zLS2qlRr5r04zU3G&q=85&s=cd769088ab3ab2dae09982915f23772d 280w, https://mintcdn.com/langchain-5e9cc07a/zLS2qlRr5r04zU3G/langsmith/images/thread-overview-light.png?w=560&fit=max&auto=format&n=zLS2qlRr5r04zU3G&q=85&s=70ae6b5a6b8edb83ba3604d4c6e0262e 560w, https://mintcdn.com/langchain-5e9cc07a/zLS2qlRr5r04zU3G/langsmith/images/thread-overview-light.png?w=840&fit=max&auto=format&n=zLS2qlRr5r04zU3G&q=85&s=61d89d8077072221373490edac65363c 840w, https://mintcdn.com/langchain-5e9cc07a/zLS2qlRr5r04zU3G/langsmith/images/thread-overview-light.png?w=1100&fit=max&auto=format&n=zLS2qlRr5r04zU3G&q=85&s=ad8159fe12f056dbc561c612e3797b97 1100w, https://mintcdn.com/langchain-5e9cc07a/zLS2qlRr5r04zU3G/langsmith/images/thread-overview-light.png?w=1650&fit=max&auto=format&n=zLS2qlRr5r04zU3G&q=85&s=3611f7bcc95c45bcb91c093ca36ef348 1650w, https://mintcdn.com/langchain-5e9cc07a/zLS2qlRr5r04zU3G/langsmith/images/thread-overview-light.png?w=2500&fit=max&auto=format&n=zLS2qlRr5r04zU3G&q=85&s=1c0426d7e83562e1d76e079959bda186 2500w" />

  <img className="hidden dark:block" src="https://mintcdn.com/langchain-5e9cc07a/zLS2qlRr5r04zU3G/langsmith/images/thread-overview-dark.png?fit=max&auto=format&n=zLS2qlRr5r04zU3G&q=85&s=f738de4cac932ed2b8657e8f3b706b77" alt="LangSmith UI showing the threads table." data-og-width="1273" width="1273" data-og-height="753" height="753" data-path="langsmith/images/thread-overview-dark.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/zLS2qlRr5r04zU3G/langsmith/images/thread-overview-dark.png?w=280&fit=max&auto=format&n=zLS2qlRr5r04zU3G&q=85&s=9bc9dd49c63661dceb981899c5f0332b 280w, https://mintcdn.com/langchain-5e9cc07a/zLS2qlRr5r04zU3G/langsmith/images/thread-overview-dark.png?w=560&fit=max&auto=format&n=zLS2qlRr5r04zU3G&q=85&s=01713d47cf762f99be1a1143b01582e8 560w, https://mintcdn.com/langchain-5e9cc07a/zLS2qlRr5r04zU3G/langsmith/images/thread-overview-dark.png?w=840&fit=max&auto=format&n=zLS2qlRr5r04zU3G&q=85&s=cfc77e449d0ce27cdfa51b2f7c6ed655 840w, https://mintcdn.com/langchain-5e9cc07a/zLS2qlRr5r04zU3G/langsmith/images/thread-overview-dark.png?w=1100&fit=max&auto=format&n=zLS2qlRr5r04zU3G&q=85&s=d84f671a8f2c1207dbb98c72a37d1832 1100w, https://mintcdn.com/langchain-5e9cc07a/zLS2qlRr5r04zU3G/langsmith/images/thread-overview-dark.png?w=1650&fit=max&auto=format&n=zLS2qlRr5r04zU3G&q=85&s=d592bd4c8671b3d7f19a49471888a901 1650w, https://mintcdn.com/langchain-5e9cc07a/zLS2qlRr5r04zU3G/langsmith/images/thread-overview-dark.png?w=2500&fit=max&auto=format&n=zLS2qlRr5r04zU3G&q=85&s=2405eaef2af227dd5e5efac85fc9e623 2500w" />
</div>

Threads can be viewed in two different ways:

* [Thread overview](/langsmith/threads#thread-overview)
* [Trace view](/langsmith/threads#trace-view)

You can use the buttons at the top of the page to switch between the two views or use the keyboard shortcut `T` to toggle between the two views.

#### Thread overview

The thread overview page shows you a chatbot-like UI where you can see the inputs and outputs for each turn of the conversation. You can configure which fields in the inputs and outputs are displayed in the overview, or show multiple fields by clicking the **Configure** button.

The JSON path for the inputs and outputs supports negative indexing, so you can use `-1` to access the last element of an array. For example, `inputs.messages[-1].content` will access the last message in the `messages` array.

#### Trace view

The trace view here is similar to the trace view when looking at a single run, except that you have easy access to all the runs for each turn in the thread.

### View feedback

When viewing a thread, across the top of the page you will see a section called `Feedback`. This is where you can see the feedback for each of the runs that make up the thread. This feedback is aggregated, so if you evaluate each run of a thread for the same criteria, you will see the average score across all the runs displayed. You can also see [thread level feedback](/langsmith/online-evaluations#configure-multi-turn-online-evaluators) left here.

### Save thread level filter

Similar to saving filters at the project level, you can also save commonly used filters at the thread level. To save filters on the threads table, set a filter using the filters button and then click the **Save filter** button.

You can open up the trace or annotate the trace in a side panel by clicking on `Annotate` and `Open trace`, respectively.

***

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/threads.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.langchain.com/llms.txt