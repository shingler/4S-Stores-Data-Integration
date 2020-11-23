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

 Date: 23/10/2020 18:27:43
*/


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
-- Primary Key structure for table K302 Zhuhai JJ$FABuffer
-- ----------------------------
ALTER TABLE [dbo].[K302 Zhuhai JJ$FABuffer] ADD CONSTRAINT [PK__FABuffer__AA723669918A383E] PRIMARY KEY CLUSTERED ([Record ID])
WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)  
ON [PRIMARY]
GO

