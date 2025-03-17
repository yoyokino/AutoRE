### 软件系统描述 (Software System Description)

LoanPS 软件系统是一个贷款处理系统，旨在管理贷款的整个生命周期，从申请到结清。该系统支持贷款请求的提交、评估、信用核查、贷款协议生成、放款、还款录入、逾期通知生成以及贷款结清等功能。该系统旨在为贷款专员、贷款助理、贷款文员、申请人和调度器提供必要的功能，以确保贷款流程的高效和准确。

The LoanPS software system is a loan processing system designed to manage the entire lifecycle of loans, from application to close out. The system supports functions such as loan request submission, evaluation, credit reference validation, loan agreement generation, loan booking, payment entry, late notice generation, and loan close out. The system is designed to provide the necessary functionalities for Loan Officers, Loan Assistants, Loan Clerks, Applicants, and Schedulers to ensure the efficiency and accuracy of the loan process.

### Actor及Actor的简介 (Actors and Their Descriptions)

*   **LoanOfficer (贷款专员):** 负责评估贷款请求、管理贷款条款。他们与系统交互以审查申请、批准或拒绝贷款，并根据需要更新贷款协议。
    LoanOfficer: Responsible for evaluating loan requests and managing loan terms. They interact with the system to review applications, approve or deny loans, and update loan agreements as needed.

*   **LoanAssistant (贷款助理):** 负责输入已验证的信用参考。他们使用系统将信用参考附加到相应的贷款申请中。
    LoanAssistant: Responsible for entering validated credit references. They use the system to attach credit references to the appropriate loan applications.

*   **LoanClerk (贷款文员):** 负责生成贷款函和协议、登记新贷款、录入贷款还款以及结清贷款。他们与系统交互以创建贷款账户、记录付款并更新贷款余额，以及在贷款全部付清时关闭账户。
    LoanClerk: Responsible for generating loan letters and agreements, booking new loans, entering loan payments, and closing out loans. They interact with the system to create loan accounts, record payments and update loan balances, and close accounts when loans are fully paid.

*   **Applicant (申请人):** 负责提交贷款请求。他们使用系统填写并提交贷款申请表。
    Applicant: Responsible for submitting loan requests. They use the system to fill out and submit loan application forms.

*  **Scheduler(调度器):** 负责生成标准付款通知和生成逾期通知.
    Scheduler: Responsible for Generating Standard Payment Notice and Generating Late Notice.

### 主要实体及其属性列表 (Main Entities and Their Attributes)

*   **LoanApplication (贷款申请)**
    *   applicationID (申请ID): string
    *   applicant (申请人): Applicant
    *   requestDate (申请日期): date
    *   loanAmount (贷款金额): float
    *   loanTerm (贷款期限): int
    *   creditReferences (信用参考): (List of) CreditReference
    *   status (状态): string (e.g., "Pending", "Approved", "Denied", "More Info Needed")

*   **CreditReference (信用参考)**
    *   referenceID (参考ID): string
    *   referenceName (参考人姓名): string
    *   contactInfo (联系信息): string
    *   isValidated (是否已验证): boolean

*   **LoanAccount (贷款账户)**
    *   accountID (账户ID): string
    *   loanAgreement (贷款协议): LoanAgreement
    *   balance (余额): float
    *   paymentHistory (还款历史): (List of) Payment
    *   status (状态): string (e.g., "Active", "Overdue", "Closed")

*   **LoanAgreement (贷款协议)**
    *   agreementID (协议ID): string
    *   loanAmount (贷款金额): float
    *   interestRate (利率): float
    *   loanTerm (贷款期限): int
    *   startDate (开始日期): date
    *   monthlyPayment (月还款额): float

*   **Payment (还款)**
    *   paymentID (还款ID): string
    *   paymentDate (还款日期): date
    *   amount (金额): float

* **Notice (通知)**
* noticeID(通知ID): string
* noticeDate(通知日期): date
* loanAccount(贷款账户): string
* noticeType(通知类型):string
* noticeContent(通知内容): string

### 用户故事及其基本流程、拓展流程 (All User Stories, Basic Processes, and Extended Processes)

#### Actor: LoanOfficer (贷款专员)

##### User Story 1: Evaluate Loan Request (评估贷款请求)

