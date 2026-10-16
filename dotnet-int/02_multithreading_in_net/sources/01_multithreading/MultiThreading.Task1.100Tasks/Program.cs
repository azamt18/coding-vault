/*
 * 1.	Write a program, which creates an array of 100 Tasks, runs them and waits all of them are not finished.
 * Each Task should iterate from 1 to 1000 and print into the console the following string:
 * “Task #0 – {iteration number}”.
 */
using System;
using System.Linq;
using System.Threading.Tasks;
using BenchmarkDotNet.Attributes;
using BenchmarkDotNet.Running;

namespace MultiThreading.Task1._100Tasks
{
    class Program
    {
        const int TaskAmount = 100;
        const int MaxIterationsCount = 1000;

        static async Task Main(string[] args)
        {
            Console.WriteLine(".Net Mentoring Program. Multi threading V1.");
            Console.WriteLine("1.	Write a program, which creates an array of 100 Tasks, runs them and waits all of them are not finished.");
            Console.WriteLine("Each Task should iterate from 1 to 1000 and print into the console the following string:");
            Console.WriteLine("“Task #0 – {iteration number}”.");
            Console.WriteLine();
            
            // HundredTasks();
            
            // await HundredTasksUsingRangeAndWaitingSequentiallyWithConfirmation();

            BenchmarkRunner.Run<TaskBenchmarks>();
            
            Console.ReadLine();
        }

        static async Task HundredTasksUsingRangeAndWaitingSequentiallyWithConfirmation()
        {
            // basic iteration (alt to for loop)
            for (int i = 0; i < TaskAmount; i++)
            {
                int taskIndex = i;
                await Task.Run(() =>
                {
                    foreach (var iteration in Enumerable.Range(1, 10))
                    {
                        Console.WriteLine($"Task #{taskIndex} - {iteration}");
                    }
                    Console.ReadKey();
                });
            }
            
            /* tasks[i].Wait() does not guarantee order of execution */
            // for (int i = 0; i < tasks.Length; i++)
            // {
            //     tasks[i].Wait();
            //     Console.WriteLine($"task #{i} completed");
            // }
        }
    }
}
