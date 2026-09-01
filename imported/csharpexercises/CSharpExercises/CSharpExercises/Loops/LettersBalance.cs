using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CSharpExercises.Loops
{
    class LettersBalance
    {
        static void Main(string[] args)
        {
            Console.WriteLine(LettersBalanceMethod("fgvgvf"));                          // True
            Console.WriteLine(LettersBalanceMethodOriginalSolution("fgvgvf"));          // True

            Console.WriteLine(LettersBalanceMethod("lampsmpser"));                      // False
            Console.WriteLine(LettersBalanceMethodOriginalSolution("lampsmpser"));      // False

            Console.WriteLine(LettersBalanceMethod("kfdfdk"));                          // True
            Console.WriteLine(LettersBalanceMethodOriginalSolution("kfdfdk"));           // True

            Console.WriteLine(LettersBalanceMethod("reyjer"));                          // False
            Console.WriteLine(LettersBalanceMethodOriginalSolution("reyjer"));           // False

            Console.WriteLine(LettersBalanceMethod("wkxzcsazsckawx"));                  // True
            Console.WriteLine(LettersBalanceMethodOriginalSolution("wkxzcsazsckawx"));   // True

            Console.ReadLine();
        }

        static bool LettersBalanceMethod(string word)
        {
            if (word.Length % 2 != 0)
                return false;

            string substringFirstPart = string.Empty;
            string substringSecondPart = string.Empty;

            for (int i = 0; i < word.Length; i++)
            {
                if (i <= word.Length / 2 -1)
                    substringFirstPart += word[i];
                else
                    substringSecondPart += word[i];
            }

            char[] charArrayFirstPart = substringFirstPart.ToLower().ToCharArray();
            char[] charArraySecondPart = substringSecondPart.ToLower().ToCharArray();

            Array.Sort(charArrayFirstPart);
            Array.Sort(charArraySecondPart);

            substringFirstPart = new string(charArrayFirstPart);
            substringSecondPart = new string(charArraySecondPart);
            

            return substringFirstPart == substringSecondPart;

        }

        static bool LettersBalanceMethodOriginalSolution(string word)
        {
            bool isBalanced;
            for (int i = 0; i < word.Length / 2; i++)
            {
                isBalanced = false;
                for (int j = word.Length - 1; j >= word.Length / 2; j--)
                {
                    if (word[i] == word[j])
                    {
                        isBalanced = true;
                    }
                }

                if (!isBalanced)
                {
                    return false;
                }
            }

            return true;
        }
    }
}
