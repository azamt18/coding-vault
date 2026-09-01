using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using SimMetrics.Net.API;
using SimMetrics.Net.Metric;

namespace AdressToPostIndex
{
    /// <summary>
    /// Contains approximate string matching
    /// </summary>
    static class LevenshteinDistance
    {
        /// <summary>
        /// Compute the distance between two strings.
        /// </summary>
        public static int Compute(string s, string t)
        {
            int n = s.Length;
            int m = t.Length;
            int[,] d = new int[n + 1, m + 1];

            // Step 1
            if (n == 0)
            {
                return m;
            }

            if (m == 0)
            {
                return n;
            }

            // Step 2
            for (int i = 0; i <= n; d[i, 0] = i++)
            {
            }

            for (int j = 0; j <= m; d[0, j] = j++)
            {
            }

            // Step 3
            for (int i = 1; i <= n; i++)
            {
                //Step 4
                for (int j = 1; j <= m; j++)
                {
                    // Step 5
                    int cost = (t[j - 1] == s[i - 1]) ? 0 : 1;

                    // Step 6
                    d[i, j] = Math.Min(
                        Math.Min(d[i - 1, j] + 1, d[i, j - 1] + 1),
                        d[i - 1, j - 1] + cost);
                }
            }
            // Step 7
            return d[n, m];
        }
    }

    static class LevenshteinDistanceV2
    {
        public static int LevenshteinDistance(string source, string target)
        {
            // degenerate cases
            if (source == target) return 0;
            if (source.Length == 0) return target.Length;
            if (target.Length == 0) return source.Length;

            // create two work vectors of integer distances
            int[] v0 = new int[target.Length + 1];
            int[] v1 = new int[target.Length + 1];

            // initialize v0 (the previous row of distances)
            // this row is A[0][i]: edit distance for an empty s
            // the distance is just the number of characters to delete from t
            for (int i = 0; i < v0.Length; i++)
                v0[i] = i;

            for (int i = 0; i < source.Length; i++)
            {
                // calculate v1 (current row distances) from the previous row v0

                // first element of v1 is A[i+1][0]
                //   edit distance is delete (i+1) chars from s to match empty t
                v1[0] = i + 1;

                // use formula to fill in the rest of the row
                for (int j = 0; j < target.Length; j++)
                {
                    var cost = (source[i] == target[j]) ? 0 : 1;
                    v1[j + 1] = Math.Min(v1[j] + 1, Math.Min(v0[j + 1] + 1, v0[j] + cost));
                }

                // copy v1 (current row) to v0 (previous row) for next iteration
                for (int j = 0; j < v0.Length; j++)
                    v0[j] = v1[j];
            }

            return v1[target.Length];
        }
        
        /// <summary>
        /// Calculate percentage similarity of two strings
        /// <param name="source">Source String to Compare with</param>
        /// <param name="target">Targeted String to Compare</param>
        /// <returns>Return Similarity between two strings from 0 to 1.0</returns>
        /// </summary>
        public static double CalculateSimilarity(string source, string target)
        {
            if ((source == null) || (target == null)) return 0.0;
            if ((source.Length == 0) || (target.Length == 0)) return 0.0;
            if (source == target) return 1.0;

            int stepsToSame = LevenshteinDistance(source, target);
            return (1.0 - ((double)stepsToSame / (double)Math.Max(source.Length, target.Length)));
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            Console.OutputEncoding = Encoding.UTF8;

            //string source = @"АБДУЛЛА КОДИРИЙ   2".ToLowerInvariant();
            string source = "Тошкент шаҳар, Юнусобод тумани, АБДУЛЛА КОДИРИЙ , 59/6, 2".ToLowerInvariant();
            //string source = "Тошкент шаҳар, Юнусобод тумани, Г.ТАШКЕНТ, УЛ.АБДУЛЛА КОДИРИЙ 2,".ToLowerInvariant();
            string target1 = "Абдулла  Кодирий 2".ToLowerInvariant();
            string target2 = "Абдулла  Кодирий 2a".ToLowerInvariant();

            Console.WriteLine("{0} <=> {1} => similarity = {2}", source, target1, LevenshteinDistanceV2.CalculateSimilarity(source, target1));
            Console.WriteLine("{0} <=> {1} => similarity = {2}", source, target2, LevenshteinDistanceV2.CalculateSimilarity(source, target2));

            var str1 = "clifton phua";
            var str2 = "clifton phua";
            
            //clifton added
            AbstractStringMetric metric = new CosineSimilarity();
            var result = metric.GetSimilarity(str1, str2);
            Console.Out.WriteLine(result); //Display the string.
            

            Console.WriteLine(Compute(str1, str2));


            Console.WriteLine(LevenshteinDistance.Compute("aunt", "ant"));
            Console.WriteLine(LevenshteinDistance.Compute("Sam", "Samantha"));
            Console.WriteLine(LevenshteinDistance.Compute("flomax", "volmax"));

            //SimMetricsMetricUtilities.Levenstein ls = new SimMetricsMetricUtilities.Levenstein(); //compare string 1, string 2 
            //double sim = ls.GetSimilarity(string_1, string_2);
            //if (sim > [some value])
            //{
            //    //do something 
            //}

            Console.ReadLine();
        }

        public static int Compute(string source, string target)
        {
            if (string.IsNullOrEmpty(source))
            {
                if (string.IsNullOrEmpty(target))
                    return 0;
                return target.Length;
            }

            if (string.IsNullOrEmpty(target))
            {
                return source.Length;
            }

            int n = source.Length;
            int m = target.Length;
            int[,] d = new int[n + 1, m + 1];

            // initialize the top and right of the table to 0, 1, 2, ...
            for (int i = 0; i <= n; d[i, 0] = i++) ;
            for (int j = 1; j <= m; d[0, j] = j++) ;

            for (int i = 1; i <= n; i++)
            {
                for (int j = 1; j <= m; j++)
                {
                    int cost = (target[j - 1] == source[i - 1]) ? 0 : 1;
                    int min1 = d[i - 1, j] + 1;
                    int min2 = d[i, j - 1] + 1;
                    int min3 = d[i - 1, j - 1] + cost;
                    d[i, j] = Math.Min(Math.Min(min1, min2), min3);
                }
            }
            return d[n, m];
        }
    }
}
