# Set up Agent Auth (Beta)

> Enable secure access from agents to any system using OAuth 2.0 credentials with Agent Auth.

<Note>Agent Auth is in **Beta** and under active development. To provide feedback or use this feature, reach out to the [LangChain team](https://forum.langchain.com/c/help/langsmith/).</Note>

## Installation

Install the Agent Auth client library from PyPI:

<CodeGroup>
  ```bash pip theme={null}
  pip install langchain-auth
  ```

  ```bash uv theme={null}
  uv add langchain-auth
  ```
</CodeGroup>

## Quickstart

### 1. Initialize the client

```python  theme={null}
from langchain_auth import Client

client = Client(api_key="your-langsmith-api-key")
```

### 2. Set up OAuth providers

Before agents can authenticate, you need to configure an OAuth provider using the following process:

1. Select a unique identifier for your OAuth provider to use in LangChain's platform (e.g., "github-local-dev", "google-workspace-prod").

2. Go to your OAuth provider's developer console and create a new OAuth application.

3. Set the callback URL in your OAuth provider using this structure:
   ```
   https://smith.langchain.com/host-oauth-callback/{provider_id}
   ```
   For example, if your provider\_id is "github-local-dev", use:
   ```
   https://smith.langchain.com/host-oauth-callback/github-local-dev
   ```

4. Use `client.create_oauth_provider()` with the credentials from your OAuth app:

```python  theme={null}
new_provider = await client.create_oauth_provider(
    provider_id="{provider_id}", # Provide any unique ID. Not formally tied to the provider.
    name="{provider_display_name}", # Provide any display name
    client_id="{your_client_id}",
    client_secret="{your_client_secret}",
    auth_url="{auth_url_of_your_provider}",
    token_url="{token_url_of_your_provider}",
)
```

### 3. Authenticate from an agent

The client `authenticate()` API is used to get OAuth tokens from pre-configured providers. On the first call, it takes the caller through an OAuth 2.0 auth flow.

#### In LangGraph context

By default, tokens are scoped to the calling agent using the Assistant ID parameter.

```python  theme={null}
auth_result = await client.authenticate(
    provider="{provider_id}",
    scopes=["scopeA"],
    user_id="your_user_id" # Any unique identifier to scope this token to the human caller
)

# Or if you'd like a token that can be used by any agent, set agent_scoped=False
auth_result = await client.authenticate(
    provider="{provider_id}",
    scopes=["scopeA"],
    user_id="your_user_id",
    agent_scoped=False
)
```

During execution, if authentication is required, the SDK will throw an [interrupt](https://langchain-ai.github.io/langgraph/how-tos/human_in_the_loop/add-human-in-the-loop/#pause-using-interrupt). The agent execution pauses and presents the OAuth URL to the user:

<img src="https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/langgraph-auth-interrupt.png?fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=94f84dd7ec822ca69f9a27b4458dca9f" alt="Studio interrupt showing OAuth URL" data-og-width="1197" width="1197" data-og-height="530" height="530" data-path="images/langgraph-auth-interrupt.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/langgraph-auth-interrupt.png?w=280&fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=8e2f6ddeb7ae2b7e3f349a23ed69270a 280w, https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/langgraph-auth-interrupt.png?w=560&fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=ed5f6697e44784a6a937f6bfd3248780 560w, https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/langgraph-auth-interrupt.png?w=840&fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=bb34295ee4128adb77cdf6dd1a76d88a 840w, https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/langgraph-auth-interrupt.png?w=1100&fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=09df9030e048467ca35ab70bf73b2272 1100w, https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/langgraph-auth-interrupt.png?w=1650&fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=ebfe20351ac52045b30713007da5ba61 1650w, https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/langgraph-auth-interrupt.png?w=2500&fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=ff3b2fcebfdb6fc76e7269d8aef34077 2500w" />

After the user completes OAuth authentication and we receive the callback from the provider, they will see the auth success page.

<img src="https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/github-auth-success.png?fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=72e6492f074507bc8888804066205fcb" alt="GitHub OAuth success page" data-og-width="447" width="447" data-og-height="279" height="279" data-path="images/github-auth-success.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/github-auth-success.png?w=280&fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=031b2f9d30e4da4240059cb25fba6d15 280w, https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/github-auth-success.png?w=560&fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=eb4d01516b4691158a47a8b2632d22e3 560w, https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/github-auth-success.png?w=840&fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=e49b04f99e4c2f485769443da039bca1 840w, https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/github-auth-success.png?w=1100&fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=930aee5e270d2fcb4d6bdfb001150d81 1100w, https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/github-auth-success.png?w=1650&fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=3b5dc841251462c3ed140800564c0ad8 1650w, https://mintcdn.com/langchain-5e9cc07a/Xbr8HuVd9jPi6qTU/images/github-auth-success.png?w=2500&fit=max&auto=format&n=Xbr8HuVd9jPi6qTU&q=85&s=0e53fbc4c56b16bf1db88c98ab2e631d 2500w" />

The agent then resumes execution from the point it left off at, and the token can be used for any API calls. We store and refresh OAuth tokens so that future uses of the service by either the user or agent do not require an OAuth flow.

```python  theme={null}
token = auth_result.token
```

#### Outside LangGraph context

Provide the `auth_url` to the user for out-of-band OAuth flows.

```python  theme={null}
# Default: user-scoped token (works for any agent under this user)
auth_result = await client.authenticate(
    provider="{provider_id}",
    scopes=["scopeA"],
    user_id="your_user_id"
)

if auth_result.needs_auth:
    print(f"Complete OAuth at: {auth_result.auth_url}")
    # Wait for completion
    completed_auth = await client.wait_for_completion(auth_result.auth_id)
    token = completed_auth.token
else:
    token = auth_result.token
```

***

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/agent-auth.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.langchain.com/llms.txt