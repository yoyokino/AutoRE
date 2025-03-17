### 软件系统描述 (Software System Description)

LibraryMS (Library Management System) 是一个图书馆管理系统，旨在自动化图书馆的各种操作。它支持图书搜索、借阅、归还、预订、取消预订、查看借阅历史、推荐图书等用户功能。对于图书馆员，系统支持图书借阅、归还处理、续借、支付逾期费用等。对于管理员，系统支持管理图书信息、副本信息、主题信息、用户信息、图书馆员信息以及查看推荐图书。此外，系统还包括由调度器执行的检查和计算逾期费用、通知用户即将到期的图书以及倒计时停借天数等功能。第三方系统用于发送通知邮件。

The LibraryMS (Library Management System) is a library management system designed to automate various library operations. It supports user functions such as searching for books, borrowing, returning, reserving, canceling reservations, viewing borrowing history, and recommending books. For librarians, the system supports book borrowing, return processing, renewals, and payment of overdue fees.  For administrators, the system supports managing book information, copy information, subject information, user information, librarian information, and viewing recommended books. In addition, the system includes functions performed by a scheduler to check and calculate overdue fees, notify users of items due soon, and countdown suspension days. A third-party system is used to send notification emails.

### Actor及Actor的简介 (Actors and Their Descriptions)

*   **用户 (User):**  用户可以使用系统搜索图书、查看借阅历史、预订图书、取消预订以及推荐图书。
    User: Users can use the system to search for books, view borrowing history, reserve books, cancel reservations, and recommend books.

*   **图书馆员 (Librarian):** 图书馆员可以使用系统处理图书借阅、归还、续借以及处理逾期费用支付。
    Librarian: Librarians can use the system to process book borrowings, returns, renewals, and handle overdue fee payments.

*   **管理员 (Administrator):** 管理员可以管理系统中的图书信息、副本信息、主题信息、用户信息、图书馆员信息，以及查看用户推荐的图书。
    Administrator: Administrators can manage book information, copy information, subject information, user information, librarian information, and view books recommended by users.

*    **调度器 (Scheduler):** 调度程序自动执行检查逾期项目和计算费用、发送即将到期通知以及计算用户停借倒计时等任务。
    Scheduler: The Scheduler automates tasks such as checking overdue items and calculating fees, sending due soon notifications, and counting down suspension days for users.

*   **第三方系统 (ThirdPartSystem):** 第三方系统负责向用户发送通知邮件。
     ThirdPartSystem: The ThirdPartSystem is responsible for sending notification emails to users.
### 主要实体及其属性列表 (Main Entities and Their Attributes)

*   **Book (图书)**
    *   bookID (图书ID): string
    *   title (书名): string
    *   author (作者): string
    *   ISBN (国际标准书号): string
    *   publicationDate (出版日期): date

*   **BookCopy (图书副本)**
    *   copyID (副本ID): string
    *   bookID (图书ID): string
    *   status (状态): string (e.g., available, checked out, reserved)

*   **Subject (主题)**
    *   subjectID (主题ID): string
    *   subjectName (主题名称): string

*   **User (用户)**
    *   userID (用户ID): string
    *   name (姓名): string
    *   address (地址): string
    *   contact (联系方式): string

*   **Librarian (图书馆员)**
    *   librarianID (图书馆员ID): string
    *   name (姓名): string
    *   contact (联系方式): string

*   **Loan (借阅)**
    *   loanID (借阅ID): string
    *   userID (用户ID): string
    *   copyID (副本ID): string
    *   dueDate (到期日期): date
    *   returnDate (归还日期): date
    *   overdueFee (逾期费用): float

*  **Reservation(预定)**
    * reservationID(预定ID)：string
    * userID(用户ID): string
    * bookID(图书ID): string
    * reservationDate(预定日期): date

* **Recommendation (推荐)**
    * recommendationID(推荐ID):string
    * userID(用户ID): string
    * bookTitle(书名):string
    * author(作者):string
    * reason(理由):string

