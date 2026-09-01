using Algorithmics.ArraysAndHashing;

namespace Algorithmics;

internal static class Program
{
    private static void Main()
    {
        var solution = new GroupAnagramsSolution();
        var result = solution.GroupAnagrams(["eat", "tea", "tan", "ate", "nat", "bat"]);

        Console.WriteLine("Grouped Anagrams:");
        foreach (var group in result)
        {
            Console.WriteLine($"[{string.Join(", ", group)}]");
        }
    }
}
