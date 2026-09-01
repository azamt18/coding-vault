using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace CodingTasks.Utilities.Renamer;

public static class StringAggregator
{
    public static string JoinNonEmpty(string separator, params string[] values)
    {
        return string.Join(separator, values.Where(s => !string.IsNullOrEmpty(s)));
    }

    public static Dictionary<string, int> CountOccurrences(IEnumerable<string> items)
    {
        return items
            .GroupBy(x => x)
            .ToDictionary(g => g.Key, g => g.Count());
    }
}