### 用户故事及其基本流程、拓展流程 (All User Stories, Basic Processes, and Extended Processes)

#### Actor: User (用户)

##### User Story 1: Search for Books (搜索图书)

*   **User Story:** As a user, I want to search for books, so that I can find the materials I need. (作为用户，我希望搜索图书，以便找到我需要的资料。)
*   **Basic Process:**
    1.  The User logs into the library management system. (用户登录图书馆管理系统。)
    2.  The system presents the search interface. (系统呈现搜索界面。)
    3.  The User enters search criteria. (用户输入搜索条件。)
    4.  The system processes the search query. (系统处理搜索查询。)
    5.  The system displays the search results. (系统显示搜索结果。)
    6.  The User browses through the results. (用户浏览结果。)
*   **Extended Process:**
    *   **Exception Handling *a. System failure during search:** The User logs back into the system. The system restores the last saved search criteria. (系统搜索过程中出现故障：用户重新登录系统。系统恢复上次保存的搜索条件。)

##### User Story 2: View Book History (查看借阅历史)

*   **User Story:** As a user, I want to view the history of books I have borrowed, so that I can keep track of my reading activity. (作为用户，我希望查看我借阅过的图书历史，以便跟踪我的阅读活动。)
*   **Basic Process:**
    1.  The User logs into the library management system. (用户登录图书馆管理系统。)
    2.  The System displays the user dashboard. (系统显示用户仪表板。)
    3.  The User selects the option to view book history. (用户选择查看图书历史记录的选项。)
    4.  The System retrieves the user's borrowing history. (系统检索用户的借阅历史记录。)
    5.  The System displays the book history to the user. (系统向用户显示图书历史记录。)
*   **Extended Process:**
    *   **Exception Handling *a. System failure during history retrieval:** The User logs back into the system. The System attempts to restore the borrowing history data. (历史记录检索过程中出现系统故障：用户重新登录系统。 系统尝试恢复借阅历史数据。)

##### User Story 3: Make Book Reservation (预订图书)

*   **User Story:** As a user, I want to reserve a book, so that I can ensure its availability for pickup. (作为用户，我希望预订一本书，以确保我可以取书。)
*   **Basic Process:**
    1.  The User logs into the library management system. (用户登录图书馆管理系统。)
    2.  The System presents the book catalog. (系统呈现图书目录。)
    3.  The User selects a book to reserve. (用户选择要预订的图书。)
    4.  The System checks the book's availability. (系统检查图书的可用性。)
    5.  The System reserves the book for the user. (系统为用户预订图书。)
    6.  The System sends a reservation confirmation to the user. (系统向用户发送预订确认。)
*   **Extended Process:**
    *   **Exception Handling *a. System failure during reservation:** The User logs back into the system. The System attempts to reprocess the reservation. (预订过程中出现系统故障：用户重新登录系统。 系统尝试重新处理预订。)

##### User Story 4: Recommend Books (推荐图书)

*   **User Story:** As a user, I want to recommend books to the library, so that they can be considered for acquisition. (作为用户，我希望向图书馆推荐图书，以便图书馆可以考虑购买。)
*   **Basic Process:**
    1.  The User logs into the library management system. (用户登录图书馆管理系统。)
    2.  The System presents the recommendation interface. (系统呈现推荐界面。)
    3.  The User enters the book recommendation details. (用户输入图书推荐详细信息。)
    4.  The System records the recommendation. (系统记录推荐。)
    5.  The System sends a confirmation to the user. (系统向用户发送确认。)
    6.  The System logs the recommendation for review by the library staff. (系统记录推荐信息以供图书馆工作人员审核。)
*   **Extended Process:**
    *   **Exception Handling *a. System failure during recommendation:** The User logs back into the system. The System attempts to restore the recommendation details. (推荐过程中出现系统故障：用户重新登录系统。 系统尝试恢复推荐详细信息。)

##### User Story 5: Cancel Book Reservation (取消图书预订)

