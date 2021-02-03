今天突然发现可以批量下载了, 不过依旧不支持文件夹下载
2021年2月3日9时28分49秒

# teambition-download-folder
teambition批量下载

## 使用方法

1. 填写认证信息 **config.py**

   ```python
   # 填写相关认证信息
   cookies = {
       'TEAMBITION_SESSIONID': '',
       'TEAMBITION_SESSIONID.sig': ''
   }                                                                 
   ```

2. 安装依赖

   ```bat
   pip install -r requirements.txt
   ```

3. 执行主文件

   ```bat
   python main.py
   ```

   

