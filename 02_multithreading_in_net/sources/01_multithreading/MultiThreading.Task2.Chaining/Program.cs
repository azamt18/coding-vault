/*
 * 2.	Write a program, which creates a chain of four Tasks.
 * First Task – creates an array of 10 random integer.
 * Second Task – multiplies this array with another random integer.
 * Third Task – sorts this array by ascending.
 * Fourth Task – calculates the average value. All this tasks should print the values to console.
 */
using System;
using System.Linq;
using System.Threading.Tasks;

namespace MultiThreading.Task2.Chaining
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine(".Net Mentoring Program. MultiThreading V1 ");
            Console.WriteLine("2.	Write a program, which creates a chain of four Tasks.");
            Console.WriteLine("First Task – creates an array of 10 random integer.");
            Console.WriteLine("Second Task – multiplies this array with another random integer.");
            Console.WriteLine("Third Task – sorts this array by ascending.");
            Console.WriteLine("Fourth Task – calculates the average value. All this tasks should print the values to console");
            Console.WriteLine();

            // feel free to add your code
            var random = new Random();
            
            // task 1
            var arr = new int[10];
            var task1 = Task.Run(() =>
            {
                Console.WriteLine("Task 1");
                for (int i = 0; i < 10; i++)
                {
                    var val = random.Next(1, 10);
                    arr[i] = val;
                    Console.WriteLine($"{i}: {val}");
                }
            });
            
            // task 2
            var task2 = task1.ContinueWith(_ =>
            {
                Console.WriteLine("Task 2");
                int multiplier = random.Next(1, 10);
                for (int i = 0; i < 10; i++)
                {
                    arr[i] *= multiplier;
                    Console.WriteLine($"{i}: {arr[i]}");
                }
            });

            var task3 = task2.ContinueWith(_ =>
            {
                Console.WriteLine("Task 3");
                arr = [.. arr.OrderBy(x => x)];
                Console.WriteLine($"array sorted: {string.Join(", ", arr)}");
            });

            Task task4 = task3.ContinueWith(_ =>
            {
                Console.WriteLine("Task 4");
                Console.WriteLine($"average: {arr.Average()}");
            });

            task4.Wait();

            Console.ReadLine();
        }
    }
}
