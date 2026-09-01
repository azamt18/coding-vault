using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CSharpExercises.Loops
{
    class ExtractString
    {
        static void Main(string[] args)
        {
            Console.WriteLine(ExtractStringMethod("##abc##def")); // → "abc"
            Console.WriteLine(ExtractStringMethod("12####78")); // → empty string
            Console.WriteLine(ExtractStringMethod("gar##d#en")); // → empty string
            Console.WriteLine(ExtractStringMethod("++##--##++")); // → "--"
        }

        public static string ExtractStringMethod(string word)
        {
            string substring = string.Empty;
            bool firstOccurance = false;
            bool secondOccurance = false;

            for (int i = 0; i < word.Length - 1; i++)
            {
                if (word[i] == '#' && word[i+1] == '#')
                {

                    firstOccurance = true;

                    for (int j = i+2; j < word.Length - 1; j++)
                    {

                        if (word[j] == '#' && word[j+1] == '#')
                        {
                            secondOccurance = true;
                            return substring;
                        }

                        substring += word[j];

                    }

                }

            }


            return string.Empty;
        }
    }
}
