using System;

namespace CSharpExercises.Sorting
{
    public class SelectionSort
    {
        private static void SelectionSorting(int[] array)
        {
            for (var i = 0; i < array.Length - 1; i++)
            {
                var minElementIndex = i;
                for (var j = minElementIndex + 1; j < array.Length; j++)
                {
                    if (array[j] < array[minElementIndex])
                        minElementIndex = j;
                }

                var temp = array[minElementIndex];
                array[minElementIndex] = array[i];
                array[i] = temp;
            }
        }

        private static void PrintArray(int[] array)
        {
            foreach (var t in array)
            {
                Console.Write(t + " ");
            }
        }

        private static void Main(string[] args)
        {
            int[] array = new[] {65, 23, 45, 11, 3};
            SelectionSorting(array);
            PrintArray(array);
            Console.ReadKey();
        }
    }
}