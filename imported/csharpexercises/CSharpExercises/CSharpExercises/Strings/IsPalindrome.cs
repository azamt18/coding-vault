using System;
using System.Linq;

namespace CSharpExercises.Strings
{
    class IsPalindrome
    {
        static void Main(string[] args)
        {
            Console.WriteLine(IsPalindromeMethod("eye"));  // True
            Console.WriteLine(IsPalindromeMethod("home")); // False

            Console.WriteLine(IsPalindromeMethod("madam")); // True
            Console.WriteLine(IsPalindromeMethod("123454321")); // True
            Console.WriteLine(IsPalindromeMethod("apple")); // False
            Console.WriteLine(IsPalindromeMethod("Curabitur vel est diam")); // False
            Console.WriteLine(IsPalindromeMethod("x")); // True

            Console.ReadLine();
        }

        public int ReturnSecondMax(int[] nums)
        {
            // Insert your code here
            var orderedNums = nums.OrderBy(i => i).ToArray();
            var secondLargest = orderedNums[1];

            return secondLargest;
        }
        
        
        
        static string IsPalindromeMethod(string str)
        {

            bool isPalindrome = true;

            str = str.ToLower();

            for (int i = 0; i < str.Length / 2; i++)
            {
                isPalindrome = str[i] == str[str.Length - 1 - i];
                 if (isPalindrome == false)
                    break;
            }

            return isPalindrome ? "Yes" : "No";
        }
    }
}
