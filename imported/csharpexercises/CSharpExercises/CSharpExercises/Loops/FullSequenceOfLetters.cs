using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CSharpExercises.Loops
{
    class FullSequenceOfLetters
    {
        static void Main(string[] args)
        {
            Console.WriteLine(FullSequenceOfLettersMethod("ds"));
            Console.WriteLine(FullSequenceOfLettersMethod("or"));

            Console.ReadLine();
        }

        static string FullSequenceOfLettersMethod(string letters)
        {
            char firstChar = letters[0];
            char lastChar = letters[1];
            string sequence = string.Empty;

            for (int i = firstChar; i <= lastChar; i++)
            {
                sequence += (char) (i);
            }

            return sequence;
        }
    }
}