*   **User Story:** As a user, I want to cancel a book reservation, so that the book is available for others. (作为用户，我希望取消图书预订，以便其他人可以使用该图书。)
*   **Basic Process:**
    1.  The User logs into the library system. (用户登录图书馆系统。)
    2.  The System displays the user's active reservations. (系统显示用户的有效预订。)
    3.  The User selects the reservation to cancel. (用户选择要取消的预订。)
    4.  The System processes the cancellation request. (系统处理取消请求。)
    5.  The System confirms the cancellation and updates the book's status. (系统确认取消并更新图书的状态。)
    6.  The System notifies the user of the successful cancellation. (系统通知用户取消成功。)
*   **Extended Process:**
    *   **Exception Handling *a. System failure during cancellation:** The User logs back into the system. The System attempts to reprocess the cancellation. (取消过程中出现系统故障：用户重新登录系统。 系统尝试重新处理取消。)

#### Actor: Librarian (图书馆员)

##### User Story 6: Borrow a Book (借阅图书)

*   **User Story:** As a librarian, I want to process book borrowings, so that users can take books home for reading. (作为图书馆员，我希望处理图书借阅，以便用户可以将图书带回家阅读。)
*   **Basic Process:**
    1.  The Librarian logs into the library management system. (图书馆员登录图书馆管理系统。)
    2.  The System displays the borrowing interface. (系统显示借阅界面。)
    3.  The Librarian scans the book barcode. (图书馆员扫描图书条形码。)
    4.  The System verifies the book's availability. (系统验证图书的可用性。)
    5.  The Librarian processes the user's library card. (图书馆员处理用户的借书卡。)
    6.  The System updates the book status to checked out and records the transaction. (系统将图书状态更新为已借出并记录交易。)
    7.  The System confirms the borrowing to the Librarian. (系统向图书馆员确认借阅。)
*   **Extended Process:**
    *  **Exception Handling *a. System failure during borrowing:** The Librarian logs back into the system. The System attempts to restore the last saved transaction details. (借阅过程中出现系统故障：图书馆员重新登录系统。 系统尝试恢复上次保存的交易详细信息。)

##### User Story 7: Process Book Return (处理图书归还)

*   **User Story:** As a librarian, I want to process book returns, so that the inventory is updated and fees are cleared. (作为图书馆员，我希望处理图书归还，以便更新库存并结算费用。)
*   **Basic Process:**
    1.  The Librarian logs into the library management system. (图书馆员登录图书馆管理系统。)
    2.  The System displays the return interface. (系统显示归还界面。)
    3.  The Librarian scans the returned book. (图书馆员扫描归还的图书。)
    4.  The System updates the inventory and checks for overdue fees. (系统更新库存并检查逾期费用。)
    5.  The Librarian informs the user of any fees. (图书馆员通知用户任何费用。)
    6.  The System records the return transaction. (系统记录归还交易。)
*   **Extended Process:**
    *   **Exception Handling *a. System failure during return:** The Librarian logs back into the system. The System attempts to restore the last transaction state. (归还过程中出现系统故障：图书馆员重新登录系统。 系统尝试恢复上次交易状态。)

##### User Story 8: Renew a Book (续借图书)

*   **User Story:** As a librarian, I want to renew borrowed books, so that users can extend their borrowing period. (作为图书馆员，我希望续借已借阅的图书，以便用户可以延长借阅期限。)
*   **Basic Process:**
    1. The Librarian logs into the library system. (图书馆员登录到图书馆系统).
    2. The System displays the renewal interface.(系统将显示续订界面).
    3. The Librarian scans the book barcode or enters book details.(图书馆员扫描条形码或输入图书详细信息).
    4. The System checks for holds or restrictions.(系统将检查是否有保留或限制).
    5.  The Librarian confirms the user information.(图书馆员需要确认用户信息).
    6. The System updates the due date and logs the renewal.(系统更新到期日期并记录续订).
*    **Extended Process**
    *   **Exception Handling *a. System failure during renewal:** The Librarian logs back into the system. The System attempts to restore the last transaction state.(续订期间发生系统故障： 图书馆员重新登录系统。 系统尝试恢复最后的交易状态。)

