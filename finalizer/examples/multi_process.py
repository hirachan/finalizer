#!/bin/env python3
from __future__ import annotations
from time import sleep
from multiprocessing import Process

from finalizer import Finalizer


class Task(Process):
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



def cleanup_main() -> None:
    print("main cleanup start")
    sleep(3)
    print("main cleanup end")


@Finalizer(cleanup_main)
def main() -> None:
    tasks: list[Task] = []
    for i in range(5):
        task = Task(i)
        task.start()
        tasks.append(task)

    for task in tasks:
        task.join()


if __name__ == "__main__":
    main()
