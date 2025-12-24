# Prompt engineering quickstart

Prompts guide the behavior of Large Language Models (LLM). [*Prompt engineering*](/langsmith/prompt-engineering-concepts) is the process of crafting, testing, and refining the instructions you give to an LLM so it produces reliable and useful responses.

LangSmith provides tools to create, version, test, and collaborate on prompts. You’ll also encounter common concepts like [*prompt templates*](/langsmith/prompt-engineering-concepts#prompts-vs-prompt-templates), which let you reuse structured prompts, and [*variables*](/langsmith/prompt-engineering-concepts#f-string-vs-mustache), which allow you to dynamically insert values (such as a user’s question) into a prompt.

In this quickstart, you’ll create, test, and improve prompts using either the UI or the SDK. This quickstart will use OpenAI as the example LLM provider, but the same workflow applies across other providers.

<Tip>
  If you prefer to watch a video on getting started with prompt engineering, refer to the quickstart [Video guide](#video-guide).
</Tip>

## Prerequisites

Before you begin, make sure you have:

* **A LangSmith account**: Sign up or log in at [smith.langchain.com](https://smith.langchain.com).
* **A LangSmith API key**: Follow the [Create an API key](/langsmith/create-account-api-key#create-an-api-key) guide.
* **An OpenAI API key**: Generate this from the [OpenAI dashboard](https://platform.openai.com/account/api-keys).

Select the tab for UI or SDK workflows:

<Tabs>
  <Tab title="UI" icon="window">
    ## 1. Set workspace secret

    In the [LangSmith UI](https://smith.langchain.com), ensure that your OpenAI API key is set as a [workspace secret](/langsmith/administration-overview#workspace-secrets).

    1. Navigate to <Icon icon="gear" /> **Settings** and then move to the **Secrets** tab.
    2. Select **Add secret** and enter the `OPENAI_API_KEY` and your API key as the **Value**.
    3. Select **Save secret**.

    <Note> When adding workspace secrets in the LangSmith UI, make sure the secret keys match the environment variable names expected by your model provider.</Note>

    ## 2. Create a prompt

    1. In the [LangSmith UI](https://smith.langchain.com), navigate to the **Prompts** section in the left-hand menu.
    2. Click on **+ Prompt** to create a prompt.
    3. Modify the prompt by editing or adding prompts and input variables as needed.

    <div style={{ textAlign: 'center' }}>
      <img className="block dark:hidden" src="https://mintcdn.com/langchain-5e9cc07a/t6ucb6rQa27Wd6Te/langsmith/images/create-a-prompt-light.png?fit=max&auto=format&n=t6ucb6rQa27Wd6Te&q=85&s=0cafd7b1330fd88caa7403772068a50d" alt="Prompt playground with the system prompt ready for editing." data-og-width="951" width="951" data-og-height="412" height="412" data-path="langsmith/images/create-a-prompt-light.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/t6ucb6rQa27Wd6Te/langsmith/images/create-a-prompt-light.png?w=280&fit=max&auto=format&n=t6ucb6rQa27Wd6Te&q=85&s=86270ac274480c09b4b772c79835c96a 280w, https://mintcdn.com/langchain-5e9cc07a/t6ucb6rQa27Wd6Te/langsmith/images/create-a-prompt-light.png?w=560&fit=max&auto=format&n=t6ucb6rQa27Wd6Te&q=85&s=0bba28323e21330632a3368603cfd436 560w, https://mintcdn.com/langchain-5e9cc07a/t6ucb6rQa27Wd6Te/langsmith/images/create-a-prompt-light.png?w=840&fit=max&auto=format&n=t6ucb6rQa27Wd6Te&q=85&s=7c6ec959c52230f4a9c1153e05c2a257 840w, https://mintcdn.com/langchain-5e9cc07a/t6ucb6rQa27Wd6Te/langsmith/images/create-a-prompt-light.png?w=1100&fit=max&auto=format&n=t6ucb6rQa27Wd6Te&q=85&s=3c76f683eb2ef9c71dc1a3d7e337fffb 1100w, https://mintcdn.com/langchain-5e9cc07a/t6ucb6rQa27Wd6Te/langsmith/images/create-a-prompt-light.png?w=1650&fit=max&auto=format&n=t6ucb6rQa27Wd6Te&q=85&s=b900411f7aa605f20f6c5182834bf4c3 1650w, https://mintcdn.com/langchain-5e9cc07a/t6ucb6rQa27Wd6Te/langsmith/images/create-a-prompt-light.png?w=2500&fit=max&auto=format&n=t6ucb6rQa27Wd6Te&q=85&s=b3b11c7507cc57b2fc178b251c0173dc 2500w" />

      <img className="hidden dark:block" src="https://mintcdn.com/langchain-5e9cc07a/t6ucb6rQa27Wd6Te/langsmith/images/create-a-prompt-dark.png?fit=max&auto=format&n=t6ucb6rQa27Wd6Te&q=85&s=16f217eb0e1c0b02ad0d7658f1a53f4d" alt="Prompt playground with the system prompt ready for editing." data-og-width="937" width="937" data-og-height="402" height="402" data-path="langsmith/images/create-a-prompt-dark.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/t6ucb6rQa27Wd6Te/langsmith/images/create-a-prompt-dark.png?w=280&fit=max&auto=format&n=t6ucb6rQa27Wd6Te&q=85&s=401ae88da122905ab2e820fc22ce1b37 280w, https://mintcdn.com/langchain-5e9cc07a/t6ucb6rQa27Wd6Te/langsmith/images/create-a-prompt-dark.png?w=560&fit=max&auto=format&n=t6ucb6rQa27Wd6Te&q=85&s=61c573f773dec1485545395c1fd37525 560w, https://mintcdn.com/langchain-5e9cc07a/t6ucb6rQa27Wd6Te/langsmith/images/create-a-prompt-dark.png?w=840&fit=max&auto=format&n=t6ucb6rQa27Wd6Te&q=85&s=0fd582cf184a36f1f2ce7dc21d7be9b9 840w, https://mintcdn.com/langchain-5e9cc07a/t6ucb6rQa27Wd6Te/langsmith/images/create-a-prompt-dark.png?w=1100&fit=max&auto=format&n=t6ucb6rQa27Wd6Te&q=85&s=32408b98f4df25413ba0e78b85c7b483 1100w, https://mintcdn.com/langchain-5e9cc07a/t6ucb6rQa27Wd6Te/langsmith/images/create-a-prompt-dark.png?w=1650&fit=max&auto=format&n=t6ucb6rQa27Wd6Te&q=85&s=102ecf375a8d66ac339b12bc163588e7 1650w, https://mintcdn.com/langchain-5e9cc07a/t6ucb6rQa27Wd6Te/langsmith/images/create-a-prompt-dark.png?w=2500&fit=max&auto=format&n=t6ucb6rQa27Wd6Te&q=85&s=3543f050b1e4e0e581c4386304284039 2500w" />
    </div>

    ## 3. Test a prompt

    1. Under the **Prompts** heading select the gear <Icon icon="gear" iconType="solid" /> icon next to the model name, which will launch the **Prompt Settings** window on the **Model Configuration** tab.

    2. Set the [model configuration](/langsmith/managing-model-configurations) you want to use. The **Provider** and **Model** you select will determine the parameters that are configurable on this configuration page. Once set, click **Save as**.

       <div style={{ textAlign: 'center' }}>
         <img className="block dark:hidden" src="https://mintcdn.com/langchain-5e9cc07a/6r3GRtwWCl4ozaHW/langsmith/images/model-config-light.png?fit=max&auto=format&n=6r3GRtwWCl4ozaHW&q=85&s=6c0f7d7012b1e5295fe545149f955e6b" alt="Model Configuration window in the LangSmith UI, settings for Provider, Model, Temperature, Max Output Tokens, Top P, Presence Penalty, Frequency Penalty, Reasoning Effort, etc." data-og-width="886" width="886" data-og-height="689" height="689" data-path="langsmith/images/model-config-light.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/6r3GRtwWCl4ozaHW/langsmith/images/model-config-light.png?w=280&fit=max&auto=format&n=6r3GRtwWCl4ozaHW&q=85&s=4e3b9ad92f6f14f4e0523bef50199318 280w, https://mintcdn.com/langchain-5e9cc07a/6r3GRtwWCl4ozaHW/langsmith/images/model-config-light.png?w=560&fit=max&auto=format&n=6r3GRtwWCl4ozaHW&q=85&s=e538eb740495a8afa8bfc552b13ae294 560w, https://mintcdn.com/langchain-5e9cc07a/6r3GRtwWCl4ozaHW/langsmith/images/model-config-light.png?w=840&fit=max&auto=format&n=6r3GRtwWCl4ozaHW&q=85&s=ebe73264e977153c869fd04d1552d09b 840w, https://mintcdn.com/langchain-5e9cc07a/6r3GRtwWCl4ozaHW/langsmith/images/model-config-light.png?w=1100&fit=max&auto=format&n=6r3GRtwWCl4ozaHW&q=85&s=2eeb01882056046bc73cc019d674af7e 1100w, https://mintcdn.com/langchain-5e9cc07a/6r3GRtwWCl4ozaHW/langsmith/images/model-config-light.png?w=1650&fit=max&auto=format&n=6r3GRtwWCl4ozaHW&q=85&s=8f28fe2fe8054cf0623fb9d17f91966f 1650w, https://mintcdn.com/langchain-5e9cc07a/6r3GRtwWCl4ozaHW/langsmith/images/model-config-light.png?w=2500&fit=max&auto=format&n=6r3GRtwWCl4ozaHW&q=85&s=cf9ad39be3623e73322d123699e73f19 2500w" />

         <img className="hidden dark:block" src="https://mintcdn.com/langchain-5e9cc07a/ppc8uxWc01j4q7Ia/langsmith/images/model-config-dark.png?fit=max&auto=format&n=ppc8uxWc01j4q7Ia&q=85&s=2e9da272c3fc8f7ac958c6e6d1da85e3" alt="Model Configuration window in the LangSmith UI, settings for Provider, Model, Temperature, Max Output Tokens, Top P, Presence Penalty, Frequency Penalty, Reasoning Effort, etc." data-og-width="881" width="881" data-og-height="732" height="732" data-path="langsmith/images/model-config-dark.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/ppc8uxWc01j4q7Ia/langsmith/images/model-config-dark.png?w=280&fit=max&auto=format&n=ppc8uxWc01j4q7Ia&q=85&s=652fb75a4682cfc813743a1260764e59 280w, https://mintcdn.com/langchain-5e9cc07a/ppc8uxWc01j4q7Ia/langsmith/images/model-config-dark.png?w=560&fit=max&auto=format&n=ppc8uxWc01j4q7Ia&q=85&s=02c980a8387f3d69a5870660b1668080 560w, https://mintcdn.com/langchain-5e9cc07a/ppc8uxWc01j4q7Ia/langsmith/images/model-config-dark.png?w=840&fit=max&auto=format&n=ppc8uxWc01j4q7Ia&q=85&s=ee633c06056fa7ad46ea58a179afa169 840w, https://mintcdn.com/langchain-5e9cc07a/ppc8uxWc01j4q7Ia/langsmith/images/model-config-dark.png?w=1100&fit=max&auto=format&n=ppc8uxWc01j4q7Ia&q=85&s=f62a35ed726b5f89c156a40c9ea76f2c 1100w, https://mintcdn.com/langchain-5e9cc07a/ppc8uxWc01j4q7Ia/langsmith/images/model-config-dark.png?w=1650&fit=max&auto=format&n=ppc8uxWc01j4q7Ia&q=85&s=18114575db8e6c7ce928763ddcb88c12 1650w, https://mintcdn.com/langchain-5e9cc07a/ppc8uxWc01j4q7Ia/langsmith/images/model-config-dark.png?w=2500&fit=max&auto=format&n=ppc8uxWc01j4q7Ia&q=85&s=ab24dc4975def52db55c4896ead5b77c 2500w" />
       </div>

    3. Specify the input variables you would like to test in the **Inputs** box and then click <Icon icon="circle-play" iconType="solid" /> **Start**.

       <div style={{ textAlign: 'center' }}>
         <img className="block dark:hidden" src="https://mintcdn.com/langchain-5e9cc07a/8DPu7MR3QecByOI5/langsmith/images/set-input-start-light.png?fit=max&auto=format&n=8DPu7MR3QecByOI5&q=85&s=bd86e76180c022a110ca0f0d9d19a198" alt="The input box with a question entered. The output box contains the response to the prompt." data-og-width="702" width="702" data-og-height="763" height="763" data-path="langsmith/images/set-input-start-light.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/8DPu7MR3QecByOI5/langsmith/images/set-input-start-light.png?w=280&fit=max&auto=format&n=8DPu7MR3QecByOI5&q=85&s=dc5f16c448685e182a0001b9dbcb1afd 280w, https://mintcdn.com/langchain-5e9cc07a/8DPu7MR3QecByOI5/langsmith/images/set-input-start-light.png?w=560&fit=max&auto=format&n=8DPu7MR3QecByOI5&q=85&s=372a5f62109cd09b57ba2ca11d73c65b 560w, https://mintcdn.com/langchain-5e9cc07a/8DPu7MR3QecByOI5/langsmith/images/set-input-start-light.png?w=840&fit=max&auto=format&n=8DPu7MR3QecByOI5&q=85&s=1fcd9d131af34af4b5e10ab5fea2a9f8 840w, https://mintcdn.com/langchain-5e9cc07a/8DPu7MR3QecByOI5/langsmith/images/set-input-start-light.png?w=1100&fit=max&auto=format&n=8DPu7MR3QecByOI5&q=85&s=f30ae237c4d2cf55918918eca39bb5e9 1100w, https://mintcdn.com/langchain-5e9cc07a/8DPu7MR3QecByOI5/langsmith/images/set-input-start-light.png?w=1650&fit=max&auto=format&n=8DPu7MR3QecByOI5&q=85&s=26326dd6839418f161f6393118f8c441 1650w, https://mintcdn.com/langchain-5e9cc07a/8DPu7MR3QecByOI5/langsmith/images/set-input-start-light.png?w=2500&fit=max&auto=format&n=8DPu7MR3QecByOI5&q=85&s=2654906d801046f11e6f96bfa7c7a59e 2500w" />

         <img className="hidden dark:block" src="https://mintcdn.com/langchain-5e9cc07a/8DPu7MR3QecByOI5/langsmith/images/set-input-start-dark.png?fit=max&auto=format&n=8DPu7MR3QecByOI5&q=85&s=bfd369e7426a57fc0cad75df8dd6942d" alt="The input box with a question entered. The output box contains the response to the prompt." data-og-width="698" width="698" data-og-height="769" height="769" data-path="langsmith/images/set-input-start-dark.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/8DPu7MR3QecByOI5/langsmith/images/set-input-start-dark.png?w=280&fit=max&auto=format&n=8DPu7MR3QecByOI5&q=85&s=9538e3e173a2f19994f08865a389f247 280w, https://mintcdn.com/langchain-5e9cc07a/8DPu7MR3QecByOI5/langsmith/images/set-input-start-dark.png?w=560&fit=max&auto=format&n=8DPu7MR3QecByOI5&q=85&s=fc8dc91b4564531bb5a27b971ca27c3e 560w, https://mintcdn.com/langchain-5e9cc07a/8DPu7MR3QecByOI5/langsmith/images/set-input-start-dark.png?w=840&fit=max&auto=format&n=8DPu7MR3QecByOI5&q=85&s=ae9db3c1ec55c4653ad86b95addeec12 840w, https://mintcdn.com/langchain-5e9cc07a/8DPu7MR3QecByOI5/langsmith/images/set-input-start-dark.png?w=1100&fit=max&auto=format&n=8DPu7MR3QecByOI5&q=85&s=0f169783a075952a0066de46aeb3bdc7 1100w, https://mintcdn.com/langchain-5e9cc07a/8DPu7MR3QecByOI5/langsmith/images/set-input-start-dark.png?w=1650&fit=max&auto=format&n=8DPu7MR3QecByOI5&q=85&s=686196a3493642cf70ff89aa235a6715 1650w, https://mintcdn.com/langchain-5e9cc07a/8DPu7MR3QecByOI5/langsmith/images/set-input-start-dark.png?w=2500&fit=max&auto=format&n=8DPu7MR3QecByOI5&q=85&s=0532f0c8cf0ff37ed7c9da7a67bf6700 2500w" />
       </div>

       To learn about more options for configuring your prompt in the Playground, refer to [Configure prompt settings](/langsmith/managing-model-configurations).

    4. After testing and refining your prompt, click **Save** to store it for future use.

    ## 4. Iterate on a prompt

    LangSmith allows for team-based prompt iteration. [Workspace](/langsmith/administration-overview#workspaces) members can experiment with prompts in the playground and save their changes as a new [*commit*](/langsmith/prompt-engineering-concepts#commits) when ready.

    To improve your prompts:

    * Reference the documentation provided by your model provider for best practices in prompt creation, such as:
      * [Best practices for prompt engineering with the OpenAI API](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api)
      * [Gemini's Introduction to prompt design](https://ai.google.dev/gemini-api/docs/prompting-intro)
    * Build and refine your prompts with the Prompt Canvas—an interactive tool in LangSmith. Learn more in the [Prompt Canvas guide](/langsmith/write-prompt-with-ai).
    * Tag specific commits to mark important moments in your commit history.

      1. To create a commit, navigate to the **Playground** and select **Commit**. Choose the prompt to commit changes to and then **Commit**.
      2. Navigate to **Prompts** in the left-hand menu. Select the prompt. Once on the prompt's detail page, move to the **Commits** tab. Find the tag icon <Icon icon="tag" iconType="solid" /> to **Add a Commit Tag**.

      <div style={{ textAlign: 'center' }}>
        <img className="block dark:hidden" src="https://mintcdn.com/langchain-5e9cc07a/7n0eM_8e3pn_DFNx/langsmith/images/add-commit-tag-light.png?fit=max&auto=format&n=7n0eM_8e3pn_DFNx&q=85&s=80e7b49cb4036e15369c9e417d1d63ad" alt="The tag, the commit tag box with the commit label, and the commit tag name box to create the tag." data-og-width="702" width="702" data-og-height="226" height="226" data-path="langsmith/images/add-commit-tag-light.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/7n0eM_8e3pn_DFNx/langsmith/images/add-commit-tag-light.png?w=280&fit=max&auto=format&n=7n0eM_8e3pn_DFNx&q=85&s=bbed6d72fa9986d211195f7cb6e3bbc3 280w, https://mintcdn.com/langchain-5e9cc07a/7n0eM_8e3pn_DFNx/langsmith/images/add-commit-tag-light.png?w=560&fit=max&auto=format&n=7n0eM_8e3pn_DFNx&q=85&s=93623e1b7ae7b4c9826c7a76694dd43d 560w, https://mintcdn.com/langchain-5e9cc07a/7n0eM_8e3pn_DFNx/langsmith/images/add-commit-tag-light.png?w=840&fit=max&auto=format&n=7n0eM_8e3pn_DFNx&q=85&s=c9ccfe378c982af55b6781691b0c6a1b 840w, https://mintcdn.com/langchain-5e9cc07a/7n0eM_8e3pn_DFNx/langsmith/images/add-commit-tag-light.png?w=1100&fit=max&auto=format&n=7n0eM_8e3pn_DFNx&q=85&s=d9464f4655a0ba67b81916eb9e69cdbc 1100w, https://mintcdn.com/langchain-5e9cc07a/7n0eM_8e3pn_DFNx/langsmith/images/add-commit-tag-light.png?w=1650&fit=max&auto=format&n=7n0eM_8e3pn_DFNx&q=85&s=43b3ad05600b7c9e0883541acccb1cc5 1650w, https://mintcdn.com/langchain-5e9cc07a/7n0eM_8e3pn_DFNx/langsmith/images/add-commit-tag-light.png?w=2500&fit=max&auto=format&n=7n0eM_8e3pn_DFNx&q=85&s=69019a8aad0d4733333f0f69ad468171 2500w" />

        <img className="hidden dark:block" src="https://mintcdn.com/langchain-5e9cc07a/7n0eM_8e3pn_DFNx/langsmith/images/add-commit-tag-dark.png?fit=max&auto=format&n=7n0eM_8e3pn_DFNx&q=85&s=80883a09fbaea8c892d0a7de88f7a6ca" alt="The tag, the commit tag box with the commit label, and the commit tag name box to create the tag." data-og-width="698" width="698" data-og-height="221" height="221" data-path="langsmith/images/add-commit-tag-dark.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/7n0eM_8e3pn_DFNx/langsmith/images/add-commit-tag-dark.png?w=280&fit=max&auto=format&n=7n0eM_8e3pn_DFNx&q=85&s=0c7eb9c966673a410811a5a08a39cbf7 280w, https://mintcdn.com/langchain-5e9cc07a/7n0eM_8e3pn_DFNx/langsmith/images/add-commit-tag-dark.png?w=560&fit=max&auto=format&n=7n0eM_8e3pn_DFNx&q=85&s=9976856ffeca88d9f8d856e0d7766613 560w, https://mintcdn.com/langchain-5e9cc07a/7n0eM_8e3pn_DFNx/langsmith/images/add-commit-tag-dark.png?w=840&fit=max&auto=format&n=7n0eM_8e3pn_DFNx&q=85&s=9a79984ca88bd3fa74b512ce8b26430b 840w, https://mintcdn.com/langchain-5e9cc07a/7n0eM_8e3pn_DFNx/langsmith/images/add-commit-tag-dark.png?w=1100&fit=max&auto=format&n=7n0eM_8e3pn_DFNx&q=85&s=82c269188447b9ecf9f7ff17fa9805ec 1100w, https://mintcdn.com/langchain-5e9cc07a/7n0eM_8e3pn_DFNx/langsmith/images/add-commit-tag-dark.png?w=1650&fit=max&auto=format&n=7n0eM_8e3pn_DFNx&q=85&s=83e03a2d056fc81440e6f11acfa1479c 1650w, https://mintcdn.com/langchain-5e9cc07a/7n0eM_8e3pn_DFNx/langsmith/images/add-commit-tag-dark.png?w=2500&fit=max&auto=format&n=7n0eM_8e3pn_DFNx&q=85&s=cc7d694fc1cc6c4a76c7dca4a9ed9dc4 2500w" />
      </div>
  </Tab>

  <Tab title="SDK" icon="code">
    ## 1. Set up your environment

    1. In your terminal, prepare your environment:

       <CodeGroup>
         ```bash Python theme={null}
         mkdir ls-prompt-quickstart && cd ls-prompt-quickstart
         python -m venv .venv
         source .venv/bin/activate
         pip install -qU langsmith openai langchain_core
         ```

         ```bash TypeScript theme={null}
         mkdir ls-prompt-quickstart-ts && cd ls-prompt-quickstart-ts
         npm init -y
         npm install langsmith openai typescript ts-node
         npx tsc --init
         ```
       </CodeGroup>

    2. Set your API keys:

       ```bash  theme={null}
       export LANGSMITH_API_KEY='<your_api_key>'
       export OPENAI_API_KEY='<your_api_key>'
       ```

    ## 2. Create a prompt

    To create a prompt, you'll define a list of messages that you want in your prompt and then push to LangSmith.

    Use the language-specific constructor and push method:

    * Python: [`ChatPromptTemplate`](https://reference.langchain.com/python/langchain_core/prompts/#langchain_core.prompts.chat.ChatPromptTemplate) → [`client.push_prompt(...)`](https://docs.smith.langchain.com/reference/python/client/langsmith.client.Client#langsmith.client.Client.push_prompt)
    * TypeScript: [`ChatPromptTemplate.fromMessages(...)`](https://v03.api.js.langchain.com/classes/_langchain_core.prompts.ChatPromptTemplate.html#fromMessages) → [`client.pushPrompt(...)`](https://langsmith-docs-7jgx2bq8f-langchain.vercel.app/reference/js/classes/client.Client#pushprompt)

    1. Add the following code to a `create_prompt` file:

       <CodeGroup>
         ```python Python theme={null}
         from langsmith import Client
         from langchain_core.prompts import ChatPromptTemplate

         client = Client()

         prompt = ChatPromptTemplate([
             ("system", "You are a helpful chatbot."),
             ("user", "{question}"),
         ])

         client.push_prompt("prompt-quickstart", object=prompt)
         ```

         ```typescript TypeScript theme={null}
         import { Client } from "langsmith";
         import { ChatPromptTemplate } from "@langchain/core/prompts";

         const client = new Client();

         const prompt = ChatPromptTemplate.fromMessages([
         ["system", "You are a helpful chatbot."],
         ["user", "{question}"],
         ]);

         await client.pushPrompt("prompt-quickstart", {
         object: prompt,
         });
         ```
       </CodeGroup>

       This creates an ordered list of messages, wraps them in `ChatPromptTemplate`, and then pushes the prompt by name to your [workspace](/langsmith/administration-overview#workspaces) for versioning and reuse.

    2. Run `create_prompt`:

       <CodeGroup>
         ```python Python theme={null}
         python create_prompt.py
         ```

         ```typescript TypeScript theme={null}
         npx tsx create_prompt.ts
         ```
       </CodeGroup>

    Follow the resulting link to view the newly created Prompt Hub prompt in the LangSmith UI.

    ## 3. Test a prompt

    In this step, you'll pull the prompt you created in [step 2](#2-create-a-prompt) by name (`"prompt-quickstart"`), format it with a test input, convert it to OpenAI’s chat format, and call the OpenAI Chat Completions API.

    Then, you'll iterate on the prompt by creating a new version. Members of your workspace can open an existing prompt, experiment with changes in the [UI](https://smith.langchain.com), and save those changes as a new commit on the same prompt, which preserves history for the whole team.

    1. Add the following to a `test_prompt` file:

       <CodeGroup>
         ```python Python theme={null}
         from langsmith import Client
         from openai import OpenAI
         from langchain_core.messages import convert_to_openai_messages

         client = Client()
         oai_client = OpenAI()

         prompt = client.pull_prompt("prompt-quickstart")

         # Since the prompt only has one variable you could also pass in the value directly
         # Equivalent to formatted_prompt = prompt.invoke("What is the color of the sky?")
         formatted_prompt = prompt.invoke({"question": "What is the color of the sky?"})

         response = oai_client.chat.completions.create(
             model="gpt-4o",
             messages=convert_to_openai_messages(formatted_prompt.messages),
         )
         ```

         ```typescript TypeScript theme={null}
         import { OpenAI } from "openai";
         import { pull } from "langchain/hub"
         import { convertPromptToOpenAI } from "@langchain/openai";

         const oaiClient = new OpenAI();

         const prompt = await pull("prompt-quickstart");

         // Format the prompt with the question
         const formattedPrompt = await prompt.invoke({ question: "What is the color of the sky?" });

         const response = await oaiClient.chat.completions.create({
             model: "gpt-4o",
             messages: convertPromptToOpenAI(formattedPrompt).messages,
         });
         ```
       </CodeGroup>

       This loads the prompt by name using `pull` for the latest committed version of the prompt that you're testing. You can also specify a specific commit by passing the commit hash `"<prompt-name>:<commit-hash>"`

    2. Run `test_prompt` :

       <CodeGroup>
         ```python Python theme={null}
         python test_prompt.py
         ```

         ```typescript TypeScript theme={null}
         npx tsx test_prompt.ts
         ```
       </CodeGroup>

    3. To create a new version of a prompt, call the same push method you used initially with the same prompt name and your updated template. LangSmith will record it as a new commit and preserve prior versions.

       Copy the following code to an `iterate_prompt` file:

       <CodeGroup>
         ```python Python theme={null}
         from langsmith import Client
         from langchain_core.prompts import ChatPromptTemplate

         client = Client()

         new_prompt = ChatPromptTemplate([
             ("system", "You are a helpful chatbot. Respond in Spanish."),
             ("user", "{question}"),
         ])

         client.push_prompt("prompt-quickstart", object=new_prompt)
         ```

         ```typescript TypeScript theme={null}
         import { Client } from "langsmith";
         import { ChatPromptTemplate } from "@langchain/core/prompts";

         const client = new Client();

         const newPrompt = ChatPromptTemplate.fromMessages([
             ["system", "You are a helpful chatbot. Speak in Spanish."],
             ["user", "{question}"]
         ]);

         await client.pushPrompt("prompt-quickstart", {
             object: newPrompt
         });
         ```
       </CodeGroup>

    4. Run `iterate_prompt` :

       <CodeGroup>
         ```python Python theme={null}
         python iterate_prompt.py
         ```

         ```typescript TypeScript theme={null}
         npx tsx iterate_prompt.ts
         ```
       </CodeGroup>

       Now your prompt will contain two commits.

    To improve your prompts:

    * Reference the documentation provided by your model provider for best practices in prompt creation, such as:
      * [Best practices for prompt engineering with the OpenAI API](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api)
      * [Gemini's Introduction to prompt design](https://ai.google.dev/gemini-api/docs/prompting-intro)
    * Build and refine your prompts with the Prompt Canvas—an interactive tool in LangSmith. Learn more in the [Prompt Canvas guide](/langsmith/write-prompt-with-ai).
  </Tab>
</Tabs>

## Next steps

* Learn more about how to store and manage prompts using the Prompt Hub in the [Create a prompt guide](/langsmith/create-a-prompt).
* Learn how to set up the Playground to [Test multi-turn conversations](/langsmith/multiple-messages) in this tutorial.
* Learn how to test your prompt's performance over a dataset instead of individual examples, refer to [Run an evaluation from the Prompt Playground](/langsmith/run-evaluation-from-prompt-playground).

<Callout type="info" icon="bird">
  Use **[Polly](/langsmith/polly)** in the Playground to help optimize your prompts, generate tools, and create output schemas.
</Callout>

## Video guide

<iframe className="w-full aspect-video rounded-xl" src="https://www.youtube.com/embed/h4f6bIWGkog?si=IVJFfhldC7M3HL4G" title="YouTube video player" frameBorder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowFullScreen />

***

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/prompt-engineering-quickstart.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.langchain.com/llms.txt