*   **User Story:** As a loan officer, I want to evaluate loan requests, so that I can determine the approval status. (作为贷款专员，我希望评估贷款请求，以便确定批准状态。) [LoanPS Use Case.docx]
*   **Basic Process:**
    1.  The LoanOfficer logs into the system. (贷款专员登录系统。) [LoanPS Use Case.docx]
    2.  The LoanOfficer selects a pending loan request. (贷款专员选择待处理的贷款请求。) [LoanPS Use Case.docx]
    3.  The system displays the loan request details. (系统显示贷款请求的详细信息。) [LoanPS Use Case.docx]
    4.  The LoanOfficer reviews the applicant's information and credit history. (贷款专员审查申请人的信息和信用记录。) [LoanPS Use Case.docx]
    5.  The LoanOfficer decides whether to approve or deny the loan. (贷款专员决定批准还是拒绝贷款。) [LoanPS Use Case.docx]
    6.  The system records the decision and updates the status of the loan request. (系统记录决定并更新贷款请求的状态。) [LoanPS Use Case.docx]
*   **Extended Process:**
    *   **(Optional) 6a. Request Additional Information (请求补充信息):**
        1.  The LoanOfficer marks the request as needing more info. (贷款专员将请求标记为需要更多信息。)
        2.  The system notifies the Applicant to provide additional information. (系统通知申请人提供补充信息。)
    *   **(Exception Handling) *b. System failure during evaluation (评估期间系统故障):**
        1.  The LoanOfficer logs in again and accesses the pending request. (贷款专员重新登录并访问待处理的请求。)
        2.  The system retrieves the last saved state of the evaluation. (系统检索上次保存的评估状态。)

##### User Story 2: Manage Loan Term (管理贷款条款)

*   **User Story:** As a loan officer, I want to manage loan terms, so that I can update or modify loan agreements as needed. (作为贷款专员，我希望管理贷款条款，以便可以根据需要更新或修改贷款协议。)
*   **Basic Process:**
    1.  The LoanOfficer logs into the system. (贷款专员登录系统。)
    2.  The LoanOfficer selects the loan to be modified. (贷款专员选择要修改的贷款。)
    3.  The system displays the current loan details. (系统显示当前的贷款详细信息。)
    4.  The LoanOfficer updates the loan terms as necessary. (贷款专员根据需要更新贷款条款。)
    5.  The LoanOfficer confirms the changes. (贷款专员确认更改。)
    6.  The system records the updated terms and notifies relevant parties. (系统记录更新后的条款并通知相关方。)
*   **Extended Process:**
    *   **(Optional) 6a. Require Approval (需要批准):**
        1.  The update requires additional approval. (更新需要额外批准。)
        2.  The system forwards the changes to the appropriate authority for approval. (系统将更改转发给相应的授权机构以供批准。)
    *   **(Exception Handling) *b. System failure during modification (修改期间系统故障):**
        1.  The LoanOfficer logs back into the system. (贷款专员重新登录系统。)
        2.  The system restores the last saved state of the loan details. (系统恢复上次保存的贷款详细信息状态。)

#### Actor: LoanAssistant (贷款助理)

##### User Story 3: Enter Validated Credit References (输入已验证的信用参考)

*   **User Story:** As a loan assistant, I want to enter validated credit references, so that the loan application process is accurate. (作为贷款助理，我希望输入已验证的信用参考，以便贷款申请流程准确无误。) [LoanPS Use Case.docx]
*   **Basic Process:**
    1.  The LoanAssistant logs into the system. (贷款助理登录系统。) [LoanPS Use Case.docx]
    2.  The LoanAssistant accesses the loan application. (贷款助理访问贷款申请。) [LoanPS Use Case.docx]
    3.  The system displays the loan application details. (系统显示贷款申请的详细信息。) [LoanPS Use Case.docx]
    4.  The LoanAssistant enters validated credit references. (贷款助理输入已验证的信用参考。) [LoanPS Use Case.docx]
    5.  The LoanAssistant confirms the entry. (贷款助理确认输入。) [LoanPS Use Case.docx]
    6.  The system saves the credit references to the loan application. (系统将信用参考保存到贷款申请中。) [LoanPS Use Case.docx]
*   **Extended Process:**
    *    **(Optional) 6a. Request Clarification (请求澄清):**
        1.  The LoanAssistant requires additional clarification on a reference. (贷款助理需要对某个参考进行额外的澄清。)
        2.  The system logs a request for clarification. (系统记录澄清请求。)
    *   **(Exception Handling) *b. System failure during entry (输入期间系统故障):**
        1.  The LoanAssistant logs back into the system. (贷款助理重新登录系统。)
        2.  The system restores the last saved state of the application. (系统恢复上次保存的申请状态。)

