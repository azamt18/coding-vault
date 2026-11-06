## questions for the self-check:

### 1. what is the purpose of threading in c#?

**answer:** two main benefits:
- ui responsiveness: prevent ui blocking when processing long-running operations
- cpu parallelism: divide cpu-bound work into chunks and run them in parallel across multiple cores

---

### 2. what is the difference between thread and process?

**answer:**
- **process**: isolated resource boundary (separate virtual address space, handles, memory). os treats each process as an independent unit.
- **thread**: basic unit of cpu execution within a process. threads share heap memory and global state, but each thread has its own call stack and cpu register state (program counter, stack pointer).
- **why threads share stack**: each thread needs its own call stack to track function calls and local variables independently.

---

### 3. what is the difference between thread, thread pool and tpl? what is the preferred way to write multithreaded and parallel code?

**answer:**
- **thread** (`new Thread(...)`): 1:1 mapping to os thread. expensive to create/teardown (~1mb per thread, context-switching overhead).
- **threadpool** (`ThreadPool.QueueUserWorkItem`): pre-allocated pool of threads. avoids allocation overhead by reusing threads. "fire-and-forget" model with no return values or continuations.
- **tpl (task parallel library)**: higher-level abstraction over threadpool. provides `Task<T>` for composable work with return values, `ContinueWith()` for chaining, and a sophisticated work-stealing scheduler.
- **preferred approach**: tpl + async/await. cleaner syntax, better composition, automatic context propagation.

---

### 4. describe a flow how exceptions are handled in threads?

**answer:**
- **raw `new Thread(...)`**: unhandled exceptions on background threads immediately crash the entire process via `AppDomain.UnhandledException`.
- **`Task.Run(...)`**: exceptions are captured inside the `Task.Exception` property as `AggregateException`.
- **awaiting or `.Wait()` / `.Result`**: re-throws the captured exception at the await/call point.
  - `await task;` → unwraps and throws the *original* exception directly, preserving stack trace.
  - `task.Wait()` or `task.Result` → throws the exception wrapped in `AggregateException`.

---

### 5. what is the difference between foreground and background threads?

**answer:**
- **foreground thread**: process stays alive while any foreground thread is running.
- **background thread**: process terminates immediately when all foreground threads exit (background threads are forcibly killed).
- **defaults**: raw `new Thread()` defaults to foreground. threadpool and tpl tasks use background threads automatically.
- **process lifetime rule**: process shutdown waits for the last foreground thread to finish, then kills all remaining background threads without running finally blocks or calling `IDisposable`.

---

### 6. what is the difference between managed and unmanaged threads?

**answer:**
- **managed thread**: `System.Threading.Thread` object created and tracked by the clr. has clr state (culture, execution context, security principals) and gc awareness.
- **unmanaged thread**: created by the os, runs outside clr control. when native code calls into managed code via p/invoke or com callbacks, clr automatically wraps it in a managed thread stub.
- **clr coordination**: clr must track managed threads so it can pause them during garbage collection (gc safe points).

---

### 7. what is spinning and how is it different from blocking?

**answer:**
- **spinning**: thread continuously loops in a tight loop checking a condition. consumes cpu cycles at near-zero latency (nanoseconds). example: `Thread.SpinWait(...)`, `SpinLock`.
- **blocking**: thread yields the cpu core to the os scheduler via a kernel syscall. saves cpu power but incurs thousands of cycles for context-switching overhead when resuming.
- **hybrid approach**: high-performance primitives like `Monitor` (used by `lock`), `SemaphoreSlim`, and `ManualResetEventSlim` first spin briefly for nanosecond-level waits, then fall back to blocking if the wait is longer.

---

### 8. what is mutex? how is it different from other synchronization primitives?

