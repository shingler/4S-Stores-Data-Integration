##更新说明及后续版本计划

当前版本：v 0.2

### 更新说明

#### v 0.2

##### API日志

- 开始访问接口时新增API日志（**无论访问成功还是失败**），并在数据读取完成后，修改该日志的状态和结果；
  - 对文件读取的日志记录；

##### 任务设置

- 读取时应根据Task_Setup.API_Type来判断。Data_Format仅当做数据处理转换的判断依据。DMS的接口和文件均有可能返回JSON格式或XML格式。
- DMS接口读取完成，更新DMS_Task_Setup.Last_Executed_Time；
- 任务失败处理=3，改为重试一次。再次失败发送报警邮件；

##### 提醒邮件

- DMS接口重试依然报错且失败处理=3；
- 两种收件人：（1）DMS_Notification_User中相应公司编码的IT人员；（2）User_List中Receive_Notification=1的所有人员；

##### 数据库变动

- API日志增加字段：Status（访问状态），Error_Message（错误信息）和API_Direction（接口访问方向）；

- NAV的6张表将转移到其他库，且表名会修改。可以根据Company_List里的数据库相关字段拼接连接字符串及表名（Company_List.NAV_Company_Code + '\$' + DMS_API_Setup.Table_Name）。

```
	NAV_DB_Name，NAV_DB_Address，NAV_DB_UserID，NAV_DB_Password，NAV_Company_Code
```

#### v 0.1

 - 根据公司数据和api设置对指定目录下的xml进行读取
 - 根据api输出参数设置，将数据保存到对应的数据库中
 - General数据保存在interfaceInfo表，除发票保存在发票抬头和发票明细表中，其他数据都保存在对应的表中。

### 后续版本计划

#### v 0.3

##### 脚本修正

	- windows测试环境下可能出现的bug修正
	- windows测试环境下sql server 2008的中文处理
	- 任务调度脚本（需判断开始时间条件是否满足）
	- 访问nav的web service，并记录相应日志

##### 供NAV访问的接口

- 数据流向为从DMS到Buffer的接口，参数为Company_Code和API_Code；
- 数据流向为从Buffer到NAV的接口；

##### 压力测试

- 1M、5M、10M大小的xml读取时间
- 结合超时设置，发送超时邮件

#### 后续列表

- 开始访问接口时新增API日志
  - <u>对DMS接口读取的日志记录需等到DMS接口就绪</u>；
  - <u>对NAV接口读取的日志记录需等到NAV接口就绪</u>；

- ##### 多线程处理：

  - 调度程序为主线程，4种接口分别为一个子线程；
  - 主线程可以根据DMS_API_Setup中规定的超时时间为依据，对读取数据结束后的时间做判断。超过时间可中止线程并发送超时邮件；