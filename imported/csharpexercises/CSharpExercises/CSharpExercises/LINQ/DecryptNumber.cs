using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CSharpExercises.LINQ
{
    class DecryptNumber
    {
        static void Main(string[] args)
        {
            Console.WriteLine(DecryptNumberMethod("())("));
            Console.WriteLine(DecryptNumberMethod("*$(#&"));
            Console.WriteLine(DecryptNumberMethod("!!!!!!!!!!"));

            Console.ReadKey();
        }

        static string DecryptNumberMethod(string encryptedNumber)
        {
            var chars = new char[] { ')', '!', '@', '#', '$', '%', '^', '&', '*', '(' };
            var decryptedNumber = string.Join("", encryptedNumber.Select(c => Array.IndexOf(chars, c)));

            var result = String.Empty;
            foreach (var specialChar in encryptedNumber)
            {
                switch (specialChar)
                {
                    case '!': result += "1"; break;
                    case '@': result += "2"; break;
                    case '#': result += "3"; break;
                    case '$': result += "4"; break;
                    case '%': result += "5"; break;
                    case '^': result += "6"; break;
                    case '&': result += "7"; break;
                    case '*': result += "8"; break;
                    case '(': result += "9"; break;
                    case ')': result += "0"; break;
                    default: result += ""; break;
                }
            }

            return decryptedNumber;

        }
    }
}
