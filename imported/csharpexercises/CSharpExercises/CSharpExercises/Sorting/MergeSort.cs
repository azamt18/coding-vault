using System;

namespace CSharpExercises.Sorting
{
    public class MergeSort
    {
        static void Merge(int[] array, int leftMost, int middle, int rightMost, out int mergeCounter)
        {
            // find sizes of two sub arrays to be merged
            int n1 = middle - leftMost + 1;
            int n2 = rightMost - middle;

            // create temp arrays
            int[] L = new int[n1];
            int[] R = new int[n2];
            int i, j;

            mergeCounter = 0;

            // copy data to temp arrays
            for (i = 0; i < n1; i++)
            {
                L[i] = array[leftMost + i];
            }

            for (j = 0; j < n2; j++)
            {
                R[j] = array[middle + 1 + j];
            }

            /* Merge two temp arrays */

            // initial indexes of 1st and 2nd sub arrays
            i = 0;
            j = 0;

            // initial index of merged sub array
            int k = leftMost;
            while (i < n1 && j < n2)
            {
                if (L[i] <= R[j])
                {
                    array[k] = L[i];
                    i++;
                }
                else
                {
                    array[k] = R[j];
                    j++;
                }

                k++;
            }

            // copy remaining elements of L[] if any
            while (i < n1)
            {
                array[k] = L[i];
                i++;
                k++;
            }

            // copy remaining elements of R[] if any
            while (j < n2)
            {
                array[k] = R[j];
                j++;
                k++;
            }

            mergeCounter++;

        }

        static void MergeSorting(int[] array, int leftMost, int rightMost, out int iterationCounter, out int mergeCounter)
        {
            iterationCounter = 0;
            mergeCounter = 0;
            if (leftMost < rightMost)
            {
                int middle = leftMost + (rightMost - leftMost) / 2;

                // sort 1st half
                MergeSorting(array, leftMost, middle, out iterationCounter, out mergeCounter);

                // sort 2nd half
                MergeSorting(array, middle + 1, rightMost, out iterationCounter, out mergeCounter);

                // merge two halves
                Merge(array, leftMost, middle, rightMost, out mergeCounter);

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
            int mergeCounter;

            MergeSorting(array, 0, array.Length - 1, out iterationCounter, out mergeCounter);
            PrintArray(array);

            Console.WriteLine();
            Console.WriteLine($"{iterationCounter} {mergeCounter} = {iterationCounter + mergeCounter}");

            Console.ReadKey();
        }
    }
}