##### User Story 9: Pay Overdue Fee (支付逾期费用)

*   **User Story:** As a librarian, I want to process overdue fee payments, so that user accounts are updated correctly. (作为图书馆员，我希望处理逾期费用支付，以便正确更新用户帐户。)
*   **Basic Process:**
    1.  The Librarian logs into the library management system. (图书馆员登录图书馆管理系统。)
    2.  The System displays the fee payment interface. (系统显示费用支付界面。)
    3.  The Librarian enters the user's account information. (图书馆员输入用户的帐户信息。)
    4.  The System calculates the total overdue fees. (系统计算逾期费用总额。)
    5.  The Librarian confirms and processes the payment. (图书馆员确认并处理付款。)
    6.  The System records the payment and updates the user's account status. (系统记录付款并更新用户的帐户状态。)
    7.  The System confirms the payment to the Librarian. (系统向图书馆员确认付款。)
*   **Extended Process:**
    *   **Exception Handling *a. System failure during payment processing:** The Librarian logs back into the system. The System attempts to restore the last transaction state. (付款处理过程中出现系统故障：图书馆员重新登录系统。 系统尝试恢复上次交易状态。)

#### Actor: Administrator (管理员)

##### User Story 10: Manage Book Information (管理图书信息)

*   **User Story:** As an administrator, I want to manage book information, so that the catalog is accurate and up-to-date. (作为管理员，我希望管理图书信息，以便目录准确且最新。)
*   **Basic Process:**
    1.  The Administrator logs into the library management system. (管理员登录图书馆管理系统。)
    2.  The System displays the book management interface. (系统显示图书管理界面。)
    3.  The Administrator selects a book management action (enter, modify, delete, inquire). (管理员选择图书管理操作（输入、修改、删除、查询）。)
    4.  The System processes the selected action. (系统处理所选操作。)
    5.  The System updates the book information accordingly. (系统相应地更新图书信息。)
    6.  The System confirms the completed action to the Administrator. (系统向管理员确认已完成的操作。)
*   **Extended Process:**
    *   **Exception Handling *a. System failure during book management:** The Administrator logs back into the system. The System attempts to recover the last saved state of book information. (图书管理过程中出现系统故障：管理员重新登录系统。 系统尝试恢复上次保存的图书信息状态。)

##### User Story 11: Manage Book Copy Information (管理图书副本信息)

*   **User Story:** As an administrator, I want to manage book copy information, so that the inventory is accurate and up-to-date. (作为管理员，我希望管理图书副本信息，以便库存准确且最新。)
*   **Basic Process:**
    1.  The Administrator logs into the library management system. (管理员登录图书馆管理系统。)
    2.  The System displays the book copy management interface. (系统显示图书副本管理界面。)
    3.  The Administrator selects a book copy management action (enter, modify, delete, inquire). (管理员选择图书副本管理操作（输入、修改、删除、查询）。)
    4.  The System processes the selected action. (系统处理所选操作。)
    5.  The System updates the book copy information accordingly. (系统相应地更新图书副本信息。)
    6.  The System confirms the completed action to the Administrator. (系统向管理员确认已完成的操作。)
*   **Extended Process:**
    *   **Exception Handling *a. System failure during book copy management:** The Administrator logs back into the system. The System attempts to recover the last saved state of book copy information. (图书副本管理过程中出现系统故障：管理员重新登录系统。 系统尝试恢复上次保存的图书副本信息状态。)

##### User Story 12: Manage Subject Information (管理主题信息)

*   **User Story:** As an administrator, I want to manage subject information, so that the catalog remains accurate and organized. (作为管理员，我希望管理主题信息，以便目录保持准确和有序。)
*   **Basic Process:**
    1.  The Administrator logs into the library management system. (管理员登录图书馆管理系统。)
    2.  The System displays the subject management interface. (系统显示主题管理界面。)
    3.  The Administrator selects a subject management action (enter, modify, delete, inquire). (管理员选择主题管理操作（输入、修改、删除、查询）。)
    4.  The System processes the selected action. (系统处理所选操作。)
    5.  The System updates the subject information accordingly. (系统相应地更新主题信息。)
    6.  The System confirms the completed action to the Administrator. (系统向管理员确认已完成的操作。)
