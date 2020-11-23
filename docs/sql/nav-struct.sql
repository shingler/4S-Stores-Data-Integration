/*
 Navicat Premium Data Transfer

 Source Server         : mssql
 Source Server Type    : SQL Server
 Source Server Version : 14003356
 Source Host           : localhost:1401
 Source Catalog        : Nav
 Source Schema         : dbo

 Target Server Type    : SQL Server
 Target Server Version : 14003356
 File Encoding         : 65001

 Date: 21/10/2020 17:12:08
*/


-- ----------------------------
-- Table structure for K302 Zhuhai JJ$CustVendBuffer
-- ----------------------------
IF EXISTS (SELECT * FROM sys.all_objects WHERE object_id = OBJECT_ID(N'[dbo].[K302 Zhuhai JJ$CustVendBuffer]') AND type IN ('U'))
	DROP TABLE [dbo].[K302 Zhuhai JJ$CustVendBuffer]
GO

CREATE TABLE [dbo].[K302 Zhuhai JJ$CustVendBuffer] (
  [Record ID] int  IDENTITY(1,1) NOT NULL,
  [No_] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [Name] varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [Address] varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [City] varchar(30) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [Post Code] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [Country] varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [Currency] varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [Gen_ Bus_ Posting Group] varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [VAT Bus_ Posting Group] varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [Cust_VendPostingGroup] varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [Application Method] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [PaymentTermsCode] varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [Template] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [Entry No_] int  NOT NULL,
  [Error Message] varchar(250) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [DateTime Imported] datetime  NOT NULL,
  [DateTime Handled] datetime  NOT NULL,
  [Type] int  NOT NULL,
  [Handled by] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [Address 2] varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [PhoneNo] varchar(30) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [FaxNo] varchar(30) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [Blocked] varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [Email] varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [ARAPAccountNo] varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [PricesIncludingVAT] int  NOT NULL,
  [PaymentMethodCode] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [Cost Center Code] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [ICPartnerCode] varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL
)
GO

ALTER TABLE [dbo].[K302 Zhuhai JJ$CustVendBuffer] SET (LOCK_ESCALATION = TABLE)
GO


-- ----------------------------
-- Table structure for K302 Zhuhai JJ$DMSInterfaceInfo
-- ----------------------------
IF EXISTS (SELECT * FROM sys.all_objects WHERE object_id = OBJECT_ID(N'[dbo].[K302 Zhuhai JJ$DMSInterfaceInfo]') AND type IN ('U'))
	DROP TABLE [dbo].[K302 Zhuhai JJ$DMSInterfaceInfo]
GO

CREATE TABLE [dbo].[K302 Zhuhai JJ$DMSInterfaceInfo] (
  [Entry No_] int  IDENTITY(1,1) NOT NULL,
  [DMSCode] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [DMSTitle] varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [CompanyCode] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [CompanyTitle] varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [CreateDateTime] datetime  NOT NULL,
  [Creator] varchar(30) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [DateTime Imported] datetime  NOT NULL,
  [DateTime Handled] datetime  NOT NULL,
  [Handled by] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [Status] varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [Error Message] varchar(250) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [XMLFileName] varchar(250) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [Customer_Vendor Total Count] int  NOT NULL,
  [Invoice Total Count] int  NOT NULL,
  [Type] int  NOT NULL,
  [Other Transaction Total Count] int  NOT NULL,
  [FA Total Count] int  NOT NULL
)
GO

ALTER TABLE [dbo].[K302 Zhuhai JJ$DMSInterfaceInfo] SET (LOCK_ESCALATION = TABLE)
GO


-- ----------------------------
-- Table structure for K302 Zhuhai JJ$FABuffer
-- ----------------------------
IF EXISTS (SELECT * FROM sys.all_objects WHERE object_id = OBJECT_ID(N'[dbo].[K302 Zhuhai JJ$FABuffer]') AND type IN ('U'))
	DROP TABLE [dbo].[K302 Zhuhai JJ$FABuffer]
GO

