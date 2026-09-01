using System;
using System.Collections;
using System.Linq;

namespace CSharpExercises.LINQ
{
    class ShuffleArray
    {
        static void Main(string[] args)
        {
            var random = new Random();
            var arrayList = new ArrayList();

            int[] array1 = new[] { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 };
            var result1 = array1.OrderBy(i => random.Next());
            arrayList.Add(result1);

            int[] array2 = new int[] { 38, 24, 8, 0, -1, -17, -33, -100 };
            var result2 = array2.OrderBy(i => random.Next());
            arrayList.Add(result2);

            Console.ReadKey();
        }
    }
}
