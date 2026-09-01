using System;

namespace CSharpExercises.Arrays
{
    public class RemoveElementClass
    {
        static void Main(string[] args)
        {
            Console.WriteLine(RemoveElementClass.RemoveElement(new []{3,2,2,3}, 3)); //  → 2, nums = [2,2,_,_]
            Console.WriteLine(RemoveElementClass.RemoveElement(new []{0,1,2,2,3,0,4,2}, 2)); //  → 5, nums = [0,1,4,0,3,_,_,_]

            Console.ReadKey();
        }

        public static int RemoveElement(int[] nums, int val)
        {
            int res = 0;

            for (var i = 0; i < nums.Length; i++)
            {
                if (nums[i] != val)
                {
                    nums[res] = nums[i];
                    res++;
                }
            }

            return res;
        }
    }
}