#### Actor: LoanClerk (贷款文员)

##### User Story 4: Generate Loan Letter and Agreement (生成贷款函和协议)

*   **User Story:** As a loan clerk, I want the system to generate an approval letter, so that the applicant can be formally notified. (作为贷款文员，我希望系统生成批准函，以便正式通知申请人。) [LoanPS Use Case.docx]
*   **Basic Process:**
    1.  The LoanClerk logs into the system. (贷款文员登录系统。) [LoanPS Use Case.docx]
    2.  The LoanClerk selects an approved loan. (贷款文员选择已批准的贷款。) [LoanPS Use Case.docx]
    3.  The system retrieves loan details. (系统检索贷款详细信息。) [LoanPS Use Case.docx]
    4.  The LoanClerk requests generation of the approval letter and agreement. (贷款文员请求生成批准函和协议。) [LoanPS Use Case.docx]
    5.  The system generates the documents. (系统生成文档。) [LoanPS Use Case.docx]
    6.  The system sends the documents to the applicant. (系统将文档发送给申请人。) [LoanPS Use Case.docx]
*   **Extended Process:**
    *    **(Optional) 6a. Customize Document (自定义文档):**
        1.  The LoanClerk customizes the letter template. (贷款文员自定义信函模板。)
    *   **(Exception Handling) *b. System failure during document generation (文档生成期间系统故障):**
        1.  The LoanClerk logs back into the system. (贷款文员重新登录系统。)
        2.  The system attempts to regenerate the documents. (系统尝试重新生成文档。)

##### User Story 5: Book New Loan (登记新贷款)

*   **User Story:** As a loan clerk, I want the system to create a new loan account, so that the agreed-upon terms are officially recorded. (作为贷款文员，我希望系统创建新的贷款账户，以便正式记录商定的条款。) [LoanPS Use Case.docx]
*   **Basic Process:**
    1. The LoanClerk logs into the system. (贷款文员登录系统。)
    2. The LoanClerk accesses the returned loan agreement.(贷款文员访问返回的贷款协议。)
    3. The system verifies the signed agreement.(系统验证已签署的协议)
    4. The LoanClerk confirms the creation of a new loan account. (贷款文员确认创建新的贷款账户。)
    5. The system creates the loan account with the agreed terms.(系统使用商定的条款创建贷款帐户。)
    6. The system confirms the successful creation of the loan account.(系统确认贷款帐户创建成功。)
*    **Extended Process:**
 * **(Optional) 6a. Modify Terms(修改条款):**
 1. Adjustments are made to the loan terms due to errors.(由于错误，对贷款条款进行调整。)
    *   **(Exception Handling) *b. System failure during account creation (账户创建期间系统故障):**
        1.  The LoanClerk logs back into the system. (贷款文员重新登录系统。)
        2.  The system attempts to recreate the loan account. (系统尝试重新创建贷款账户。)

##### User Story 6: Enter Loan Payment (录入贷款还款)

*   **User Story:** As a loan clerk, I want to enter payments into the loan account, so that payment records are updated accurately. (作为贷款文员，我希望将还款录入贷款账户，以便准确更新还款记录。) [LoanPS Use Case.docx]
*   **Basic Process:**
    1.  The LoanClerk logs into the system. (贷款文员登录系统。) [LoanPS Use Case.docx]
    2.  The LoanClerk accesses the loan account. (贷款文员访问贷款账户。) [LoanPS Use Case.docx]
    3.  The system displays the loan account details. (系统显示贷款账户的详细信息。) [LoanPS Use Case.docx]
    4.  The LoanClerk enters the payment details. (贷款文员输入还款详细信息。) [LoanPS Use Case.docx]
    5.  The system records the payment and updates the account balance. (系统记录还款并更新账户余额。) [LoanPS Use Case.docx]
    6.  The system confirms the payment entry. (系统确认还款录入。) [LoanPS Use Case.docx]
*   **Extended Process:**
    *   **(Exception Handling) *b. System failure during payment entry (还款录入期间系统故障):**
        1.  The LoanClerk logs back into the system. (贷款文员重新登录系统。)
        2.  The system attempts to recover the payment entry. (系统尝试恢复还款录入。)

##### User Story 7: Close Out Loan (结清贷款)

