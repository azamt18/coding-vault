using System;

namespace CSharpExercises.Arrays
{
    public static class RemoveDuplicatesClass
    {
        static void Main(string[] args)
        {
            Console.WriteLine(RemoveDuplicates(new []{0,0,1,1,1,2,2,3,3,4})); //  → [0,1,2,3,4,_,_,_,_,_]

            Console.ReadKey();
        }

        public static int RemoveDuplicates(int[] nums)
        {
            int res = 0;

            for (var i = 0; i < nums.Length; i++)
            {
                if (i == 0 || nums[i] != nums[i-1])
                {
                    nums[res] = nums[i];
                    res++;
                }
                
            }

            return res;
        }
    }
}