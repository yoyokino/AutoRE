### 软件系统描述 (Software System Description)

CoCoME (Common Components Modeling Example) 软件系统是一个用于零售环境的收银管理系统。它支持销售处理、现金桌管理、库存管理、产品定价、供应商管理以及商店的开关店操作。该系统旨在为收银员、商店经理和管理员提供必要的功能，以确保日常运营的顺利进行。

The CoCoME (Common Components Modeling Example) software system is a cash register management system for retail environments. It supports sales processing, cash desk management, inventory management, product pricing, supplier management, and store opening and closing operations. The system is designed to provide the necessary functionalities for cashiers, store managers, and administrators to ensure smooth daily operations.

### Actor及Actor的简介 (Actors and Their Descriptions)

*   **收银员 (Cashier):** 收银员的主要职责是处理销售、打开和关闭现金桌。他们与系统交互以记录销售、处理付款并管理现金桌的日常操作。
    Cashier: The primary responsibility of the cashier is to process sales, open, and close the cash desk. They interact with the system to record sales, handle payments, and manage the daily operations of the cash desk.

*   **商店经理 (StoreManager):** 商店经理负责监督商店的运营，包括订购产品、接收产品、查看库存报告、更改价格、管理供应商以及开关店操作。
    Store Manager: The store manager is responsible for overseeing the store's operations, including ordering products, receiving products, viewing stock reports, changing prices, managing suppliers, and opening and closing the store.

*   **管理员 (Administrator):** 管理员负责管理系统中的各种信息，如商店信息、产品目录、现金桌信息、收银员信息、商品信息和供应商信息。
    Administrator: The administrator is responsible for managing various information in the system, such as store information, product catalog, cash desk information, cashier information, item information, and supplier information.

### 主要实体及其属性列表 (Main Entities and Their Attributes)

*   **Sale (销售)**
    *   saleID (销售ID): string
    *   date (日期): datetime
    *   total (总计): float
    *   tax (税): float

*   **SaleLineItem (销售行项目)**
    *   itemID (商品ID): string
    *   quantity (数量): int
    *   subtotal (小计): float

*   **Item (商品)**
    *   itemID (商品ID): string
    *   description (描述): string
    *   price (价格): float
    *   stockLevel (库存水平): int

*   **CashDesk (现金桌)**
    *   deskID (现金桌ID): string
    *   openingBalance (开户余额): float
    *   closingBalance (结算余额): float
    *   isOpen (是否打开): boolean

*   **Cashier (收银员)**
    *   cashierID (收银员ID): string
    *   name (姓名): string
    *   password (密码): string

*   **Store (商店)**
    *   storeID (商店ID): string
    *   name (名称): string
    *   address (地址): string

*    **Supplier(供应商)**
    * supplierID(供应商ID): string
    * supplierName(供应商名称): string
    * supplierAddress(供应商地址): string

* **ProductCatalog(产品目录)**
  *  productID(产品ID): string
  * productName(产品名称):string
  * productDescription(产品描述): string

*   **Order (订单)**
    *   orderID (订单ID): string
    *   date (日期): date
    *   supplier (供应商): string
    *   products (产品): (List of) Item
    *   status (状态): string

### 用户故事及其基本流程、拓展流程 (All User Stories, Basic Processes, and Extended Processes)

#### Actor: Cashier (收银员)

##### User Story 1: Process Sale (处理销售)

*   **User Story:** As a cashier, I want to process sale, so that customers can buy goods. (作为收银员，我希望处理销售，以便顾客可以购买商品。)
*   **Basic Process (基本流程):**
    1.  The Cashier starts a new sale. (收银员开始新的销售。)
    2.  The CoCoME system starts a new sale. (CoCoME 系统开始新的销售。)
    3.  The Cashier enters item identifier. (收银员输入商品标识符。)
    4.  The CoCoME system records each sale line item and presents item description and running total (loop 3-4 until end of entry). (CoCoME 系统记录每个销售行项目并显示商品描述和运行总计 (循环 3-4 直到输入结束)。)
    5.  The Cashier tells customer the total payment. (收银员告诉顾客总付款额。)
    6.  The CoCoME system presents total payment with taxes calculated. (CoCoME 系统显示含税的总付款额。)
    7.  The Cashier deals with the payment. (收银员处理付款。)
