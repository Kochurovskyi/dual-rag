# Self-hosted LangSmith

<Note>
  **Important**<br />
  Self-hosted LangSmith is an add-on to the Enterprise plan designed for our largest, most security-conscious customers. For more details, refer to [Pricing](https://www.langchain.com/pricing). [Contact our sales team](https://www.langchain.com/contact-sales) if you want to get a license key to trial LangSmith in your environment.
</Note>

LangSmith supports different self-hosted configurations depending on your scale, security, and infrastructure needs.

You can use LangSmith for [observability](/langsmith/observability) and [evaluation](/langsmith/evaluation) without agent deployment. Or, you can set up the **full self-hosted platform** for observability, evaluation, and [agent deployment](/langsmith/deployments). Alternatively, you can deploy agents directly without the [control plane](/langsmith/control-plane).

This page provides an overview of each self-hosted model:

<Columns cols={1}>
  <Card title="LangSmith Observability and Evaluation" icon="chart-line" href="#langsmith">
    Host an instance of LangSmith that includes observability, tracing, and evaluations in the UI and API. Best for teams who want self-hosted monitoring and evaluation without deploying agents.
  </Card>

  <Card title="LangSmith Observability, Evaluation, and Deployment" icon="layer-group" href="#enable-langsmith-deployment">
    Enables deploying graphs to Agent Server via the control plane. The control plane and data plane provide the full LangSmith platform for running and monitoring agents. This includes observability, evaluation, and deployment.
  </Card>

  <Card title="Standalone server" icon="server" href="#standalone-server">
    Host an Agent Server directly without the control plane UI. A lightweight option for running one or a few agents as independent services, with full control over scaling and integration.
  </Card>
</Columns>

| Model                                      | Includes                                                                                                                                                                                                                | Best for                                                                                                                                                                               | Methods                                                                                                                                               |
| ------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Observability & Evaluation**             | <ul><li>LangSmith (UI + API)</li><li>Backend services (queue, playground, ACE)</li><li>Datastores: PostgreSQL, Redis, ClickHouse, optional blob storage</li></ul>                                                       | <ul><li>Teams who need self-hosted observability, tracing, and evaluation</li><li>Running LangSmith without deploying agents/graphs</li></ul>                                          | <ul><li>Docker Compose (dev/test)</li><li>Kubernetes + Helm (production)</li></ul>                                                                    |
| **Observability, Evaluation & Deployment** | <ul><li>Everything from Observability and Evaluation</li><li>Control plane (deployments UI, revision management, Studio)</li><li>Data plane (Agent Server pods)</li><li>Kubernetes operator for orchestration</li></ul> | <ul><li>Enterprise teams needing a private LangChain Cloud</li><li>Centralized UI/API for managing multiple agents/graphs</li><li>Integrated observability and orchestration</li></ul> | <ul><li>Kubernetes with Helm (required)</li><li>Runs on EKS, GKE, AKS, or self-managed clusters</li></ul>                                             |
| **Standalone server**                      | <ul><li>Agent Server container(s)</li><li>Requires PostgreSQL + Redis (shared or dedicated)</li><li>Optional LangSmith integration for tracing</li></ul>                                                                | <ul><li>Lightweight deployments of one or a few agents</li><li>Integrating Agent Servers as microservices</li><li>Teams preferring to manage scaling & CI/CD themselves</li></ul>      | <ul><li>Docker / Docker Compose (dev/test)</li><li>Kubernetes + Helm (production)</li><li>Any container runtime or VM (ECS, EC2, ACI, etc.)</li></ul> |

<Note>
  For setup guides, refer to:

  * [Enable LangSmith Deployment](/langsmith/deploy-self-hosted-full-platform)
  * [Deploy Standalone Server](/langsmith/deploy-standalone-server)

  Supported compute platforms: [Kubernetes](https://kubernetes.io/) (for LangSmith Deployment), any compute platform (for Standalone Server)
</Note>

## Self-host LangSmith Observability and Evaluation

Host an instance of LangSmith that includes observability, tracing, and evaluations in the UI and API, but **without** the ability to deploy agents through the control plane.

This includes:

**Services:**

* LangSmith frontend UI
* LangSmith backend API
* LangSmith Platform backend
* LangSmith Playground
* LangSmith queue
* LangSmith ACE (Arbitrary Code Execution) backend

**Storage services:**

* ClickHouse (traces and feedback data)
* PostgreSQL (operational data)
* Redis (queuing and caching)
* Blob storage (optional, but recommended for production)

<img className="block dark:hidden" src="https://mintcdn.com/langchain-5e9cc07a/rqYqeBEA_2oeiw17/langsmith/images/cloud-arch-light.png?fit=max&auto=format&n=rqYqeBEA_2oeiw17&q=85&s=0790cbdf4fe131c74d1e60bb120834e3" alt="LangSmith architecture showing services and datastores" data-og-width="2210" width="2210" data-og-height="1463" height="1463" data-path="langsmith/images/cloud-arch-light.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/rqYqeBEA_2oeiw17/langsmith/images/cloud-arch-light.png?w=280&fit=max&auto=format&n=rqYqeBEA_2oeiw17&q=85&s=c04d8a044d221559fe2f7b9121275638 280w, https://mintcdn.com/langchain-5e9cc07a/rqYqeBEA_2oeiw17/langsmith/images/cloud-arch-light.png?w=560&fit=max&auto=format&n=rqYqeBEA_2oeiw17&q=85&s=a15351b254f11cc149ce237ba8853e91 560w, https://mintcdn.com/langchain-5e9cc07a/rqYqeBEA_2oeiw17/langsmith/images/cloud-arch-light.png?w=840&fit=max&auto=format&n=rqYqeBEA_2oeiw17&q=85&s=d4a409e73830e588519cb1d0b2a17f3b 840w, https://mintcdn.com/langchain-5e9cc07a/rqYqeBEA_2oeiw17/langsmith/images/cloud-arch-light.png?w=1100&fit=max&auto=format&n=rqYqeBEA_2oeiw17&q=85&s=6dbeda77b57083efb988e15af38f0a6e 1100w, https://mintcdn.com/langchain-5e9cc07a/rqYqeBEA_2oeiw17/langsmith/images/cloud-arch-light.png?w=1650&fit=max&auto=format&n=rqYqeBEA_2oeiw17&q=85&s=24aadbe2e79db02d76fd5deaea6564e1 1650w, https://mintcdn.com/langchain-5e9cc07a/rqYqeBEA_2oeiw17/langsmith/images/cloud-arch-light.png?w=2500&fit=max&auto=format&n=rqYqeBEA_2oeiw17&q=85&s=a126aa1f02d36de0a8e391f0e1059b8e 2500w" />

<img className="hidden dark:block" src="https://mintcdn.com/langchain-5e9cc07a/rqYqeBEA_2oeiw17/langsmith/images/cloud-arch-dark.png?fit=max&auto=format&n=rqYqeBEA_2oeiw17&q=85&s=767f3bc3dc73ffe1a806f54e0aaa428b" alt="LangSmith architecture showing services and datastores" data-og-width="2210" width="2210" data-og-height="1463" height="1463" data-path="langsmith/images/cloud-arch-dark.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/rqYqeBEA_2oeiw17/langsmith/images/cloud-arch-dark.png?w=280&fit=max&auto=format&n=rqYqeBEA_2oeiw17&q=85&s=f7367df5b782c821882605418c50563f 280w, https://mintcdn.com/langchain-5e9cc07a/rqYqeBEA_2oeiw17/langsmith/images/cloud-arch-dark.png?w=560&fit=max&auto=format&n=rqYqeBEA_2oeiw17&q=85&s=60759ef9e927ba0985e21e38acacae6d 560w, https://mintcdn.com/langchain-5e9cc07a/rqYqeBEA_2oeiw17/langsmith/images/cloud-arch-dark.png?w=840&fit=max&auto=format&n=rqYqeBEA_2oeiw17&q=85&s=383ac38ba52733548d8d97ffabfe384e 840w, https://mintcdn.com/langchain-5e9cc07a/rqYqeBEA_2oeiw17/langsmith/images/cloud-arch-dark.png?w=1100&fit=max&auto=format&n=rqYqeBEA_2oeiw17&q=85&s=b045b8e19a9926d4d10ec8ad2d2767c1 1100w, https://mintcdn.com/langchain-5e9cc07a/rqYqeBEA_2oeiw17/langsmith/images/cloud-arch-dark.png?w=1650&fit=max&auto=format&n=rqYqeBEA_2oeiw17&q=85&s=23778aa891c1b42336b274ab1b2f8bec 1650w, https://mintcdn.com/langchain-5e9cc07a/rqYqeBEA_2oeiw17/langsmith/images/cloud-arch-dark.png?w=2500&fit=max&auto=format&n=rqYqeBEA_2oeiw17&q=85&s=5a64734b4e9fb5dd4af690edf3fa6248 2500w" />

To access the LangSmith UI and send API requests, you will need to expose the [LangSmith frontend](#langsmith-frontend) service. Depending on your installation method, this can be a load balancer or a port exposed on the host machine.

### Services

| Service                                                                                                        | Description                                                                                                                                                                                                                                                                                                                                              |
| -------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <a id="langsmith-frontend" /> **LangSmith frontend**                                                           | The frontend uses Nginx to serve the LangSmith UI and route API requests to the other servers. This serves as the entrypoint for the application and is the only component that must be exposed to users.                                                                                                                                                |
| <a id="langsmith-backend" /> **LangSmith backend**                                                             | The backend is the main entrypoint for CRUD API requests and handles the majority of the business logic for the application. This includes handling requests from the frontend and SDK, preparing traces for ingestion, and supporting the hub API.                                                                                                      |
| <a id="langsmith-queue" /> **LangSmith queue**                                                                 | The queue handles incoming traces and feedback to ensure that they are ingested and persisted into the traces and feedback datastore asynchronously, handling checks for data integrity and ensuring successful insert into the datastore, handling retries in situations such as database errors or the temporary inability to connect to the database. |
| <a id="langsmith-platform-backend" /> **LangSmith platform backend**                                           | The platform backend is another critical service that primarily handles authentication, run ingestion, and other high-volume tasks.                                                                                                                                                                                                                      |
| <a id="langsmith-playground" /> **LangSmith playground**                                                       | The playground is a service that handles forwarding requests to various LLM APIs to support the LangSmith Playground feature. This can also be used to connect to your own custom model servers.                                                                                                                                                         |
| <a id="langsmith-ace-arbitrary-code-execution-backend" /> **LangSmith ACE (Arbitrary Code Execution) backend** | The ACE backend is a service that handles executing arbitrary code in a secure environment. This is used to support running custom code within LangSmith.                                                                                                                                                                                                |

### Storage services

<Note>
  LangSmith will bundle all storage services by default. You can configure it to use external versions of all storage services. In a production setting, we **strongly recommend using external storage services**.
</Note>

| Service                                  | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| <a id="clickhouse" /> **ClickHouse**     | [ClickHouse](https://clickhouse.com/docs/en/intro) is a high-performance, column-oriented SQL database management system (DBMS) for online analytical processing (OLAP).<br /><br />LangSmith uses ClickHouse as the primary data store for traces and feedback (high-volume data).                                                                                                                                                                                      |
| <a id="postgresql" /> **PostgreSQL**     | [PostgreSQL](https://www.postgresql.org/about/) is a powerful, open source object-relational database system that uses and extends the SQL language combined with many features that safely store and scale the most complicated data workloads.<br /><br />LangSmith uses PostgreSQL as the primary data store for transactional workloads and operational data (almost everything besides traces and feedback).                                                        |
| <a id="redis" /> **Redis**               | [Redis](https://github.com/redis/redis) is a powerful in-memory key-value database that persists on disk. By holding data in memory, Redis offers high performance for operations like caching.<br /><br />LangSmith uses Redis to back queuing and caching operations.                                                                                                                                                                                                  |
| <a id="blob-storage" /> **Blob storage** | LangSmith supports several blob storage providers, including [AWS S3](https://aws.amazon.com/s3/), [Azure Blob Storage](https://azure.microsoft.com/en-us/services/storage/blobs/), and [Google Cloud Storage](https://cloud.google.com/storage).<br /><br />LangSmith uses blob storage to store large files, such as trace artifacts, feedback attachments, and other large data objects. Blob storage is optional, but highly recommended for production deployments. |

### Setup methods

* **Docker Compose** (development/testing only)
* **Kubernetes + Helm** (recommended for production)

### Setup guides

* [Install on Kubernetes](/langsmith/kubernetes) (production)
* [Install with Docker](/langsmith/docker) (development only)

## Enable LangSmith Deployment

**LangSmith Deployment** is an optional add-on that can be enabled on your [LangSmith](#langsmith) instance. It's ideal for enterprise teams who want a centralized, UI-driven platform to deploy and manage multiple agents and graphs, with all infrastructure, data, and orchestration fully under their control.

This includes everything from [LangSmith](#langsmith), plus:

| Component                                                                                                | Responsibilities                                                                                                                                    | Where it runs | Who manages it |
| -------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- | -------------- |
| <Tooltip tip="The LangSmith UI and APIs for managing deployments.">Control plane</Tooltip>               | <ul><li>UI for creating deployments & revisions</li><li>APIs for deployment management</li></ul>                                                    | Your cloud    | You            |
| <Tooltip tip="The runtime environment where your Agent Servers and agents execute.">Data plane</Tooltip> | <ul><li>Operator/listener to reconcile deployments</li><li>Agent Servers (agents/graphs)</li><li>Backing services (Postgres, Redis, etc.)</li></ul> | Your cloud    | You            |

You run both the control plane and the data plane entirely within your own infrastructure. You are responsible for provisioning and managing all components.

<Note>
  Learn more about the [control plane](/langsmith/control-plane) and [data plane](/langsmith/data-plane) architecture concepts.
</Note>

<img className="block dark:hidden" src="https://mintcdn.com/langchain-5e9cc07a/JOyLr_spVEW0t2KF/langsmith/images/full-platform-with-deployment-light.png?fit=max&auto=format&n=JOyLr_spVEW0t2KF&q=85&s=78861d689cf446190d0c1e80ed1a65dd" alt="Full platform architecture with control plane and data plane" data-og-width="2138" width="2138" data-og-height="2104" height="2104" data-path="langsmith/images/full-platform-with-deployment-light.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/JOyLr_spVEW0t2KF/langsmith/images/full-platform-with-deployment-light.png?w=280&fit=max&auto=format&n=JOyLr_spVEW0t2KF&q=85&s=28f2db3fb8d323baa1ed925fa39a0f82 280w, https://mintcdn.com/langchain-5e9cc07a/JOyLr_spVEW0t2KF/langsmith/images/full-platform-with-deployment-light.png?w=560&fit=max&auto=format&n=JOyLr_spVEW0t2KF&q=85&s=724b17ae55c6fc19c8ced2d8e081bcb3 560w, https://mintcdn.com/langchain-5e9cc07a/JOyLr_spVEW0t2KF/langsmith/images/full-platform-with-deployment-light.png?w=840&fit=max&auto=format&n=JOyLr_spVEW0t2KF&q=85&s=46d965e47f66ece91077b1dfdf56196b 840w, https://mintcdn.com/langchain-5e9cc07a/JOyLr_spVEW0t2KF/langsmith/images/full-platform-with-deployment-light.png?w=1100&fit=max&auto=format&n=JOyLr_spVEW0t2KF&q=85&s=d723ddff8b6942e8fcf15fe5523102b0 1100w, https://mintcdn.com/langchain-5e9cc07a/JOyLr_spVEW0t2KF/langsmith/images/full-platform-with-deployment-light.png?w=1650&fit=max&auto=format&n=JOyLr_spVEW0t2KF&q=85&s=06932f510e15f96376c67c790dcb31e3 1650w, https://mintcdn.com/langchain-5e9cc07a/JOyLr_spVEW0t2KF/langsmith/images/full-platform-with-deployment-light.png?w=2500&fit=max&auto=format&n=JOyLr_spVEW0t2KF&q=85&s=c482dbbe51709c394194bb3ea7842c09 2500w" />

<img className="hidden dark:block" src="https://mintcdn.com/langchain-5e9cc07a/JOyLr_spVEW0t2KF/langsmith/images/full-platform-with-deployment-dark.png?fit=max&auto=format&n=JOyLr_spVEW0t2KF&q=85&s=f5253bab42b0b351e1d13489fea4311b" alt="Full platform architecture with control plane and data plane" data-og-width="2138" width="2138" data-og-height="2104" height="2104" data-path="langsmith/images/full-platform-with-deployment-dark.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/JOyLr_spVEW0t2KF/langsmith/images/full-platform-with-deployment-dark.png?w=280&fit=max&auto=format&n=JOyLr_spVEW0t2KF&q=85&s=ba56323cd1e66109847f8adea173063c 280w, https://mintcdn.com/langchain-5e9cc07a/JOyLr_spVEW0t2KF/langsmith/images/full-platform-with-deployment-dark.png?w=560&fit=max&auto=format&n=JOyLr_spVEW0t2KF&q=85&s=6e529069bd427fde7c940ab944f0a1ba 560w, https://mintcdn.com/langchain-5e9cc07a/JOyLr_spVEW0t2KF/langsmith/images/full-platform-with-deployment-dark.png?w=840&fit=max&auto=format&n=JOyLr_spVEW0t2KF&q=85&s=ee4ed77d09b804dc2de32af0ddedbfbe 840w, https://mintcdn.com/langchain-5e9cc07a/JOyLr_spVEW0t2KF/langsmith/images/full-platform-with-deployment-dark.png?w=1100&fit=max&auto=format&n=JOyLr_spVEW0t2KF&q=85&s=ce52832ec7c18f9dc374546651545c42 1100w, https://mintcdn.com/langchain-5e9cc07a/JOyLr_spVEW0t2KF/langsmith/images/full-platform-with-deployment-dark.png?w=1650&fit=max&auto=format&n=JOyLr_spVEW0t2KF&q=85&s=8c8781ac82576d68faa8fc11c4b47a83 1650w, https://mintcdn.com/langchain-5e9cc07a/JOyLr_spVEW0t2KF/langsmith/images/full-platform-with-deployment-dark.png?w=2500&fit=max&auto=format&n=JOyLr_spVEW0t2KF&q=85&s=a0b4f5a8a31a23136d03160744305700 2500w" />

### Workflow

If you want to self-host LangSmith for observability, evaluation, and agent deployment, follow these steps:

<Steps>
  <Step title="Install self-hosted LangSmith">
    You must already have a [self-hosted LangSmith instance](#langsmith) installed in your cloud with a Kubernetes cluster (required for control plane and data plane).
  </Step>

  <Step title="Test your graph locally">
    Use `langgraph-cli` or [Studio](/langsmith/studio) to test your graph locally.
  </Step>

  <Step title="Enable LangSmith Deployment">
    Follow the [setup guide](/langsmith/deploy-self-hosted-full-platform) to enable LangSmith Deployment on your LangSmith instance.
  </Step>
</Steps>

## Standalone Server

The **Standalone server** option is the most lightweight and flexible way to run LangSmith. Unlike the other models, you only manage a simplified <Tooltip tip="The runtime environment where your Agent Servers and agents execute.">data plane</Tooltip> made up of Agent Servers and their required backing services (PostgreSQL, Redis, etc.).

This includes:

| Component         | Responsibilities                                              | Where it runs | Who manages it |
| ----------------- | ------------------------------------------------------------- | ------------- | -------------- |
| **Control plane** | n/a                                                           | n/a           | n/a            |
| **Data plane**    | <ul><li>Agent Servers</li><li>Postgres, Redis, etc.</li></ul> | Your cloud    | You            |

This option gives you full control over scaling, deployment, and CI/CD pipelines, while still allowing optional integration with LangSmith for tracing and evaluation.

<Warning>
  Do not run standalone servers in serverless environments. Scale-to-zero may cause task loss and scaling up will not work reliably.
</Warning>

<img className="block dark:hidden" src="https://mintcdn.com/langchain-5e9cc07a/Mwtbhvs2R50foe4Y/langsmith/images/standalone-server-light.png?fit=max&auto=format&n=Mwtbhvs2R50foe4Y&q=85&s=db67e2add4cf039b1ce2324fa1c1f244" alt="Standalone server architecture" data-og-width="752" width="752" data-og-height="821" height="821" data-path="langsmith/images/standalone-server-light.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/Mwtbhvs2R50foe4Y/langsmith/images/standalone-server-light.png?w=280&fit=max&auto=format&n=Mwtbhvs2R50foe4Y&q=85&s=e28c7f91a45d2608e74febe474066b27 280w, https://mintcdn.com/langchain-5e9cc07a/Mwtbhvs2R50foe4Y/langsmith/images/standalone-server-light.png?w=560&fit=max&auto=format&n=Mwtbhvs2R50foe4Y&q=85&s=6956b33b01bd4fa69269d890d09fa571 560w, https://mintcdn.com/langchain-5e9cc07a/Mwtbhvs2R50foe4Y/langsmith/images/standalone-server-light.png?w=840&fit=max&auto=format&n=Mwtbhvs2R50foe4Y&q=85&s=9e4727b09b6c88780787c6d6ff7bd490 840w, https://mintcdn.com/langchain-5e9cc07a/Mwtbhvs2R50foe4Y/langsmith/images/standalone-server-light.png?w=1100&fit=max&auto=format&n=Mwtbhvs2R50foe4Y&q=85&s=e380af553cd4dd0ddec93a44aee6ce09 1100w, https://mintcdn.com/langchain-5e9cc07a/Mwtbhvs2R50foe4Y/langsmith/images/standalone-server-light.png?w=1650&fit=max&auto=format&n=Mwtbhvs2R50foe4Y&q=85&s=5a0da7b4a6b3da6b5ac6fe804fe219b4 1650w, https://mintcdn.com/langchain-5e9cc07a/Mwtbhvs2R50foe4Y/langsmith/images/standalone-server-light.png?w=2500&fit=max&auto=format&n=Mwtbhvs2R50foe4Y&q=85&s=11f1fbd4fdbb59dd77ef3ebde76422f3 2500w" />

<img className="hidden dark:block" src="https://mintcdn.com/langchain-5e9cc07a/Mwtbhvs2R50foe4Y/langsmith/images/standalone-server-dark.png?fit=max&auto=format&n=Mwtbhvs2R50foe4Y&q=85&s=57ede6682332db867f1900200f675a5f" alt="Standalone server architecture" data-og-width="752" width="752" data-og-height="821" height="821" data-path="langsmith/images/standalone-server-dark.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/Mwtbhvs2R50foe4Y/langsmith/images/standalone-server-dark.png?w=280&fit=max&auto=format&n=Mwtbhvs2R50foe4Y&q=85&s=d38e2ee8deee27d3bbd2d465854bc850 280w, https://mintcdn.com/langchain-5e9cc07a/Mwtbhvs2R50foe4Y/langsmith/images/standalone-server-dark.png?w=560&fit=max&auto=format&n=Mwtbhvs2R50foe4Y&q=85&s=19f7f77f74f6c11c1b40c0169796cbe3 560w, https://mintcdn.com/langchain-5e9cc07a/Mwtbhvs2R50foe4Y/langsmith/images/standalone-server-dark.png?w=840&fit=max&auto=format&n=Mwtbhvs2R50foe4Y&q=85&s=68547f892a250fc426ce9f0dad79a80e 840w, https://mintcdn.com/langchain-5e9cc07a/Mwtbhvs2R50foe4Y/langsmith/images/standalone-server-dark.png?w=1100&fit=max&auto=format&n=Mwtbhvs2R50foe4Y&q=85&s=66b5b9d43d2d08cae16755d9f510d418 1100w, https://mintcdn.com/langchain-5e9cc07a/Mwtbhvs2R50foe4Y/langsmith/images/standalone-server-dark.png?w=1650&fit=max&auto=format&n=Mwtbhvs2R50foe4Y&q=85&s=1c045709ec08809225b084d8c850cdc2 1650w, https://mintcdn.com/langchain-5e9cc07a/Mwtbhvs2R50foe4Y/langsmith/images/standalone-server-dark.png?w=2500&fit=max&auto=format&n=Mwtbhvs2R50foe4Y&q=85&s=49c858d75788a600cdc558f78fa2dc41 2500w" />

### Workflow

1. Define and test your graph locally using the `langgraph-cli` or [Studio](/langsmith/studio)
2. Package your agent as a Docker image
3. Deploy the Agent Server to your compute platform of choice (Kubernetes, Docker, VM)
4. Optionally, configure LangSmith API keys and endpoints so the server reports traces and evaluations back to LangSmith (self-hosted or SaaS)

### Supported compute platforms

* **Kubernetes**: Use the LangSmith Helm chart to run Agent Servers in a Kubernetes cluster. This is the recommended option for production-grade deployments.

* **Docker**: Run in any Docker-supported compute platform (local dev machine, VM, ECS, etc.). This is best suited for development or small-scale workloads.

### Setup guide

<Tip>
  To set up an [Agent Server](/langsmith/agent-server), refer to the [how-to guide](/langsmith/deploy-standalone-server) in the application deployment section.
</Tip>

***

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/self-hosted.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.langchain.com/llms.txt