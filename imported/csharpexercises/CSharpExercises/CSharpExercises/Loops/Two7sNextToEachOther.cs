using System;

namespace CSharpExercises.Loops
{
    class Two7sNextToEachOther
    {
        static void Main(string[] args)
        {
            int[] array1 = new int[] { 8, 2, 5, 7, 9, 0, 7, 7, 3, 1 };
            int[] array2 = new[] { 9, 4, 5, 3, 7, 7, 7, 3, 2, 5, 7, 7 };

            Console.WriteLine($"{Two7sNextToEachOtherMethod(array1)}");
            Console.WriteLine($"{Two7sNextToEachOtherMethod(array2)}");
            Console.ReadLine();
        }

        public static int Two7sNextToEachOtherMethod(int[] array)
        {
            int counter = 0;

            for (int i = 0; i < array.Length - 1; i++)
            {
                if (array[i] == 7 && array[i+1] == 7)
                {
                    counter++;
                }
            }

            return counter;
        }
    }
}
