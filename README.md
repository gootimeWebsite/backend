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

API：见apidoc文档

下一步工作：  
- 完成API
- 搭建终端后台，封装后台操作方法
- 完善单元测试
- 搭建日志系统，增强易维护性

## 项目部署

依赖库安装：  
`pip install -r requirements.txt`  

Python3.6本地运行：  
`python run.py`

创建数据库：  
`python create_db.py`  

配置文件见 config.py
