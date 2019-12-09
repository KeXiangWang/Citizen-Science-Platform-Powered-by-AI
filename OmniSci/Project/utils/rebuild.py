from haystack.management.commands import update_index, rebuild_index
from os import system


def rebuild():
    # FIXME 暂时修补，不知道为什么update_index无法起作用，
    #  自动更新无效，rebuild_index command无法正确执行，
    #  所以用了最原始的写法
    # update_index.Command().handle(using='default')
    # rebuild_index.Command().handle(interactive=False)
    print('hit rebuild')
    system('python manage.py rebuild_index --noinput')