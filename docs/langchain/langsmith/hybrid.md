# Hybrid

<Info>
  **Important**
  The hybrid option requires an [Enterprise](https://langchain.com/pricing) plan.
</Info>

The **hybrid** model splits LangSmith infrastructure between LangChain's cloud and yours:

* **Control plane** (LangSmith UI, APIs, and orchestration) runs in LangChain's cloud, managed by LangChain.
* **Data plane** (your <Tooltip tip="The server that runs your applications.">Agent Servers</Tooltip> and agent workloads) runs in your cloud, managed by you.

This combines the convenience of a managed interface with the flexibility of running workloads in your own environment.

<Note>
  Learn more about the [control plane](/langsmith/control-plane), [data plane](/langsmith/data-plane), and [Agent Server](/langsmith/agent-server) architecture concepts.
</Note>

| Component                                                                                                | Responsibilities                                                                                                                                    | Where it runs     | Who manages it |
| -------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------- | -------------- |
| <Tooltip tip="The LangSmith UI and APIs for managing deployments.">Control plane</Tooltip>               | <ul><li>UI for creating deployments and revisions</li><li>APIs for managing deployments</li><li>Observability data storage</li></ul>                | LangChain's cloud | LangChain      |
| <Tooltip tip="The runtime environment where your Agent Servers and agents execute.">Data plane</Tooltip> | <ul><li>Operator/listener to reconcile deployments</li><li>Agent Servers (agents/graphs)</li><li>Backing services (Postgres, Redis, etc.)</li></ul> | Your cloud        | You            |

When running LangSmith in a hybrid model, you authenticate with a [LangSmith API key](/langsmith/create-account-api-key).

### Workflow

1. Use the `langgraph-cli` or [Studio](/langsmith/studio) to test your graph locally.
2. Build a Docker image using the `langgraph build` command.
3. Deploy your Agent Server from the [control plane UI](/langsmith/control-plane#control-plane-ui).

<Note>
  Supported Compute Platforms: [Kubernetes](https://kubernetes.io/).<br />
  For setup, refer to the [Hybrid setup guide](/langsmith/deploy-hybrid).
</Note>

### Architecture

<img className="block dark:hidden" src="https://mintcdn.com/langchain-5e9cc07a/JOyLr_spVEW0t2KF/langsmith/images/hybrid-with-deployment-light.png?fit=max&auto=format&n=JOyLr_spVEW0t2KF&q=85&s=86d548632d33be3644bad7213287ac78" alt="Hybrid deployment: LangChain-hosted control plane (LangSmith UI/APIs) manages deployments. Your cloud runs a listener, Agent Server instances, and backing stores (Postgres/Redis) on Kubernetes." data-og-width="1784" width="1784" data-og-height="1782" height="1782" data-path="langsmith/images/hybrid-with-deployment-light.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/JOyLr_spVEW0t2KF/langsmith/images/hybrid-with-deployment-light.png?w=280&fit=max&auto=format&n=JOyLr_spVEW0t2KF&q=85&s=2fe7b82524e32a2ce1e3726ad3bce553 280w, https://mintcdn.com/langchain-5e9cc07a/JOyLr_spVEW0t2KF/langsmith/images/hybrid-with-deployment-light.png?w=560&fit=max&auto=format&n=JOyLr_spVEW0t2KF&q=85&s=807a35d47b9c8e740a96f0a8aa4389a1 560w, https://mintcdn.com/langchain-5e9cc07a/JOyLr_spVEW0t2KF/langsmith/images/hybrid-with-deployment-light.png?w=840&fit=max&auto=format&n=JOyLr_spVEW0t2KF&q=85&s=84333efa9a9e83305b93f4b6e770b2f8 840w, https://mintcdn.com/langchain-5e9cc07a/JOyLr_spVEW0t2KF/langsmith/images/hybrid-with-deployment-light.png?w=1100&fit=max&auto=format&n=JOyLr_spVEW0t2KF&q=85&s=1d8bd0547f7814cad914b1ddc6dbfa48 1100w, https://mintcdn.com/langchain-5e9cc07a/JOyLr_spVEW0t2KF/langsmith/images/hybrid-with-deployment-light.png?w=1650&fit=max&auto=format&n=JOyLr_spVEW0t2KF&q=85&s=09f181972952ab4362b3ac70b7934d59 1650w, https://mintcdn.com/langchain-5e9cc07a/JOyLr_spVEW0t2KF/langsmith/images/hybrid-with-deployment-light.png?w=2500&fit=max&auto=format&n=JOyLr_spVEW0t2KF&q=85&s=e2d292d67dbf1fdb68758fac293c0cc7 2500w" />

<img className="hidden dark:block" src="https://mintcdn.com/langchain-5e9cc07a/JOyLr_spVEW0t2KF/langsmith/images/hybrid-with-deployment-dark.png?fit=max&auto=format&n=JOyLr_spVEW0t2KF&q=85&s=829f0ef40c315c493ef8e30857e9abf5" alt="Hybrid deployment: LangChain-hosted control plane (LangSmith UI/APIs) manages deployments. Your cloud runs a listener, Agent Server instances, and backing stores (Postgres/Redis) on Kubernetes." data-og-width="1784" width="1784" data-og-height="1782" height="1782" data-path="langsmith/images/hybrid-with-deployment-dark.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/JOyLr_spVEW0t2KF/langsmith/images/hybrid-with-deployment-dark.png?w=280&fit=max&auto=format&n=JOyLr_spVEW0t2KF&q=85&s=bdb7a126e3914a07ed1ff72b66e50e9a 280w, https://mintcdn.com/langchain-5e9cc07a/JOyLr_spVEW0t2KF/langsmith/images/hybrid-with-deployment-dark.png?w=560&fit=max&auto=format&n=JOyLr_spVEW0t2KF&q=85&s=14f4f01c71edca5ce1594f3f2145f0e4 560w, https://mintcdn.com/langchain-5e9cc07a/JOyLr_spVEW0t2KF/langsmith/images/hybrid-with-deployment-dark.png?w=840&fit=max&auto=format&n=JOyLr_spVEW0t2KF&q=85&s=04f8b60076c4ff6263af77da5a65ccc1 840w, https://mintcdn.com/langchain-5e9cc07a/JOyLr_spVEW0t2KF/langsmith/images/hybrid-with-deployment-dark.png?w=1100&fit=max&auto=format&n=JOyLr_spVEW0t2KF&q=85&s=50fe58a42273562591bf695d5cdbfe57 1100w, https://mintcdn.com/langchain-5e9cc07a/JOyLr_spVEW0t2KF/langsmith/images/hybrid-with-deployment-dark.png?w=1650&fit=max&auto=format&n=JOyLr_spVEW0t2KF&q=85&s=20025a5634783e2eb1d2ba177724ccc6 1650w, https://mintcdn.com/langchain-5e9cc07a/JOyLr_spVEW0t2KF/langsmith/images/hybrid-with-deployment-dark.png?w=2500&fit=max&auto=format&n=JOyLr_spVEW0t2KF&q=85&s=79e4e542803c26c38e5fffaf2bc961bf 2500w" />

### Compute Platforms

* **Kubernetes**: Hybrid supports running the data plane on any Kubernetes cluster.

<Tip>
  For setup in Kubernetes, refer to the [Hybrid setup guide](/langsmith/deploy-hybrid)
</Tip>

### Egress to LangSmith and the control plane

In the hybrid deployment model, your self-hosted data plane will send network requests to the control plane to poll for changes that need to be implemented in the data plane. Traces from data plane deployments also get sent to the LangSmith instance integrated with the control plane. This traffic to the control plane is encrypted, over HTTPS. The data plane authenticates with the control plane with a LangSmith API key.

In order to enable this egress, you may need to update internal firewall rules or cloud resources (such as Security Groups) to [allow certain IP addresses](/langsmith/cloud#ingress-into-langchain-saas).

<Warning>
  AWS/Azure PrivateLink or GCP Private Service Connect is currently not supported. This traffic will go over the internet.
</Warning>

## Listeners

In the hybrid option, one or more ["listener" applications](/langsmith/data-plane#”listener”-application) can run depending on how your LangSmith workspaces and Kubernetes clusters are organized.

### Kubernetes cluster organization

* One or more listeners can run in a Kubernetes cluster.
* A listener can deploy into one or more namespaces in that cluster.
* Multiple listeners cannot deploy to the same namespace.
* Cluster owners are responsible for planning listener layout and Agent Server deployments.

### LangSmith workspace organization

* A workspace can be associated with one or more listeners.
* A listener can only be associated with one workspace. LangSmith workspace to listener is a one-to-many relationship.
* A workspace can only deploy to Kubernetes clusters where all of its listeners are deployed.

## Use Cases

Here are some common listener configurations (not strict requirements):

### Each LangSmith workspace → separate Kubernetes cluster

* Cluster `alpha` runs workspace `A`
* Cluster `beta` runs workspace `B`

### One cluster, one namespace per workspace

* Cluster `alpha`, namespace `1` runs workspace `A`
* Cluster `alpha`, namespace `2` runs workspace `B`

### Separate clusters, with shared “dev” cluster

* Cluster `alpha` runs workspace `A`
* Cluster `beta` runs workspace `B`
* Cluster `dev` runs workspaces `A` and `B`
* Both workspaces have two listeners; cluster `dev` has two listener deployments

***

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/hybrid.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.langchain.com/llms.txt