*   **Extended Process (拓展流程):**
    *   **Selection 7a. Cash Payment (现金支付):** The Cashier clicks to execute the operation makeCashPayment, with entering amount. (收银员点击执行现金支付操作，并输入金额。)
    *   **Selection 7b. Card Payment (刷卡支付):** The Cashier clicks to execute the operation makeCardPayment, with entering cardAccountNumber, expiryDate, fee. (收银员点击执行刷卡支付操作，并输入卡号、有效期和费用。)
    *   **Optional *a. Manager Override (经理覆盖):** At any time, the Manager requests an override operation. The system enters Manager authorized mode. The Manager/Cashier performs a Manager mode operation. The system reverts to Cashier authorization mode. (在任何时候，经理请求覆盖操作。系统进入经理授权模式。经理/收银员执行经理模式操作。系统恢复到收银员授权模式。)
    *   **Exception Handling *b. System Failure (系统故障):** At any time, System fails. The Cashier restarts System, logs in, and requests recovery of prior state. The System reconstructs prior state. (在任何时候，系统发生故障。收银员重新启动系统，登录并请求恢复先前的状态。系统重建先前的状态。)

##### User Story 2: Open Cash Desk (打开现金桌)

*   **User Story:** As a cashier, I want to open cash desk, so that customers can buy goods. (作为收银员，我希望打开现金桌，以便顾客可以购买商品。)
*   **Basic Process:**
    1.  The Cashier initiates the opening of cash desk. (收银员发起打开现金桌的操作。)
    2.  The system verifies cashier authorization. (系统验证收银员的授权。)
    3.  The Cashier inputs opening balance. (收银员输入开户余额。)
    4.  The system records the opening of cash desk and logs the initial balance. (系统记录现金桌的打开并记录初始余额。)
*   **Extended Process:**
    *   **Optional *a. Discrepancy in Opening Balance (开户余额差异):** The Cashier reports discrepancy. The StoreManager authorizes adjusted opening balance. (收银员报告差异。商店经理授权调整后的开户余额。)
    *   **Exception Handling *b. System Error (系统错误):** If system error occurs during opening, the Cashier restarts the system and reinitiates the opening process. (如果在打开过程中发生系统错误，收银员重新启动系统并重新启动打开过程。)

##### User Story 3: Close Cash Desk (关闭现金桌)

*   **User Story:** As a cashier, I want to close the cash desk, so that the day's transactions are concluded securely. (作为收银员，我希望关闭现金桌，以便安全地结束当天的交易。)
*   **Basic Process:**
    1.  The Cashier initiates the closing of the cash desk. (收银员发起关闭现金桌的操作。)
    2.  The system calculates the total sales and reconciles the final balance. (系统计算总销售额并核对最终余额。)
    3.  The Cashier confirms the final balance and notifies the StoreManager. (收银员确认最终余额并通知商店经理。)
    4.  The System logs the closing action and updates records. (系统记录关闭操作并更新记录。)
*   **Extended Process:**
    *    **Optional *a. Discrepancy in Cash Balance (现金余额差异):** The Cashier reports the discrepancy. The StoreManager or Administrator reviews and authorizes actions to resolve discrepancies. (收银员报告差异。商店经理或管理员审查并授权解决差异的行动。)
    *   **Exception Handling *b. System Error (系统错误):** If system error occurs during closing, the Cashier restarts the system. (如果在关闭过程中发生系统错误，收银员重新启动系统。)

#### Actor: Store Manager (商店经理)

##### User Story 4: Order Products (订购产品)

*   **User Story:** As a store manager, I want to place an order for products, so that inventory is restocked appropriately. (作为商店经理，我希望下订单购买产品，以便适当地补充库存。)
* **Basic Process:**
    1.  The StoreManager initiates a new product order. (商店经理发起新的产品订单。)
    2.  The system displays current inventory levels and suggests reorder quantities. (系统显示当前库存水平并建议重新订购数量。)
    3.  The StoreManager selects products and quantities to order. (商店经理选择要订购的产品和数量。)
    4.  The system processes the order and updates inventory records. (系统处理订单并更新库存记录。)
*   **Extended Process:**
    *   **Optional *a. Administrator Approval for Large Orders (大订单需要管理员批准):** The StoreManager submits order for approval. The Administrator reviews and approves or modifies the order. (商店经理提交订单以供批准。管理员审查并批准或修改订单。)
    *    **Exception Handling *b. System Error (系统错误):** If system error occurs during ordering, the StoreManager restarts the system and reinitiates the order process.(如果在订购过程中发生系统错误，商店经理重新启动系统并重新发起订购过程。)

