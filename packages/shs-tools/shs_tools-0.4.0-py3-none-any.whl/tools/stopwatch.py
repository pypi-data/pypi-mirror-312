from __future__ import annotations
from time import perf_counter_ns
from .tools import human_readable_time_from_ns


class StopWatch:
    started: int | None = None
    stopped: int | None = None

    def __init__(self, auto_start=True):
        self.total_elapsed = 0
        if auto_start:
            self.start()

    def start(self):
        self.started = perf_counter_ns()
        self.stopped = None

    def stop(self):
        self.stopped = perf_counter_ns()
        self.total_elapsed += self.elapsed()

    def reset(self):
        self.total_elapsed = 0
        self.start()

    def elapsed(self) -> int:
        if self.stopped is None:
            return perf_counter_ns() - self.started
        else:
            return self.stopped - self.started

    def elapsed_string(self) -> str:
        return human_readable_time_from_ns(self.total_elapsed)

    def avg_elapsed(self, divider: int) -> float:
        return self.total_elapsed / divider

    def avg_string(self, divider: int) -> str:
        return human_readable_time_from_ns(int(self.avg_elapsed(divider)))

    def __str__(self):
        return self.avg_string(1)
