<!-- Source: https://docs.langchain.com/langsmith/configuration-cloud -->

This page describes how to create, configure, and manage [assistants](/langsmith/assistants). Assistants allow you to customize your [deployed](/langsmith/deployments) graph’s behavior through configuration—such as model selection, prompts, and tool availability—without changing the underlying graph code. You can work with the [SDK](https://reference.langchain.com/python/langsmith/deployment/sdk/) or in the [LangSmith UI](https://smith.langchain.com).



Understand assistant configuration

Assistants store _context_ values that customize graph behavior at runtime. You define a context schema in your graph code, then provide specific context values when creating an assistant via the [`context` parameter](https://reference.langchain.com/python/langsmith/deployment/sdk/#langgraph_sdk.client.AssistantsClient.create). Consider this example of a `call_model` node that reads the `model_name` from the context:

Python

JavaScript

Copy

    class ContextSchema(TypedDict):
        model_name: str

    builder = StateGraph(AgentState, context_schema=ContextSchema)

    def call_model(state, runtime: Runtime[ContextSchema]):
        messages = state["messages"]
        model = _get_model(runtime.context.get("model_name", "anthropic"))
        response = model.invoke(messages)
        return {"messages": [response]}

When you create an assistant, you provide specific values for these configuration fields. The assistant stores this configuration and applies it whenever the graph runs. For more information on configuration in [LangGraph](/oss/python/langgraph/overview), refer to the [runtime context documentation](/oss/python/langgraph/graph-api#runtime-context). **Select SDK or UI for your workflow:**

  * SDK

  * UI



Create an assistant

Use the [AssistantsClient.create](https://reference.langchain.com/python/langsmith/deployment/sdk/#langgraph_sdk.client.AssistantsClient.create) method to create a new assistant. This method requires:

  * **Graph ID** : The name of the deployed graph this assistant will use (e.g., `"agent"`).
  * **Context** : Configuration values matching your graph’s context schema.
  * **Name** : A descriptive name for the assistant.

The following example creates an assistant with `model_name` set to `openai`:

Python

JavaScript

cURL

Copy

    from langgraph_sdk import get_client

    # Initialize the client with your deployment URL
    client = get_client(url=<DEPLOYMENT_URL>)

    # Create an assistant for the "agent" graph
    # The first parameter is the graph ID (also called graph name)
    openai_assistant = await client.assistants.create(
        "agent",  # Graph ID of the deployed graph
        context={"model_name": "openai"},
        name="Open AI Assistant"
    )

    print(openai_assistant)
    # Output includes the assistant_id (UUID) that uniquely identifies this assistant

**Response:** The API returns an assistant object containing:

  * `assistant_id`: A UUID that uniquely identifies this assistant
  * `graph_id`: The graph this assistant is configured for
  * `context`: The configuration values you provided
  * `name`, `metadata`, timestamps, and other fields

Copy

    {
      "assistant_id": "62e209ca-9154-432a-b9e9-2d75c7a9219b",
      "graph_id": "agent",
      "name": "Open AI Assistant",
      "context": {
        "model_name": "openai"
      },
      "metadata": {},
      "created_at": "2024-08-31T03:09:10.230718+00:00",
      "updated_at": "2024-08-31T03:09:10.230718+00:00"
    }

The `assistant_id` (a UUID like `"62e209ca-9154-432a-b9e9-2d75c7a9219b"`) uniquely identifies this assistant configuration. You’ll use this ID when running your graph to specify which configuration to apply.

**Graph ID vs Assistant ID** When creating an assistant, you specify a **graph ID** (graph name like `"agent"`). This returns an **assistant ID** (UUID like `"62e209ca..."`). You can use either when running your graph:

  * **Graph ID** (e.g., `"agent"`): Uses the default assistant for that graph
  * **Assistant ID** (UUID): Uses the specific assistant configuration

See [Use an assistant](#use-an-assistant) for examples.



Use an assistant

To use an assistant, pass its `assistant_id` when creating a run. The example below uses the assistant we created above:

Python

JavaScript

cURL

Copy

    # Create a thread for the conversation
    thread = await client.threads.create()

    # Prepare the input
    input = {"messages": [{"role": "user", "content": "who made you?"}]}

    # Run the graph using the assistant's configuration
    # Pass the assistant_id (UUID) as the second parameter
    async for event in client.runs.stream(
        thread["thread_id"],
        openai_assistant["assistant_id"],  # Assistant ID (UUID)
        input=input,
        stream_mode="updates",
    ):
        print(f"Receiving event of type: {event.event}")
        print(event.data)
        print("\n\n")

**Response:** The stream returns events as the graph executes with your assistant’s configuration:

Copy

    Receiving event of type: metadata
    {'run_id': '1ef6746e-5893-67b1-978a-0f1cd4060e16'}

    Receiving event of type: updates
    {'agent': {'messages': [{'content': 'I was created by OpenAI...', ...}]}}

**Using graph ID vs assistant ID** You can pass either a **graph ID** or **assistant ID** when running your graph:

Copy

    # Option 1: Use graph ID to get the default assistant
    client.runs.stream(thread_id, "agent", input=input)

    # Option 2: Use assistant ID (UUID) for a specific configuration
    client.runs.stream(thread_id, "62e209ca-9154-432a-b9e9-2d75c7a9219b", input=input)



Create a new version for your assistant

Use the [AssistantsClient.update](https://reference.langchain.com/python/langsmith/deployment/sdk/#langgraph_sdk.client.AssistantsClient.update) method to create a new version of an assistant.

**Updates require full configuration** You must provide the **entire** configuration when updating. The update endpoint creates new versions from scratch and does not merge with previous versions. Include all configuration fields you want to retain.

For example, to add a system prompt to the assistant:

Python

JavaScript

cURL

Copy

    # Update the assistant with a new configuration
    # IMPORTANT: Include ALL configuration fields, not just the ones you're changing
    openai_assistant_v2 = await client.assistants.update(
        openai_assistant["assistant_id"],  # Assistant ID (UUID)
        context={
              "model_name": "openai",  # Must include existing fields
              "system_prompt": "You are a mindful assistant!",  # New field
        },
    )

    # This creates version 2 and sets it as the active version
    # Future runs using this assistant_id will use version 2

The update creates a new version and automatically sets it as active. All future runs using this assistant ID will use the new configuration.



Use a previous assistant version

Use the `setLatest` method to change which version is active:

Python

JavaScript

cURL

Copy

    # Roll back to version 1 of the assistant
    await client.assistants.set_latest(
        openai_assistant['assistant_id'],  # Assistant ID (UUID)
        1  # Version number
    )

    # All future runs using this assistant_id will now use version 1

After changing the active version, all runs using this assistant ID will use the specified version’s configuration.



Create an assistant

You can create assistants from the [LangSmith UI](https://smith.langchain.com):

  1. Navigate to your deployment and select the **Assistants** tab.
  2. Click **\+ New assistant**.
  3. In the form that opens:
     * Select the graph this assistant is for.
     * Provide a name and description.
     * Configure the assistant using the configuration schema for that graph.
  4. Click **Create assistant**.

This will take you to [Studio](/langsmith/studio) where you can test the assistant. Return to the **Assistants** tab to see your newly created assistant in the table.



Use an assistant

To use an assistant in the LangSmith UI:

  1. Navigate to your deployment and select the **Assistants** tab.
  2. Find the assistant you want to use.
  3. Click **Studio** for that assistant.

This opens [Studio](/langsmith/studio) with the selected assistant. When you submit an input (in **Graph** or **Chat** mode), the assistant’s configuration will be applied to the run.



Create a new version for your assistant

To update an assistant and create a new version from the UI, you can use either the Assistants tab or Studio. Either method creates a new version and sets it as the active version:

  * Assistants tab

  * Studio

  1. Navigate to your deployment and select the **Assistants** tab.
  2. Find the assistant you want to edit.
  3. Click **Edit**.
  4. Modify the assistant’s name, description, or configuration.
  5. Save your changes.

  1. Open Studio for the assistant.
  2. Click **Manage Assistants**.
  3. Edit the assistant’s configuration.
  4. Save your changes.



Use a previous assistant version

To set a previous version as active from Studio:

  1. Open Studio for the assistant.
  2. Click **Manage Assistants**.
  3. Locate the assistant and select the version you want to use.
  4. Toggle the **Active** switch for that version.

This updates the assistant to use the selected version for all future runs.

Deleting an assistant will delete **all** of its versions. There is currently no way to delete a single version. To skip a version, simply set a different version as active.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/configuration-cloud.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.