using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CSharpExercises.Strings
{
    class LengthOfAString
    {
        static void Main(string[] args)
        {
            Console.WriteLine(LengthOfAStringMethod("computer")); // → 8
            Console.WriteLine(LengthOfAStringMethod("ice cream")); // → 9

            Console.WriteLine(LengthOfAStringMethod("Lorem ipsum dolor sit amet")); //26
            Console.WriteLine(LengthOfAStringMethod(string.Empty));                 //0
            Console.WriteLine(LengthOfAStringMethod("conse12ctetur "));             //14

            Console.ReadLine();
        }

        static int LengthOfAStringMethod(string word)
        {
            int length = 0;
            foreach (var letter in word)
            {
                length++;
            }

            return length;
        }
    }
}
