using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CSharpExercises.Loops
{
    class ReplaceWords
    {
        static void Main(string[] args)
        {
            Console.WriteLine(ReplaceWordsMethod("abc_xyz", '_')); // xyz_abc
            Console.WriteLine(ReplaceWordsMethodOriginalSolution("abc_xyz", '_')); // xyz_abc

            Console.WriteLine(ReplaceWordsMethod("trolling.master", '.')); // master.trolling
            Console.WriteLine(ReplaceWordsMethodOriginalSolution("trolling.master", '.')); // master.trolling

            Console.WriteLine(ReplaceWordsMethod("dog_octopus", '_'));     // octopus_dog
            Console.WriteLine(ReplaceWordsMethodOriginalSolution("dog_octopus", '_'));     // octopus_dog

            Console.WriteLine(ReplaceWordsMethod("a.b", '.'));                     // b.a
            Console.WriteLine(ReplaceWordsMethodOriginalSolution("a.b", '.'));                     // b.a

            Console.WriteLine(ReplaceWordsMethod("good very", ' '));         // very good
            Console.WriteLine(ReplaceWordsMethodOriginalSolution("good very", ' '));         // very good

            Console.ReadLine();
        }

        static string ReplaceWordsMethod(string words, char separator)
        {
            string wordPartOne = "";
            string wordPartTwo = "";

            string replacedWords = "";

            for (int i = 0; i < words.Length; i++)
            {
                if (words[i] == separator)
                {
                    wordPartTwo = words.Substring(i + 1);
                    break;
                }

                wordPartOne += words[i];
            }

            replacedWords = wordPartTwo + separator +  wordPartOne;

            return replacedWords;
        }

        public static string ReplaceWordsMethodOriginalSolution(string word, char ch)
        {
            string firstWord = string.Empty;
            string secondWord = string.Empty;

            for (int i = 0; i <= word.Length - 1; i++)
            {
                if (word[i] != ch)
                {
                    secondWord += word[i];
                }
                else
                {
                    for (int j = i + 1; j <= word.Length - 1; j++)
                    {
                        firstWord += word[j];
                    }
                    break;
                }
            }

            return firstWord + ch + secondWord;
        }

    }
}
