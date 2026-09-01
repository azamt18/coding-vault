/*
*  Create a Task and attach continuations to it according to the following criteria:
   a.    Continuation task should be executed regardless of the result of the parent task.
   b.    Continuation task should be executed when the parent task finished without success.
   c.    Continuation task should be executed when the parent task would be finished with fail and parent task thread should be reused for continuation
   d.    Continuation task should be executed outside of the thread pool when the parent task would be cancelled
   Demonstrate the work of the each case with console utility.
*/
using System;
using System.Threading;
using System.Threading.Tasks;

namespace MultiThreading.Task6.Continuation
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Create a Task and attach continuations to it according to the following criteria:");
            Console.WriteLine("a.    Continuation task should be executed regardless of the result of the parent task.");
            Console.WriteLine("b.    Continuation task should be executed when the parent task finished without success.");
            Console.WriteLine("c.    Continuation task should be executed when the parent task would be finished with fail and parent task thread should be reused for continuation.");
            Console.WriteLine("d.    Continuation task should be executed outside of the thread pool when the parent task would be cancelled.");
            Console.WriteLine("Demonstrate the work of the each case with console utility.");
            Console.WriteLine();

            // feel free to add your code
            
            // a) runs no matter what
            var parent1 = new Task(() => { });
            parent1.ContinueWith(SuccessfulContinuation);
            void SuccessfulContinuation(Task task)
            {
                Console.WriteLine(task.Id);
            }
            parent1.Start();
            parent1.Wait();
            
            // b) runs only when parent didnt succeed
            var parent2 = new Task(() => { throw new Exception(); });
            parent2.ContinueWith(ContinuationThrows,
                continuationOptions: TaskContinuationOptions.NotOnRanToCompletion);
            parent2.Start();
            
            // c) runs when parent didnt succeed and reuses parent thread
            var parent3 = new Task(() => { throw new Exception(); });
            parent3.ContinueWith(ContinuationThrows, 
                continuationOptions: TaskContinuationOptions.ExecuteSynchronously | TaskContinuationOptions.OnlyOnFaulted);
            parent3.Start();

            void ContinuationThrows(Task task)
            {
                Console.WriteLine(task.Id);
            }


            // d) runs on cancellation and runs outside the threadpool
            var cts = new CancellationTokenSource();
            var parent4 = new Task(() => { }, cts.Token);
            parent4.ContinueWith(SuccessfulContinuation,
                continuationOptions: TaskContinuationOptions.LongRunning | TaskContinuationOptions.OnlyOnCanceled);
            cts.Cancel();
            parent4.Start();

            Console.ReadLine();
        }
    }
}
