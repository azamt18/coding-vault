using System;
using System.Text.RegularExpressions;

namespace CSharpExercises.RegularExpressions
{
    class AlmostOnlyLetters
    {
        static void Main(string[] args)
        {

            Console.WriteLine(AlmostOnlyLettersMethod("Very hot."));      // True
            Console.WriteLine(AlmostOnlyLettersMethod("full of hope"));   // False
            Console.WriteLine(AlmostOnlyLettersMethod(""));               // False
            Console.WriteLine(AlmostOnlyLettersMethod("short."));         // True
            Console.ReadKey();
        }

        static bool AlmostOnlyLettersMethod(string str)
        {
            Regex regex = new Regex(@"^[A-Za-z\s]+\.$");
            Match match = regex.Match(str);

            return match.Success;
        }
            
    }
}
