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

 Date: 23/10/2020 18:27:21
*/


-- ----------------------------
-- Table structure for K302 Zhuhai JJ$CustVendBuffer
-- ----------------------------
IF EXISTS (SELECT * FROM sys.all_objects WHERE object_id = OBJECT_ID(N'[dbo].[K302 Zhuhai JJ$CustVendBuffer]') AND type IN ('U'))
	DROP TABLE [dbo].[K302 Zhuhai JJ$CustVendBuffer]
GO

CREATE TABLE [dbo].[K302 Zhuhai JJ$CustVendBuffer] (
  [Record ID] int  NOT NULL,
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
-- Primary Key structure for table K302 Zhuhai JJ$CustVendBuffer
-- ----------------------------
ALTER TABLE [dbo].[K302 Zhuhai JJ$CustVendBuffer] ADD CONSTRAINT [PK__CustVend__AA7236695923DF06] PRIMARY KEY CLUSTERED ([Record ID])
WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)  
ON [PRIMARY]
GO

