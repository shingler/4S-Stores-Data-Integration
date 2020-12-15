## 更新说明及后续版本计划

当前版本：v 0.6.4

### 更新说明

#### v 0.6.4

- 增加对文件大小的判断，可通过API设置File_Size_Max来定义，单位：M；
- 当归档失败时，保证后续动作继续；
- 修复手动调用时，对options里参数不起作用的问题；

#### v 0.6.3

- 支持对主进程中非CustVend任务的多线程进行配置管理；
- 存储入参时将保存完整的数字签名；

#### v 0.6.2

- 回滚了0.6.1，基于0.6.0；
- 优化了master的线程调度，改为custvend单线程堵塞执行，其他任务多线程执行；

#### v 0.6.1
- 手动执行事务提交以减少SQL Server的连接丢失问题；

#### v 0.6.0

- 多线程主程序master改为以公司为单位进行任务调度；
- 修改多线程写库有可能造成写库混乱的问题；

#### v 0.5.9

- 改进日志记录；

#### v 0.5.6

- 优化bin.log日志内容，带上公司代码和api代码；
- 访问NAV的ws时，改为同步模式；

#### v 0.5.5

- 当archive_path为空时，不再做归档操作；
- Node:T,r,a,n,s,a,c,t,i,o,n is missing的问题分析和解决；
- bin.log输出调用ws的userID和密码；

#### v 0.5.4

- 优化任务判断和分发逻辑；
- 增加接口调用的日志输出；
- 任务时间冗余量及日志开关读自配置；
- 修正api日志中，入参没有记录和api_content返回dms原文；

#### v 0.5.3

- DMS的json请求的错误处理；
- 输入参数日期公式支持；
- 解析内容，一级二级标题读取自配置；

#### v 0.5.2

- 修复timestamp导致写库报错问题；
- 修复一些字段的内容导入不符合预期的问题；
- 支持PYYYYMMDD的文件格式，取昨天的数据文件；
- 修改邮件标题

#### v 0.5

##### DMS的JSON接口

- 支持DMS的JSON接口请求流程；
- 对DMS接口读取的日志记录；
- 动态写nav数据库；
- 检查字段内容长度通过DMS_API_P_Out的配置来判断；
- 检查字段内容长度时，读取system设置来决定超长内容报错还是截断；

##### 0.4版本的修复

- 提供给NAV的web api针对没有提供file_path的情况，不再读取当天的数据文件；
- 数据重复导入，只检查文件名，忽略路径；
- 修复时间检查不准确的问题；

#### v0.4.4

- 11月12日word文档里提出的优化；
- 任务加载指定顺序（Company_Code,Execute_Time,Sequence asc）；
- 针对非SSL邮件服务器做优化（system设置里是否启用ssl）；
- 任务执行的时候，需要做如下判断：
  1.DMS_Company_List表里DMS_Interface_Activated为1-继续执行，0-执行下一个任务
  2.DMS_API_Setup表里Activated为1-继续执行，0-执行下一个任务
- 任务脚本调用用api_setup的callback_command_code来判断；
- 一个文件一个提醒邮件，收件人里可以是多个
- 修改邮件内容

#### v 0.4.3

- 使用指定的测试用例进行调试

#### v 0.4.2

##### 11月6日、9日的修改意见

- 修正Other数据的数量统计错误和中文乱码问题；
- 修正发票明细导入不全的问题；
- 对XML做节点完整性验证，不符合则写错误日志并根据设置发送提醒邮件；
- 修改提醒邮件的内容模板并和报错话术放在一起；
- 调用NAV的WebService方式变更（SoapAction及CommandCode）；
- 将对外接口统一为一个；

#### v 0.4.1

##### 11月5日的问题修复

- API日志中XML内容需要做中文编码，以便于数据库中能看到中文；
- NAV表中特定字段需要按照一个汉字=2个字符来做长度判断（参照Database20201105.xlsx）；
- 将报错话术统一独立处理；
- web service的500错误忽略；
- xml文件名格式支持“YYYYMMDD”、“YYYY.MM.DD”，“YYYY-MM-DD”；

#### v 0.4

##### 多线程处理

- 调度程序为主线程，通过扫描Task表，将符合运行条件的task分别为一个子线程运行；
- 子线程内部异步调用web service；
- 通过手动调用的api将会同步调用web service；

##### 脚本修正

- other的数量统计改为统计行数，忽略Daydook节点；

##### 其他

- 任务处理增加类型4：失败发提醒；
- 通过对DMSInterfaceInfo表中导入文件名的判断，来决定是否导入数据（避免重复导入），并写入API_Log（手动、自动模式均适用）；
- 手动调用的接口增加重复导入的错误码；
- 针对只有General节点的xml文件做了修正；
- 对xml文件里时间格式做了统一化预处理（只取YYYY-mm-ddTHH:MM:SS）;
- 对web service的返回状态只处理40x错误；
- 优化了对NAV表需要转中文的字段逻辑处理；
- 对task.py，master.py做了命令行参数设置；



#### v 0.3

##### 脚本修正

- windows测试环境下可能出现的bug修正
- windows测试环境下sql server 2008的中文处理
- 任务调度脚本（需判断开始时间条件是否满足）
- 访问nav的web service，并记录相应日志

##### 供NAV访问的接口

- 数据流向为从DMS到Buffer，参数为Company_Code和API_Code；
- 数据流向为从Buffer到NAV；

##### 压力测试

- 1M、5M、10M大小的xml读取时间
- 结合超时设置，发送超时邮件

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