CREATE TABLE [dbo].[K302 Zhuhai JJ$FABuffer] (
  [Record ID] int  NOT NULL,
  [FANo_] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [Description] varchar(30) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [SerialNo] varchar(30) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [Inactive] int  NOT NULL,
  [Blocked] int  NOT NULL,
  [FAClassCode] varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [FASubclassCode] varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [FALocationCode] varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [BudgetedAsset] int  NOT NULL,
  [VendorNo] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [MaintenanceVendorNo] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [Entry No_] int  NOT NULL,
  [Error Message] varchar(250) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [DateTime Imported] datetime  NOT NULL,
  [DateTime Handled] datetime  NOT NULL,
  [UnderMaintenance] int  NOT NULL,
  [Handled by] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [NextServiceDate] datetime  NOT NULL,
  [WarrantyDate] datetime  NOT NULL,
  [DepreciationPeriod] int  NOT NULL,
  [DepreciationStartingDate] datetime  NOT NULL,
  [CostCenterCode] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL
)
GO

ALTER TABLE [dbo].[K302 Zhuhai JJ$FABuffer] SET (LOCK_ESCALATION = TABLE)
GO


-- ----------------------------
-- Table structure for K302 Zhuhai JJ$InvoiceHeaderBuffer
-- ----------------------------
IF EXISTS (SELECT * FROM sys.all_objects WHERE object_id = OBJECT_ID(N'[dbo].[K302 Zhuhai JJ$InvoiceHeaderBuffer]') AND type IN ('U'))
	DROP TABLE [dbo].[K302 Zhuhai JJ$InvoiceHeaderBuffer]
GO

CREATE TABLE [dbo].[K302 Zhuhai JJ$InvoiceHeaderBuffer] (
  [Record ID] int  NOT NULL,
  [InvoiceNo] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [Posting Date] datetime  NOT NULL,
  [Document Date] datetime  NOT NULL,
  [Due Date] datetime  NOT NULL,
  [PayToBillToNo] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [SellToBuyFromNo] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [CostCenterCode] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [VehicleSeries] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [ExtDocumentNo] varchar(30) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [Entry No_] int  NOT NULL,
  [InvoiceType] varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [DateTime Imported] datetime  NOT NULL,
  [DateTime handled] datetime  NOT NULL,
  [Error Message] varchar(250) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [Handled by] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [Line Total Count] int  NOT NULL,
  [PriceIncludeVAT] int  NOT NULL,
  [Description] varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [Location] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL
)
GO

ALTER TABLE [dbo].[K302 Zhuhai JJ$InvoiceHeaderBuffer] SET (LOCK_ESCALATION = TABLE)
GO


-- ----------------------------
-- Table structure for K302 Zhuhai JJ$InvoiceLineBuffer
-- ----------------------------
IF EXISTS (SELECT * FROM sys.all_objects WHERE object_id = OBJECT_ID(N'[dbo].[K302 Zhuhai JJ$InvoiceLineBuffer]') AND type IN ('U'))
	DROP TABLE [dbo].[K302 Zhuhai JJ$InvoiceLineBuffer]
GO

CREATE TABLE [dbo].[K302 Zhuhai JJ$InvoiceLineBuffer] (
  [Record ID] int  NOT NULL,
  [Line No_] int  NOT NULL,
  [DMSItemType] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [GLAccount] varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [Description] varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [CostCenterCode] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [VehicleSeries] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [VIN] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [Quantity] decimal(38,20)  NOT NULL,
  [Line Amount] decimal(38,20)  NOT NULL,
  [LineCost] decimal(38,20)  NOT NULL,
  [TransactionType] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [Entry No_] int  NOT NULL,
  [Error Message] varchar(250) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [DateTime Imported] datetime  NOT NULL,
  [DateTime Handled] datetime  NOT NULL,
  [Handled by] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [InvoiceNo] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [Line Discount Amount] decimal(38,20)  NOT NULL,
  [WIP No_] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [Line VAT Amount] decimal(38,20)  NOT NULL,
  [Line VAT Rate] decimal(38,20)  NOT NULL,
  [FromCompanyName] varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [ToCompanyName] varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [Location] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [MovementType] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [OEMCode] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL
)
GO

ALTER TABLE [dbo].[K302 Zhuhai JJ$InvoiceLineBuffer] SET (LOCK_ESCALATION = TABLE)
GO


