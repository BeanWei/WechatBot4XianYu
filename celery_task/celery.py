from celery import Celery
from celery.signals import worker_ready


CeleryApp = Celery('celery_task', inclue=['celery_task.tasks'])
CeleryApp.config_from_object('celery_task.celeryconfig')


# @worker_ready.connect
# def at_start(sender, **k):
#     with sender.app.connection() as conn:  # noqa
#         task_id = sender.app.send_task('wechat.tasks.listener')
#         # db.set(LISTENER_TASK_KEY, task_id)


if __name__ == '__main__':
    CeleryApp.start()