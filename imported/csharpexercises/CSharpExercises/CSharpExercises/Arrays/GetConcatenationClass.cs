using System;

namespace CSharpExercises.Arrays
{
    public class GetConcatenationClass
    {
        static void Main(string[] args)
        {
            Console.WriteLine(GetConcatenationClass.GetConcatenation(new []{1,2,1})); //  → [1,2,1,1,2,1]
            Console.WriteLine(GetConcatenationClass.GetConcatenation(new []{1,3,2,1})); //  → [1,3,2,1,1,3,2,1]

            Console.ReadKey();
        }

        public static int[] GetConcatenation(int[] nums)
        {
            int[] ans = new int[nums.Length * 2];
            int inArrayCounter = 0;
            int outArrayCounter = 0;

            while (outArrayCounter < ans.Length)
            {
                while (inArrayCounter != nums.Length)
                {
                    ans[outArrayCounter] = nums[inArrayCounter];

                    outArrayCounter++;
                    inArrayCounter++;
                }

                inArrayCounter = 0;
            }


            return ans;
        }
    }
}