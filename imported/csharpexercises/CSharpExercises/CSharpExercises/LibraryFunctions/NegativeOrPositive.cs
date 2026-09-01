using System;

namespace CSharpExercises.LibraryFunctions
{
    public class NegativeOrPositive
    {
        static void Main(string[] args)
        {
            Console.WriteLine(NegativeOrPositiveMethod(-2)); // 4
            Console.WriteLine(NegativeOrPositiveMethod(6.25)); // 2.5
            Console.WriteLine(NegativeOrPositiveMethod(0)); // 2.5
            Console.WriteLine(NegativeOrPositiveMethod(3.334)); // 2.5

            Console.ReadKey();
        }

        static double NegativeOrPositiveMethod(double num)
        {
            return num == 0 || num > 0 ? Math.Sqrt(num) : Math.Pow(num, 2);
        }
    }
}