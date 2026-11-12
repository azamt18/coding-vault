## questions for the self-check:

### 1. what is async programming in c#?

**answer:** a language-level abstraction for writing **non-blocking, composable code** that:
- **frees threads during i/o waits** — doesn't block like `.Wait()` or `.Result` (unlike sync-over-async antipattern from module 2)
- **enables high concurrency** with few threads (10k concurrent requests on ~200 threadpool threads, vs. one thread per request with synchronous code)
- **built on tasks** (tpl from module 2), but with cleaner syntax via `async/await` keywords

**why it matters:** without async, you'd need one thread per request → memory explosion. with async, you reuse threads efficiently during i/o waits.

---

### 2. what are the key operators that are used for asynchronous operation?

**answer:**

| operator | role | effect |
|----------|------|--------|
| **`async`** | marks method as async-capable | enables `await`, transforms return type to `Task` |
| **`await`** | pauses execution | frees thread to threadpool, resumes after awaitable completes |

**key insight:** `async` keyword tells compiler to generate a state machine. `await` pauses and resumes execution while freeing the thread to handle other work.

---

### 3. if you mark a method with the `async` keyword, does this mean the method is executed asynchronously?

**answer: no.** marking a method `async` doesn't make it async—it just **enables** `await`. execution is async only if the method contains `await` for an incomplete task.

**compare:**

```csharp
// ❌ sync-over-async (misleading)
async Task<int> Calculate()
{
    return 42;  // executes immediately, returns completed Task
}

// ✓ actually async
async Task<int> FetchData()
{
    return await httpClient.GetAsync(...);  // pauses, frees thread
}
```

**both return `Task<int>`, but behavior differs:**
- first: synchronous code wrapped in task, wastes the `async` keyword
- second: genuinely async, frees thread during i/o

---

### 4. what asynchronous programming patterns do you know?

**answer:**

**three main patterns:**

1. **sequential**: await one operation, then the next
   ```csharp
   var result1 = await Operation1();
   var result2 = await Operation2(result1);  // depends on result1
   ```
   **use case:** operations are dependent; order matters.

2. **parallel**: start multiple operations, wait for all
   ```csharp
   var task1 = Operation1();
   var task2 = Operation2();
   await Task.WhenAll(task1, task2);  // wait for both
   ```
   **use case:** operations are independent; maximize concurrency.

3. **fire-and-forget**: start an operation, don't wait (⚠️ dangerous!)
   ```csharp
   _ = Operation();  // exceptions silently disappear, crashes process
   ```
   **avoid:** exceptions are unobserved, causing hard-to-debug crashes.

**best practice:** use sequential or parallel patterns with proper exception handling. avoid fire-and-forget.

---

### 5. can a method contain multiple "await" key operators?

**answer: yes.** a method can have multiple `await` statements.

**example:**

```csharp
async Task<string> FetchAndProcess()
{
    var data = await FetchFromApi();  // first await
    var processed = await ProcessData(data);  // second await
    var result = await SaveToDatabase(processed);  // third await
    return result;
}
```

**execution:** awaits are executed **sequentially** (one after another), not in parallel. thread is freed at each `await` point.

**parallel alternative with `Task.WhenAll()`:**

```csharp
async Task<(int, int, int)> FetchMultiple()
{
    var taskA = FetchA();
    var taskB = FetchB();
    var taskC = FetchC();
    await Task.WhenAll(taskA, taskB, taskC);  // wait for all in parallel
    return (await taskA, await taskB, await taskC);
}
```

---

### 6. what types can be returned?

**answer:**

**return types for async methods:**

| return type | represents | use case |
|-------------|------------|----------|
| **`Task`** | async operation without return value | fire-and-forget (bad), or void-like operations |
| **`Task<T>`** | async operation returning value of type `T` | most common, awaitable with result |
| **`ValueTask`** | lightweight task wrapper for zero-allocation scenarios | high-performance hot paths |
| **`ValueTask<T>`** | lightweight task wrapper returning value | high-performance hot paths |
| **`IAsyncEnumerable<T>`** | streams values asynchronously over time | async iterators, streaming data |

**best practice comparison:**

```csharp
// ✓ correct
async Task<int> FetchData() { return 42; }
await result;  // unwraps and returns 42

// ❌ wrong (sync-over-async)
async Task<int> FetchData() { return 42; }
int result = await task;  // works, but wastes async

// ⚠️ avoid
async void OnClick() { await DoWork(); }  // exceptions crash process

// ✓ correct for UI
async Task OnClick() { await DoWork(); }  // exceptions propagate
```

**key constraint:** `async void` should **only** be used for event handlers. everywhere else, use `async Task` or `async Task<T>`.
