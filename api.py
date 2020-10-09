import random
import threading
import time, datetime
from statistics import mean
import sys

class DataApi:

    def __init__(self,
        func,
        data: list = None,
        parallelism: int = 10,
        size: int = 999,
        scope: int = 5000,
        check_func = sum,
        max_message_size = 50,
        max_worker_calls = 110
    ):
        self.func = func
        self.scope = scope
        self.max_message_size = max_message_size
        self.max_worker_calls = max_worker_calls
        
        self.check_func = check_func
        self.data = data or [random.randint(0, scope) for i in range(size)]
        self.size = len(self.data)

        self.parallelism = parallelism
        self.current_location = 0
        self.calls = 0
        self.messages = {i: [] for i in range(self.parallelism)}
        self.lock = threading.Lock()

        self.passed = False

    def get_size(self):
        return self.size

    def get_data(self, location):
        try:
            return self.data[location]
        except:
            return None

    def send_message(self, target, message):
        assert type(message) == bytes
        assert sys.getsizeof(message) <= self.max_message_size
        with self.lock:
            self.messages[target].append(message)

    def receive_message(self, target):
        start = datetime.datetime.now()
        while True:
            try:
                with self.lock:
                    return self.messages[target].pop()
            except:
                time.sleep(0.1)
                if datetime.datetime.now() - start > datetime.timedelta(seconds=5):
                    return Exception("Receive message timed out.")

    def record_result(self, result):
        if result == self.check():
            self.passed = True

    def run(self):
        start = datetime.datetime.now()
        threads = []
        for i in range(self.parallelism):
            worker = Worker(i, self, self.max_worker_calls)
            thread = threading.Thread(target=self.func, args=(i, worker))
            thread.daemon = True
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        if datetime.datetime.now() - start > datetime.timedelta(seconds=2):
            raise Exception('Not fast enough. Make sure you are taking advantage of parallelism.')

    def check(self):
        return self.check_func(self.data)


class Worker:
    def __init__(self, whoami, dataapi, call_limit=110):
        self.whoami = whoami
        self.dataapi = dataapi
        self.call_limit = call_limit
        self.calls = 0

    def call(self):
        time.sleep(0.01)
        if self.calls > self.call_limit:
            raise Exception(f'Reached maxium calls for worker {self.whoami}.')
        self.calls += 1

    def get_size(self):
        return self.dataapi.get_size()

    def send_message(self, target, message):
        self.call()
        self.dataapi.send_message(target, message)
    
    def receive_message(self):
        self.call()
        result = self.dataapi.receive_message(self.whoami)
        if type(result) == Exception:
            raise result
        return result

    def get_data(self, index):
        self.call()
        return self.dataapi.get_data(index)

    def record_result(self, result):
        self.call()
        self.dataapi.record_result(result)





def tests(worker, func):
    test_cases = {
        'Simple test 1': {'data': [1,2,3,4,5,1000]},
        'Simple test 2': {'data': [0]},
        'Medium case': {'data': list(range(500))},
        'Large random case 1': {'size': 999},
        'Large random case 2': {'size': 1000},
        'Large gauss case': {'data': [int(random.gauss(2500, 10)) for i in range(1000)]},
        'Large camel case': {'data': 
            [int(random.gauss(1000, 10)) for i in range(200)] +
            [int(random.gauss(3000, 10)) for i in range(800)]
        }
    }
    for test, kw in test_cases.items():
        api = DataApi(
            worker,
            check_func=func,
            **kw
            )
        api.run()
        status = 'passed' if api.passed else 'failed'
        print(f"{test}: {status}")
