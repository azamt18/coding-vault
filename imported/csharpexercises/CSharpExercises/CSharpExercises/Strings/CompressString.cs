using System;

namespace CSharpExercises.Strings
{
    class CompressString
    {
        static void Main(string[] args)
        {
            Console.WriteLine(CompressStringMethod("kkkktttrrrrrrrrrr")); // "k4t3r10"
            Console.WriteLine(CompressStringMethod("p555ppp7www")); // → "p153p371w3"
            Console.WriteLine(CompressStringMethod("$999j*#jjjfYyyy")); // $193j1*1#1j3f1Y1y3
            Console.ReadKey();
        }

        static string CompressStringMethod(string str)
        {
            String result = String.Empty;
            int counter = 0;
            int k = 0;

            for (int i = 0; i < str.Length; i = k)
            {
                char c = str[i];
                while (k < str.Length && str[k] == c)
                {
                    counter++;
                    k++;
                }

                result += c.ToString() + counter;
                counter = 0;

            }

            return result;
        }
    }
}
