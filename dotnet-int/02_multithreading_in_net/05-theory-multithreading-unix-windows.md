#### **how behave multithreading in unix and windows?**
https://share.google/aimode/7esJ75CSn1hq50tdz

#### Comparison

| feature         | unix                                                                                                                    | windows                                                                                                                                         |
| --------------- | ----------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| threat modeling | - 1-1 (user level threads maps to kernel level thread),<br>- unified task model: process and threads are both tasks<br> | - 1-1 (first-class thread objects)<br>- process is resource container for shared memory and file descriptors<br>- thread is to execute the code |
| API             | POSIX (pthread, clone())                                                                                                | Win32 (CreateThread)                                                                                                                            |
| signal handling | POSIX system calls                                                                                                      | ACP (async procedure calls)                                                                                                                     |
| usage           | large-scale servers, high-concurrency cloud backends                                                                    | desktop, priority-based envs                                                                                                                    |
| cpu scheduling  | preemptive scheduling: kernel forcibly interrupts threads to assign cpu time                                            | preemptive scheduling: kernel forcibly interrupts threads to assign cpu time                                                                    |
| leverage        |                                                                                                                         |                                                                                                                                                 |

primary difference
> Unix treats thread as lightweight process
>     but/and threads share everything, process nothing
> Windows treats thread as distinct object managed by dedicated subsystem

#### Multithreading in Unix
1. Unified task model: process = thread = task
2. Shared space
    1. thread spawning via clone() -> share virtual memory address space
    2. process spawning via fork() -> copy
3. Signals: can be directed to specific thread or process

#### Multithreading in Windows
1. Supporting OO arch -> container model (process is virtual memory address space, execution is on thread)
2. Thread objects: more heavier than Unix threads
3. Built-in abstractions: Thread pool API

#### Process forking vs Multithreading

Unix:
- process creation cheap -> **multi-processing over multi-threading**
- Inter-Process communication btw processes

Windows:
- process creation slow -> multi-threading inside single process

|         | Unix | Windows |
| ------- | ---- | ------- |
| Process |      |         |
| Thread  |      |         |

#### how single c# code in modern .net handles these concepts to both windows and unix?
Through abstraction layer CoreCLR (.NET Runtime).
