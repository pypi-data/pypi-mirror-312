## Trans curl request to  json data

将参数转化为json 的时候尽量使用 -- 之后的值，作为字典的键。
这个库的目的是将curl 发送请求的参数转化为json 格式，方便在python 中使用。

curl 功能很强大，支持的参数也很多，这里只做了部分的解析

重点放在curl HTTP发送请求的方面.

其他一些特性，--ipv4,--ipv6,本地文件读取，指定dns 寻址服务器
DoH,ftp 等协议暂未支持

支持的参数

- `-X`, `  --request` 支持的请求方法，

- `--http2` 是否使用http2 协议 默认为否

- `-d`,`--data` 支持, 支持在一行命令中多次使用`-d` 参数，此时HTTP 请求头中
  `Content-Type : application/x-www-form-urlencoded`

  使用该参数，请求自动转化为POST.

- `-H`,`--header`  添加HTTP请求头,支持多行

- `-I`,`--head` 发送HEAD请求，并打印header，支持

- `-s`,`--silent`, 不输出任何东西，只返回HTTP 头

- `-v`, `--verbose` 输出通信的整个过程，用于调试

- `-b`, `--cookie` cookie 支持多个-b 参数，不支持文件读取

- `-A`, `--user-agent` 设置User-Agent,curl 默认的User-Agent 为 curl/version,本项目默认为空

- `--compressed` 是否压缩请求

- `-k`, `--insecure` 允许不验证服务器的证书

- `-u`, `--user` 用户名:密码

- `-L`, `--location` 允许自动跟随重定向

- `-I`,`--include` 打印头信息

- `-x`，`--proxy` 使用代理 代理 格式为：hostname:port，如果没有scheme 默认使用http

- `-U`, `--proxy-user` 代理用户名密码 ,格式为：username:password 如果有会自动将账号密码添加到代理url 中

- `-u`, `--user` basic 认证，格式为：username:password，输出为headers 中的Authorization

- `--connect-timeout` 连接超时时间

- `--referer` 请求头中的referer

## usage

1. 命令行中使用
```shell
python -m curl_to_json  curl_to_json curl -X GET http://example.com
```
2. 也可以直接使用 
```shell
curl_to_json curl -X GET http://example.com
```

3. 也可以使用 以下格式
```shell
curl_to_json "curl -X GET http://example.com"
```

4. 在python 代码中使用
```python
from curl_to_json import parse

cmd = 'curl -X GET http://example.com'

print(parse(cmd))

```

       
## Reference

*1. [curl 的用法指南](https://www.ruanyifeng.com/blog/2019/09/curl-reference.html)*

*2. [Linux命令大全-curl](https://hezhiqiang.gitbook.io/linux/ming-ling/curl)*

*3. [Uncurl](https://github.com/spulec/uncurl)*

*4. [curl 在线手册](https://man.cx/curl)*

