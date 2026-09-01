using System;
using System.Globalization;

namespace CSharpExercises.Edabit
{
    public class MonthNameByNumber
    {
        public static string MonthNameMethod(int num)
        {
            return CultureInfo.CurrentUICulture.DateTimeFormat.GetMonthName(num);
        }
    }


}