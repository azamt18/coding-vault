using System;

namespace CSharpExercises.Searching
{
    public class LinearSearch
    {
        static int linearSearch(int[] array, int searchingElement)
        {
            for (int i = 0; i < array.Length; i++)
            {
                if (array[i] == searchingElement)
                    return i;
            }

            return -1;
        }

        static void Main(string[] args)
        {
            int[] arr = { 2, 3, 4, 10, 40 };
            int x = 10;

            // Function call 
            int result = linearSearch(arr, x);
            if (result == -1)
                Console.WriteLine(
                    "Element is not present in array");
            else
                Console.WriteLine("Element is present at index "
                                  + result);

            Console.ReadKey();
        }
    }
}