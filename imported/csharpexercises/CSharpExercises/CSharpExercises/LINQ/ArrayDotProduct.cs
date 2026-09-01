using System;
using System.Linq;

namespace CSharpExercises.LINQ
{
    class ArrayDotProduct
    {
        static void Main(string[] args)
        {
            int[] array1 = new int[] { 5, 8, 2, 9 };
            int[] array2 = new int[] { 1, 7, 2, 4 };

            int dotProduct = array1.Zip(array2, (a, b) => a * b).Sum();

            Console.WriteLine(dotProduct);

            Console.ReadKey();
        }
    }
}
