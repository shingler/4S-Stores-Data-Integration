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

 Date: 04/11/2020 17:44:28
*/


-- ----------------------------
-- Table structure for K302 Zhuhai JJ$DMSInterfaceInfo
-- ----------------------------
IF EXISTS (SELECT * FROM sys.all_objects WHERE object_id = OBJECT_ID(N'[dbo].[K302 Zhuhai JJ$DMSInterfaceInfo]') AND type IN ('U'))
	DROP TABLE [dbo].[K302 Zhuhai JJ$DMSInterfaceInfo]
GO

CREATE TABLE [dbo].[K302 Zhuhai JJ$DMSInterfaceInfo] (
  [timestamp] timestamp  NOT NULL,
  [Entry No_] int  NOT NULL,
  [DMSCode] varchar(20) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL,
  [DMSTitle] varchar(50) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL,
  [CompanyCode] varchar(20) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL,
  [CompanyTitle] varchar(50) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL,
  [CreateDateTime] datetime  NOT NULL,
  [Creator] varchar(30) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL,
  [DateTime Imported] datetime  NOT NULL,
  [DateTime Handled] datetime  NOT NULL,
  [Handled by] varchar(20) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL,
  [Status] varchar(10) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL,
  [Error Message] varchar(250) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL,
  [XMLFileName] varchar(250) COLLATE SQL_Latin1_General_CP437_BIN  NOT NULL,
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
-- Indexes structure for table K302 Zhuhai JJ$DMSInterfaceInfo
-- ----------------------------
CREATE UNIQUE NONCLUSTERED INDEX [$1]
ON [dbo].[K302 Zhuhai JJ$DMSInterfaceInfo] (
  [Type] ASC,
  [Status] ASC,
  [Entry No_] ASC
)
GO

CREATE UNIQUE NONCLUSTERED INDEX [$2]
ON [dbo].[K302 Zhuhai JJ$DMSInterfaceInfo] (
  [Type] ASC,
  [CreateDateTime] ASC,
  [Entry No_] ASC
)
GO


-- ----------------------------
-- Primary Key structure for table K302 Zhuhai JJ$DMSInterfaceInfo
-- ----------------------------
ALTER TABLE [dbo].[K302 Zhuhai JJ$DMSInterfaceInfo] ADD CONSTRAINT [K302 Zhuhai JJ$DMSInterfaceInfo$0] PRIMARY KEY CLUSTERED ([Entry No_])
WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)  
ON [Data Filegroup 1]
GO

