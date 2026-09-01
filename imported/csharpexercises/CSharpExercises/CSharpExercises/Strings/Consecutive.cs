using System;

namespace CSharpExercises.Strings
{
    public class Consecutive
    {
        // TC: O(N)
        // SC: O(1)
        public static int MaxPower(string s)
        {
            var prevCharacter = s[0];
            var currentCount = 0;
            var maxCount = 0;

            foreach (char c in s)
            {
                if (prevCharacter != c)
                {
                    maxCount = Math.Max(currentCount, maxCount);
                    prevCharacter = c;
                    currentCount = 1;
                }
                else
                {
                    currentCount++;
                }
            }

            return Math.Max(currentCount, maxCount);
        }


        public static int FindMaxConsecutiveOnes(int[] nums)
        {
            var currentCount = 0;
            var maxCount = 0;

            foreach (var item in nums)
            {
                if (item != 1)
                {
                    currentCount = 0;
                    continue;
                }

                currentCount++;

                if (currentCount > maxCount)
                    maxCount = currentCount;
            }


            return maxCount;
        }
    }
}
