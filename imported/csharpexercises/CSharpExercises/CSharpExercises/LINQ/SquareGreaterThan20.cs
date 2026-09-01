using System;
using System.Collections.Generic;
using System.Linq;

namespace CSharpExercises.LINQ
{
    class SquareGreaterThan20
    {
        static void Main(string[] args)
        {
            List<int> numbers = new List<int> { 7, 2, 30 };
            var result = numbers.Where(n => Math.Pow(n, 2) > 20);

            foreach (var item in result)
            {
                Console.WriteLine($"{item} - {Math.Pow(item, 2)}");
            }

            Console.ReadKey();
        }
    }
}
