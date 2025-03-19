# AutoRE Project README

This project is an implementation of AutoRE method, contrasted with a manual approach.  The goal is to compare the two methods in terms of efficiency and quality of generated requirements.

## Usage

**frontend:** 

1. Use AppSmith (you can use Docker Image: appsmith-ce) to load the "AutoRE.json".
2. Change the "DataSource-LocalHost" URL into your backend URL (may be 127.0.0.1:8000).
3. Be aware of cross-domain issues!
4. Deploy the project.

**backend:** 

1. Fill in the OpenAI format api-key and URL in "workflow.py".
2. Install the packages in "requirements.txt", then run "main.py" (better in Python 3.9 or 3.10).
3. You can test the APIs in 127.0.0.1:8000/api/docs#/

**Trial Materials:**

*   **XX Software System Description:** Primary reference document.
*   **Use Case Document (Draft):**  Provides a baseline for comparison.
*   **Systems for Trial:**
    1.  CoCoME (16)
    2.  LoanPS (10)
    3.  ATM (6)
    4.  LibraryMS (19)  *(The numbers in parentheses represent number of use cases)*

**Trial Instructions:**

Follow the structure and content of the "XX Software System Description" document when using the tool to generate structured requirements.

**AutoRE Method:**

A stakeholder representative will use the provided tool, guided by the on-screen prompts, to generate the following requirements elements:

*   Actors
*   User Stories
*   Preconditions
*   Postconditions
*   Basic Flow (Main Success Scenario)
*   Extension Flow (Alternative Flows/Exceptions)

**Manual Method:**

Stakeholders and a product manager will collaborate to capture requirements through discussion.  A product manager or requirements engineer will then manually document the same requirements elements (Actors, User Stories, Pre/Postconditions, Basic/Extension Flows).  This process requires:

*   Multiple participants in the discussion.
*   Structured formatting of the captured requirements.
*   Verification against established requirements specifications.

## AutoRE Tool Instructions

> [!NOTE]
> Most operations involve interaction with a Large Language Model (LLM).  LLM responses may have significant latency.  Please wait for the loading indicator (spinning circle) to complete before proceeding.

> [!CAUTION]
> **If you encounter display bugs or data errors, try the following steps in order:**
>
> 1.  **On the main Actor page, click the "Sync" button in the upper-right corner to fetch the latest data from the backend.**
> 2.  **If data display or generation issues persist, try clicking the "Regenerate" button.**
> 3.  **If the application becomes unresponsive, try refreshing the browser tab.**
> 4.  **If a component displays "Oops," for entities, user stories, extension flows, etc., first try refreshing the page. This might directly take you to the edit or detail view, allowing you to delete or modify the content. This should not affect these functions or the display of the detail page.**
>
> _Summary: If any component displays errors, return to the home page, refresh, and then click the sync button in the upper right corner._

**Steps:**

1.  **Open the application link.**  On the initial "Actor" page, click the "Sync" button to load data from the backend.

2.  **Data Cleanup (IMPORTANT):** If any data exists, *delete all existing Actors and Entities*.  **Ensure you do not delete data being used by other participants.**

3.  **Start Timing:** After the data cleanup is complete and verified, begin timing the trial.

4.  **Generate Actors:** On the main "Actor" page, input the system description text. Click the "Generate Actors" button.

5.  **Refine Actors:**  Review and modify the generated Actors, referring to the system description document.  Prioritize deleting Actors to match the expected number, then refine the remaining Actors.

6.  **Generate User Stories:** Click the "Generate All User Stories" button.

7.  **Refine User Stories:** Navigate to the "User Stories" detail page for *each* Actor.  Review and modify the User Stories, again prioritizing deletion to match the expected quantity, followed by refinement of the remaining User Stories.

8.  **Generate Entities:** Click the "Entity Analysis" button (or similarly named button) to generate Entities.

9.  **Refine Entities:** Review and modify the generated Entities. Prioritize deleting Entities to retain only *essential* entities.  The completeness or richness of the entities is less important than conciseness.  After modifying an Entity and returning to the list, you may need to refresh the page to see the updated data.

10. **Generate Conditions and Flows:** Navigate to the "User Stories" detail page for *each* Actor *one at a time*.  For each User Story:

    *   Click "Generate Pre/Postconditions".  Review and modify the conditions (general semantic accuracy is sufficient).
    *   You can either submit modification suggestions or edit directly.  If editing directly, confirm the changes on the confirmation section at the bottom of the modification page.
    *   Click "Generate Basic Flow".  Review and modify the basic flow, prioritizing deletion to the correct number of steps, then refining the remaining steps.
    *   You can either submit modification suggestions or edit directly. If editing directly, confirm the changes on the confirmation section at the bottom of the modification page.
    *   Click "Generate Extension Flows". Review and modify extension flows, prioritizing deletion to the correct number, then refining the remaining flows.
    *   You can either submit modification suggestions or edit directly. If editing directly, confirm the changes on the confirmation section at the bottom of the modification page. (Specifying that changes are for the "content" field is preferred).

11. **Final Synchronization and Export:** After completing all modifications, return to the "Actors" page and click "Sync".  Thoroughly review the data.  Once verified, click "Export" to download the `REdoc.json` file.

12. **Stop Timing:** Stop the timer after successfully downloading the `REdoc.json` file.
