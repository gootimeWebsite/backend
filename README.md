# backend
后端部分

---
## 项目进度
后端部分进度如下  
数据库部分:
- User表存储用户信息
- Message表存储短信验证码
- Article表存储新闻文章
- ArticleRole表存储新闻版块角色权限
- Forum表存储论坛帖子
- ForumRole表存储论坛版块角色权限

完成了认证功能，用户登录返回短期token和长期rftoken  
完成了蓝图中restfulAPI的框架设计  
完成了用户权限的数据库设计  
完成了初步的后台设计  
完成了单元测试，代码覆盖率达到90%以上  
完成了日志系统的搭建，输出日志到log/server.log  

API：见apidoc文档

下一步工作：  
- 完善API

## 项目部署

依赖库安装：  
`pip install -r requirements.txt`  

创建数据库：  
`python run.py connectdb -u <username> -p <password>`  
配置文件见 config.py  

初始化数据库，创建数据表：  
`python run.py initdb`  

单元测试：  
`python run.py test`  

分析代码覆盖率:  
`python run.py test -c True`  

Python3.6本地运行：  
`python run.py` (debug模式) 或：  
`python run.py runserver -d <debug> -h <host> -p <port>`  

后台终端:  
`python run.py shell`  
其中调用run()函数运行服务器 (非debug模式)
