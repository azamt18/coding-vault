using System.Diagnostics.CodeAnalysis;

namespace Algorithmics.ArraysAndHashing;

/// <summary>
/// Problem: Group Anagrams (LeetCode 49 / Blind 75)
/// Given an array of strings strs, group the anagrams together. You can return the answer in any order.
/// </summary>
public class GroupAnagramsSolution
{
    public IList<IList<string>> GroupAnagrams(string[] strs)
    {
        var dict = new Dictionary<string, IList<string>>();
        foreach (var word in strs)
        {
            Span<char> count1 = stackalloc char[26];
            var count2 = new int[26];
            foreach (var c in word)
            {
                // count['z' - c] += (char)1;
                count2['z' - c]++;
            }

            var key1 = new string(count1); // produces "\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0".
            var key2 = string.Join(',', count2);
            if (!dict.TryGetValue(key2, out var list))
            {
                list = new List<string>();
                dict[key2] = list;
            }

            list.Add(word);
        }

        return [.. dict.Values];
    }
    
    public IList<IList<string>> GroupAnagramsUsingLinq(string[] strs)
    {
        var grouped1 = strs.GroupBy(word => word.Order().ToArray()); // <- returns char[]
        var grouped2 = strs.GroupBy(word => new string(word.Order().ToArray()));
        var result = grouped2.Select(group => group.ToList());
        return result.ToList<IList<string>>();
    }
    
    public IList<IList<string>> GroupAnagramsUsingDict(string[] strs)
    {
        var dict = new Dictionary<string, IList<string>>();
        foreach (var word in strs)
        {
            var sortedWordArr = word.Order();
            string key = string.Concat(sortedWordArr);
            if (!dict.TryGetValue(key, out var list))
            {
                list = new List<string>();
                dict[key] = list;
            }

            list.Add(word);
        }

        return [.. dict.Values];
    }
    
    public IList<IList<string>> GroupAnagramsDefault(string[] strs)
    {
        var dict = new Dictionary<string, List<string>>();

        foreach (var word in strs)
        {
            var arr = word.ToCharArray();
            Array.Sort(arr);
            var key = new string(arr);

            if (!dict.TryGetValue(key, out var list))
            {
                list = new List<string>();
                dict[key] = list;
            }
            list.Add(word);
        }

        return new List<IList<string>>(dict.Values);
    }
}
