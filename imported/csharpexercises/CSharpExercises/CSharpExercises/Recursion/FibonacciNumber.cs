using System;

namespace CSharpExercises.Recursion
{
    class FibonacciNumber
    {
        // FIBONACCI SERIES: 0 1 1 2 3 5 8 13 21

        static void Main(string[] args)
        {
            Console.WriteLine(FibonacciNumberMethod(3)); // 2
            Console.WriteLine(FibonacciNumberMethod(7)); // 13

            Console.ReadKey();
        }

        static int FibonacciNumberMethod(int num)
        {
            return num <= 1 ? num : FibonacciNumberMethod(num - 2) + FibonacciNumberMethod(num - 1);
        }
    }
}
