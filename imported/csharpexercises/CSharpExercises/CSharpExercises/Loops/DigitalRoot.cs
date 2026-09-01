using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CSharpExercises.Loops
{
    class DigitalRoot
    {
        static void Main(string[] args)
        {
            Console.WriteLine(DigitalRootMethod(83)); // 2
            Console.WriteLine(DigitalRootMethodOriginalSolution(83)); // 2

            Console.WriteLine(DigitalRootMethod(40002938)); // 8
            Console.WriteLine(DigitalRootMethodOriginalSolution(40002938)); // 8

            Console.ReadLine();
        }

        public static int DigitalRootMethod(int number)
        {
            return number == 0 ? 0 :
                number % 9 == 0 ? 9 : 
                number % 9;
        }

        public static int DigitalRootMethodOriginalSolution(uint number)
        {
            while (number / 10 != 0)
            {
                uint sum = 0;
                int i = 10;
                int j = 1;

                while (number / j >= 1)
                {
                    sum += (uint)(number % i / j);

                    i *= 10;
                    j *= 10;
                }

                number = sum;
            }

            return (int)number;
        }
    }
}
