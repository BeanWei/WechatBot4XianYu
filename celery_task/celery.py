from celery import Celery
from celery.signals import worker_ready


CeleryApp = Celery('celery_task', inclue=['celery_task.tasks'])
CeleryApp.config_from_object('celery_task.celeryconfig')


# worker_ready 为信号
@worker_ready.connect
def at_start(sender, **k):
    """
    Celery 跑起来的时候直接执行listener任务来运行机器人
    :param sender:
    :param k:
    :return:
    """
    with sender.app.connection() as conn:  # noqa
        sender.app.send_task('wechat.tasks.listener')


if __name__ == '__main__':
    CeleryApp.start()