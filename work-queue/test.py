import time
from celery.result import AsyncResult
from tasks import add


def issue_tasks():
    tasks = []
    for i in range(5):
        tasks.append(add.delay(i, i))
    return tasks


def get_results(task_id):
    task_result = AsyncResult(task_id)
    # result = {
    #     'task_id': task_id,
    #     'task_status': task_result.status,
    #     'task_result': task_result.result
    # }
    return task_result


def run_task():
    tasks = issue_tasks()
    while 1:
        done = True
        for task in tasks:
            res = get_results(task.task_id)
            print(res.backend())
            # if res['task_status'] == 'SUCCESS' or \
            #         res['task_status'] == 'FAILURE':
            #     print(res['task_result'])
            # else:
            #     done = False
            #     print(res['task_status'])
        print('sleeping for 1 secound ...')
        time.sleep(1)
        if done:
            break


if __name__ == '__main__':
    run_task()
