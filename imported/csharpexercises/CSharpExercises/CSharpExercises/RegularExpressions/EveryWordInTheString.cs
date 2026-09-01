using System;
using System.Text.RegularExpressions;

namespace CSharpExercises.RegularExpressions
{
    class EveryWordInTheString
    {
        static void Main(string[] args)
        {
            Console.WriteLine(EveryWordInTheStringMethod("I Love You"));                    // True
            Console.WriteLine(EveryWordInTheStringMethod("Greater Than 9"));                // False
            Console.WriteLine(EveryWordInTheStringMethod("Pig And Horse!!!"));              // True
            Console.WriteLine(EveryWordInTheStringMethod("Make   Some      Whitespaces?")); // True
            Console.WriteLine(EveryWordInTheStringMethod("As Fit As a Fiddle."));           // False
            Console.ReadKey();
        }

        static bool EveryWordInTheStringMethod(string str)
        {
            Regex regex1 = new Regex(@"^([A-Z]\w*\s*)+\W*$");
            Match match1 = regex1.Match(str);
            Regex regex2 = new Regex(@"^([A-Z]\w*\s*)+\W*$");
            Match match2 = regex2.Match(str);
             
            return match2.Success;
        }
    }
}
