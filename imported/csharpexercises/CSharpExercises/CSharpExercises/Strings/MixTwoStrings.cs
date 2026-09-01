using System;

namespace CSharpExercises.Strings
{
    public class MixTwoStrings
    {
        static void Main(string[] args)
        {
            Console.WriteLine(MixTwoStringsMethod("aaa", "BBB")); // → "aBaBaB"
            Console.WriteLine(MixTwoStringsMethod("good one", "111")); // → "g1o1o1d one"
            Console.ReadKey();
        }

        static string MixTwoStringsMethod(string str1, string str2)
        {
            string result = string.Empty;

            for (int i = 0; i < (str1.Length > str2.Length ? str1.Length : str2.Length); i++)
            {
                if (i < str1.Length)
                {
                    result += str1[i];
                }
                if (i < str2.Length)
                {
                    result += str2[i];
                }
            }

            return result;
        }
    }
}