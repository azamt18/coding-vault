using System;
using System.Collections.Generic;

namespace CSharpExercises.Strings
{
    class RevertWordsOrder
    {
        static void Main(string[] args)
        {
            Console.WriteLine(RevertWordsOrderMethod("John Doe.")); // → "Doe John."
            Console.WriteLine(RevertWordsOrderMethod("A, B. C.")); // → "C B. A,"
            Console.WriteLine(RevertWordsOrderMethod("Proin in odio viverra, accumsan purus vel, placerat elit!")); // → elit placerat vel, purus accumsan viverra, odio in Proin!

            Console.ReadKey();
        }

        static string RevertWordsOrderMethod(string text)
        {
            String result = String.Empty;

            char[] delimeterChars = { ' ' };
            string[] words = text.Split(delimeterChars);
            List<string> list = new List<string>();

            for (int i = words.Length - 1; i >= 0 ; i--)
            {
                list.Add(words[i]);
            }

            String[] wordsArray = list.ToArray();
            result = String.Join(" ", wordsArray);

            return result;
        }
    }
}
