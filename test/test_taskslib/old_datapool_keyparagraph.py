from taskslib.tasks_postdata.old_datapool.task_post_keyparagraph import Task_Post_Keyparagraph
from taskslib.tasks_postdata.old_datapool import \
    task_post_keyparagraph

if __name__ == '__main__':
    # tk = Task_Post_Keyparagraph()
    # res = tk.run()
    timerConfig = {}
    tpkp = task_post_keyparagraph.Task_Post_Keyparagraph()
    tpkp.env_config = timerConfig
    res = tpkp.run('tb_key_paragraph')
