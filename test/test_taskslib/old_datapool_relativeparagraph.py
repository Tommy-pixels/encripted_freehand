from taskslib.tasks_postdata.old_datapool.task_post_keyparagraph import Task_Post_Keyparagraph
from taskslib.tasks_postdata.old_datapool import \
    task_post_relateparagraph

if __name__ == '__main__':
    # tk = Task_Post_Keyparagraph()
    # res = tk.run()
    timerConfig = {}
    tprp = task_post_relateparagraph.Task_Post_Relativeparagraph()
    tprp.env_config = timerConfig
    res = tprp.run('tb_relative_paragraph', ['公共', '股市', 'A股', '港股', '新股', '美股', '创业板', '证券股', '股票', '炒股', '散户', '短线', '操盘', '波段'])
    print(res)
