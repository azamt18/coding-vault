using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CSharpExercises.Loops
{
    class BitsToNumber
    {
        static void Main(string[] args)
        {
            Console.WriteLine(BitsToNumberMethod("1")); // 1
            Console.WriteLine(BitsToNumberMethod("11")); // 3
            Console.WriteLine(BitsToNumberMethodOriginalSolution("111")); // 7
            Console.WriteLine(BitsToNumberMethod("100010")); // 34
            Console.WriteLine(BitsToNumberMethod("100101")); // 37

            Console.ReadLine();
        }

        public static double BitsToNumberMethod(string bitString)
        {
            double result = 0;

            int k = 0;

            for (int i = bitString.Length - 1; i >= 0; i--)
            {
                double digit = Int32.Parse(bitString[k].ToString());
                result += digit * Math.Pow(2, i);
                k++;
            }

            return result;
        }

        static int BitsToNumberMethodOriginalSolution(string bits)
        {
            var number = 0;

            for (var i = 0; i < bits.Length; i++)
            {
                number += (int)(char.GetNumericValue(bits[i]) * Math.Pow(2, bits.Length - i - 1));
            }

            return number;
        }
    }
}
