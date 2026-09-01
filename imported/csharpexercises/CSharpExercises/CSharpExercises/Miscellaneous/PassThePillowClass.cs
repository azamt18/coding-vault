using System;

namespace CSharpExercises
{
    public class PassThePillowClass
    {
        void Main(string[] args)
        {
            Console.WriteLine(PassThePillow(4,5));  // 2
            Console.WriteLine(PassThePillow(3,2));  // 3

            Console.ReadLine();
        }
        
        public int PassThePillow(int n, int time)
        {
            var array = new int[n];
            var counter = 0;
            var i = 0;

            while (i < time)
            {
                counter++;
                i++;
            }
            
            return counter;
        }
    }
}