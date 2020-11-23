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

 Date: 23/10/2020 18:27:54
*/


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
-- Primary Key structure for table K302 Zhuhai JJ$InvoiceHeaderBuffer
-- ----------------------------
ALTER TABLE [dbo].[K302 Zhuhai JJ$InvoiceHeaderBuffer] ADD CONSTRAINT [PK__InvoiceH__AA723669771E96D9] PRIMARY KEY CLUSTERED ([Record ID])
WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)  
ON [PRIMARY]
GO

