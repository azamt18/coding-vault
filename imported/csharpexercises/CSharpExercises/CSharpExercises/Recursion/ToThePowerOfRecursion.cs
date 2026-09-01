using System;

namespace CSharpExercises.Recursion
{
    public class ToThePowerOfRecursion
    {
        static void Main(string[] args)
        {
            Console.WriteLine(ToThePowerOfRecursionMethod(2,3)); // 8
            Console.WriteLine(ToThePowerOfRecursionMethod(5,2)); // 25

            Console.WriteLine(ToThePowerOfRecursionByRecursion(2,3)); // 8
            Console.WriteLine(ToThePowerOfRecursionByRecursion(5,2)); // 25

            Console.ReadLine();
        }

        // MY SOLUTION
        static int ToThePowerOfRecursionMethod(int num, int power)
        {
            var result = 1;

            for (int i = 1; i <= power; i++)
            {
                result *= num;
            }

            return result;
        }

        // AUTHOR'S SOLUTION
        static int ToThePowerOfRecursionByRecursion(int num, int exp)
        {
            if (exp == 0)
            {
                return 1;
            } 
            else if (exp > 1)
            {
                return num * ToThePowerOfRecursionByRecursion(num, exp - 1);
            }
            else
            {
                return num;
            }
        }
    }
}