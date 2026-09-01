using System;
using System.Text.RegularExpressions;

namespace CSharpExercises.RegularExpressions
{
    class DecimalDigitInformation
    {
        static void Main(string[] args)
        {
            Console.WriteLine(DecimalDigitInformationMethod("The 7 is the digit!"));    // Digit 7 at position 4
            Console.WriteLine(DecimalDigitInformationMethod("Hamster and lion"));       // No digit found!
            Console.WriteLine(DecimalDigitInformationMethod("1st"));                    // Digit 1 at position 0
            Console.ReadKey();
        }

        static string DecimalDigitInformationMethod(string str)
        {
            string regex = @"\d";
            Match match = Regex.Match(str, regex);

            return match.Success ? $"Digit '{match.Value}' at position {match.Index}" : "No digit found!";
        }
    }
}
