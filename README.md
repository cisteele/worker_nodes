# worker_nodes
# CodingTest

### Directions:
Implement the worker function in `./main.py`

    ...
    def worker(whoami, api):
        pass
    ...

This function is called by worker node of a distributed compute cluster. The
objective is to implement this function so that when it is called by each of 10
workers, together they will compute the sum (or perhaps other functions) of a 
distributed list of integers.


The worker function receives 2 arguments:

`whoami`: an integer (0-9) indicating the worker calling the function.

`api`: An object with an interface to the distributed api with
  the following methods:

 - `api.record_result(result: int)`
      Should be called exactly once. Records the integer result of the distributed calulation.

 - `api.get_size()`
      Retrieves the length of the distributed list.

 - `api.get_data(index: int)`
      Retieves an item from a given `index` location from the distributed list.

 - `api.send_message(target: int, message: bytes)`
      Sends a `message` of no more that 50 bytes to a `target` worker node.

 - `api.receive_message()`
      Receives a message from the local worker's message queue. If there are no messages in
      the queue, the worker will wait for a message. This is a blocking call.

NOTE: There is a limit to the number of times a worker can call the api.

Hit the `run` button to test your function.
