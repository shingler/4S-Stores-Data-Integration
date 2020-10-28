/*
 Navicat Premium Data Transfer

 Source Server         : local
 Source Server Type    : MySQL
 Source Server Version : 50649
 Source Host           : localhost:3306
 Source Schema         : NAV

 Target Server Type    : MySQL
 Target Server Version : 50649
 File Encoding         : 65001

 Date: 25/10/2020 15:40:50
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for K302 Zhuhai JJ$CustVendBuffer
-- ----------------------------
DROP TABLE IF EXISTS `K302 Zhuhai JJ$CustVendBuffer`;
CREATE TABLE `K302 Zhuhai JJ$CustVendBuffer`  (
  `Record ID` int(11) NOT NULL AUTO_INCREMENT COMMENT '非自增字段',
  `No_` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Address` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `City` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Post Code` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Country` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Currency` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'FA记录数, 对应FA文件或接口',
  `Gen_ Bus_ Posting Group` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `VAT Bus_ Posting Group` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Cust_VendPostingGroup` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Application Method` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `PaymentTermsCode` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Template` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Entry No_` int(11) NOT NULL,
  `Error Message` varchar(250) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `DateTime Imported` datetime(0) NOT NULL COMMENT '导入时间',
  `DateTime Handled` datetime(0) NOT NULL COMMENT '处理时间, 初始插入数据时插入(\'1753-01-01 00:00:00.000\')',
  `Type` int(11) NOT NULL COMMENT '类型(0 - Customer, 1 - Vendor, 3 - Unknow)',
  `Handled by` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '处理人',
  `Address 2` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `PhoneNo` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `FaxNo` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Blocked` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Email` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `ARAPAccountNo` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `PricesIncludingVAT` int(11) NOT NULL,
  `PaymentMethodCode` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Cost Center Code` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `ICPartnerCode` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`Record ID`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 17 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = COMPACT;

-- ----------------------------
-- Table structure for K302 Zhuhai JJ$DMSInterfaceInfo
-- ----------------------------
DROP TABLE IF EXISTS `K302 Zhuhai JJ$DMSInterfaceInfo`;
CREATE TABLE `K302 Zhuhai JJ$DMSInterfaceInfo`  (
  `Entry No_` int(11) NOT NULL AUTO_INCREMENT COMMENT '非自增字段',
  `DMSCode` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `DMSTitle` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `CompanyCode` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `CompanyTitle` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `CreateDateTime` datetime(0) NOT NULL,
  `Creator` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `DateTime Imported` datetime(0) NOT NULL COMMENT '导入时间',
  `DateTime Handled` datetime(0) NOT NULL COMMENT '处理时间',
  `Handled by` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '处理人',
  `Status` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '状态(INIT, PROCESSING, ERROR, COMPLETED), 初始插入数据INIT',
  `Error Message` varchar(250) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '错误消息, 初始插入数据时插入空字符(\'\')',
  `XMLFileName` varchar(250) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'XML文件名',
  `Customer_Vendor Total Count` int(11) NOT NULL COMMENT '客户供应商记录数，对应CustVendorInfo文件或接口',
  `Invoice Total Count` int(11) NOT NULL COMMENT '发票记录数, 对应Invoice文件或接口',
  `Type` int(11) NOT NULL COMMENT '类型(0 - CustVendInfo, 1 - FA, 2 - Invoice, 3 - Other)',
  `Other Transaction Total Count` int(11) NOT NULL COMMENT 'Other记录数, 对应Other文件或接口',
  `FA Total Count` int(11) NOT NULL COMMENT 'FA记录数, 对应FA文件或接口',
  PRIMARY KEY (`Entry No_`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 28 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = COMPACT;

-- ----------------------------
-- Table structure for K302 Zhuhai JJ$FABuffer
-- ----------------------------
DROP TABLE IF EXISTS `K302 Zhuhai JJ$FABuffer`;
CREATE TABLE `K302 Zhuhai JJ$FABuffer`  (
  `Record ID` int(11) NOT NULL,
  `FANo_` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Description` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `SerialNo` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Inactive` int(11) NOT NULL,
  `Blocked` int(11) NOT NULL,
  `FAClassCode` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `FASubclassCode` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `FALocationCode` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `BudgetedAsset` int(11) NOT NULL,
  `VendorNo` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `MaintenanceVendorNo` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Entry No_` int(11) NOT NULL,
  `Error Message` varchar(250) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '错误消息',
  `DateTime Imported` datetime(0) NOT NULL COMMENT '导入时间',
  `DateTime Handled` datetime(0) NOT NULL COMMENT '处理时间, 初始插入数据时插入(\'1753-01-01 00:00:00.000\')',
  `UnderMaintenance` int(11) NOT NULL,
  `Handled by` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '处理人, 初始插入数据时插入空字符(\'\')',
  `NextServiceDate` datetime(0) NOT NULL,
  `WarrantyDate` datetime(0) NOT NULL,
  `DepreciationPeriod` int(11) NOT NULL,
  `DepreciationStartingDate` datetime(0) NOT NULL,
  `CostCenterCode` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`Record ID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = COMPACT;

-- ----------------------------
-- Table structure for K302 Zhuhai JJ$InvoiceHeaderBuffer
-- ----------------------------
DROP TABLE IF EXISTS `K302 Zhuhai JJ$InvoiceHeaderBuffer`;
CREATE TABLE `K302 Zhuhai JJ$InvoiceHeaderBuffer`  (
  `Record ID` int(11) NOT NULL,
  `InvoiceNo` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Posting Date` datetime(0) NOT NULL,
  `Document Date` datetime(0) NOT NULL,
  `Due Date` datetime(0) NOT NULL,
  `PayToBillToNo` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `SellToBuyFromNo` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `CostCenterCode` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `VehicleSeries` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `ExtDocumentNo` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Entry No_` int(11) NOT NULL,
  `InvoiceType` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `DateTime Imported` datetime(0) NOT NULL,
  `DateTime handled` datetime(0) NOT NULL COMMENT '处理时间',
  `Error Message` varchar(250) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '错误消息',
  `Handled by` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '处理人',
  `Line Total Count` int(11) NOT NULL COMMENT '发票行里的记录数',
  `PriceIncludeVAT` int(11) NOT NULL,
  `Description` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Location` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`Record ID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = COMPACT;

-- ----------------------------
-- Table structure for K302 Zhuhai JJ$InvoiceLineBuffer
-- ----------------------------
DROP TABLE IF EXISTS `K302 Zhuhai JJ$InvoiceLineBuffer`;
CREATE TABLE `K302 Zhuhai JJ$InvoiceLineBuffer`  (
  `Record ID` int(11) NOT NULL,
  `Line No_` int(11) NOT NULL,
  `DMSItemType` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `GLAccount` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Description` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `CostCenterCode` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `VehicleSeries` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `VIN` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Quantity` decimal(38, 20) NOT NULL,
  `Line Amount` decimal(38, 20) NOT NULL,
  `LineCost` decimal(38, 20) NOT NULL,
  `TransactionType` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Entry No_` int(11) NOT NULL,
  `Error Message` varchar(250) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '错误消息',
  `DateTime Imported` datetime(0) NOT NULL COMMENT '导入时间',
  `DateTime Handled` datetime(0) NOT NULL COMMENT '处理时间',
  `Handled by` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '处理人',
  `InvoiceNo` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Line Discount Amount` decimal(38, 20) NOT NULL,
  `WIP No_` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Line VAT Amount` decimal(38, 20) NOT NULL,
  `Line VAT Rate` decimal(38, 20) NOT NULL,
  `FromCompanyName` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `ToCompanyName` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Location` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `MovementType` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `OEMCode` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`Record ID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = COMPACT;

-- ----------------------------
-- Table structure for K302 Zhuhai JJ$OtherBuffer
-- ----------------------------
DROP TABLE IF EXISTS `K302 Zhuhai JJ$OtherBuffer`;
CREATE TABLE `K302 Zhuhai JJ$OtherBuffer`  (
  `Record ID` int(11) NOT NULL,
  `DocumentNo_` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `TransactionType` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Line No_` int(11) NOT NULL,
  `Posting Date` datetime(0) NOT NULL,
  `Document Date` datetime(0) NOT NULL,
  `ExtDocumentNo_` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Account No_` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Description` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Debit Value` decimal(38, 20) NOT NULL,
  `Credit Value` decimal(38, 20) NOT NULL,
  `CostCenterCode` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `VehicleSeries` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Entry No_` int(11) NOT NULL,
  `DateTime Imported` datetime(0) NOT NULL,
  `DateTime handled` datetime(0) NOT NULL COMMENT '处理时间',
  `Error Message` varchar(250) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '错误消息',
  `Handled by` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '处理人',
  `AccountType` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `WIP No_` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `FA Posting Type` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `EntryType` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `FromCompanyName` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `ToCompanyName` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `VIN` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `SourceType` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `SourceNo` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `NotDuplicated` int(11) NOT NULL,
  `NAVDocumentNo_` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `DMSItemType` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `DMSItemTransType` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Location` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `MovementType` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`Record ID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = COMPACT;

SET FOREIGN_KEY_CHECKS = 1;
