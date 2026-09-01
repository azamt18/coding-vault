using System;
using System.Collections.Generic;

namespace CSharpExercises.Recursion
{
    class DigitsMultiplication
    {
        static void Main(string[] args)
        {
            Console.WriteLine(DigitsMultiplicationByRecursion(456)); // 120
            Console.WriteLine(DigitsMultiplicationByRecursion(123)); // 6
            Console.WriteLine(DigitsMultiplicationByRecursion(1234)); // 24

            Console.WriteLine(DigitsMultiplicationMethod(456)); // 120
            Console.WriteLine(DigitsMultiplicationMethod(123)); // 6
            Console.WriteLine(DigitsMultiplicationMethod(222222222)); // 512
            Console.ReadKey();
        }

        static int DigitsMultiplicationByRecursion(int number)
        {
            int result = 1;
            if (number > 10)
                result = (number % 10) * DigitsMultiplicationByRecursion(number / 10);
            else
                result = number % 10;

            return result;
        }

        static int DigitsMultiplicationMethod(int number)
        {
            int result = 1;

            char[] numbersCharArray = number.ToString().ToCharArray();
            List<int> numbersList = new List<int>();

            foreach (var x in numbersCharArray)
            {
                numbersList.Add(Int32.Parse(x.ToString()));
            }

            foreach (var x in numbersList)
            {
                result *= x;
            }

            return result;
        }
    }
}