**answer:**
- **mutex**: os-level kernel synchronization primitive. supports cross-process synchronization (named mutex). example: `new Mutex(false, "Global\\MyUniqueAppId")`.
- **why different**: in-process primitives like `lock` (Monitor), `SemaphoreSlim`, `AutoResetEvent` can only coordinate threads within a single process.
- **thread affinity**: mutex is owned by the thread that called `.WaitOne()`. if that thread dies while holding the mutex, `.WaitOne()` throws `AbandonedMutexException` on the next acquirer.
- **cost**: slower than user-mode primitives because acquiring/releasing transitions between user mode and kernel mode via syscalls.

---

### 9. what ways/options to avoid deadlocks, race conditions, and other threading issues do you know?

**answer:** 

**deadlock prevention:**
- **lock ordering**: enforce a strict, consistent global order for acquiring multiple locks. prevents circular wait condition.
- **timeouts**: use `Monitor.TryEnter(lock, timeout)` or `SemaphoreSlim.WaitAsync(timeout)` to back off and release held locks if acquisition times out.

**race condition prevention:**
- **interlocked operations**: `Interlocked.Increment()`, `Interlocked.Exchange()`, `Interlocked.CompareExchange()` for lock-free atomic updates on primitives.
- **concurrent collections**: `ConcurrentDictionary`, `ConcurrentQueue`, `ConcurrentBag` use lock-striping and lock-free algorithms.
- **immutability**: make data immutable (`readonly`, `record`, `IReadOnlyCollection`) so shared state cannot be mutated unsafely.

---

### 10. what is the difference between `lock` and `monitor`?

**answer:**
- **`lock` statement**: compiler syntactic sugar. lowered to a `try/finally` block wrapping `Monitor.Enter(obj, ref lockTaken)` and `Monitor.Exit(obj)`.
- **`Monitor` class**: provides advanced coordination methods unavailable in `lock`:
  - `Monitor.TryEnter(obj, timeout)` → acquire with timeout.
  - `Monitor.Wait(obj)` → release lock and wait for notification.
  - `Monitor.Pulse(obj)` → wake one waiting thread.
  - `Monitor.PulseAll(obj)` → wake all waiting threads.
- **sync object best practice**: use private, reference-type objects (e.g., `private readonly object _lock = new object();`). never use strings, `typeof(Type)`, or value types.

---

### 11. how to write thread-safe code?

**answer:** three foundational principles (beyond just adding locks):
1. **synchronization object encapsulation**: sync objects must be private reference types. prevents external code from holding the lock.
2. **embrace immutability**: code that doesn't mutate shared data doesn't require synchronization. use `readonly`, `record`, `IReadOnlyCollection`.
3. **thread isolation**: keep state local to single threads using `ThreadLocal<T>`, message-passing channels (`System.Threading.Channels.Channel<T>`), or actor models. avoids the need for synchronization altogether.

---

### 12. name potential pitfalls in task parallelism?

**answer:**

1. **sync-over-async antipattern**: calling `.Wait()` or `.Result` on an incomplete task blocks the thread synchronously. can trigger deadlock (especially in single-threaded sync contexts like asp.net classic or wpf/winforms) or threadpool starvation.

2. **`async void` methods**: cannot be awaited. unhandled exceptions inside them crash the process directly, bypassing the caller's `try/catch`.

3. **over-parallelization**: spawning thousands of tasks without throttling (e.g., `ParallelOptions.MaxDegreeOfParallelism` or `SemaphoreSlim`) starves the threadpool and burns memory.

---

### 13. what is the difference between attached and detached child tasks?

**answer:**
- **detached (default)**: parent task does not wait for child tasks. parent can complete independently before children finish. child exceptions are not automatically propagated.
- **attached (`TaskCreationOptions.AttachedToParent`)**: parent task will not transition to `RanToCompletion` until all attached child tasks finish.
- **exception aggregation**: attached child exceptions bubble up into the parent's `AggregateException`.
- **modern alternative**: `Task.Run` uses `TaskCreationOptions.DenyChildAttach` internally (children cannot attach). use `Task.Factory.StartNew(...)` if you need attached task support, or use `Task.WhenAll(...)` for clearer structured concurrency.
