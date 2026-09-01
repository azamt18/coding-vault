using System;

namespace CSharpExercises.Recursion
{
    public class NumbersMultiplication
    {
        static void Main(string[] args)
        {
            Console.WriteLine(NumbersMultiplicationMethod(5, 7)); // 210
            Console.WriteLine(NumbersMultiplicationMethod(50, 50)); // 210

            Console.ReadLine();
        }

        static int NumbersMultiplicationMethod(int a, int b)
        {
            while (a == b)
            {
                return a;
            }

            var result = a * NumbersMultiplicationMethod(a + 1, b);

            return result;
        }
    }
}