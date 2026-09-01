using System;
using System.Globalization;

namespace CSharpExercises.Edabit
{
    public class SmallerNum
    {
        private static void Main(string[] args)
        {
            Console.WriteLine(SmallerNumMethod("21", "44"));
            Console.WriteLine(SmallerNumMethod("1500", "1"));
            Console.WriteLine(SmallerNumMethod("1500", "16"));
            Console.WriteLine(SmallerNumMethod("5", "5"));

            Console.ReadKey();
        }

        public static string SmallerNumMethod(string n1, string n2)
        {
            if (n1.Length == n2.Length)
            {
                var length = n1.Length > n2.Length ? n1.Length : n2.Length;
                var compareResult = string.CompareOrdinal(n1, 0, n2, 0, length);
                return compareResult <= 0 ? n1 : n2;
            }

            try
            {
                var val1 = int.Parse(n1);
                var val2 = int.Parse(n2);
                return val1 > val2 ? n2 : n1;
            }
            catch (Exception e)
            {
                Console.WriteLine(e);
                throw;
            }
        }
    }
}