*   **User Story:** As a loan clerk, I want to close loans that have been paid in full, so that records are updated accurately. (作为贷款文员，我希望结清已全部付清的贷款，以便准确更新记录。) [LoanPS Use Case.docx]
*   **Basic Process:**
    1.  The LoanClerk logs into the system. (贷款文员登录系统。) [LoanPS Use Case.docx]
    2.  The LoanClerk accesses the paid-in-full loan account. (贷款文员访问已全部付清的贷款账户。) [LoanPS Use Case.docx]
    3.  The system verifies the full payment of the loan. (系统验证贷款已全部付清。) [LoanPS Use Case.docx]
    4.  The LoanClerk initiates the loan closure process. (贷款文员启动贷款结清流程。) [LoanPS Use Case.docx]
    5.  The system closes the loan account. (系统关闭贷款账户。) [LoanPS Use Case.docx]
    6.  The system sends a confirmation of closure to the customer. (系统向客户发送结清确认。) [LoanPS Use Case.docx]
*   **Extended Process:**
    *   **(Exception Handling) *b. System failure during loan closure (贷款结清期间系统故障):**
        1.  The LoanClerk logs back into the system. (贷款文员重新登录系统。)
        2.  The system attempts to complete the loan closure process. (系统尝试完成贷款结清流程。)

#### Actor: Applicant (申请人)

##### User Story 8: Submit Loan Request (提交贷款请求)

*   **User Story:** As an applicant, I want to submit a loan request, so that I can apply for a loan. (作为申请人，我希望提交贷款请求，以便申请贷款。) [LoanPS Use Case.docx]
*   **Basic Process:**
    1.  The Applicant logs into the loan system. (申请人登录贷款系统。)
    2.  The system presents the loan application form. (系统显示贷款申请表。)
    3.  The Applicant fills in the required information. (申请人填写所需信息。)
    4.  The Applicant reviews and confirms the loan request details. (申请人审查并确认贷款请求的详细信息。)
    5.  The system validates the entered information. (系统验证输入的信息。)
    6.  The system submits the loan request for approval. (系统提交贷款请求以供审批。)
*   **Extended Process:**
    *   **(Exception Handling) *b. Submission error (提交错误):**
        1.  The Applicant retries submission after correcting errors. (申请人在更正错误后重新提交。)
        2.  The system confirms successful submission. (系统确认提交成功。)

#### Actor: Scheduler (调度器)

##### User Story 9: Generate Late Notice (生成逾期通知)

*   **User Story:** As a scheduler, I want the system to generate late payment notices, so that customers are informed of overdue payments. (作为调度器，我希望系统生成逾期付款通知，以便通知客户逾期付款。) [LoanPS Use Case.docx]
* **Basic Process:**
  1. The Scheduler initiates the late notice generation process.(调度器启动延迟通知生成过程。)
  2. The system identifies overdue loan accounts.(系统识别逾期贷款帐户。)
  3. The system compiles payment history for each overdue account.(系统编译每个逾期帐户的付款历史记录。)
  4. The system generates a late notice for each overdue account.(系统为每个逾期帐户生成延迟通知。)
  5. The system queues the notices for mailing.(系统将通知排队以进行邮寄。)
  6. The system logs the generation of all late notices. (系统记录所有延迟通知的生成。)
* **Extended Process:**
    *   **(Exception Handling) *b. System failure during notice generation: (通知生成期间的系统故障：)**
        1.  The Scheduler reviews error logs.(调度程序查看错误日志。)
        2. The system retries generating the remaining notices. (系统重试生成剩余的通知。)

##### User Story 10: Generate Standard Payment Notice (生成标准付款通知)

*   **User Story:** As a scheduler, I want the system to generate monthly billing statements, so that customers receive their payment notices on time. (作为调度器，我希望系统生成每月账单，以便客户按时收到付款通知。) [LoanPS Use Case.docx]
*   **Basic Process:**
1.  The Scheduler initiates the billing process. (计划程序启动计费过程。)
2.  The system retrieves all active loan accounts.(系统检索所有活动贷款帐户。)
3.   The system calculates due payments for each account. (系统计算每个帐户的到期付款。)
4.  The system generates a billing statement for each loan account.(系统为每个贷款帐户生成帐单。)
5.  The system queues the statements for mailing.(系统将报表排队以进行邮寄。)
6.  The system logs the successful generation of all notices.(系统记录所有通知的成功生成。)
* **Extended Process:**
     * **(Exception Handling) *b. System failure during billing:(结算期间的系统故障：)**