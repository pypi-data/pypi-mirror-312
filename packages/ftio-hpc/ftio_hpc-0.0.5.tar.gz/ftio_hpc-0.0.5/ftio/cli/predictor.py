"""This functions performs the prediction with the the help of ftio.py
"""
from __future__ import annotations
import sys
from multiprocessing import Manager
from ftio.prediction.pools import predictor_with_pools
from ftio.prediction.processes_zmq import predictor_with_processes_zmq
from ftio.prediction.processes import predictor_with_processes

def main(args: list[str] = sys.argv) -> None:
    """runs the prediction and launches new threads whenever data is available

    Args:
        args (list[str]): arguments passed from command line
    """
    # Init
    manager = Manager()
    filename = args[1]
    queue = manager.Queue()
    data = manager.list() # stores prediction
    aggregated_bytes = manager.Value("d", 0.0)
    hits = manager.Value("d", 0.0)
    start_time = manager.Value("d", 0.0)
    count = manager.Value('i', 0)
    b_app = manager.list()
    t_app = manager.list()
    
    mode = "procs" # "procs" or "pool"
    
    if "pool" in mode.lower():
        # prediction with a Pool of process and a callback mechanism
        predictor_with_pools(filename, data, queue, count, hits, start_time, aggregated_bytes, args)
    else:
        if any("zmq" in x for x in args):
            # prediction with Processes of process and a callback mechanism + zmq
            predictor_with_processes_zmq(data, queue, count, hits, start_time, aggregated_bytes, args, b_app, t_app)
        else:
            # prediction with Processes of process and a callback mechanism
            predictor_with_processes(filename, data, queue, count, hits, start_time, aggregated_bytes, args)

if __name__ == "__main__":
    main(sys.argv)
