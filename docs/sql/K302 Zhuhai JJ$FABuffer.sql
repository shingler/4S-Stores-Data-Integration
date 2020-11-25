/*
 Navicat Premium Data Transfer

 Source Server         : 同创测试环境

 Source Server Type    : SQL Server
 Source Server Version : 10501600
 Source Host           : 62.234.26.35:1433
 Source Catalog        : PH_Dev
 Source Schema         : dbo

 Target Server Type    : SQL Server
 Target Server Version : 10501600
 File Encoding         : 65001

 Date: 24/11/2020 17:58:49
*/


-- ----------------------------
-- Table structure for K302 Zhuhai JJ$FABuffer
-- ----------------------------
IF EXISTS (SELECT * FROM sys.all_objects WHERE object_id = OBJECT_ID(N'[dbo].[K302 Zhuhai JJ$FABuffer]') AND type IN ('U'))
	DROP TABLE [dbo].[K302 Zhuhai JJ$FABuffer]
GO

CREATE TABLE [dbo].[K302 Zhuhai JJ$FABuffer] (
  [timestamp] timestamp  NOT NULL,
  [Record ID] int  NOT NULL,
  [FANo_] varchar(20) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL,
  [Description] varchar(30) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL,
  [SerialNo] varchar(30) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL,
  [Inactive] tinyint  NOT NULL,
  [Blocked] tinyint  NOT NULL,
  [FAClassCode] varchar(10) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL,
  [FASubclassCode] varchar(10) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL,
  [FALocationCode] varchar(10) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL,
  [BudgetedAsset] tinyint  NOT NULL,
  [VendorNo] varchar(20) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL,
  [MaintenanceVendorNo] varchar(20) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL,
  [Entry No_] int  NOT NULL,
  [Error Message] varchar(250) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL,
  [DateTime Imported] datetime  NOT NULL,
  [DateTime Handled] datetime  NOT NULL,
  [UnderMaintenance] tinyint  NOT NULL,
  [Handled by] varchar(20) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL,
  [NextServiceDate] datetime  NOT NULL,
  [WarrantyDate] datetime  NOT NULL,
  [DepreciationPeriod] int  NOT NULL,
  [DepreciationStartingDate] datetime  NOT NULL,
  [CostCenterCode] varchar(20) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL
)
GO

ALTER TABLE [dbo].[K302 Zhuhai JJ$FABuffer] SET (LOCK_ESCALATION = TABLE)
GO


-- ----------------------------
-- Indexes structure for table K302 Zhuhai JJ$FABuffer
-- ----------------------------
CREATE UNIQUE NONCLUSTERED INDEX [$1]
ON [dbo].[K302 Zhuhai JJ$FABuffer] (
  [FANo_] ASC,
  [Record ID] ASC
)
GO

CREATE UNIQUE NONCLUSTERED INDEX [$2]
ON [dbo].[K302 Zhuhai JJ$FABuffer] (
  [Entry No_] ASC,
  [Record ID] ASC
)
GO

CREATE UNIQUE NONCLUSTERED INDEX [$3]
ON [dbo].[K302 Zhuhai JJ$FABuffer] (
  [Entry No_] ASC,
  [FANo_] ASC,
  [Record ID] ASC
)
GO


-- ----------------------------
-- Primary Key structure for table K302 Zhuhai JJ$FABuffer
-- ----------------------------
ALTER TABLE [dbo].[K302 Zhuhai JJ$FABuffer] ADD CONSTRAINT [K302 Zhuhai JJ$FABuffer$0] PRIMARY KEY CLUSTERED ([Record ID])
WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)  
ON [Data Filegroup 1]
GO

