"""?"""
from queue import Queue
from threading import Thread, Lock
import os
import json
from app.data_ingestor import DataIngestor

class ThreadPool:
    """threadpool"""
    def __init__(self):
        """init"""
        self.job_queue = Queue()
        self.threads = []
        self.job_dict = {}

        # getting the number of threads
        if os.getenv("TP_NUM_OF_THREADS"):
            self.number_of_threads = int(os.getenv("TP_NUM_OF_THREADS"))
        else:
            self.number_of_threads = os.cpu_count()

        for i in range(self.number_of_threads):           
            tasks = TaskRunner(self, self.job_queue, self.job_dict)
            tasks.start()
            self.threads.append(tasks)


    def add_task(self, job_id, data, question_type, target_state):
        """add job to job_queue"""
        self.job_queue.put((job_id, data, question_type, target_state))

class TaskRunner(Thread):
    """asynchronous tasks"""

    def __init__(self, thread_pool, job_queue, job_dict):
        super().__init__()
        self.thread_pool = thread_pool
        self.job_queue = job_queue
        self.job_dict = job_dict
        self.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")
        self.lock = Lock()

    def run(self):
        """run task"""
        while True:
            #get work
            work = self.job_queue.get()

            #extract parameters
            work_q = work[1]
            q = work_q['question']

            if work[2] == "/api/state_mean":
                result = self.data_ingestor.state_mean(q, work[3])
            elif work[2] == "/api/state_diff_from_mean":
                result = self.data_ingestor.state_diff_from_mean(q, work[3])
            elif work[2] == "/api/state_mean_by_category":
                result = self.data_ingestor.state_mean_by_category(q, work[3])
                
            #handle general endpoints
            elif work[2] == "/api/states_mean":
                result = self.data_ingestor.states_mean(q)
            elif work[2] == "/api/global_mean":
                result = self.data_ingestor.global_mean(q)
            elif work[2] == "/api/best5":
                result = self.data_ingestor.best5(q)
            elif work[2] == "/api/worst5":
                result = self.data_ingestor.worst5(q)
            elif work[2] == "/api/diff_from_mean":
                result = self.data_ingestor.diff_from_mean(q)
            elif work[2] == "/api/mean_by_category":
                result = self.data_ingestor.mean_by_category(q)

            #lock for shared resource
            with self.lock:
                self.job_dict[work[0]] = result

            file_path = os.path.join(f'results/job_id_{work[0]}.json')
            with open(file_path, 'w') as f:
                f.write(json.dumps(result))

            
            #no work = stop
            if work is None:
                break
