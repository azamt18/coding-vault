using System;
using System.Collections.Generic;
using System.Linq;

namespace CSharpExercises.LINQ
{
    class MinimumLength
    {
        static void Main(string[] args)
        {
            var result = MinimumLengthMethod(new List<string> { "zebra", "elephant", "cat", "dog", "rhino", "bat" });
            foreach (var item in result)
            {
                Console.Write($"{item} ");
            }
            Console.WriteLine();
            Console.ReadKey();
        }

        static List<string> MinimumLengthMethod(List<string> strings)
        {
            List<string> result = null;

            result = strings.Where(s => s.Length >= 5).Select(x => x.ToUpper()).ToList();

            return result;
        }
    }
}
