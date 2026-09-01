using System;
using System.Linq;

namespace CSharpExercises.LINQ
{
    class NumbersFromRange
    {
        static void Main(string[] args)
        {
            int[] array = { 67, 92, 153, 15 };
            NumbersFromRangeMethod(array);
            NumbersFromRangeMethod2(array);

            Console.ReadKey();
        }

        static void NumbersFromRangeMethod(int[] array)
        {
            var selectedNumbers = from x in array
                                  where x > 30 && x < 100
                                  select x;

            foreach (var x in selectedNumbers)
            {
                Console.Write($"{x} ");
            }
            Console.WriteLine();
        }

        static void NumbersFromRangeMethod2(int[] array)
        {
            var selectedNumbers = array.Where(x => x > 30).Where(x => x < 100);

            foreach (var x in selectedNumbers)
            {
                Console.Write($"{x} ");
            }
            Console.WriteLine();
        }
    }
}
