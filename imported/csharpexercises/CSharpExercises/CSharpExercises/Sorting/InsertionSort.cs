using System;

namespace CSharpExercises.Sorting
{
    public class InsertionSort
    {
        static void InsertionSorting(int[] array)
        {
            int arrayLength = array.Length;
            for (int i = 1; i < arrayLength; i++)
            {
                int key = array[i];
                int j = i - 1;

                // Move elements that are greater than key
                // to one position ahead of their current position
                while (j >= 0 && key < array[j])
                {
                    array[j + 1] = array[j];
                    j = j - 1;
                }

                array[j + 1] = key;
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
            int[] array = new[] { 65, 23, 45, 11, 3 };
            InsertionSorting(array);
            PrintArray(array);

            Console.ReadLine();
        }
    }
}