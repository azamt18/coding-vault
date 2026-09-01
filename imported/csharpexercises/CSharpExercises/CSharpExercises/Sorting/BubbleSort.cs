using System;

namespace CSharpExercises.Sorting
{
    public class BubbleSort
    {

        static void BubbleSorting(int[] array, out int iterationCounter)
        {
            iterationCounter = 0;
            for (var i = 0; i < array.Length - 1; i++)
            {
                for (int j = 0; j < array.Length - i - 1; j++)
                {
                    if (array[j] > array[j+1])
                    {
                        // swap
                        int temp = array[j];
                        array[j] = array[j + 1];
                        array[j + 1] = temp;
                    }
                }
                iterationCounter++;
            }
        }

        private static void PrintArray(int[] array)
        {
            foreach (var t in array)
            {
                Console.Write(t + " ");
            }
        }

        static void Main(string[] args)
        {
            int[] array = new[] { 2, 7, 4, 1, 5, 8, 6, 9, 0 };
            int iterationCounter;
            BubbleSorting(array, out iterationCounter);
            PrintArray(array);
            Console.WriteLine();
            Console.WriteLine(iterationCounter);
            Console.ReadKey();
        }
    }
}