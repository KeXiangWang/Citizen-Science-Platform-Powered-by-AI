# OmniSci部署手册

## Web部署
1. 登录服务器
2. 安装python3.7
3. 将项目克隆到本地
3. `cd OmniSci/`
4. `git pull origin release`
5. `git checkout release`
4. `pip3 install -r requirements.txt` 或者 `source install.sh`
5. `source rerun.sh`

注意：
1. 对数据库进行修改后，请运行 `python manage.py rebuild_index` 重新建立数据库索引
2. git仓库内共两个分支：master和release。一般修改项目、修复问题在master分支上进行，测试无问题后在软开云上将master分支合并到release分支即可。
## Android部署
1. 登录服务器
2. `cd Android/`
3. 将目录下的app-release.apk文件scp到本地
4. 将app-release.apk文件从本地传输到Android手机
5. 在手机上点击安装由系统自动安装