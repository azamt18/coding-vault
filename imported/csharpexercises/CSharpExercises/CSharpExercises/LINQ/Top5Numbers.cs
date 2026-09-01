using System;
using System.Collections.Generic;
using System.Linq;

namespace CSharpExercises.LINQ
{
    class Top5Numbers
    {
        static void Main(string[] args)
        {
            List<int> numbers = new List<int> { 78, -9, 0, 23, 54, 21, 7, 86 };

            var selectedNumbers = numbers.OrderByDescending(x => x).Take(5);

            foreach (var item in selectedNumbers)
            {
                Console.Write($"{item} ");
            }

            Console.ReadKey();
        }
    }
}
