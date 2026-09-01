using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;

namespace CSharpExercises.LibraryFunctions
{
    public class IfStartsWithLowerCase
    {
        static void Main(string[] args)
        {
            Console.WriteLine(IfStartsWithLowerCaseMethod("Alfa Beta gamma"));
            Console.WriteLine(IfStartsWithLowerCaseMethod("Alfa beta gamma"));
            Console.WriteLine(IfStartsWithLowerCaseMethod("alfa Beta gamma"));
            Console.ReadKey();
        }

        static string IfStartsWithLowerCaseMethod(string str)
        {
            char[] delimeterChars = { ' ' };
            string[] stringsArray = str.Split(delimeterChars);
            List<string> stringsList = new List<string>();
            foreach (var s in stringsArray)
            {
                stringsList.Add(s);
            }

            for (var index = 0; index < stringsList.Count; index++)
            {
                var s = stringsList[index];
                if (StartsWithLowercase(s))
                {
                    stringsList.Remove(s);
                }
            }

            string result = String.Empty;

            foreach (var s in stringsList)
            {
                result += s;
            }

            return result;
        }

        private static bool StartsWithLowercase(string s)
        {
            var chars = s.ToCharArray();
            return chars[0] >= 97 && chars[0] <= 122;
        }
    }
}