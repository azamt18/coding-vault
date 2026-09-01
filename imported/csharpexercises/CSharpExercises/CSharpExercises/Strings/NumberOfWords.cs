using System;

namespace CSharpExercises.Strings
{
    public class NumberOfWords
    {
        static void Main(string[] args)
        {
            //todo - this should return 0, now it returns 1
            Console.WriteLine(NumberOfWordsMethod("")); // 0

            Console.WriteLine(NumberOfWordsMethod("This is sample sentence")); //  → 4
            Console.WriteLine(NumberOfWordsMethod("OK")); //  → 1
            Console.WriteLine(NumberOfWordsMethod("Mauris consectetur urna sit amet risus ultricies rutrum.")); // 8
            Console.WriteLine(NumberOfWordsMethod("Quisque M"));                                                // 2
            Console.WriteLine(NumberOfWordsMethod("Xor"));

            Console.ReadKey();
        }

        static int NumberOfWordsMethod(string str)
        {
            int counter = 0;
            for (int i = 1; i < str.Length; i++)
            {
                counter = char.IsWhiteSpace(str[i]) ? counter + 1 : counter;
            }

            return counter + 1;
        }
    }
}