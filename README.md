# 1.bilibili_push
小爬虫——b站up主更新视频推送

创建的时候，传入两个参数，bid——你的B站id，email——你能收到的邮箱
里面有连数据库的，稍微注意下。
有问题提问吧（本来想开服务的，但是我们朋友们貌似没有这个需求）。

### 9-28
以前只能爬取少量的页数，现在修改成动态爬取，每次50个关注，一共5页，因为B站规定除了本人外只能查看他人5页的关注数
 
新添加 config.py 都是一些配置项，比如数据库，email推送的接口，自行导入吧。

### 邮箱格式
 title：标题
 msg：内容
 to：收件人
 
 
# 2.flask_lib_spider

用flask写的爬取学校图书馆的书籍数据接口，传入书籍id即可

# 3.image_maker

maker.py为入口文件，具体功能就是生成表情包（需要传入模版图）

# 4.lsu_final_exam_result

爬取学校期末考试成绩，传入姓名和学号即可

# 5.lsu_login
python 模拟登陆方正系统教育系统

login_code 是存登录时候的验证码的文件

train
 image 训练集
 cnn_dama.py 训练文件
 check.py 识别验证码
 ok.h5 训练好的模型

# 6.mybatis_tools
二次处理mybatis逆向工程生成的实体类,Dao层,XML文件

1.实体类加上@Data注解，继承PageHelper（XML分页）

2.Dao层加上Component注解

3.XML加上分页sql语句

## 2019-02-13
Mybatis逆向工程生成的实体类默认对应关系
数据库类型 tinyint -> Byte 二次处理成 Integer
          decimal -> Short 二次处理成 BigDecimal
# 7.vjudge_auto_register
### Vjudge注册（10-16）
register里面是自动注册帐号的(需要手动输入验证码)
### 分发帐号（10-17）
程序在getAccount包里面
用flask写的后台，直接用模版了，没分离。而且还是用的单文件，接受到的信息，直接存json文件了，这样方便。
### update
根据新生填写的表单得到的json文件，来修改vjudge账号的信息（用户名等）


