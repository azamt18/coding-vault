//Find the longest running positive sequence in an array
//Input : arr[] = {1, 2, -3, 2, 3, 4, -6, 1, 2, 3, 4, 5, -8, 5, 6}
//Output :Index : 7, length : 5

using System;
using System.Collections.Generic;
using System.IO;
class Solution
{
    // Time complexity: O(n)
    // Space complexity: O(1)
    static (int, int) LongestPositiveSequence(int[] arr)
    {
        int index = 0; // starting point
        int counter = 0; // longest sequence of positive numbers

        // validation
        // checking empty array
        if (arr.Length == 0)
            return (0, 0); // just for starting

        for (int i = 0; i < arr.Length; i++)
        {
            if (arr[i] > 0) // set as function
            {
                index = i;
                counter++;
            }
            else
            {
                // reset the counters
                counter = 0;
                index = 0;
            }
        }

        return (index, counter);
    }

    static void Main(String[] args)
    {
        int[] arr = new int[] { 1, 2, -3, 2, 3, 4, -6, 1, 2, 3, 4, 5, -8, 5, 6 };
        var (index, counter) = LongestPositiveSequence(arr);

        Console.WriteLine($"{index}{counter}");
    }
}
