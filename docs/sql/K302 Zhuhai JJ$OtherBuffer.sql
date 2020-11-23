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

 Date: 23/10/2020 18:28:15
*/


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
-- Primary Key structure for table K302 Zhuhai JJ$OtherBuffer
-- ----------------------------
ALTER TABLE [dbo].[K302 Zhuhai JJ$OtherBuffer] ADD CONSTRAINT [PK__OtherBuf__AA72366945384753] PRIMARY KEY CLUSTERED ([Record ID])
WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)  
ON [PRIMARY]
GO