-- ----------------------------
-- Table structure for K302 Zhuhai JJ$OtherBuffer
-- ----------------------------
IF EXISTS (SELECT * FROM sys.all_objects WHERE object_id = OBJECT_ID(N'[dbo].[K302 Zhuhai JJ$OtherBuffer]') AND type IN ('U'))
	DROP TABLE [dbo].[K302 Zhuhai JJ$OtherBuffer]
GO

CREATE TABLE [dbo].[K302 Zhuhai JJ$OtherBuffer] (
  [Record ID] int  NOT NULL,
  [DocumentNo_] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [TransactionType] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [Line No_] int  NOT NULL,
  [Posting Date] datetime  NOT NULL,
  [Document Date] datetime  NOT NULL,
  [ExtDocumentNo_] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [Account No_] varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [Description] varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [Debit Value] decimal(38,20)  NOT NULL,
  [Credit Value] decimal(38,20)  NOT NULL,
  [CostCenterCode] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [VehicleSeries] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [Entry No_] int  NOT NULL,
  [DateTime Imported] datetime  NOT NULL,
  [DateTime handled] datetime  NOT NULL,
  [Error Message] varchar(250) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [Handled by] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [AccountType] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [WIP No_] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [FA Posting Type] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [EntryType] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [FromCompanyName] varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [ToCompanyName] varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [VIN] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [SourceType] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [SourceNo] varchar(30) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [NotDuplicated] int  NOT NULL,
  [NAVDocumentNo_] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [DMSItemType] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [DMSItemTransType] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL,
  [Location] varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS  NOT NULL
)
GO

ALTER TABLE [dbo].[K302 Zhuhai JJ$OtherBuffer] SET (LOCK_ESCALATION = TABLE)
GO


-- ----------------------------
-- Primary Key structure for table K302 Zhuhai JJ$CustVendBuffer
-- ----------------------------
ALTER TABLE [dbo].[K302 Zhuhai JJ$CustVendBuffer] ADD CONSTRAINT [PK__CustVend__AA7236695923DF06] PRIMARY KEY CLUSTERED ([Record ID])
WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)  
ON [PRIMARY]
GO


-- ----------------------------
-- Primary Key structure for table K302 Zhuhai JJ$DMSInterfaceInfo
-- ----------------------------
ALTER TABLE [dbo].[K302 Zhuhai JJ$DMSInterfaceInfo] ADD CONSTRAINT [PK__DMSInter__248139D58BC743B2] PRIMARY KEY CLUSTERED ([Entry No_])
WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)  
ON [PRIMARY]
GO


-- ----------------------------
-- Primary Key structure for table K302 Zhuhai JJ$FABuffer
-- ----------------------------
ALTER TABLE [dbo].[K302 Zhuhai JJ$FABuffer] ADD CONSTRAINT [PK__FABuffer__AA723669918A383E] PRIMARY KEY CLUSTERED ([Record ID])
WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)  
ON [PRIMARY]
GO


-- ----------------------------
-- Primary Key structure for table K302 Zhuhai JJ$InvoiceHeaderBuffer
-- ----------------------------
ALTER TABLE [dbo].[K302 Zhuhai JJ$InvoiceHeaderBuffer] ADD CONSTRAINT [PK__InvoiceH__AA723669771E96D9] PRIMARY KEY CLUSTERED ([Record ID])
WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)  
ON [PRIMARY]
GO


-- ----------------------------
-- Primary Key structure for table K302 Zhuhai JJ$InvoiceLineBuffer
-- ----------------------------
ALTER TABLE [dbo].[K302 Zhuhai JJ$InvoiceLineBuffer] ADD CONSTRAINT [PK__InvoiceL__AA7236696C8BCC23] PRIMARY KEY CLUSTERED ([Record ID])
WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)  
ON [PRIMARY]
GO


-- ----------------------------
-- Primary Key structure for table K302 Zhuhai JJ$OtherBuffer
-- ----------------------------
ALTER TABLE [dbo].[K302 Zhuhai JJ$OtherBuffer] ADD CONSTRAINT [PK__OtherBuf__AA72366945384753] PRIMARY KEY CLUSTERED ([Record ID])
WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)  
ON [PRIMARY]
GO

