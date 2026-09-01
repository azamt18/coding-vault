using System;
using System.Linq;

namespace CSharpExercises.Edabit
{
    public class EdabitExercises
    {
        public static int[] SortNumsAscending(int[] arr) => arr.OrderBy(x => x).ToArray();

        public static int GetAbsSum(int[] arr) => arr.Sum(Math.Abs);

        public static int CountDs(string str) => str.Count(c => c.Equals('D') || c.Equals('d'));

        public static bool SameCase(string str)
        {
            var newStr = char.IsUpper(str.First()) ? str.ToUpper() : str.ToLower();
            return string.Equals(str, newStr);
        }
    }
}