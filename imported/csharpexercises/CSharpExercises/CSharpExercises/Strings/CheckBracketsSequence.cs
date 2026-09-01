using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CSharpExercises.Strings
{
    class CheckBracketsSequence
    {
        static void Main(string[] args)
        {
            Console.WriteLine(CheckBracketsSequenceMethod("((()))")); // true
            Console.WriteLine(CheckBracketsSequenceMethod("()(())(")); // false
            Console.WriteLine(CheckBracketsSequenceMethod(")")); // false

            Console.ReadLine();
        }

        static bool CheckBracketsSequenceMethod(string sequence)
        {
            int balance = 0;

            for (int i = 0; i < sequence.Length; i++)
            {
                balance = sequence[i] == '(' ? ++balance : --balance;
            }

            return balance == 0;
        }
    }
}