*   **Extended Process:**
    *   **Exception Handling *a. System failure during subject management:** The Administrator logs back into the system. The System attempts to recover the last saved state of subject information. (主题管理过程中出现系统故障：管理员重新登录系统。 系统尝试恢复上次保存的主题信息状态。)

##### User Story 13: Manage User Information (管理用户信息)

*   **User Story:** As an administrator, I want to manage user information, so that I can ensure records are up to date. (作为管理员，我希望管理用户信息，以便确保记录是最新的。)
*   **Basic Process:**
    1.  The Administrator logs into the library system. (管理员登录图书馆系统。)
    2.  The System presents the user management interface. (系统呈现用户管理界面。)
    3.  The Administrator selects a user management action (enter, modify, delete, inquire). (管理员选择用户管理操作（输入、修改、删除、查询）。)
    4.  The System processes the selected action. (系统处理所选操作。)
    5.  The System updates the user information accordingly. (系统相应地更新用户信息。)
    6.  The System confirms the completed action to the Administrator. (系统向管理员确认已完成的操作。)
*   **Extended Process:**
    *   **Exception Handling *a. System failure during user management:** The Administrator logs back into the system. The System restores the last saved state of user information. (用户管理过程中出现系统故障：管理员重新登录系统。 系统恢复上次保存的用户信息状态。)

##### User Story 14: Manage Librarian Information (管理图书馆员信息)

*  **User Story:** As an administrator, I want to manage librarian information, so that staff records are accurate and up-to-date. (作为管理员，我希望管理图书馆员信息，以便员工记录准确且最新。)
*   **Basic Process:**
    1.  The Administrator logs into the library management system. (管理员登录图书馆管理系统。)
    2.  The System displays the librarian management interface. (系统显示图书馆员管理界面。)
    3.  The Administrator selects a librarian management action (enter, modify, delete, inquire). (管理员选择图书馆员管理操作（输入、修改、删除、查询）。)
    4.  The System processes the selected action. (系统处理所选操作。)
    5.  The System updates the librarian information accordingly. (系统相应地更新图书馆员信息。)
    6.  The System confirms the completed action to the Administrator. (系统向管理员确认已完成的操作。)
*   **Extended Process:**
    *   **Exception Handling *a. System failure during librarian management:** The Administrator logs back into the system. The System attempts to recover the last saved state of librarian information. (图书馆员管理过程中出现系统故障：管理员重新登录系统。 系统尝试恢复上次保存的图书馆员信息状态。)

##### User Story 15: View Recommended Books (查看推荐图书)

*   **User Story:** As an administrator, I want to view books recommended by users, so that I can consider them for acquisition. (作为管理员，我希望查看用户推荐的图书，以便考虑是否购买。)
*   **Basic Process:**
    1.  The Administrator logs into the library management system. (管理员登录图书馆管理系统。)
    2.  The System displays the dashboard. (系统显示仪表板。)
    3.  The Administrator selects the recommended books view. (管理员选择推荐图书视图。)
    4.  The System retrieves the list of recommended books. (系统检索推荐图书列表。)
    5.  The System displays the recommended books to the Administrator. (系统向管理员显示推荐的图书。)
*   **Extended Process:**
    *   **Exception Handling *a. System failure during retrieval:** The Administrator logs back into the system. The System attempts to restore the last saved state of the recommended books list. (检索过程中出现系统故障：管理员重新登录系统。 系统尝试恢复上次保存的推荐图书列表状态。)

#### Actor: Scheduler (调度器)

##### User Story 16: Check and Compute Overdue Fees (检查和计算逾期费用)

