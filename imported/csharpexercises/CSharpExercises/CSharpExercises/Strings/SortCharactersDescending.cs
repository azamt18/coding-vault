using System;

namespace CSharpExercises.Strings
{
    class SortCharactersDescending
    {
        static void Main(string[] args)
        {
            Console.WriteLine(SortCharactersDescendingMethod("onomatopoeia")); // tpoooonmieaa
            Console.WriteLine(SortCharactersDescendingMethod("fohjwf42os")); // wsoojhff42
            Console.WriteLine(SortCharactersDescendingMethod("Aliquam pulvinar aliquam libero, in fringilla erat.")); // vuuutrrrrqqponnnmmlllllliiiiiiigfeebaaaaaaA.,

            Console.ReadKey();
        }

        static char[] SortCharactersDescendingMethod(string str)
        {
            char[] characters = str.ToCharArray();
            Array.Sort(characters);
            Array.Reverse(characters);

            return characters;
        }
    }
}
