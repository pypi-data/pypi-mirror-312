"""
profiling memory usage and execution time
"""

import time
import tracemalloc
import linecache

class MemorySnapshot:
    def __init__(self, name="NN"):
        self.name = name
        self.snapshot = None
        self.size = None
        self.peak = None

    def take(self):
        self.size, self.peak = tracemalloc.get_traced_memory()
        self.snapshot = tracemalloc.take_snapshot()
        tracemalloc.reset_peak()


act_snapshot = MemorySnapshot("NN")
prev_snapshot = MemorySnapshot("NN")


def start():
    tracemalloc.start()


def stop():
    tracemalloc.stop()


def take_Snapshot(name="NN"):
    global act_snapshot
    global prev_snapshot
    prev_snapshot = act_snapshot
    act_snapshot = MemorySnapshot(name)
    act_snapshot.take()


def report_Snapshots(print_fn=print):
    global act_snapshot
    global prev_snapshot
    print_fn(f'[ Reporting snapshot {act_snapshot.name} ]')
    if act_snapshot.snapshot is None:
        return
    #######################
    # top 10 files
    top_stats = act_snapshot.snapshot.statistics('lineno')
    print_fn(f"[ Top 10 files: {act_snapshot.name} ]")
    for stat in top_stats[:10]:
        print_fn(stat)
    #######################
    # top 10 differences
    if prev_snapshot.snapshot is not None:
        top_stats = act_snapshot.snapshot.compare_to(prev_snapshot.snapshot, 'lineno')
        print_fn(f"[ Top 10 file differences: {prev_snapshot.name} -> {act_snapshot.name} ]")
        for stat in top_stats[:10]:
            print_fn(stat)
    #######################
    # top 10 lines
    limit = 10
    key_type = 'lineno'
    filt_snapshot = act_snapshot.snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = filt_snapshot.statistics(key_type)
    print_fn(f"[ Top {limit} lines: {act_snapshot.name} ]")
    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        print_fn("#%s: %s:%s: %.1f KiB"
              % (index, frame.filename, frame.lineno, stat.size / 1024))
        line = linecache.getline(frame.filename, frame.lineno).strip()
        if line:
            print_fn('    %s' % line)
    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        print_fn("%s other: %.1f KiB" % (len(other), size / 1024))
    total = sum(stat.size for stat in top_stats)
    print_fn("Total allocated size: %.1f KiB" % (total / 1024))
    #######################
    # peak memory usage
    print_fn(f"[ Peak memory usage: {prev_snapshot.name} -> {act_snapshot.name} ]")
    print_fn(f"size={act_snapshot.size / 1024 / 1024:.1f} MiB, peak={act_snapshot.peak / 1024 / 1024:.1f} MiB")


def take_report_Snapshot(name="NN", print_fn=print):
    take_Snapshot(name=name)
    report_Snapshots(print_fn=print_fn)

