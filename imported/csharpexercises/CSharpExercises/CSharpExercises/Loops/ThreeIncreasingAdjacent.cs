using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CSharpExercises.Loops
{
    class ThreeIncreasingAdjacent
    {
        static void Main(string[] args)
        {
            int[] array1 = new int[] { 45, 23, 44, 68, 65, 70, 80, 81, 82 };
            int[] array2 = new[] { 7, 3, 5, 8, 9, 3, 1, 4 };

            Console.WriteLine($"{ThreeIncreasingAdjacentMethod(array1)}");
            Console.WriteLine($"{ThreeIncreasingAdjacentMethod(array2)}");
            Console.WriteLine(ThreeIncreasingAdjacentMethod(new int[] { 9, 0, -1, -6, -5, -4, -8, 0 }));
            Console.ReadLine();
        }

        public static bool ThreeIncreasingAdjacentMethod(int[] array)
        {
            for (int i = 1; i < array.Length - 1; i++)
            {
                bool secondIsGreaterByOneThanTheFirstOne = array[i] - array[i - 1] == 1;
                bool thirdIsGreaterByOneThanTheThirdOne = array[i+1] - array[i] == 1;

                if (secondIsGreaterByOneThanTheFirstOne & thirdIsGreaterByOneThanTheThirdOne)
                {
                    return true;
                }
            }

            return false;
        }
    }
}
