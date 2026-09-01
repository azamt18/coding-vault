using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CSharpExercises.Loops
{
    class SumAndAverage
    {
        static void Main(string[] args)
        {
            Console.WriteLine(SumAndAverageMethod(11, 66)); // "Sum: 2156, Average: 38.5"
            Console.WriteLine(SumAndAverageMethod(-10, 0)); // "Sum: -55, Average: -5"

            Console.ReadLine();
        }

        public static string SumAndAverageMethod(int numberFrom, int numberTo)
        {
            int sum = 0;
            int numberCounter = 0;
            double average = 0.0;

            for (int i = numberFrom; i <= numberTo ; i++)
            {
                sum += i;
                numberCounter++;
            }

            average = sum / (double) numberCounter;

            return string.Format($"Sum: {sum}, Average: {average}");
        }
    }
}
