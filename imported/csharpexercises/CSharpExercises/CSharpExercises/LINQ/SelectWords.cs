using System;
using System.Collections.Generic;
using System.Linq;

namespace CSharpExercises.LINQ
{
    class SelectWords
    {
        static void Main(string[] args)
        {
            List<string> words = new List<string> { "mum", "amsterdam", "bloom" };

            var result = words.Where(w => w.StartsWith("a")).Where(w => w.EndsWith("m"));

            foreach (var item in result)
            {
                Console.Write($"{item} ");
            }

            Console.ReadKey();
        }
    }
}
