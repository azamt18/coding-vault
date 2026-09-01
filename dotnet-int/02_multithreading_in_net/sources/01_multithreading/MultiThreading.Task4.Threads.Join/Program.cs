/*
 * 4.	Write a program which recursively creates 10 threads.
 * Each thread should be with the same body and receive a state with integer number, decrement it,
 * print and pass as a state into the newly created thread.
 * Use Thread class for this task and Join for waiting threads.
 * 
 * Implement all of the following options:
 * - a) Use Thread class for this task and Join for waiting threads.
 * - b) ThreadPool class for this task and Semaphore for waiting threads.
 */

using System;
using System.Threading;

namespace MultiThreading.Task4.Threads.Join
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("4.	Write a program which recursively creates 10 threads.");
            Console.WriteLine("Each thread should be with the same body and receive a state with integer number, decrement it, print and pass as a state into the newly created thread.");
            Console.WriteLine("Implement all of the following options:");
            Console.WriteLine();
            Console.WriteLine("- a) Use Thread class for this task and Join for waiting threads.");
            Console.WriteLine("- b) ThreadPool class for this task and Semaphore for waiting threads.");

            Console.WriteLine();

            // feel free to add your code
            // UsingThread();
            UsingThreadPool();

            Console.ReadLine();
        }
        
        static void UsingThread()
        {
            int count = 10;
            var thread = new Thread(CreateThread);
            thread.Start(10);
            thread.Join();

            void CreateThread(object state)
            {
                int count = (int)state;
                Console.WriteLine(count);
                if (count > 0)
                {
                    var nextThread = new Thread(CreateThread);
                    nextThread.Start(count - 1);
                    nextThread.Join();
                }
            }
        }
        
        private static void UsingThreadPool()
        {
            SemaphoreSlim semaphoreSlim = new SemaphoreSlim(0);
            int total = 10;
            ThreadPool.QueueUserWorkItem(CreateThread, total);
            semaphoreSlim.Wait();

            void CreateThread(object state)
            {
                int current = (int)state;
                Console.WriteLine(current);
                if (current > 0)
                {
                    ThreadPool.QueueUserWorkItem(CreateThread, current - 1);
                    semaphoreSlim.Wait();
                }
                semaphoreSlim.Release();
            }
        }

    }
}
