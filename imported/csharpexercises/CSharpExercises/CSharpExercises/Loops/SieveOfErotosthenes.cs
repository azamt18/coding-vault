using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CSharpExercises.Loops
{
    class SieveOfErotosthenes
    {
        static void Main(string[] args)
        {
            Console.WriteLine("SieveOfErotosthenes called");
            bool[] primeNumbers = SieveOfErotosthenesMethod(30);
            for (int p = 0; p < primeNumbers.Length; p++)
            {
                if (primeNumbers[p] == true)
                {
                    Console.Write($"{p} ");
                }
            }

            Console.ReadLine();
        }

        public static bool[] SieveOfErotosthenesMethod(int n)
        {
            bool[] primeNumbers = new bool[n + 1];

            for (int i = 2; i < n; i++)
            {
                primeNumbers[i] = true;
            }

            for (int j = 2; j * j < n; j++)
            {
                if (primeNumbers[j] == true)
                {
                    for (int k = j * j; k < n; k += j)
                    {
                        primeNumbers[k] = false;
                    }
                }
            }

            return primeNumbers;
        }
    }

}
