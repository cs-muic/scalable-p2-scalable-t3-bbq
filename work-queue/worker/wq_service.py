from celery.result import AsyncResult

import compose
import extract


def issue_tasks(worker, tasks):
    extract_q = []
    compose_q = []
    for param in tasks:
        if worker == 'extract':
            task = extract.celery_app.send_task('extract.get_frames', queue='q01', kwargs={'fp_in': param})
            extract_q.append(task)
        elif worker == 'compose':
            task = compose.celery_app.send_task('compose.to_gif', queue='q01', kwargs={'fp_out': param})
            compose_q.append(task)
    return extract_q, compose_q


def get_results(task_id):
    task_result = AsyncResult(task_id)
    result = {
        'task_id': task_id,
        'task_status': task_result.status,
        'task_result': task_result.result,
        'task_bucket': task_result.task_bucket
    }
    return result


def run_task(worker, tasks):
    extract_q, compose_q = issue_tasks(worker, tasks)
    while 1:
        done = True
        for tid in extract_q:
            res = get_results(tid)
            if res['task_status'] == 'SUCCESS':
                compose_q.append('tid?????')
                print(f'queue: q01, task: {tid}, result: {res["task_result"]}')
            elif res['task_status'] == 'FAILURE':
                print(f'queue: q01, task: {tid}, result: {res["task_result"]}')
            else:
                done = False
                print(f'queue: q01, task: {tid}, status: {res["task_status"]}')
        compose_q = issue_tasks('compose', compose_q)

        for tid in compose_q:
            res = get_results(tid)
            if res['task_status'] == 'SUCCESS' or \
                    res['task_status'] == 'FAILURE':
                print(f'queue: q02, task: {tid}, result: {res["task_result"]}')
            else:
                done = False
                print(f'queue: q02, task: {tid}, status: {res["task_status"]}')
        if done:
            break


if __name__ == '__main__':
    run_task('extract', ['../../test3.mp4'])
