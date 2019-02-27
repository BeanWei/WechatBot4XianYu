from celery import Celery
from celery.signals import worker_ready


CeleryApp = Celery('celery_task', inclue=['celery_task.tasks'])
CeleryApp.config_from_object('celery_task.celeryconfig')


# worker_ready 为信号
@worker_ready.connect
def at_start(sender, **k):
    """
    Celery 跑起来的时候直接执行
                      1.  listener任务来运行机器人
                      2.  xyspider任务来运行爬虫
    :param sender:
    :param k:
    :return:
    """
    with sender.app.connection() as conn:  # noqa
        sender.app.send_task('celery_task.tasks.listener')
        sender.app.send_task('celery_task.tasks.xyspider')


if __name__ == '__main__':
    CeleryApp.start()