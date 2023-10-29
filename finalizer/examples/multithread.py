#!/bin/env python3
from __future__ import annotations
from time import sleep
from threading import Thread

from finalizer import Finalizer


class Task(Thread):
    def __init__(self, num: int) -> None:
        self.num = num
        super().__init__()

    def cleanup1(self) -> None:
        print(f"task1({self.num}) cleanup start")
        sleep(3)
        print(f"task1({self.num}) cleanup end")

    def task1(self) -> None:
        print(f"task1({self.num}) start")
        with Finalizer(self.cleanup1):
            sleep(30)
            print(f"task1({self.num}) end")

    def run(self) -> None:
        self.task1()



def join_threads(tasks: list[Thread]) -> None:
    print("main cleanup start")
    for task in tasks:
        task.join()
    print("main cleanup end")


def main() -> None:
    tasks: list[Task] = []
    for i in range(5):
        task = Task(i)
        tasks.append(task)

    with Finalizer(join_threads, tasks):
        for task in tasks:
            task.start()


if __name__ == "__main__":
    main()
