using System;
using System.Collections.Generic;
using System.Linq;

namespace CSharpExercises.Arrays
{
    public class ArraysAndHashing
    {
        public static bool ContainsDuplicate(int[] nums)
        {
            var result = false;
            var hashSet = new HashSet<int>();
            for (int i = 0; i < nums.Length; i++)
            {
                if (hashSet.Contains(nums[i]))
                {
                    result = true;
                    break;
                }

                hashSet.Add(nums[i]);
            }

            return result;
        }

        public static bool IsAnagram(string s, string t)
        {
            if (s.Length != t.Length)
                return false;

            // sorted (hash) array
            return s.ToCharArray().OrderBy(x => x).SequenceEqual(t.ToCharArray().OrderBy(x => x));
        }
    }
}
