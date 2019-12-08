import threading
import datetime


class Task(object):
    def __init__(self, func_list=None):
        self.threads = []
        self.rs = {}
        self.func_list = func_list
        self.start()

    # 封装的线程函数
    def trace_func(self, func, name, *args, **kwargs):
        ret = func(*args, **kwargs)
        self.rs[name] = ret

    # 执行多线程
    def start(self):
        for v in self.func_list:
            if v["args"]:
                lists = []
                lists.append(v["func"])
                lists.append(v["name"])
                for arg in v["args"]:
                    lists.append(arg)
                    tuples = tuple(lists)
                    t = threading.Thread(target=self.trace_func, args=tuples)
            else:
                t = threading.Thread(target=self.trace_func, args=(v["func"], v["name"],))
            self.threads.append(t)
        for t in self.threads:
            t.start()
        for t in self.threads:
            t.join()