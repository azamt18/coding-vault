using System;

namespace CSharpExercises.Edabit
{
    public class NameShuffle
    {
        static void Main(string[] args)
        {
            Console.WriteLine(NameShuffleMethod("Donald Trump")); // ➞ "Trump Donald"

            Console.WriteLine(NameShuffleMethod("Rosie O'Donnell")); // ➞ "O'Donnell Rosie"

            Console.WriteLine(NameShuffleMethod("Seymour Butts")); // ➞ "Butts Seymour"

            Console.ReadKey();
        }

        public static string NameShuffleMethod(string str)
        {
            string[] names = str.Split(' ');
            Array.Reverse(names);
            var @join = string.Join(" ", names);
            return @join;
        }
    }
}