using System;

namespace CSharpExercises.Recursion
{
    class Factorial
    {
        static void Main(string[] args)
        {
            Console.WriteLine(FactorialMethod(4)); // 24
            Console.WriteLine(FactorialMethod(7)); // 5040

            Console.ReadKey();
        }

        static int FactorialMethod(int num)
        {
            // MY SOLUTION
            //return num > 0 ? num * FactorialMethod(num - 1) : 1;

            // AUTHOR'S SOLUTION
            return num == 0 || num == 1 ? 1 : num * FactorialMethod(num - 1);
        }
    }
}
