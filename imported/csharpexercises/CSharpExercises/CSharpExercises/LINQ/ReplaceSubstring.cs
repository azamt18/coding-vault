using System;
using System.Collections.Generic;
using System.Linq;

namespace CSharpExercises.LINQ
{
    class ReplaceSubstring
    {
        static void Main(string[] args)
        {
            List<string> strings = new List<string> { "learn", "current", "deal" };

            //var result = strings.Where(s => s.Contains("ea")).Select(s => s.ToString().Replace("ea", "*"));

            var result = strings.Select(s => s.Contains("ea") ? s.Replace("ea", "*") : s);

            foreach (var item in result)
            {
                Console.WriteLine(item);
            }

            Console.ReadKey();
        }
    }
}
