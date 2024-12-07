# coding:utf-8
from multiprocessing import Pool
from uuid import uuid1


def main():
    pass


class ProcessPool():
    """ 维护一个线程池 """
    
    def __init__(self, size):
        self.pp = Pool(processes=size)
        self.ars_pool = []

    def run(self, func, args=(), kwds={}, name=None, callback=None, error_callback=None):
        id_ = uuid1()
        mess = {'id':id_, 'name':name}
        ars = self.pp.apply_async(func=func, args=args, kwds=kwds, callback=callback, error_callback=error_callback)
        mess['ars'] = ars
        self.ars_pool.append(mess)
        return id_
    
    def wait(self):
        self.pp.close()
        self.pp.join()
        
    def get_running_num(self):
        i = 0
        for ars in self.ars_pool:
            if not ars['ars'].ready():
                i = i + 1
        return i
    
    def get_running_name(self):
        running_list = []
        for ars in self.ars_pool:
            if not ars['ars'].ready():
                running_list.append(ars['name'])
        return running_list
    

if __name__ == '__main__':
    main()
