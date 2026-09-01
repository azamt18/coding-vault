using System.Globalization;

namespace CSharpExercises
{
    public class Program
    {
        public static string MonthNameMethod(int num)
        {
            return CultureInfo.CurrentUICulture.DateTimeFormat.GetMonthName(num);
        }
    }
}
