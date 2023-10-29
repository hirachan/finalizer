# finalizer

This is a context manager to cleanup your environment. Your claenup code will be called even if the program is stopped by Ctrl-C or kill command.

This is useful for;
- Create a directory in the middle of the process, but you don't want it to remain when the process finished.
- You put temporary data in a database, but you don't want it to remain when the process finished.
- You want to be notified when a program terminates, whether it ends normal or dead.
- Etc...

You can also use for cleanup process for docker container, but be careful for the timeout after docker stop. (Default 10 secs)

## Limitation

This module cannot prevent from kill -9 (SIGKILL).


## Install

```cosole
pip install finalizer
```

## How to Use

### With `with` clause

#### Simple code

```
from time import sleep
from finalizer import Finalizer

def cleanup1() -> None:
    print("cleanup1 start")
    sleep(3)
    print("cleanup1 end")

def task1() -> None:
    print("task1 start")
    with Finalizer(cleanup1):
        sleep(3)
    print("task1 end")
```

**Output**:
```
task1 start
cleanup1 start
cleanup1 end
task1 end
```


#### with options

```
def cleanup2(param1: str, param2: int) -> None:
    print("cleanup2 start", param1, param2)
    sleep(3)
    print("cleanup2 end")

def task2() -> None:
    print("task2 start")
    with Finalizer(cleanup2, "test", param2=42):
        sleep(3)
    print("task2 end")
```

**Output**:
```
task2 start
cleanup2 start test 42
cleanup2 end
task2 end
```

#### you can nest `with` clause

```
def cleanup3() -> None:
    print("cleanup3 start")
    sleep(3)
    print("cleanup3 end")

def task3() -> None:
    print("task3 start")
    with Finalizer(cleanup3):
        sleep(3)
        task1()
        sleep(3)
    print("task3 end")
```

**Output**:
```
task3 start
task1 start
cleanup1 start
cleanup1 end
task1 end
cleanup3 start
cleanup3 end
task3 end
```

### With decorator

```
def cleanup4() -> None:
    print("cleanup4 start")
    sleep(3)
    print("cleanup4 end")

@Finalizer(cleanup4)
def task4() -> None:
    print("task4 start")
    sleep(3)
    print("task4 end")
```

**Output**:
```
task4 start
task4 end
cleanup4 start
cleanup4 end
```

## How it works

Even if Ctrl-C is pressed, all cleanup will work.

```
>>> task3()
task3 start
task1 start  <== Press Ctrl-C key here
^Ccleanup1 start
cleanup1 end
cleanup3 start
cleanup3 end
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 5, in task3
  File "<stdin>", line 4, in task1
KeyboardInterrupt
```

Even if Python process is killed, all cleanup will work.

```
>>> task3()
task3 start
task1 start  <== kill python process here
cleanup1 start
cleanup1 end
cleanup3 start
cleanup3 end
```

While cleanup process is running, Ctrl-C or kill signal does not work.

```
>>> task3()
task3 start
task1 start  <== Press Ctrl-C key here
^Ccleanup1 start  <== Press Ctrl-C key here but does not stop
^C^C^Ccleanup1 end
cleanup3 start  <== Same here, press Ctrl-C key here many times but does not stop
^C^C^C^C^C^C^C^C^C^C^Ccleanup3 end
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 5, in task3
  File "<stdin>", line 4, in task1
KeyboardInterrupt
```
