using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CSharpExercises.LINQ
{
    class MostFrequentLetter
    {
        static void Main(string[] args)
        {
            Console.WriteLine(MostFrequentLetterMethod("panda"));
            Console.WriteLine(MostFrequentLetterMethod("n093nfv034nie9"));

            Console.ReadKey();
        }

        static char MostFrequentLetterMethod(string str)
        {
            var result = str.GroupBy(c => c).OrderByDescending(c => c.Count()).First().Key;

            return result;
        }
    }
}
