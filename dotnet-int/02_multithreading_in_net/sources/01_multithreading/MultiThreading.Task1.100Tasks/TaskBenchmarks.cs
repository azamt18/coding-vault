using System;
using System.Linq;
using System.Threading.Tasks;
using BenchmarkDotNet.Attributes;

namespace MultiThreading.Task1._100Tasks;

[MemoryDiagnoser]
public class TaskBenchmarks
{
    private const int TaskAmount = 100;                        
    private const int MaxIterationsCount = 1000;
    
    [Benchmark]
    public void HundredTasksArray()
    {
        Task[] tasks =  new Task[TaskAmount];
        for (int i = 0; i < tasks.Length; i++)
        {
            tasks[i] = Task.Run(() =>
            {
                int sum = 0;
                for (int j = 1; j <= MaxIterationsCount; j++)
                {
                    sum += j;
                }
                return sum;
            });
        }

        Task.WaitAll(tasks);
    }

    [Benchmark]
    public void HundredTasksRange()
    {
        Task[] tasks =  new Task[TaskAmount];
        for (int i = 0; i < tasks.Length; i++)
        {
            tasks[i] = Task.Run(() =>
            {
                int sum = 0;
                foreach (var iteration in Enumerable.Range(1, MaxIterationsCount))
                {
                    sum += iteration;
                }
                return sum;
            });
        }

        Task.WaitAll(tasks);
    }
    
    void Output(int taskNumber, int iterationNumber)
    {
        Console.WriteLine($"Task #{taskNumber} – {iterationNumber}");
    }

}