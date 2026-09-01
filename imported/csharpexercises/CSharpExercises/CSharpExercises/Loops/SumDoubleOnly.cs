using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CSharpExercises.Loops
{
    class SumDoubleOnly
    {
        static void Main(string[] args)
        {
            Console.WriteLine(SumDoubleOnlyMethod(new object[] { "abc", 5.6, 14, 'c', true, 'x', false, 567, 2.22 })); // 7.82

            Console.ReadLine();
        }

        public static double SumDoubleOnlyMethod(object[] array)
        {
            double sum = 0.0;

            foreach (var item in array)
            {
                if (item is Double)
                    sum += (double) item;
            }

            return sum;
        }
    }
}
