<!-- Source: https://docs.langchain.com/langsmith/deployments -->

**Start here if you’re building or operating agent applications.** This section is about deploying **your application**. If you need to set up LangSmith infrastructure, the [Platform setup section](/langsmith/platform-setup) covers infrastructure options (cloud, hybrid, self-hosted) and setup guides for hybrid and self-hosted deployments.

This section covers how to package, build, and deploy your _agents_ and applications as [Agent Servers](/langsmith/agent-server). A typical deployment workflow consists of the following steps:

1

Run your application on a local server.

2

Set up dependencies, project structure, and environment configuration.

3

(Required for deployment) Select Cloud, Hybrid, or Self-hosted.

4

Deploy your app

  * [**Cloud**](/langsmith/deploy-to-cloud): Push code from a git repository
  * [**Hybrid or Self-hosted with control plane**](/langsmith/deploy-with-control-plane): Build and push Docker images, deploy via UI
  * [**Standalone servers**](/langsmith/deploy-standalone-server): Deploy directly without control plane

5

Track traces, alerts, and dashboards.



What you’ll learn

  * Configure your [app for deployment](/langsmith/application-structure) (dependencies, [project setup](/langsmith/setup-app-requirements-txt), and [monorepo support](/langsmith/monorepo-support)).
  * Build, deploy, and update [Agent Servers](/langsmith/agent-server).
  * Secure your deployments with [authentication and access control](/langsmith/auth).
  * Customize your server runtime ([lifespan hooks](/langsmith/custom-lifespan), [middleware](/langsmith/custom-middleware), and [routes](/langsmith/custom-routes)).
  * Debug, observe, and troubleshoot deployed agents using the [Studio UI](/langsmith/studio).

## [Get started with deploymentPackage, build, and deploy your agents and graphs to Agent Server.Configure your app](/langsmith/application-structure)



Related

  * [Agent Server](/langsmith/agent-server)
  * [Application structure](/langsmith/application-structure)
  * [Local server testing](/langsmith/local-server)

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/deployments.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.