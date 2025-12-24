# Implement a CI/CD pipeline using LangSmith Deployment and Evaluation

This guide demonstrates how to implement a comprehensive CI/CD pipeline for AI agent applications deployed in LangSmith Deployment. In this example, you'll use the [LangGraph](/oss/python/langgraph/overview) open source framework for orchestrating and building the agent, [LangSmith](/langsmith/home) for observability and evaluations. This pipeline is based on the [cicd-pipeline-example repository](https://github.com/langchain-ai/cicd-pipeline-example).

## Overview

The CI/CD pipeline provides:

* <Icon icon="check-circle" /> **Automated testing**: Unit, integration, and end-to-end tests.
* <Icon icon="chart-line" /> **Offline evaluations**: Performance assessment using [AgentEvals](https://github.com/langchain-ai/agentevals), [OpenEvals](https://github.com/langchain-ai/openevals) and [LangSmith](https://docs.langchain.com/langsmith/home).
* <Icon icon="rocket" /> **Preview and production deployments**: Automated staging and quality-gated production releases using the Control Plane API.
* <Icon icon="eye" /> **Monitoring**: Continuous evaluation and alerting.

## Pipeline architecture

The CI/CD pipeline consists of several key components that work together to ensure code quality and reliable deployments:

```mermaid  theme={null}
graph TD
    A1[Code or Graph Change] --> B1[Trigger CI Pipeline]
    A2[Prompt Commit in PromptHub] --> B1
    A3[Online Evaluation Alert] --> B1
    A4[PR Opened] --> B1

    subgraph "Testing"
        B1 --> C1[Run Unit Tests]
        B1 --> C2[Run Integration Tests]
        B1 --> C3[Run End to End Tests]
        B1 --> C4[Run Offline Evaluations]

        C4 --> D1[Evaluate with OpenEvals or AgentEvals]
        C4 --> D2[Assertions: Hard and Soft]

        C1 --> E1[Run LangGraph Dev Server Test]
        C2 --> E1
        C3 --> E1
        D1 --> E1
        D2 --> E1
    end

    E1 --> F1[Push to Staging Deployment - Deploy to LangSmith as Development Type]

    F1 --> G1[Run Online Evaluations on Live Data]
    G1 --> H1[Attach Scores to Traces]

    H1 --> I1[If Quality Below Threshold]
    I1 --> J1[Send to Annotation Queue]
    I1 --> J2[Trigger Alert via Webhook]
    I1 --> J3[Push Trace to Golden Dataset]

    F1 --> K1[Promote to Production if All Pass - Deploy to LangSmith Production]

    J2 --> L1[Slack or PagerDuty Notification]

    subgraph Manual Review
        J1 --> M1[Human Labeling]
        M1 --> J3
    end
```

### Trigger sources

There are multiple ways you can trigger this pipeline, either during development or if your application is already live. The pipeline can be triggered by:

* <Icon icon="code-branch" /> **Code changes**: Pushes to main/development branches where you can modify the LangGraph architecture, try different models, update agent logic, or make any code improvements.
* <Icon icon="edit" /> **PromptHub updates**: Changes to prompt templates stored in LangSmith PromptHub—whenever there's a new prompt commit, the system triggers a webhook to run the pipeline.
* <Icon icon="exclamation-triangle" /> **Online evaluation alerts**: Performance degradation notifications from live deployments
* <Icon icon="webhook" /> **LangSmith traces webhooks**: Automated triggers based on trace analysis and performance metrics.
* <Icon icon="play" /> **Manual trigger**: Manual initiation of the pipeline for testing or emergency deployments.

### Testing layers

Compared to traditional software, testing AI agent applications also requires assessing response quality, so it is important to test each part of the workflow. The pipeline implements multiple testing layers:

1. <Icon icon="puzzle-piece" /> **Unit tests**: Individual node and utility function testing.
2. <Icon icon="link" /> **Integration tests**: Component interaction testing.
3. <Icon icon="route" /> **End-to-end tests**: Full graph execution testing.
4. <Icon icon="brain" /> **Offline evaluations**: Performance assessment with real-world scenarios including end-to-end evaluations, single-step evaluations, agent trajectory analysis, and multi-turn simulations.
5. <Icon icon="server" /> **LangGraph dev server tests**: Use the [langgraph-cli](/langsmith/cli) tool for spinning up (inside the GitHub Action) a local server to run the LangGraph agent. This polls the `/ok` server API endpoint until it is available and for 30 seconds, after that it throws an error.

## GitHub Actions workflow

The CI/CD pipeline uses GitHub Actions with the [Control Plane API](/langsmith/api-ref-control-plane) and [LangSmith API](https://api.smith.langchain.com/redoc) to automate deployment. A helper script manages API interactions and deployments: [https://github.com/langchain-ai/cicd-pipeline-example/blob/main/.github/scripts/langgraph\_api.py](https://github.com/langchain-ai/cicd-pipeline-example/blob/main/.github/scripts/langgraph_api.py).

The workflow includes:

* **New agent deployment**: When a new PR is opened and tests pass, a new preview deployment is created in LangSmith Deployment using the [Control Plane API](/langsmith/api-ref-control-plane). This allows you to test the agent in a staging environment before promoting to production.

* **Agent deployment revision**: A revision happens when an existing deployment with the same ID is found, or when the PR is merged into main. In the case of merging to main, the preview deployment is deleted and a production deployment is created. This ensures that any updates to the agent are properly deployed and integrated into the production infrastructure.

  <img src="https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-new-lgp-revision.png?fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=3ef7d51a322b8b5e2f9c2c70579fcc97" alt="Agent Deployment Revision Workflow" data-og-width="1022" width="1022" data-og-height="196" height="196" data-path="langsmith/images/cicd-new-lgp-revision.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-new-lgp-revision.png?w=280&fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=a3d06c339e84a1af99450d23e8bd617f 280w, https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-new-lgp-revision.png?w=560&fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=30589c8727af3ecb1d97881fd6692554 560w, https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-new-lgp-revision.png?w=840&fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=c05ab515ea0901fb2d076dee256ad108 840w, https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-new-lgp-revision.png?w=1100&fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=b939ad6842110227f70cc0526468d21d 1100w, https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-new-lgp-revision.png?w=1650&fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=0559d5b2a85414e954a72377b2eed9ec 1650w, https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-new-lgp-revision.png?w=2500&fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=b8b96047a8b37f31b78d793cd7d18f45 2500w" />

* **Testing and evaluation workflow**: In addition to the more traditional testing phases (unit tests, integration tests, end-to-end tests, etc.), the pipeline includes [offline evaluations](/langsmith/evaluation-concepts#offline-evaluation) and [Agent dev server testing](/langsmith/local-server) because you want to test the quality of your agent. These evaluations provide comprehensive assessment of the agent's performance using real-world scenarios and data.

  <img src="https://mintcdn.com/langchain-5e9cc07a/MrTet_AXQVddxOlO/langsmith/images/cicd-test-with-results.png?fit=max&auto=format&n=MrTet_AXQVddxOlO&q=85&s=477c3f5ec3d9bb9dfc354b9a57860636" alt="Test with Results Workflow" data-og-width="2050" width="2050" data-og-height="996" height="996" data-path="langsmith/images/cicd-test-with-results.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/MrTet_AXQVddxOlO/langsmith/images/cicd-test-with-results.png?w=280&fit=max&auto=format&n=MrTet_AXQVddxOlO&q=85&s=7c5885b5f85c1c408fda449c5a0c706a 280w, https://mintcdn.com/langchain-5e9cc07a/MrTet_AXQVddxOlO/langsmith/images/cicd-test-with-results.png?w=560&fit=max&auto=format&n=MrTet_AXQVddxOlO&q=85&s=3b9a25332a9f6b56edfc9fbbfec248c1 560w, https://mintcdn.com/langchain-5e9cc07a/MrTet_AXQVddxOlO/langsmith/images/cicd-test-with-results.png?w=840&fit=max&auto=format&n=MrTet_AXQVddxOlO&q=85&s=380cb346fffbaf13365b37c6fa955c05 840w, https://mintcdn.com/langchain-5e9cc07a/MrTet_AXQVddxOlO/langsmith/images/cicd-test-with-results.png?w=1100&fit=max&auto=format&n=MrTet_AXQVddxOlO&q=85&s=8994d1e816e725865f90a2ac6601f7a4 1100w, https://mintcdn.com/langchain-5e9cc07a/MrTet_AXQVddxOlO/langsmith/images/cicd-test-with-results.png?w=1650&fit=max&auto=format&n=MrTet_AXQVddxOlO&q=85&s=42b752f1e5f0043dd6998ae372e83874 1650w, https://mintcdn.com/langchain-5e9cc07a/MrTet_AXQVddxOlO/langsmith/images/cicd-test-with-results.png?w=2500&fit=max&auto=format&n=MrTet_AXQVddxOlO&q=85&s=043be8ed1ef59cea171f30146790a877 2500w" />

  <AccordionGroup>
    <Accordion title="Final Response Evaluation" icon="check-circle">
      Evaluates the final output of your agent against expected results. This is the most common type of evaluation that checks if the agent's final response meets quality standards and answers the user's question correctly.
    </Accordion>

    <Accordion title="Single Step Evaluation" icon="step-forward">
      Tests individual steps or nodes within your LangGraph workflow. This allows you to validate specific components of your agent's logic in isolation, ensuring each step functions correctly before testing the full pipeline.
    </Accordion>

    <Accordion title="Agent Trajectory Evaluation" icon="route">
      Analyzes the complete path your agent takes through the graph, including all intermediate steps and decision points. This helps identify bottlenecks, unnecessary steps, or suboptimal routing in your agent's workflow. It also evaluates whether your agent invoked the right tools in the right order or at the right time.
    </Accordion>

    <Accordion title="Multi-Turn Evaluation" icon="comments">
      Tests conversational flows where the agent maintains context across multiple interactions. This is crucial for agents that handle follow-up questions, clarifications, or extended dialogues with users.
    </Accordion>
  </AccordionGroup>

  See the [LangGraph testing documentation](/oss/python/langgraph/test) for specific testing approaches and the [evaluation approaches guide](/langsmith/evaluation-approaches) for a comprehensive overview of offline evaluations.

### Prerequisites

Before setting up the CI/CD pipeline, ensure you have:

* <Icon icon="robot" /> An AI agent application (in this case built using [LangGraph](/oss/python/langgraph/overview))
* <Icon icon="user" /> A [LangSmith account](https://smith.langchain.com/)
* <Icon icon="key" /> A [LangSmith API key](/langsmith/create-account-api-key) needed to deploy agents and retrieve experiment results
* <Icon icon="cog" /> Project-specific environment variables configured in your repository secrets (e.g., LLM model API keys, vector store credentials, database connections)

<Note>
  While this example uses GitHub, the CI/CD pipeline works with other Git hosting platforms including GitLab, Bitbucket, and others.
</Note>

## Deployment options

LangSmith supports multiple deployment methods, depending on how your [LangSmith instance is hosted](/langsmith/platform-setup):

* <Icon icon="cloud" /> **Cloud LangSmith**: Direct GitHub integration.
* <Icon icon="server" /> **Self-Hosted/Hybrid**: Container registry-based deployments.

The deployment flow starts by modifying your agent implementation. At minimum, you must have a [`langgraph.json`](/langsmith/application-structure) and dependency file in your project (`requirements.txt` or `pyproject.toml`). Use the `langgraph dev` CLI tool to check for errors—fix any errors; otherwise, the deployment will succeed when deployed to LangSmith Deployment.

```mermaid  theme={null}
graph TD
    A[Agent Implementation] --> B[langgraph.json + dependencies]
    B --> C[Test Locally with langgraph dev]
    C --> D{Errors?}
    D -->|Yes| E[Fix Issues]
    E --> C
    D -->|No| F[Choose LangSmith Instance]

    F --> G[Cloud LangSmith]
    F --> H[Self-Hosted/Hybrid LangSmith]

    subgraph "Cloud LangSmith"
        G --> I[Method 1: Connect GitHub Repo in UI]
        G --> J[Method 2: Control Plane API with GitHub Repo]
        I --> K[Deploy via LangSmith UI]
        J --> L[Deploy via Control Plane API]
    end

    subgraph "Self-Hosted/Hybrid LangSmith"
        H --> S[Build Docker Image langgraph build]
        S --> T[Push to Container Registry]
        T --> U{Deploy via?}
        U -->|UI| V[Specify Image URI in UI]
        U -->|API| W[Use Control Plane API]
        V --> X[Deploy via LangSmith UI]
        W --> Y[Deploy via Control Plane API]
    end

    K --> AA[Agent Ready for Use]
    L --> AA
    X --> AA
    Y --> AA

    AA --> BB{Connect via?}
    BB -->|LangGraph SDK| CC[Use LangGraph SDK]
    BB -->|RemoteGraph| DD[Use RemoteGraph]
    BB -->|REST API| EE[Use REST API]
    BB -->|LangGraph Studio UI| FF[Use LangGraph Studio UI]
```

### Prerequisites for manual deployment

Before deploying your agent, ensure you have:

1. <Icon icon="project-diagram" /> **LangGraph graph**: Your agent implementation (e.g., `./agents/simple_text2sql.py:agent`).
2. <Icon icon="box" /> **Dependencies**: Either `requirements.txt` or `pyproject.toml` with all required packages.
3. <Icon icon="cog" /> **Configuration**: `langgraph.json` file specifying:
   * Path to your agent graph
   * Dependencies location
   * Environment variables
   * Python version

Example `langgraph.json`:

```json  theme={null}
{
    "graphs": {
        "simple_text2sql": "./agents/simple_text2sql.py:agent"
    },
    "env": ".env",
    "python_version": "3.11",
    "dependencies": ["."],
    "image_distro": "wolfi"
}
```

### Local development and testing

<img src="https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-studio-cli.png?fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=425460d3401221ab441e21fc706c9cf1" alt="Studio CLI Interface" data-og-width="2972" width="2972" data-og-height="1354" height="1354" data-path="langsmith/images/cicd-studio-cli.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-studio-cli.png?w=280&fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=35e64359dba47f4db4962148073cfadb 280w, https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-studio-cli.png?w=560&fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=c12eb479d5c46921633c56bdead978bc 560w, https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-studio-cli.png?w=840&fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=b36efc12f81027b7364cea82a4600fc3 840w, https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-studio-cli.png?w=1100&fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=131c3fa2e989fbb8ebc4748a5790dc36 1100w, https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-studio-cli.png?w=1650&fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=afa56b4e5ca02495ef5e7cb69d8e1329 1650w, https://mintcdn.com/langchain-5e9cc07a/-UAx6PdOIJpPyTy2/langsmith/images/cicd-studio-cli.png?w=2500&fit=max&auto=format&n=-UAx6PdOIJpPyTy2&q=85&s=774ec3dcf76a4b0e61989cd12e41e0c3 2500w" />

First, test your agent locally using [Studio](/langsmith/studio):

```bash  theme={null}
# Start local development server with Studio
langgraph dev
```

This will:

* Spin up a local server with Studio.
* Allow you to visualize and interact with your graph.
* Validate that your agent works correctly before deployment.

<Note>
  If your agent runs locally without any errors, it means that deployment to LangSmith will likely succeed. This local testing helps catch configuration issues, dependency problems, and agent logic errors before attempting deployment.
</Note>

See the [LangGraph CLI documentation](/langsmith/cli#dev) for more details.

### Method 1: LangSmith Deployment UI

Deploy your agent using the LangSmith deployment interface:

1. Go to your [LangSmith dashboard](https://smith.langchain.com).
2. Navigate to the **Deployments** section.
3. Click the **+ New Deployment** button in the top right.
4. Select your GitHub repository containing your LangGraph agent from the dropdown menu.

**Supported deployments:**

* <Icon icon="cloud" /> **Cloud LangSmith**: Direct GitHub integration with dropdown menu
* <Icon icon="server" /> **Self-Hosted/Hybrid LangSmith**: Specify your image URI in the Image Path field (e.g., `docker.io/username/my-agent:latest`)

<Info>
  **Benefits:**

  * Simple UI-based deployment
  * Direct integration with your GitHub repository (cloud)
  * No manual Docker image management required (cloud)
</Info>

### Method 2: Control Plane API

Deploy using the Control Plane API with different approaches for each deployment type:

**For Cloud LangSmith:**

* Use the Control Plane API to create deployments by pointing to your GitHub repository
* No Docker image building required for cloud deployments

**For Self-Hosted/Hybrid LangSmith:**

```bash  theme={null}
# Build Docker image
langgraph build -t my-agent:latest

# Push to your container registry
docker push my-agent:latest
```

You can push to any container registry (Docker Hub, AWS ECR, Azure ACR, Google GCR, etc.) that your deployment environment has access to.

**Supported deployments:**

* <Icon icon="cloud" /> **Cloud LangSmith**: Use the Control Plane API to create deployments from your GitHub repository
* <Icon icon="server" /> **Self-Hosted/Hybrid LangSmith**: Use the Control Plane API to create deployments from your container registry

See the [LangGraph CLI build documentation](/langsmith/cli#build) for more details.

### Connect to Your Deployed Agent

* <Icon icon="code" /> **[LangGraph SDK](https://langchain-ai.github.io/langgraph/cloud/reference/sdk/python_sdk_ref/#langgraph-sdk-python)**: Use the LangGraph SDK for programmatic integration.
* <Icon icon="project-diagram" /> **[RemoteGraph](/langsmith/use-remote-graph)**: Connect using RemoteGraph for remote graph connections (to use your graph in other graphs).
* <Icon icon="globe" /> **[REST API](/langsmith/server-api-ref)**: Use HTTP-based interactions with your deployed agent.
* <Icon icon="desktop" /> **[Studio](/langsmith/studio)**: Access the visual interface for testing and debugging.

### Environment configuration

#### Database & cache configuration

By default, LangSmith Deployment create PostgreSQL and Redis instances for you. To use external services, set the following environment variables in your new deployment or revision:

```bash  theme={null}
# Set environment variables for external services
export POSTGRES_URI_CUSTOM="postgresql://user:pass@host:5432/db"
export REDIS_URI_CUSTOM="redis://host:6379/0"
```

See the [environment variables documentation](/langsmith/env-var#postgres-uri-custom) for more details.

## Troubleshooting

### Wrong API endpoints

If you're experiencing connection issues, verify you're using the correct endpoint format for your LangSmith instance. There are two different APIs with different endpoints:

#### LangSmith API (Traces, Ingestion, etc.)

For LangSmith API operations (traces, evaluations, datasets):

| Region | Endpoint                             |
| ------ | ------------------------------------ |
| US     | `https://api.smith.langchain.com`    |
| EU     | `https://eu.api.smith.langchain.com` |

For self-hosted LangSmith instances, use `http(s)://<langsmith-url>/api` where `<langsmith-url>` is your self-hosted instance URL.

<Note>
  If you're setting the endpoint in the `LANGSMITH_ENDPOINT` environment variable, you need to add `/v1` at the end (e.g., `https://api.smith.langchain.com/v1` or `http(s)://<langsmith-url>/api/v1` if self-hosted).
</Note>

#### LangSmith Deployment API (Deployments)

For LangSmith Deployment operations (deployments, revisions):

| Region | Endpoint                            |
| ------ | ----------------------------------- |
| US     | `https://api.host.langchain.com`    |
| EU     | `https://eu.api.host.langchain.com` |

For self-hosted LangSmith instances, use `http(s)://<langsmith-url>/api-host` where `<langsmith-url>` is your self-hosted instance URL.

***

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/cicd-pipeline-example.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.langchain.com/llms.txt