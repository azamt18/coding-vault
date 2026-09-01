using System;

namespace CSharpExercises.Strings
{
    class MakeUppercase
    {
        static void Main(string[] args)
        {
            Console.WriteLine(MakeUppercaseMethod("modem")); // → "MoDeM"
            Console.WriteLine(MakeUppercaseMethod("BookWorm")); // → "BoOkWoRm"
            Console.WriteLine(MakeUppercaseMethod("Aliquam dolor nisl?")); // → "AlIqUaM DoLoR NiSl?"

            //#todo complete the task for these cases
            Console.WriteLine(MakeUppercaseMethod("very short sentence."));   // VeRy ShOrT SeNtEnCe.
            Console.WriteLine(MakeUppercaseMethod("motorcycle"));             // MoToRcYcLe
            Console.WriteLine(MakeUppercaseMethod("Events And Delegates"));   // EvEnTs AnD DeLeGaTeS

            Console.ReadKey();
        }

        static string MakeUppercaseMethod(string str)
        {
            string result = String.Empty;

            for (int i = 0; i < str.Length; i++)
                result = i % 2 == 0 ? result + str[i].ToString().ToUpper() : result + str[i];

            return result;
        }
    }
}