##### User Story 5: Receive Ordered Product (接收订购的产品)

*   **User Story:** As a store manager, I want to receive ordered products, so that inventory is updated accurately. (作为商店经理，我希望接收订购的产品，以便准确地更新库存。)
*    **Basic Process:**
    1. The StoreManager initiates the receipt of products. (商店经理发起收货。)
    2. The system displays the details of the order to be received. (系统显示要接收的订单的详细信息。)
    3. The StoreManager verifies and confirms the received quantities.(商店经理核实并确认收到的数量。)
    4. The system updates the inventory records and closes the purchase order.(系统更新库存记录并关闭采购订单。)
*   **Extended Process:**
        *   **Optional *a. Administrator involvement for discrepancies(差异需要管理员参与):**The StoreManager reports discrepancies.The Administrator reviews and authorizes necessary corrections.(商店经理报告差异。管理员审查并授权进行必要的更正。)
        *   **Exception Handling *b. If system error occurs during receiving(如果在接收过程中发生系统错误):** The StoreManager restarts the system. The StoreManager reinitiates the receiving process. (商店经理重新启动系统。商店经理重新启动接收过程。)

##### User Story 6: Show Stock Reports (显示库存报告)

*   **User Story:** As a store manager, I want to view stock reports, so that I can make informed inventory decisions. (作为商店经理，我希望查看库存报告，以便做出明智的库存决策。)
*   **Basic Process:**
    1.  The StoreManager requests to view stock reports. (商店经理请求查看库存报告。)
    2.  The system retrieves and displays current stock levels and history. (系统检索并显示当前库存水平和历史记录。)
    3.  The StoreManager reviews the stock information. (商店经理审查库存信息。)
    4.  The system logs the viewing action for auditing purposes. (系统记录查看操作以供审计。)
*   **Extended Process:**
    *   **Optional *a. Administrator Customization (管理员定制):** The Administrator configures report templates. The StoreManager views customized stock reports. (管理员配置报告模板。商店经理查看定制的库存报告。)
    *   **Exception Handling *b. System Error (系统错误):** If system error occurs during report generation, the StoreManager restarts the system and reinitiates the report request. (如果在报告生成过程中发生系统错误，商店经理重新启动系统并重新启动报告请求。)

##### User Story 7: Change Price (更改价格)

*   **User Story:** As a store manager, I want to change the price of items, so that pricing is competitive and accurate. (作为商店经理，我希望更改商品的价格，以便定价具有竞争力和准确性。)
*   **Basic Process:**
    1.  The StoreManager selects an item to change the price. (商店经理选择要更改价格的商品。)
    2.  The system displays current pricing details. (系统显示当前定价详细信息。)
    3.  The StoreManager enters the new price. (商店经理输入新价格。)
    4.  The system updates the price and logs the change. (系统更新价格并记录更改。)
* **Extended Process:**
    *   **Optional *a. Administrator Approval for Significant Changes (重大更改需要管理员批准):** The StoreManager submits price change for approval. The Administrator reviews and approves the change. (商店经理提交价格变更以供批准。管理员审查并批准更改。)
    *   **Exception Handling *b. System Error (系统错误):** If system error occurs during price update, the StoreManager restarts the system and reinitiates the price change process. (如果在价格更新过程中发生系统错误，商店经理重新启动系统并重新发起价格更改过程。)

##### User Story 8: List Suppliers (列出供应商)

*   **User Story:** As a store manager, I want to view all suppliers, so that I can manage supplier relationships effectively. (作为商店经理，我希望查看所有供应商，以便有效地管理供应商关系。)
*   **Basic Process:**
   1. The StoreManager requests to view the supplier list. (商店经理请求查看供应商列表。)
   2. The system retrieves and displays all supplier details. (系统检索并显示所有供应商的详细信息。)
   3. The StoreManager reviews the supplier information. (商店经理查看供应商信息。)
   4.  The system logs the viewing action. (系统记录查看操作。)
*   **Extended Process**
    *    **Optional *a. Administrator updates supplier info:(管理员更新供应商信息):** The Administrator makes updates to supplier details.The StoreManager views the updated list. (管理员更新供应商详细信息。商店经理查看更新后的列表。)
    *  **Exception Handling *b. If system error occurs during retrieval(如果在检索过程中发生系统错误):** The StoreManager restarts the system.The StoreManager reinitiates the request to view suppliers. (商店经理重新启动系统。商店经理重新发起查看供应商的请求。)

