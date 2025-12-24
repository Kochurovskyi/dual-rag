# Use annotation queues

*Annotation queues* provide a streamlined, directed view for human annotators to attach feedback to specific [runs](/langsmith/observability-concepts#runs). While you can always annotate [traces](/langsmith/observability-concepts#traces) inline, annotation queues provide a way to group runs together, prescribe rubrics, and track reviewer progress.

LangSmith supports two queue styles:

* [**Single-run annotation queues**](#single-run-annotation-queues) present one run at a time and let reviewers submit any rubric feedback you configure.
* [**Pairwise annotation queues (PAQs)**](#pairwise-annotation-queues) present two runs side-by-side so reviewers can quickly decide which output is better (or if they are equivalent) against the rubric items you define.

## Single-run annotation queues

Single-run queues present one run at a time and let reviewers submit any rubric feedback you configure. They can be created directly from the **Annotation queues** section in the [LangSmith UI](https://smith.langchain.com/).

### Create a single-run queue

1. Navigate to **Annotation queues** in the left navigation.
2. Click **+ New annotation queue** in the top-right corner.

   <img src="https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/create-annotation-queue-new.png?fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=c5c28c10a5522af0a37f40236ed57510" alt="Create Annotation Queue form with Basic Details, Annotation Rubric, and Feedback sections." data-og-width="3456" width="3456" data-og-height="1912" height="1912" data-path="langsmith/images/create-annotation-queue-new.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/create-annotation-queue-new.png?w=280&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=daa5c44976804eae5ca8bbfef1d0a9d0 280w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/create-annotation-queue-new.png?w=560&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=167955e0202671425e6cd1476c31a756 560w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/create-annotation-queue-new.png?w=840&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=71627eeab271c6d4581f00506731cc09 840w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/create-annotation-queue-new.png?w=1100&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=cd30341efa9d5eea82d85b63518b53a0 1100w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/create-annotation-queue-new.png?w=1650&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=3e71d31b42b3411946f73d79e8735599 1650w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/create-annotation-queue-new.png?w=2500&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=832e7c8b99d332176bc9d9de702a6bac 2500w" />

#### Basic Details

1. Fill in the **Name** and **Description** of the queue.
2. Optionally assign a **default dataset** to streamline exporting reviewed runs into a dataset in your LangSmith [workspace](/langsmith/administration-overview#workspaces).

#### Annotation Rubric

1. Draft some high-level instructions for your annotators, which will be shown in the sidebar on every run.
2. Click **+ Desired Feedback** to add feedback keys to your annotation queue. Annotators will be presented with these feedback keys on each run.
3. Add a description for each, as well as a short description of each category, if the feedback is categorical.

   <img src="https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/create-annotation-rubric.png?fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=8adfdba2649847f82543674978b0d1b1" alt="Annotation queue rubric form with instructions and desired feedback entered." data-og-width="3456" width="3456" data-og-height="1914" height="1914" data-path="langsmith/images/create-annotation-rubric.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/create-annotation-rubric.png?w=280&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=5d73a7688b61b3b9489aacac1223f7c6 280w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/create-annotation-rubric.png?w=560&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=ede9b22be4e3ce82e4feabf86575e8a5 560w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/create-annotation-rubric.png?w=840&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=768747aa9e314c66631f27e794d9174b 840w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/create-annotation-rubric.png?w=1100&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=f3061b6ba68c4d9cab997bbed2efe76e 1100w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/create-annotation-rubric.png?w=1650&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=27545c5b64b3b82ae9ebed853ff02168 1650w, https://mintcdn.com/langchain-5e9cc07a/aKRoUGXX6ygp4DlC/langsmith/images/create-annotation-rubric.png?w=2500&fit=max&auto=format&n=aKRoUGXX6ygp4DlC&q=85&s=801397056da06004808b6c38df30c139 2500w" />

   For example, with the descriptions in the previous screenshot, reviewers will see the **Annotation Rubric** details in the right-hand pane of the UI.

   <img src="https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/rubric-for-annotators.png?fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=44452f7da89329acc06672beba4e4c0e" alt="The rendered rubric for reviewers from the example instructions." data-og-width="3456" width="3456" data-og-height="1912" height="1912" data-path="langsmith/images/rubric-for-annotators.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/rubric-for-annotators.png?w=280&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=fa18a86229854c27a85c341da2638501 280w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/rubric-for-annotators.png?w=560&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=67f5880b9d79e05e2dcd3703db92f79a 560w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/rubric-for-annotators.png?w=840&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=01436264374f87f9baab4ac4f3f8c161 840w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/rubric-for-annotators.png?w=1100&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=80b8569a8ef3acc5b7d94a9276dc0d26 1100w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/rubric-for-annotators.png?w=1650&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=b4c6f43fe2e91f57de4a2790757a2083 1650w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/rubric-for-annotators.png?w=2500&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=aae4a68208b5b6838c3fdf77f2c57efe 2500w" />

#### Collaborator Settings

When there are multiple annotators for a run:

* **Number of reviewers per run**: This determines the number of reviewers that must mark a run as **Done** for it to be removed from the queue. If you check **All workspace members review each run**, then a run will remain in the queue until all [workspace](/langsmith/administration-overview#workspaces) members have marked their review as **Done**.

  * Reviewers cannot view the feedback left by other reviewers.
  * Comments on runs are visible to all reviewers.

* **Enable reservations on runs**: When a reviewer views a run, the run is reserved for that reviewer for the specified **Reservation length**. If there are multiple reviewers per run as specified above, the run can be reserved by multiple reviewers (up to the number of reviewers per run) at the same time.

  <Tip>
    We recommend enabling reservations. This will prevent multiple annotators from reviewing the same run at the same time.
  </Tip>

  If a reviewer has viewed a run and then leaves the run without marking it **Done**, the reservation will expire after the specified **Reservation length**. The run is then released back into the queue and can be reserved by another reviewer.

  <Note>
    Clicking **Requeue** for a run's annotation will only move the current run to the end of the current user's queue; it won't affect the queue order of any other user. It will also release the reservation that the current user has on that run.
  </Note>

Because of these settings, the number of runs visible to each reviewer can differ from the total queue size.

You can revisit the pencil icon <Icon icon="pencil" /> in **Annotation queues** to update any settings later.

### Assign runs to a single-run queue

There are several ways to populate a single-run queue with work items:

* **From a trace view**: Click **Add to Annotation Queue** in the top-right corner of any [trace](/langsmith/observability-concepts#traces) view. You can add any intermediate [run](/langsmith/observability-concepts#runs), but not the root span.

  <img src="https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/add-to-annotation-queue.png?fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=fc604c7f91bc8795dc688c4f9db73ce9" alt="Trace view with the Add to Annotation Queue button highlighted at the top of the screen." data-og-width="1373" width="1373" data-og-height="1028" height="1028" data-path="langsmith/images/add-to-annotation-queue.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/add-to-annotation-queue.png?w=280&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=0ff1545d09984dfb766067ad65ecbfb9 280w, https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/add-to-annotation-queue.png?w=560&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=055554579c01cc8c48471e0d74fe27d6 560w, https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/add-to-annotation-queue.png?w=840&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=10412c26d4042358e098631386cddbf2 840w, https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/add-to-annotation-queue.png?w=1100&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=be2c6162599ab18ef34975a439f16e93 1100w, https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/add-to-annotation-queue.png?w=1650&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=4e0b51a16246b1e28d415f23d86643c7 1650w, https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/add-to-annotation-queue.png?w=2500&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=c7744f75389cd270f60bbbee9571582a 2500w" />

* **From the runs table**: Select multiple runs, then click **Add to Annotation Queue** at the bottom of the page.

  <img src="https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/multi-select-annotation-queue.png?fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=c6781e6a7345ef7e16ea7a0bb306a474" alt="View of the runs table with runs selected. Add to Annotation Queue button at the botton of the page." data-og-width="1323" width="1323" data-og-height="1317" height="1317" data-path="langsmith/images/multi-select-annotation-queue.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/multi-select-annotation-queue.png?w=280&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=03fff2a1f8cc40bf86f4b9251dacc0e1 280w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/multi-select-annotation-queue.png?w=560&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=2cc50c1d4f1b9ec24f9e3bc4d5fabbff 560w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/multi-select-annotation-queue.png?w=840&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=b37ce7b181457582652a22405f240750 840w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/multi-select-annotation-queue.png?w=1100&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=badc9ef126c220b9aa8f5e8212421b93 1100w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/multi-select-annotation-queue.png?w=1650&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=ae02333d194a955c1a6c86a2bf87c75f 1650w, https://mintcdn.com/langchain-5e9cc07a/4kN8yiLrZX_amfFn/langsmith/images/multi-select-annotation-queue.png?w=2500&fit=max&auto=format&n=4kN8yiLrZX_amfFn&q=85&s=9dce63a0eedfc4a02a5ad822cee67bce 2500w" />

* **Automation rules**: [Set up a rule](/langsmith/rules) to automatically assign runs that match a filter (for example, errors or low user scores) into a queue.

* **Datasets & experiments**: Select one or more [experiments](/langsmith/evaluation-concepts#experiment) within a dataset and click **<Icon icon="pencil" /> Annotate**. Choose an existing queue or create a new one, then confirm the (single-run) queue option.

  <img src="https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/annotate-experiment.png?fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=7622e6db855711542de24270ddc129dc" alt="Selected experiments with the Annotate button at the bottom of the page." data-og-width="3456" width="3456" data-og-height="1914" height="1914" data-path="langsmith/images/annotate-experiment.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/annotate-experiment.png?w=280&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=6bc0abf70504c439b413dfb6a3ff59f7 280w, https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/annotate-experiment.png?w=560&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=c511826c68b2ecf9fb75addc50df48c3 560w, https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/annotate-experiment.png?w=840&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=450345b069f8de91a982d66bfe6ce8a9 840w, https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/annotate-experiment.png?w=1100&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=fb67c24cd3f6fee0042ad3ef94fc9a59 1100w, https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/annotate-experiment.png?w=1650&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=83aab2b2cd3cc7a84440caa0d57a68be 1650w, https://mintcdn.com/langchain-5e9cc07a/E8FdemkcQxROovD9/langsmith/images/annotate-experiment.png?w=2500&fit=max&auto=format&n=E8FdemkcQxROovD9&q=85&s=08a045816ca42285ad46570280ee7061 2500w" />

### Review a single-run queue

1. Navigate to the **Annotation Queues** section through the left-hand navigation bar.
2. Click on the queue you want to review. This will take you to a focused, cyclical view of the runs in the queue that require review.
3. You can attach a comment, attach a score for a particular [feedback](/langsmith/observability-concepts#feedback) criteria, add the run to a dataset or mark the run as reviewed. You can also remove the run from the queue for all users, despite any current reservations or settings for the queue, by clicking the **Trash** icon <Icon icon="trash" /> next to **View run**.

   <Tip>
     The keyboard shortcuts that are next to each option can help streamline the review process.
   </Tip>

   <img src="https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/review-runs.png?fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=9065d4b85e6165084b65d3908d61778a" alt="View or a run with the Annotate side panel. Keyboard shortcuts visible for options." data-og-width="1532" width="1532" data-og-height="1080" height="1080" data-path="langsmith/images/review-runs.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/review-runs.png?w=280&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=f69f94916e247ff498e1d9e5ed2755a2 280w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/review-runs.png?w=560&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=64f16b8b83ffc56d1ad078ae1bfacd65 560w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/review-runs.png?w=840&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=085b9e1ea9b3797bc10117c326a80018 840w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/review-runs.png?w=1100&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=4321324e5d276d12864e446cd2a97c82 1100w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/review-runs.png?w=1650&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=7eeb685e4d4064518613283e502c9395 1650w, https://mintcdn.com/langchain-5e9cc07a/Fr2lazPB4XVeEA7l/langsmith/images/review-runs.png?w=2500&fit=max&auto=format&n=Fr2lazPB4XVeEA7l&q=85&s=059f57fb238aa0cd1ebcf6a2fb0ede95 2500w" />

## Pairwise annotation queues

Pairwise annotation queues (PAQs) present two runs side-by-side so reviewers can quickly decide which output is better (or if they are equivalent) against the rubric items you define. They are designed for fast A/B comparisons between two experiments (often a baseline vs. a candidate model) and must be created from the **Datasets & Experiments** pages.

### Create a pairwise queue

1. Navigate to **Datasets & Experiments**, open a dataset, and select **exactly two experiments** you want to compare.

2. Click **Annotate**. In the popover, choose **Add to Pairwise Annotation Queue**. (The button is disabled until exactly two experiments are selected.)

   <img src="https://mintcdn.com/langchain-5e9cc07a/jimZt8pd1vc7LfPM/langsmith/images/pairwise-annotation-queue-popup.png?fit=max&auto=format&n=jimZt8pd1vc7LfPM&q=85&s=ef08b7166abce2d890ba4b9be8cae927" alt="Popover showing the &#x22;Add to Pairwise Annotation Queue&#x22; card highlighted after two experiments are selected." data-og-width="3456" width="3456" data-og-height="1980" height="1980" data-path="langsmith/images/pairwise-annotation-queue-popup.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/jimZt8pd1vc7LfPM/langsmith/images/pairwise-annotation-queue-popup.png?w=280&fit=max&auto=format&n=jimZt8pd1vc7LfPM&q=85&s=96d0a67c3745542396ee4940228ffa1c 280w, https://mintcdn.com/langchain-5e9cc07a/jimZt8pd1vc7LfPM/langsmith/images/pairwise-annotation-queue-popup.png?w=560&fit=max&auto=format&n=jimZt8pd1vc7LfPM&q=85&s=fc02da4f82cab44767aa74c3e418de59 560w, https://mintcdn.com/langchain-5e9cc07a/jimZt8pd1vc7LfPM/langsmith/images/pairwise-annotation-queue-popup.png?w=840&fit=max&auto=format&n=jimZt8pd1vc7LfPM&q=85&s=8b719d329f260dfa8f0869f089a9caa5 840w, https://mintcdn.com/langchain-5e9cc07a/jimZt8pd1vc7LfPM/langsmith/images/pairwise-annotation-queue-popup.png?w=1100&fit=max&auto=format&n=jimZt8pd1vc7LfPM&q=85&s=2475caf18fde10b9f4539553d3963211 1100w, https://mintcdn.com/langchain-5e9cc07a/jimZt8pd1vc7LfPM/langsmith/images/pairwise-annotation-queue-popup.png?w=1650&fit=max&auto=format&n=jimZt8pd1vc7LfPM&q=85&s=c829586016d288d59e1c8158870a8ad1 1650w, https://mintcdn.com/langchain-5e9cc07a/jimZt8pd1vc7LfPM/langsmith/images/pairwise-annotation-queue-popup.png?w=2500&fit=max&auto=format&n=jimZt8pd1vc7LfPM&q=85&s=f91c18ad5c0c2e4b85092fe2a113a0af 2500w" />

3. Decide whether to send the experiments to an existing pairwise queue or create a new one.

4. Provide the queue details:
   * **Basic details** (name and description)
   * **Instructions & rubrics** tailored to pairwise scoring
   * **Collaborator settings** (reviewer count, reservations, reservation length)

5. Submit the form to create the queue. LangSmith immediately pairs runs from the two experiments and populates the queue.

Key differences for PAQs:

* **Experiments**: You must provide two experiment sessions up front. LangSmith automatically pairs their runs in chronological order and populates the queue during creation.
* **Rubric**: Pairwise rubric items only require a feedback key and (optionally) a description. Annotators decide whether Run A, Run B, or both are better for each rubric item.
* **Dataset**: Pairwise queues do not use a default dataset, because comparisons span two experiments.
* **Reservations & reviewers**: The same collaborator controls apply. Reservations help prevent two people from judging the same comparison simultaneously.

### Add more comparisons to a pairwise queue

If you need to add more comparisons later, return to **Datasets & Experiments**, select the two experiments again, and choose **Add to Pairwise Annotation Queue** to append new pairs.

Selecting two experiments and creating a PAQ automatically pairs the runs. When augmenting an existing PAQ, LangSmith preserves historical comparisons and appends new pairs to the queue.

### Review a pairwise queue

1. From **Annotation queues**, select the pairwise queue you want to review.
2. Each queue item displays Run A on the left and Run B on the right, along with your rubric.
3. For every rubric item:
   * Choose **A is better**, **B is better**, or **Equal**. The UI records binary feedback on both runs behind the scenes.
   * Use hotkeys `A`, `B`, or `E` to lock in your choice.
4. Once you finish all rubric items, press **Done** (or `Enter` on the final rubric item) to advance to the next comparison.
5. Optional actions:
   * Leave comments tied to either run.
   * Requeue the comparison if you need to revisit it later.
   * Open the full trace view for deeper debugging.

Reservations, reviewer thresholds, and comments behave identically to those in single-run queues, enabling teams to use different queue types without modifying their existing workflow.

<img src="https://mintcdn.com/langchain-5e9cc07a/jimZt8pd1vc7LfPM/langsmith/images/pairwise-annotation-queue-review-feedback-pane.png?fit=max&auto=format&n=jimZt8pd1vc7LfPM&q=85&s=b144d168c4f4fd1f624c1d0fd5ce7e3e" alt="Pairwise review screen showing runs side-by-side with the feedback pane containing A/B/Equal buttons and keyboard shortcuts." data-og-width="3456" width="3456" data-og-height="1980" height="1980" data-path="langsmith/images/pairwise-annotation-queue-review-feedback-pane.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/jimZt8pd1vc7LfPM/langsmith/images/pairwise-annotation-queue-review-feedback-pane.png?w=280&fit=max&auto=format&n=jimZt8pd1vc7LfPM&q=85&s=4398df0649f7941284f411e713b9324e 280w, https://mintcdn.com/langchain-5e9cc07a/jimZt8pd1vc7LfPM/langsmith/images/pairwise-annotation-queue-review-feedback-pane.png?w=560&fit=max&auto=format&n=jimZt8pd1vc7LfPM&q=85&s=077edf8001c6b308c618413707b0c10b 560w, https://mintcdn.com/langchain-5e9cc07a/jimZt8pd1vc7LfPM/langsmith/images/pairwise-annotation-queue-review-feedback-pane.png?w=840&fit=max&auto=format&n=jimZt8pd1vc7LfPM&q=85&s=51df52243ba575ef82ebc22ad1112d8a 840w, https://mintcdn.com/langchain-5e9cc07a/jimZt8pd1vc7LfPM/langsmith/images/pairwise-annotation-queue-review-feedback-pane.png?w=1100&fit=max&auto=format&n=jimZt8pd1vc7LfPM&q=85&s=612d906fe461da78958a624d3fb7ab0a 1100w, https://mintcdn.com/langchain-5e9cc07a/jimZt8pd1vc7LfPM/langsmith/images/pairwise-annotation-queue-review-feedback-pane.png?w=1650&fit=max&auto=format&n=jimZt8pd1vc7LfPM&q=85&s=66aa9cad6b4f2ce5c2fa02fd844c89dc 1650w, https://mintcdn.com/langchain-5e9cc07a/jimZt8pd1vc7LfPM/langsmith/images/pairwise-annotation-queue-review-feedback-pane.png?w=2500&fit=max&auto=format&n=jimZt8pd1vc7LfPM&q=85&s=913a8b6dc35b46af02da7673ca0d963d 2500w" />

<Check>
  Consider routing runs that already have user feedback (e.g., thumbs-down) into a single-run queue for triage and a pairwise queue for head-to-head comparisons against a stronger baseline. This helps you identify regressions quickly. To learn more about how to capture user feedback from your LLM application, follow the guide on [attaching user feedback](/langsmith/attach-user-feedback).
</Check>

## Video guide

<iframe className="w-full aspect-video rounded-xl" src="https://www.youtube.com/embed/rxKYHA-2KS0?si=V4EnrUmzJaUVJh0m" title="YouTube video player" frameBorder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowFullScreen />

***

<Callout icon="pen-to-square" iconType="regular">
  [Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/langsmith/annotation-queues.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.langchain.com/llms.txt