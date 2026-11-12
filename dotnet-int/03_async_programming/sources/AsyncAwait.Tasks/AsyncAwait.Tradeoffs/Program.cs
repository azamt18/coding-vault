using System.Diagnostics;
using System.Net;
using System.Net.Sockets;

await AsyncAwaitTest2026Q1TasksRunOutput();
// 1) output
// start
// start RunA()
// delay 12sec started
// after RunA()
// start RunB()
// delay 8sec started
// after RunB()
// delay 8sec ended
// end RunB()
// delay 12sec ended
// end RunA()
// start RunC()
// delay 5sec started
// delay 5sec ended
// end RunC()
// after RunC(): 12
// End

// 2) execution time: 17

// 3) how to improve the code: a) make RunA(), RunB() sync; b) wrap into Task.WhenAll()
async Task AsyncAwaitTest2026Q1TasksRunOutput()
{
    var stopwatch = Stopwatch.StartNew();
    Console.WriteLine("start");
    var taskA = RunA();
    Console.WriteLine("after RunA()");
    
    var taskB = RunB();
    Console.WriteLine("after RunB()");

    await Task.WhenAll(RunA(), RunB());

    var taskC = RunC(await taskA, await taskB);
    // var taskC = RunC(taskA.Result, taskB.Result); // is await taskA = taskA.Result? no
    // await TaskA: thread freed to threadpool,
    // taskA.Result: blocked, wasted
    Console.WriteLine($"after RunC(): {taskC.Result}");
    Console.WriteLine("End");
    stopwatch.Stop();
    Console.WriteLine($"execution time: {stopwatch.Elapsed.Seconds}");
}

async Task<int> RunA()
{
    Console.WriteLine("start RunA()");
    Console.WriteLine("delay 12sec started");
    await Task.Delay(12000);
    Console.WriteLine("delay 12sec ended");
    Console.WriteLine("end RunA()");
    return 5;
}
async Task<int> RunB()
{
    Console.WriteLine("start RunB()");
    Console.WriteLine("delay 8sec started");
    await Task.Delay(8000);
    Console.WriteLine("delay 8sec ended");
    Console.WriteLine("end RunB()");
    return 7;
}
async Task<int> RunC(int a, int b)
{
    Console.WriteLine("start RunC()");
    Console.WriteLine("delay 5sec started");
    await Task.Delay(5000);
    Console.WriteLine("delay 5sec ended");
    Console.WriteLine("end RunC()");
    return a + b;
}

// 1) what happens if developer didnt put using()
// a: [wrong] inproper resource allocation/memory usage -> no cleanups -> new instance every time in memory
// [correct]: socket is unmanaged resource, belongs to OS, it is outside CLR -> so
// on every opens new socket but never closes -> heats OS limit of open files at ~1000 iteration -> fails with SocketException

// 2) what happens after one week
// a: [wrong] memory allocation overhead -> out of memory exception
// [correct] resource exhaustion -> process is dead

// 3) when it is wrapped inside using() and what happens if ConnectAsync() throws an exception?
// using (var tcpClient = new TcpClient())                                                             
// {                                                                                                   
//     await tcpClient.ConnectAsync(...);  // throws SocketException                                   
//     await tcpClient.GetStream().WriteAsync(...);  // never reaches here                             
// }                                                                                                   
// a: socket cleanup will be in finally block 

// 4) if you have 1000 concurrent async methods calling AsyncAwaitTest2026Q2SocketCall() simultaneously   
// (e.g., web server handling 1000 requests):
//  var tasks = Enumerable.Range(0, 1000)                                                               
//      .Select(i => AsyncAwaitTest2026Q2SocketCall())                                                  
//      .ToList();                                                                                      
//  await Task.WhenAll(tasks);  // all running concurrently
// a: 
// - how many sockets are open at peak? up to OS limit (~1000) 
// - bottleneck is in OS limit as socket is OS resource
// - how would you throttle to stay under OS limits? use semaphore to manage multithreading in OS-level
    
async Task AsyncAwaitTest2026Q2SocketCall()
{
    while (true)
    {
        using (var tcpClient = new TcpClient())
        {
            await tcpClient.ConnectAsync(new IPEndPoint(IPAddress.Parse("127.0.0.1"), 8080));
            byte[] data = new byte[] { 1, 2, 3, 4, 5 };
            await tcpClient.GetStream().WriteAsync(data, 0, data.Length);
        }
        await Task.Delay(1000);
    }
}

SemaphoreSlim semaphoreSlim = new SemaphoreSlim(100); // max 100 concurrent sockets

async Task AsyncAwaitTest2026Q2SocketCallWithSemSlim()
{
    await semaphoreSlim.WaitAsync();
    try
    {
        using (var tcpClient = new TcpClient())
        {
            await tcpClient.ConnectAsync(new IPEndPoint(IPAddress.Parse("127.0.0.1"), 8080));
            byte[] data = new byte[] { 1, 2, 3, 4, 5 };
            await tcpClient.GetStream().WriteAsync(data, 0, data.Length);
        }
    }
    finally
    {
        semaphoreSlim.Release(); // release slot
    }
}
// 5)  in your throttled code above, what happens if an exception is thrown in ConnectAsync()?
// - semaphore slot get released
// - socket get cleaned up as wrapped with using
// - in this order: socket cleanup -> slot release 

async Task AsyncAwaitTest2024()
{
    Console.WriteLine("Start");
    var a = Wait1();
    Console.WriteLine("After Wait1()");
    var b = Wait2();
    Console.WriteLine("After Wait2()");
    Console.WriteLine(await a + await b);
    Console.WriteLine("End");
}

async Task<int> Wait1()
{ Console.WriteLine("Start Wait1()"); await Task.Delay(20000); Console.WriteLine("End Wait1()"); return 1; }

async Task<int> Wait2()
{ Console.WriteLine("Start Wait2()"); await Task.Delay(10000); Console.WriteLine("End Wait2()"); return 2; }