##### User Story 9: Open Store (开店)

*   **User Story:** As a store manager, I want to open the store, so that it is ready for business operations. (作为商店经理，我希望开店，以便为业务运营做好准备。)
*   **Basic Process:**
    1.  The StoreManager performs security checks and unlocks the store. (商店经理执行安全检查并解锁商店。)
    2.  The system confirms readiness for operations. (系统确认运营准备就绪。)
    3.  The StoreManager activates store systems and utilities. (商店经理激活商店系统和公用设施。)
    4.  The system logs the store opening action. (系统记录开店操作。)
*   **Extended Process:**
    *   **Optional *a. Administrator Performs Additional Setup (管理员执行额外的设置):** The Administrator configures system settings for the day. The StoreManager verifies the setup. (管理员配置当天的系统设置。商店经理验证设置。)
    *   **Exception Handling *b. System Error (系统错误):** If system error occurs during opening, the StoreManager restarts the system and reinitiates the store opening process. (如果在开店过程中发生系统错误，商店经理重新启动系统并重新启动开店过程。)

##### User Story 10: Close Store (关店)

*   **User Story:** As a store manager, I want to close the store, so that all operations are ended safely and securely. (作为商店经理，我希望关店，以便所有操作都安全可靠地结束。)
* **Basic Process:**
    1. The StoreManager performs closing routines and secures all entrances. (商店经理执行关闭程序并锁好所有入口。)
    2. The system confirms all transactions are complete. (系统确认所有交易均已完成。)
    3. The StoreManager deactivates store systems and utilities. (商店经理停用商店系统和公用设施。)
    4. The system logs the store closing action.(系统记录商店关闭操作。)
*    **Extended Process**
    *  **Optional *a. Administrator performs end-of-day reporting(管理员执行日终报告):** The Administrator generates and reviews reports.The StoreManager verifies completion of the closing process. (管理员生成和审查报告。商店经理核实关闭过程是否完成。)
    *    **Exception Handling *b. If system error occurs during closing:(如果关店过程中发生系统错误):**The StoreManager restarts the system.The StoreManager reinitiates the store closing process.(商店经理重新启动系统。商店经理重新启动商店关闭流程。)

#### Actor: Administrator (管理员)

##### User Story 11: Manage Store Information (管理商店信息)

*   **User Story:** As an administrator, I want to manage store information, so that all details are accurate and up-to-date. (作为管理员，我希望管理商店信息，以便所有详细信息都是准确和最新的。)
* **Basic Process:**
  1. The Administrator accesses the store information management system.(管理员访问商店信息管理系统。)
  2. The system displays current store information.(系统显示当前商店信息。)
  3.  The Administrator enters, modifies, or deletes store information as needed.(管理员根据需要输入、修改或删除商店信息。)
  4. The system updates the database and logs changes.(系统更新数据库并记录更改。)
*   **Extended Process:**
    * **(Optional) *a. Changes require verification(更改需要验证):** The Administrator verifies entered information.The System cross-checks consistency with related data. (管理员验证输入的信息。系统交叉检查与相关数据的一致性。)
     *   **Exception Handling) *b. If system error occurs during management(如果管理过程中发生系统错误):** The Administrator restarts the system.The Administrator reinitiates information management actions.(管理员重新启动系统。管理员重新启动信息管理操作。)

##### User Story 12: Manage Product Catalog (管理产品目录)
* **User Story**: As an administrator, I want to manage the product catalog, so that all item information is accurate and current.(作为管理员，我希望管理产品目录，以便所有商品信息都是准确和最新的。)
* **Basic Process**:
  1.  The Administrator accesses the product catalog management system.(管理员访问产品目录管理系统。)
  2.  The system displays current catalog information.(系统显示当前目录信息。)
  3. The Administrator enters, modifies, or deletes catalog information as needed.(管理员根据需要输入、修改或删除目录信息。)
  4. The system updates the database and logs changes.(系统更新数据库并记录更改。)
*  **Extended Process**:
    *   **Optional) *a. Changes require verification(更改需要验证):** The Administrator verifies entered information. The System cross-checks consistency with related data.(管理员验证输入的信息。系统交叉检查与相关数据的一致性。)
    * **Exception Handling) *b. If system error occurs during management(如果管理过程中发生系统错误):** The Administrator restarts the system. The Administrator reinitiates catalog management actions.(管理员重新启动系统。管理员重新启动目录管理操作。)

