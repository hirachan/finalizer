#!/bin/env python3
from __future__ import annotations
from time import sleep

from finalizer import Finalizer


def cleanup3() -> None:
    print("task3 cleanup start")
    sleep(3)
    print("task3 cleanup end")


@Finalizer(cleanup3)
def task3() -> None:
    print("task3 start")
    sleep(3)
    print("task3 end")


def cleanup2() -> None:
    print("task2 cleanup start")
    sleep(3)
    print("task2 cleanup end")


def task2() -> None:
    print("task2 start")
    with Finalizer(cleanup2):
        sleep(3)
        print("task2 end")


def cleanup1(opt: str) -> None:
    print("task1 cleanup start", opt)
    sleep(3)
    print("task1 cleanup end", opt)


def task1() -> None:
    print("task1 start")
    with Finalizer(cleanup1, opt="opt2"):
        sleep(3)
        task2()
        sleep(3)
        print("task1 end")


def cleanup_main() -> None:
    print("main cleanup start")
    sleep(3)
    print("main cleanup end")


@Finalizer(cleanup_main)
def main() -> None:
    task1()
    print("--------")
    task3()


if __name__ == "__main__":
    main()
