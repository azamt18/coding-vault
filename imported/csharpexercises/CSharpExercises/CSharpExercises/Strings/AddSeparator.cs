using System;

namespace CSharpExercises.Strings
{
    class AddSeparator
    {
        static void Main(string[] args)
        {
            Console.WriteLine(AddSeparatorMethod("ABCD", "^")); // "A^B^C^D^"
            Console.WriteLine(AddSeparatorMethod("chocolate", "-")); // "c-h-o-c-o-l-a-t-e"

            Console.ReadLine();
        }

        static string AddSeparatorMethod(string word, string separator)
        {
            string generatedString = string.Empty;

            for (int i = 0; i < word.Length; i++)
            {

                //if (i == word.Length - 1)
                //    generatedString += word[i];
                //else
                //    generatedString += word[i] + separator;

                generatedString += (i == word.Length - 1) ? word[i].ToString() : word[i] + separator;

            }

            return generatedString;
        }
    }
}
