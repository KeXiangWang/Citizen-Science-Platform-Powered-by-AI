

#================================================================
#   Copyright (C) 2019 OmniSci. All rights reserved.
#
#   Title：run.sh
#   Author：Yong Bai
#   Time：2019-03-31 09:52:18
#   Description：For Linux User
#
#================================================================

# 检查数据库是否更新
python manage.py makemigrations

python manage.py migrate

# 往数据库批量添加项目,为避免重复会先把数据库项目表清空,请谨慎使用
# python manage.py createProject

# 创建admin超级用户,用于对于项目数据的快速管理
# python manage.py createsuperuser

# 建立数据库索引
python manage.py rebuild_index

# run
python manage.py runserver 0.0.0.0:80
