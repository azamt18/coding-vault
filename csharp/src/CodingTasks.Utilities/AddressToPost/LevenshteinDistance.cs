using System;

namespace CodingTasks.Utilities.AddressToPost;

public static class LevenshteinDistance
{
    public static int Compute(string s, string t)
    {
        if (string.IsNullOrEmpty(s)) return t?.Length ?? 0;
        if (string.IsNullOrEmpty(t)) return s.Length;

        int n = s.Length;
        int m = t.Length;
        int[,] d = new int[n + 1, m + 1];

        for (int i = 0; i <= n; d[i, 0] = i++) { }
        for (int j = 0; j <= m; d[0, j] = j++) { }

        for (int i = 1; i <= n; i++)
        {
            for (int j = 1; j <= m; j++)
            {
                int cost = (t[j - 1] == s[i - 1]) ? 0 : 1;
                d[i, j] = Math.Min(
                    Math.Min(d[i - 1, j] + 1, d[i, j - 1] + 1),
                    d[i - 1, j - 1] + cost);
            }
        }
        return d[n, m];
    }

    public static double CalculateSimilarity(string source, string target)
    {
        if (source == null || target == null) return 0.0;
        if (source.Length == 0 && target.Length == 0) return 1.0;
        if (source.Length == 0 || target.Length == 0) return 0.0;
        if (source == target) return 1.0;

        int stepsToSame = Compute(source, target);
        return 1.0 - ((double)stepsToSame / Math.Max(source.Length, target.Length));
    }
}
