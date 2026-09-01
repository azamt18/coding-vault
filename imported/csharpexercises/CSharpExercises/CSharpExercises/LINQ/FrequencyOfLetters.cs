using System;
using System.Linq;

namespace CSharpExercises.LINQ
{
    class FrequencyOfLetters
    {
        static void Main(string[] args)
        {
            string word = "gamma";

            var result = word.GroupBy(x => x);

            foreach (var l in result)
            {
                Console.Write($"Letter {l.Key} occurs {l.Count()} time(s), ");
            }
             
            Console.ReadKey();
        }
    }
}
