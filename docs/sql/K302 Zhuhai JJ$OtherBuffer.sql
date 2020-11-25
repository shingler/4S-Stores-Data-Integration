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

 Date: 25/11/2020 11:43:31
*/


-- ----------------------------
-- Table structure for K302 Zhuhai JJ$OtherBuffer
-- ----------------------------
IF EXISTS (SELECT * FROM sys.all_objects WHERE object_id = OBJECT_ID(N'[dbo].[K302 Zhuhai JJ$OtherBuffer]') AND type IN ('U'))
	DROP TABLE [dbo].[K302 Zhuhai JJ$OtherBuffer]
GO

CREATE TABLE [dbo].[K302 Zhuhai JJ$OtherBuffer] (
  [timestamp] timestamp  NOT NULL,
  [Record ID] int  NOT NULL,
  [DocumentNo_] varchar(20) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL,
  [TransactionType] varchar(20) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL,
  [Line No_] int  NOT NULL,
  [Posting Date] datetime  NOT NULL,
  [Document Date] datetime  NOT NULL,
  [ExtDocumentNo_] varchar(20) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL,
  [Account No_] varchar(50) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL,
  [Description] varchar(100) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL,
  [Debit Value] decimal(38,20)  NOT NULL,
  [Credit Value] decimal(38,20)  NOT NULL,
  [CostCenterCode] varchar(20) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL,
  [VehicleSeries] varchar(20) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL,
  [Entry No_] int  NOT NULL,
  [DateTime Imported] datetime  NOT NULL,
  [DateTime handled] datetime  NOT NULL,
  [Error Message] varchar(250) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL,
  [Handled by] varchar(20) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL,
  [AccountType] varchar(20) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL,
  [WIP No_] varchar(20) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL,
  [FA Posting Type] varchar(20) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL,
  [EntryType] varchar(20) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL,
  [FromCompanyName] varchar(50) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL,
  [ToCompanyName] varchar(50) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL,
  [VIN] varchar(20) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL,
  [SourceType] varchar(20) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL,
  [SourceNo] varchar(30) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL,
  [NotDuplicated] tinyint  NOT NULL,
  [NAVDocumentNo_] varchar(20) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL,
  [DMSItemType] varchar(20) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL,
  [DMSItemTransType] varchar(20) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL,
  [Location] varchar(20) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL,
  [MovementType] varchar(20) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL
)
GO

ALTER TABLE [dbo].[K302 Zhuhai JJ$OtherBuffer] SET (LOCK_ESCALATION = TABLE)
GO


-- ----------------------------
-- Indexes structure for table K302 Zhuhai JJ$OtherBuffer
-- ----------------------------
CREATE UNIQUE NONCLUSTERED INDEX [$1]
ON [dbo].[K302 Zhuhai JJ$OtherBuffer] (
  [Entry No_] ASC,
  [Record ID] ASC
)
GO

CREATE UNIQUE NONCLUSTERED INDEX [$2]
ON [dbo].[K302 Zhuhai JJ$OtherBuffer] (
  [Entry No_] ASC,
  [DocumentNo_] ASC,
  [Line No_] ASC,
  [Record ID] ASC
)
GO

CREATE UNIQUE NONCLUSTERED INDEX [$3]
ON [dbo].[K302 Zhuhai JJ$OtherBuffer] (
  [Entry No_] ASC,
  [DocumentNo_] ASC,
  [Record ID] ASC
)
GO

CREATE UNIQUE NONCLUSTERED INDEX [$4]
ON [dbo].[K302 Zhuhai JJ$OtherBuffer] (
  [Entry No_] ASC,
  [DocumentNo_] ASC,
  [TransactionType] ASC,
  [Line No_] ASC,
  [Record ID] ASC
)
GO


-- ----------------------------
-- Primary Key structure for table K302 Zhuhai JJ$OtherBuffer
-- ----------------------------
ALTER TABLE [dbo].[K302 Zhuhai JJ$OtherBuffer] ADD CONSTRAINT [K302 Zhuhai JJ$OtherBuffer$0] PRIMARY KEY CLUSTERED ([Record ID])
WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)  
ON [Data Filegroup 1]
GO

