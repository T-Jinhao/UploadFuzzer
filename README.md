# UploadFuzzer
### 描述
构造动态文件上传

### 功能
- 可填写api等进行动态文件上传
- 含有简单的bypass功能，如构造各种畸形请求绕过
- 可选择正常图片再attach webshell上传
- 可选择带有cookies请求

### 参数
选项 | 示例 | 作用
--- | --- | ---
-h | |帮助
-u | -u htttp://xxx.com/upload | 文件上传路径
-c | -c "sessionid=xxx;userid=1" | 身份认证，cookies，格式为document.cookie()
-f | -f ~/image/a.jpg | 上传的文件
--field | --field upload_file | 文件上传对应的参数值
--data | --data "submit=提交;token=xxx" | 文件上传时一并发送的数据
--attach | --attach ~/exploit/webshell.php | webshell文件，附加时将尝试合并在正常文件内
--bypass | --bypass | 尝试构造畸形请求绕过WAF，成功即停
--bypass_ignore | --bypass_ignore |  尝试构造畸形请求绕过WAF，将尝试全部payload
--content_type | --content_type png | 指定文件上传类型，可MIME欺骗

### 开发ing
- 普通文件上传已完成
- bypass部分持续开发中