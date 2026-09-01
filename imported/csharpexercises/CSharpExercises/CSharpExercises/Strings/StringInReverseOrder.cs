using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CSharpExercises.Strings
{
    class StringInReverseOrder
    {
        static void Main(string[] args)
        {
            Console.WriteLine(StringInReverseOrderMethod("qwerty")); // → "ytrewq"
            Console.WriteLine(StringInReverseOrderMethod("oe93 kr")); // → "rk 39eo"

            Console.WriteLine(StringInReverseOrderMethod("Vivamus commodo quam at purus ")); //  surup ta mauq odommoc sumaviV
            Console.WriteLine(StringInReverseOrderMethod("34 ( 9  9@*"));                    // *@9  9 ( 43
            Console.WriteLine(StringInReverseOrderMethod("malesuada"));                      // adauselam
            Console.ReadLine();
        }

        static string StringInReverseOrderMethod(string str)
        {
            string stringInReverseOrder = "";

            for (int i = str.Length - 1; i >= 0; i--)
            {
                stringInReverseOrder += str[i];
            }

            return stringInReverseOrder;
        }
    }
}
