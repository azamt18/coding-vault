using System;
using System.Linq;

namespace CSharpExercises.LibraryFunctions
{
    public class ReplaceXWithY
    {
        static void Main(string[] args)
        {
            Console.WriteLine(ReplaceXWithYMethod("yellow"));
            Console.WriteLine(ReplaceXWithYMethod("mushroom"));
            Console.WriteLine(ReplaceXWithYMethod("strawberry youghurt"));
            Console.WriteLine(ReplaceXWithYMethod("tym ryhosx oifg 6 t6 ypeg ergh"));
            Console.WriteLine(ReplaceXWithYMethod(""));
            Console.ReadKey();
        }

        static string ReplaceXWithYMethod(string str)
        {
            foreach (var c in str.Where(c => c == 'y'))
            {
                str = str.Replace(c, 'x');
            }

            return str;
        }
    }
}