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

 Date: 23/10/2020 18:28:04
*/


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
-- Primary Key structure for table K302 Zhuhai JJ$InvoiceLineBuffer
-- ----------------------------
ALTER TABLE [dbo].[K302 Zhuhai JJ$InvoiceLineBuffer] ADD CONSTRAINT [PK__InvoiceL__AA7236696C8BCC23] PRIMARY KEY CLUSTERED ([Record ID])
WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)  
ON [PRIMARY]
GO

