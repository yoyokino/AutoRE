好的，以下是根据提供的 ATM 软件系统需求文档总结的新摘要，包含中英文对照，并遵循了所有要求：

### 1. 软件系统描述 (Software System Description)

ATM 软件系统是一个允许客户进行自助银行交易的系统，例如取款、存款、余额查询。 它还支持银行职员管理银行卡和用户信息。该系统旨在为客户和银行职员提供安全、便捷的银行服务。

The ATM software system is a system that allows customers to perform self-service banking transactions, such as withdrawals, deposits, and balance inquiries. It also supports bank clerks in managing bank cards and user information. The system is designed to provide secure and convenient banking services for customers and bank clerks.

### 2. 软件系统涉及的所有的Actor及Actor的简介 (Actors and Their Descriptions)

*   **Customer (客户):** 客户可以使用 ATM 进行取款、存款和查询余额。
    Customer: Customers can use the ATM to withdraw cash, deposit funds, and check their account balance.

*   **Bank Clerk (银行职员):** 银行职员可以使用银行系统管理银行卡信息和用户信息。
    Bank Clerk: Bank clerks can use the bank system to manage bank card information and user information.

* **System(系统)**: Card Identification
    System: Card Identification

### 3. 软件系统中存在的主要实体及其属性列表 (Main Entities and Their Attributes)

*   **Bank Card (银行卡)**
    *   cardNumber (卡号): string
    *   expiryDate (有效期): date
    *   PIN (密码): string

*   **Account (账户)**
    *   accountNumber (账号): string
    *   balance (余额): float

* **User(用户/客户)**
    * userID(用户ID):string
    * userName(用户姓名):string
    * userAddress(用户地址):string

*   **Transaction (交易)**
    *   transactionID (交易ID): string
    *   type (类型): string (e.g., "Withdrawal", "Deposit", "Balance Inquiry")
    *   amount (金额): float
    *   date (日期): datetime

* **BankClerk(银行职员)**
  * clerkID(职员ID): string
  * clerkName(职员姓名): string
  * clerkPassword(职员密码): string

### 4. 所有的用户故事、每个用户故事涉及的基本流程、拓展流程 (All User Stories, Basic Processes, and Extended Processes)

#### Actor: Customer (客户)

##### User Story 1: Withdraw Cash (取款)

*   **User Story:** As a customer, I want to withdraw cash, so that I can have physical money. (作为客户，我希望取款，以便获得现金。) 
*   **Basic Process (基本流程):**
    1.  The Customer inserts the bank card. (客户插入银行卡。) 
    2.  The System performs card identification. (系统进行卡片识别。) 
    3.  The Customer enters the PIN. (客户输入密码。) 
    4.  The System verifies the PIN. (系统验证密码。) 
    5.  The Customer selects the withdraw cash option. (客户选择取款选项。) 
    6.  The Customer enters the amount. (客户输入金额。) 
    7.  The System checks for sufficient balance. (系统检查余额是否充足。) 
    8.  The System dispenses the cash. (系统出钞。) 
    9.  The System updates the account balance. (系统更新账户余额。) 
*   **Extended Process (拓展流程):**
    *   **(Optional) a. If the withdrawal amount exceeds the limit (如果取款金额超过限额):**
        1.  The System notifies the Customer about the limit. (系统通知客户有关限额。) 
        2.  The Customer selects a new amount. (客户选择新的金额。) 
    *   **(Exception Handling) b. If card identification fails (如果卡片识别失败):**
        1.  The System returns the card and prompts the Customer to retry. (系统退回卡片并提示客户重试。) 

##### User Story 2: Deposit Funds (存款)

*   **User Story:** As a customer, I want to deposit cash, so that I can add money to my account. (作为客户，我希望存款，以便将钱存入我的账户。) 
*   **Basic Process (基本流程):**
    1.  The Customer inserts the bank card. (客户插入银行卡。) 
    2.  The System performs card identification. (系统进行卡片识别。) 
    3.  The Customer enters the PIN. (客户输入密码。) 
    4.  The System verifies the PIN. (系统验证密码。) 
    5.  The Customer selects the deposit option. (客户选择存款选项。) 
    6.  The Customer inserts cash and confirms the amount. (客户放入现金并确认金额。) 
    7.  The System counts the cash and verifies the amount. (系统清点现金并验证金额。) 
    8.  The System updates the account balance. (系统更新账户余额。) 
