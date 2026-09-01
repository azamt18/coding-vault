using System;

namespace CSharpExercises.Loops
{
    class ToThePowerOf
    {
        static void Main(string[] args)
        {
            Console.WriteLine(ToThePowerOfMethod(-2, 3)); // -8
            Console.WriteLine(ToThePowerOfMethod(5, 5)); // 3125

            Console.WriteLine(ToThePowerOfMethodOriginalSolution(-2, 3)); // -8
            Console.WriteLine(ToThePowerOfMethodOriginalSolution(5, 5)); // 3125

            Console.ReadLine();
        }

        public static double ToThePowerOfMethod(double number, double power)
        {
            return Math.Pow(number, power);
        }

        static double ToThePowerOfMethodOriginalSolution(int b, int exp)
        {
            double result = 1;
            if (exp == 0)
            {
                return 1;
            }

            for (int i = 1; exp > 0 ? i <= exp : i <= exp * (-1); i++)
            {
                result *= b;
            }

            return exp > 0 ? result : 1 / result;
        }
    }
}
