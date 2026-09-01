using System;
using System.Linq;

namespace CSharpExercises.LINQ
{
    class UppercaseOnly
    {
        static void Main(string[] args)
        {
            string str = "DDD example CQRS Event Sourcing";

            var result = str.Split(' ').Where(s => string.Equals(s, s.ToUpper()));

            foreach (var item in result)
            {
                Console.WriteLine($"{item}");
            }

            Console.ReadKey();
        }
    }
}
