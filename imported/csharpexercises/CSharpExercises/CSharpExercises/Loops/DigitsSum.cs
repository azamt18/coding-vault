using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CSharpExercises.Loops
{
    class DigitsSum
    {
        static void Main(string[] args)
        {
            Console.WriteLine(DigitsSumMethod(11)); //  1 + 1 = 2
            Console.WriteLine(DigitsSumMethod(2233)); // 2 + 2 + 3 + 3 = 10
            Console.WriteLine(DigitsSumMethod(5434)); //  5 + 4 + 3 + 4 = 16
            Console.WriteLine(DigitsSumMethod(904861)); //  28

            Console.WriteLine(DigitsSumMethodOriginalSolution(11)); //  1 + 1 = 2
            Console.WriteLine(DigitsSumMethodOriginalSolution(2233)); // 2 + 2 + 3 + 3 = 10
            Console.WriteLine(DigitsSumMethodOriginalSolution(5434)); //  5 + 4 + 3 + 4 = 16
            Console.WriteLine(DigitsSumMethodOriginalSolution(904861)); //  28

            Console.ReadLine();
        }

        public static int DigitsSumMethod(int number)
        {
            int sum = 0;

            string numberInString = number.ToString();

            for (int i = 0; i < numberInString.Length; i++)
            {
                int digit = Int32.Parse(numberInString[i].ToString());
                sum += digit;
            }

            return sum;
        }

        public static int DigitsSumMethodOriginalSolution(uint number)
        {
            int sum = 0;
            int i = 10;
            int j = 1;

            while (number / j >= 1)
            {
                sum += (int)(number % i / j);

                i *= 10;
                j *= 10;
            }

            return sum;
        }

    }
}