*   **User Story:** As a scheduler, I want to automate the process of checking overdue items and calculating fees, so that users are billed accurately. (作为调度器，我希望自动化检查逾期项目和计算费用的过程，以便准确地向用户收费。)
*   **Basic Process:**
    1.  The Scheduler initiates the overdue check process. (调度器启动逾期检查过程。)
    2.  The System reviews all active loans. (系统审查所有有效借阅。)
    3.  The System identifies overdue items. (系统识别逾期项目。)
    4.  The System calculates the overdue fee for each item. (系统计算每个项目的逾期费用。)
    5.  The System updates the user accounts with the calculated fees. (系统使用计算的费用更新用户帐户。)
    6.  The System logs the completed fee calculation. (系统记录已完成的费用计算。)
*   **Extended Process:**
    *  **Exception Handling *a. System failure during processing:** The Scheduler logs back into the system. The System attempts to resume the process from the last successful operation. (处理过程中出现系统故障：调度器重新登录系统。 系统尝试从上次成功操作恢复进程。)

##### User Story 17: Due Soon Notification (即将到期通知)

*  **User Story:** As a scheduler, I want to notify users about books due soon, so they can return them on time. (作为调度器，我希望通知用户即将到期的图书，以便他们可以按时归还。)
*  **Basic Process:**
  1.  The Scheduler initiates the due soon notification process. (调度器启动即将到期通知过程。)
  2.  The System reviews all active loans to identify items due soon. (系统审查所有有效借阅以识别即将到期的项目。)
  3.  The System compiles a list of users with items due soon. (系统编制即将到期项目的用户列表。)
  4.  The System sends notifications to these users. (系统向这些用户发送通知。)
  5.  The System logs the notification process. (系统记录通知过程。)
*   **Extended Process:**
    *   **Exception Handling *a. System failure during notification:** The Scheduler logs back into the system. The System attempts to continue from the last successful notification. (通知过程中出现系统故障：调度器重新登录系统。 系统尝试从上次成功的通知继续。)

##### User Story 18: Countdown Suspension Day (倒计时停借天数)

*  **User Story:** As a scheduler, I want to count down suspension days for users with overdue items, so that they are informed of their suspension status. (作为调度器，我希望为有逾期项目的用户倒计时停借天数，以便他们了解自己的停借状态。)
* **Basic Process:**
    1.  The Scheduler initiates the suspension countdown process. (调度器启动停借倒计时过程。)
    2.  The System identifies users with overdue items. (系统识别有逾期项目的用户。)
    3.  The System calculates remaining suspension days for each user. (系统计算每个用户的剩余停借天数。)
    4.  The System updates user accounts with the new suspension countdown. (系统使用新的停借倒计时更新用户帐户。)
    5.  The System logs the countdown updates. (系统记录倒计时更新。)
*   **Extended Process:**
    *   **Exception Handling *a. System failure during countdown:** The Scheduler logs back into the system. The System attempts to resume the countdown process from the last successful operation. (倒计时过程中出现系统故障：调度器重新登录系统。 系统尝试从上次成功操作恢复倒计时过程。)

#### Actor: ThirdPartSystem (第三方系统)

##### User Story 19: Send Notification Email (发送通知邮件)

*    **User Story:** As a third-party system, I want to send notification emails to users, so that they are informed about their library status.(作为第三方系统，我想向用户发送通知电子邮件，以便他们了解自己的图书馆状态。)
*   **Basic Process:**
    1. The ThirdPartSystem receives notification triggers.(第三方系统接收通知触发器).
    2.  The System retrieves user contact information.(系统检索用户联系信息).
    3.  The System compiles the notification content.(系统编译通知内容).
    4.  The System sends the email notifications to users.(系统向用户发送电子邮件通知).
    5.  The System logs the notification emails sent.(系统记录发送的通知电子邮件).
*   **Extended Process:**
    *  **Exception Handling *a. System failure during email sending:**The ThirdPartSystem retries sending the email. The System logs any failed attempts.(电子邮件发送期间的系统故障：第三方系统重试发送电子邮件。 系统记录任何失败的尝试。)