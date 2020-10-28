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

 Date: 23/10/2020 18:27:33
*/


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
-- Primary Key structure for table K302 Zhuhai JJ$DMSInterfaceInfo
-- ----------------------------
ALTER TABLE [dbo].[K302 Zhuhai JJ$DMSInterfaceInfo] ADD CONSTRAINT [PK__DMSInter__248139D58BC743B2] PRIMARY KEY CLUSTERED ([Entry No_])
WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)  
ON [PRIMARY]
GO