*   **Extended Process (拓展流程):**
    *   **(Exception Handling) a. If card identification fails (如果卡片识别失败):**
        1.  The System returns the card and prompts the Customer to retry. (系统退回卡片并提示客户重试。) 
    *   **(Exception Handling) b. If cash counting fails (如果现金清点失败):**
        1.  The System prompts the Customer to reinsert the cash. (系统提示客户重新放入现金。) 

##### User Story 3: Check Balance (查询余额)

*   **User Story:** As a customer, I want to check my account balance, so that I can know how much money I have. (作为客户，我希望查询我的账户余额，以便了解我有多少钱。) 
*   **Basic Process (基本流程):**
    1.  The Customer inserts the bank card. (客户插入银行卡。) 
    2.  The System performs card identification. (系统进行卡片识别。) 
    3.  The Customer enters the PIN. (客户输入密码。) 
    4.  The System verifies the PIN. (系统验证密码。) 
    5.  The Customer selects the check balance option. (客户选择查询余额选项。) 
    6.  The System retrieves and displays the account balance. (系统检索并显示账户余额。) 
*   **Extended Process (拓展流程):**
     *   **(Exception Handling) b. If card identification fails (如果卡片识别失败):**
        1.  The System returns the card and prompts the Customer to retry. (系统退回卡片并提示客户重试。) 

##### User Story 6: Card Identification(卡片识别)

*   **User Story:** As a customer, I need to verify card details, so that I can ensure secure transactions.(作为一个客户，我需要验证卡的详细信息，这样我才能确保交易的安全。)
*   **Basic Process(基本流程):**
    1.  The Customer inserts or scans the bank card. (顾客/银行职员插入或者扫描银行卡。)
    2.  The System reads the card data. (系统读取卡片数据)
    3.  The System checks the card validity and authenticity. (系统检测卡片的合法性和真实性)
    4.  The System grants access if the card is valid. (如果卡片是合法的，系统将授权访问)
*   **Extended Process(拓展流程):**
    * **(Exception Handling) a. If card verification fails:(如果卡片认证失败：)**
      1.  The System returns the card.

#### Actor: Bank Clerk (银行职员)

##### User Story 4: Manage Bank Card (管理银行卡)

*   **User Story:** As a bank clerk, I want to manage bank card information, so that I can keep customer records up to date. (作为银行职员，我希望管理银行卡信息，以便保持客户记录的更新。) 
*   **Basic Process (基本流程):**
    1.  The Bank Clerk logs into the bank's system. (银行职员登录银行系统。) 
    2.  The System verifies the Bank Clerk's credentials. (系统验证银行职员的凭据。) 
    3.  The Bank Clerk selects manage bank card option. (银行职员选择管理银行卡选项。) 
    4.  The Bank Clerk enters, inquires, modifies, or deletes bank card information as needed. (银行职员根据需要输入、查询、修改或删除银行卡信息。) 
    5.  The System processes the request and updates the records accordingly. (系统处理请求并相应地更新记录。) 
*   **Extended Process (拓展流程):**
    *   **(Exception Handling) a. If credential verification fails (如果凭据验证失败):**
        1.  The System prompts for re-login. (系统提示重新登录。) 
    *   **(Optional) b. If data entry is incorrect (如果数据输入不正确):**
        1.  The System prompts the Bank Clerk to correct the information. (系统提示银行职员更正信息。) 

##### User Story 5: Manage User Information (管理用户信息)

*   **User Story:** As a bank clerk, I want to manage user information, so that I can keep customer records accurate and up to date. (作为银行职员，我希望管理用户信息，以便保持客户记录的准确性和最新性。) 
*   **Basic Process (基本流程):**
    1.  The Bank Clerk logs into the user management system. (银行职员登录用户管理系统。) 
    2.  The System verifies the Bank Clerk's credentials. (系统验证银行职员的凭据。) 
    3.  The Bank Clerk selects manage user option. (银行职员选择管理用户选项。) 
    4.  The Bank Clerk enters, inquires, modifies, or deletes user information as needed. (银行职员根据需要输入、查询、修改或删除用户信息。) 
    5.  The System processes the request and updates the records accordingly. (系统处理请求并相应地更新记录。) 
*   **Extended Process (拓展流程):**
    *   **(Exception Handling) a. If credential verification fails (如果凭据验证失败):**
        1.  The System prompts for re-login. (系统提示重新登录。)
     *   **(Optional) b. If data entry is incorrect (如果数据输入不正确):**
        1.  The System prompts the Bank Clerk to correct the information. (系统提示银行职员更正信息。)
