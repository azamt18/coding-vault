/*
 * 5. Write a program which creates two threads and a shared collection:
 * the first one should add 10 elements into the collection and the second should print all elements
 * in the collection after each adding.
 * Use Thread, ThreadPool or Task classes for thread creation and any kind of synchronization constructions.
 */
using System;
using System.Threading;
using System.Threading.Tasks;
using System.Collections.Concurrent;

namespace MultiThreading.Task5.Threads.SharedCollection
{
    class Program
    {
        
        
        static void Main(string[] args)
        {
            Console.WriteLine("5. Write a program which creates two threads and a shared collection:");
            Console.WriteLine("the first one should add 10 elements into the collection and the second should print all elements in the collection after each adding.");
            Console.WriteLine("Use Thread, ThreadPool or Task classes for thread creation and any kind of synchronization constructions.");
            Console.WriteLine();

            // feel free to add your code
            // UsingThread();

            // UsingThreadPool();

            UsingTask();

            Console.ReadLine();
        }
        
        // both are unsignaled
        private static readonly AutoResetEvent EventWrite = new AutoResetEvent(false);
        private static readonly AutoResetEvent EventRead = new AutoResetEvent(false);
        private static ConcurrentQueue<int> _sharedData = new ConcurrentQueue<int>();
        
        // as option - bundle state
        private class ThreadState
        {
            public ConcurrentQueue<int> Data { get; set; }
            public AutoResetEvent EventWrite { get; set; }
            public AutoResetEvent EventRead { get; set; }
        }
        
        static void UsingThread()
        {
            var t1 = new Thread(AddElements);
            t1.Start(_sharedData);
            var t2 = new Thread(PrintElements);
            t2.Start(_sharedData);
        }

        private static void UsingThreadPool()
        {
            ThreadPool.QueueUserWorkItem(AddElements, _sharedData);
            ThreadPool.QueueUserWorkItem(PrintElements, _sharedData);
        }

        private static void UsingTask()
        {
            var task1 = new Task(AddElements, _sharedData);
            task1.Start();
            var task2 = new Task(PrintElements, _sharedData);
            task2.Start();
            Task.WaitAll(task1, task2);
        }

        
        private static void AddElements(object state)
        {
            for (int i = 0; i < 10; i++)
            {
                _sharedData.Enqueue(i);
                EventWrite.Set();
                EventRead.WaitOne();
            }
        }

        private static void PrintElements(object state)
        {
            for (int i = 0; i < 10; i++)
            {
                EventWrite.WaitOne();
                Console.WriteLine(string.Join(" ", _sharedData));
                // foreach (var val in current)
                // {
                //     Console.Write(val + " ");
                // }

                Console.WriteLine();
                EventRead.Set();
            }
        }
    }
}
