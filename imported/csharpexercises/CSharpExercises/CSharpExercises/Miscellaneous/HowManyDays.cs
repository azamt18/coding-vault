using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CSharpExercises.Miscellaneous
{
    class HowManyDays
    {
        static void Main(string[] args)
        {
            Console.WriteLine(HowManyDaysMethod(new DateTime(2006, 1, 31), DateTime.Now));
            Console.ReadKey();
        }

        static int HowManyDaysMethod(DateTime fromDate, DateTime presentDate)
        {
            var result = (presentDate - fromDate).Days;

            return result;
        }
    }
}
