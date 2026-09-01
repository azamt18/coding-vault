using System;
using System.Text.RegularExpressions;

namespace CSharpExercises.Strings
{
    class HowManyOccurrences
    {
        static void Main(string[] args)
        {
            Console.WriteLine(HowManyOccurrencesMethod("do it now", "do")); //  → 1
            Console.WriteLine(HowManyOccurrencesMethod("empty", "d")); //  → 0
            Console.WriteLine(HowManyOccurrencesMethod("104 593 00 - 930 720193", "93")); //  → 3

            Console.ReadKey();
        }

        static int HowManyOccurrencesMethod(string input, string pattern)
        {
            //var count = Regex.Matches(input, pattern).Count;
            int count = 0;
            int found = 0;

            for (int i = 0; i < input.Length; i++)
            {
                found = input.IndexOf(pattern, i);

                if (found > -1)
                {
                    count++;
                    i = found;
                }
            }

            return count;
        }
    }
}
