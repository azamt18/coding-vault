using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

namespace CSharpExercises.RegularExpressions
{
    class CheckPhoneNumber
    {
        static void Main(string[] args)
        {
            Console.WriteLine(CheckPhoneNumberMethod("+35 392-022-194")); // → true
            Console.WriteLine(CheckPhoneNumberMethod("+958 28492-503")); // → false

            Console.WriteLine(CheckPhoneNumberMethod("+48 592-045-990"));    // True
            Console.WriteLine(CheckPhoneNumberMethod("+999 543-000-305"));   // False
            Console.WriteLine(CheckPhoneNumberMethod("00 204-145-722"));     // False
            Console.WriteLine(CheckPhoneNumberMethod("+47 420-053-934"));    // True
            Console.ReadKey();
        }

        static bool CheckPhoneNumberMethod(string str)
        {
            Regex regex = new Regex(@"^\+\d{2}\s\d{3}\-\d{3}\-\d{3}");
            Match match = regex.Match(str);

            return match.Success;
        }
    }
}
