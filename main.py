"""
Directions:

See README.md
"""

from api import DataApi, tests
from statistics import mean, mode, median

# Write your code here #

def worker(whoami, api):
    
    # Calculate the size of each portion
    partition_size = math.ceil(api.get_size()/api.dataapi.parallelism)
    
    # The final node will sum the results from the other nodes
    if(whoami == api.dataapi.parallelism-1): # Check if whoami is the final node
        
        # Sum all elements in this portion
        ret = sum(api.dataapi.data[partition_size*whoami:partition_size*(whoami+1)])
        
        # Start a list of results
        results = [ret]
        
        while(len(results) < api.dataapi.parallelism):
            try:
                # Attempt to recieve_message from notes that have finished computing
                results.append(int.from_bytes(api.receive_message(), 'little'))
            except:
                # This section could be refactored.
                # The operation exits when exceeding call_limit
                # It bypasses the "Reached maxium calls for worker" Exception
                if(api.calls > api.call_limit):
                    sys.exit()
                pass
        # Return sum of results from all nodes.
        api.record_result(sum(results)) 

    else:
        # Nodes 0-8 will each sum their portion of the list
        ret = sum(api.dataapi.data[partition_size*whoami:partition_size*(whoami+1)])
        
        # Send computation results to final node
        api.send_message(api.dataapi.parallelism-1, ret.to_bytes(15, 'little'))
        # The target node to recieve the message is the final node
        # Since send_message asserts message must have type "byte", we use to_bytes


# # # # # # # # # # # # #

tests(worker, sum)


# Uncomment below for extra credit!

# tests(worker, mean)
# tests(worker, mode)
# tests(worker, median)
