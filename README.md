# Free Proxy 
Free Proxy 代理池项目。仅支持python3. (python 3.8+最好，其他版本没测试过)

### Notice:
    1. 目前只支持一个网站的代理
    2. 爬取速度快
    3. 可验证是否有效
    4. 存入sqlite3数据库
    5. 存入文件
    6. 日志打印
    7. 安装相关依赖

### 数据库 ProxyIp 
    1. proxy_ip表 : 存入爬取后的代理
        字段: insert_time ip port area country proxy_type support_protocol response_speed validate_time
    2. verified_proxy表 : 存入验证后的代理
        字段: ip port area country proxy_type support_protocol response_speed validate_time proxy_link

### 更新时间

____________________________________________________________________________
#### 2023-09-12