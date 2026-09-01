using System;

namespace CSharpExercises.ULearn
{
    public class TypeConverting
    {
        static void Main(string[] args)
        {
            Console.WriteLine(GetLastHalf("I love CSharp!"));
            Console.WriteLine(GetLastHalf("1234567890"));
            Console.WriteLine(GetLastHalf("до ре ми фа соль ля си"));
        }

        static string GetLastHalf(string text)
        {
            string res = text.Substring(text.Length / 2, text.Length - 1).Replace(" ", string.Empty);
            return res;
        }
    }
}
