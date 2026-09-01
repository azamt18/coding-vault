using System;
using System.Runtime.InteropServices;

namespace CSharpExercises.Searching
{
    public class BinarySearch
    {
        static int BinarySearchRecursive(int[] array, int searchingElement, int leftmostIndex, int rightmostIndex)
        {

            if (leftmostIndex < rightmostIndex)
            {
                // find middle index
                int middleIndex = leftmostIndex + (rightmostIndex - leftmostIndex) / 2;

                if (array[middleIndex] == searchingElement)
                    return middleIndex;

                // If element is smaller than mid, then it can only be present in left sub-array 
                if (array[middleIndex] > searchingElement)
                    return BinarySearchRecursive(array, searchingElement, leftmostIndex, middleIndex - 1);

                // Else the element can only be present in right sub-array 
                return BinarySearchRecursive(array, searchingElement, middleIndex + 1, rightmostIndex);
            }

            return -1;
        }

        static int BinarySearchIterative(int[] array, int searchingElement)
        {
            int leftmostIndex = 0;
            int rightmostIndex = array.Length - 1;
            while (leftmostIndex <= rightmostIndex)
            {
                int middleIndex = leftmostIndex + (rightmostIndex - leftmostIndex) / 2;

                if (array[middleIndex] == searchingElement)
                    return middleIndex;

                if (array[middleIndex] < searchingElement)
                    leftmostIndex = middleIndex + 1;
                else
                    rightmostIndex = middleIndex - 1;
            }
            return -1;
        }

        static void Main(string[] args)
        {
            int[] arr = { 2, 3, 4, 10, 40 };
            int n = arr.Length;
            int x = 10;

            int binarySearchRecursiveResult = BinarySearchRecursive(arr, x, 0, n - 1);
            if (binarySearchRecursiveResult == -1)
                Console.WriteLine("BinarySearchRecursive: Element not present");
            else
                Console.WriteLine("BinarySearchRecursive: Element found at index " + binarySearchRecursiveResult);

            int binarySearchIterativeResult = BinarySearchIterative(arr, x);

            if (binarySearchIterativeResult == -1)
                Console.WriteLine("BinarySearchIterative: Element not present");
            else
                Console.WriteLine("BinarySearchIterative: Element found at index " + binarySearchIterativeResult);

            Console.ReadKey();
        }
    }
}