##### User Story 13: Manage Cash Desk Information (管理现金桌信息)

*   **User Story:** As an administrator, I want to manage cash desk information, so that all data is accurate and efficiently handled. (作为管理员，我希望管理现金桌信息，以便所有数据都得到准确和有效的处理。)
*    **Basic Process:**
    1.  The Administrator accesses the cash desk management system.(管理员访问现金课桌管理系统。)
    2. The system displays current cash desk information.(系统显示当前现金课桌信息。)
    3.  The Administrator enters, modifies, or deletes cash desk information as needed.(管理员根据需要输入、修改或删除现金课桌信息。)
    4. The system updates the database and logs changes.(系统更新数据库并记录更改。)
*   **Extended Process:**
    *   **Optional) *a. Changes require verification(更改需要验证):**The Administrator verifies entered information.The System cross-checks consistency with related data. (管理员验证输入的信息。系统交叉检查与相关数据的一致性。)
    *   **Exception Handling) *b. If system error occurs during management(如果管理过程中发生系统错误):** The Administrator restarts the system.The Administrator reinitiates cash desk management actions.(管理员重新启动系统。管理员重新启动现金课桌管理操作。)

##### User Story 14: Manage Cashier Information (管理收银员信息)

*   **User Story:** As an administrator, I want to manage cashier information, so that all records are accurate and up-to-date. (作为管理员，我希望管理收银员信息，以便所有记录都是准确和最新的。)
*  **Basic Process**
    1. The Administrator accesses the cashier management system.(管理员访问收银员管理系统。)
    2. The system displays current cashier information.(系统显示当前收银员信息。)
    3.  The Administrator enters, modifies, or deletes cashier information as needed.(管理员根据需要输入、修改或删除收银员信息。)
    4.  The system updates the database and logs changes.(系统更新数据库并记录更改。)
* **Extended Process:**
   * **Optional) *a. Changes require verification(更改需要验证):** The Administrator verifies entered information. The System cross-checks consistency with related data.(管理员验证输入的信息。系统交叉检查与相关数据的一致性。)
   *   **Exception Handling) *b. If system error occurs during management(如果管理过程中发生系统错误):** The Administrator restarts the system. The Administrator reinitiates cashier management actions. (管理员重新启动系统。管理员重新启动收银员管理操作。)

##### User Story 15: Manage Item Information(管理商品信息)
*   **User Story:** As an administrator, I want to manage item information, so that all item records are accurate and up-to-date.(作为管理员，我希望管理商品信息，以便所有商品记录都是准确和最新的。)
* **Basic Process:**
    1.  The Administrator accesses the item management system.(管理员访问商品管理系统。)
    2. The system displays current item information.(系统显示当前商品信息。)
    3.  The Administrator enters, modifies, or deletes item information as needed.(管理员根据需要输入、修改或删除商品信息。)
    4. The system updates the database and logs changes.(系统更新数据库并记录更改。)
*    **Extended Process:**
    *   **Optional) *a. Changes require verification(更改需要验证):** The Administrator verifies entered information. The System cross-checks consistency with related data.(管理员验证输入的信息。系统交叉检查与相关数据的一致性。)
    *  **Exception Handling) *b. If system error occurs during management(如果管理过程中发生系统错误):** The Administrator restarts the system. The Administrator reinitiates item management actions.(管理员重新启动系统。管理员重新启动商品管理操作。)

##### User Story 16: Manage Supplier Information(管理供应商信息)
*   **User Story:** As an administrator, I want to manage supplier information, so that all records are accurate and up-to-date.(作为管理员，我希望管理供应商信息，以便所有记录都是准确和最新的。)
*  **Basic Process:**
  1.  The Administrator accesses the supplier management system.(管理员访问供应商管理系统。)
  2.  The system displays current supplier information.(系统显示当前供应商信息。)
  3. The Administrator enters, modifies, or deletes supplier information as needed.(管理员根据需要输入、修改或删除供应商信息。)
  4. The system updates the database and logs changes.(系统更新数据库并记录更改。)
*  **Extended Process:**
 * **(Optional) *a. Changes require verification(更改需要验证):** The Administrator verifies entered information. The System cross-checks consistency with related data.(管理员验证输入的信息。系统交叉检查与相关数据的一致性。)
 *   **(Exception Handling) *b. If system error occurs during management(如果管理过程中发生系统错误):** The Administrator restarts the system. The Administrator reinitiates supplier management actions. (管理员重新启动系统。）