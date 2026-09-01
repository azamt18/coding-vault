

using CSharpExercises.Edabit;

namespace CSharpExercises.Tests.Edabit
{
    [TestFixture]
    public class Tests
    {
        [Test]
        [TestCase(1, "January")]
        [TestCase(2, "February")]
        [TestCase(3, "March")]
        [TestCase(4, "April")]
        [TestCase(5, "May")]
        [TestCase(6, "June")]
        [TestCase(7, "July")]
        [TestCase(8, "August")]
        [TestCase(9, "September")]
        [TestCase(10, "October")]
        [TestCase(11, "November")]
        [TestCase(12, "December")]
        public void MonthName(int num, string expected)
        {
            Console.WriteLine($"Input: {num}");
            Assert.That(MonthNameByNumber.MonthNameMethod(num), Is.EqualTo(expected), "correct");
        }

        [Test]
        public void SortNumsAscending()
        {
            int[] haystack_1 = new int[] { 1, 2, 10, 50, 5 };
            int[] haystack_2 = new int[] { 80, 29, 4, -95, -24, 85 };
            int[] haystack_4 = new int[] { };
            int[] haystack_5 = new int[] { 47, 51, -17, -16, 91, 47, -85, -8, -16, -27 };
            int[] haystack_6 = new int[] { -51, -73, 65, 69, -76, 74, -14 };
            int[] haystack_7 = new int[] { 45, 98, 35, 65, 97, 21, 33 };
            int[] haystack_8 = new int[] { -23, -69, -54, -2, -32 };
            int[] haystack_9 = new int[] { -21, -9, -96 };
            int[] haystack_10 = new int[] { 0 };

            Assert.That(EdabitExercises.SortNumsAscending(haystack_1), Is.EqualTo(new int[] { 1, 2, 5, 10, 50 }));
            Assert.That(EdabitExercises.SortNumsAscending(haystack_2), Is.EqualTo(new int[] { -95, -24, 4, 29, 80, 85 }));
            Assert.That(EdabitExercises.SortNumsAscending(haystack_4), Is.EqualTo(new int[] { }));
            Assert.That(EdabitExercises.SortNumsAscending(haystack_5), Is.EqualTo(new int[] { -85, -27, -17, -16, -16, -8, 47, 47, 51, 91 }));
            Assert.That(EdabitExercises.SortNumsAscending(haystack_6), Is.EqualTo(new int[] { -76, -73, -51, -14, 65, 69, 74 }));
            Assert.That(EdabitExercises.SortNumsAscending(haystack_7), Is.EqualTo(new int[] { 21, 33, 35, 45, 65, 97, 98 }));
            Assert.That(EdabitExercises.SortNumsAscending(haystack_8), Is.EqualTo(new int[] { -69, -54, -32, -23, -2 }));
            Assert.That(EdabitExercises.SortNumsAscending(haystack_9), Is.EqualTo(new int[] { -96, -21, -9 }));
            Assert.That(EdabitExercises.SortNumsAscending(haystack_10), Is.EqualTo(new int[] { 0 }));
        }

        [Test]
        [TestCase(new int[] { 2, -1, -3, 4, 8 }, ExpectedResult = 18)]
        [TestCase(new int[] { -1 }, ExpectedResult = 1)]
        [TestCase(new int[] { -1, -3, -5, -4, -10, 0 }, ExpectedResult = 23)]
        [TestCase(new int[] { 8, 9, 10, 32, 101, -10 }, ExpectedResult = 170)]
        [TestCase(new int[] { 500 }, ExpectedResult = 500)]
        public static int GetAbsSum(int[] arr)
        {
            return EdabitExercises.GetAbsSum(arr);
        }

        [Test]
        [TestCase("My friend Dylan got distracted at school", ExpectedResult = 4)]
        [TestCase("Debris was scattered all over the place.", ExpectedResult = 2)]
        [TestCase("The rodents hibernated in their den.", ExpectedResult = 3)]
        public static int CountDs(string str)
        {
            return EdabitExercises.CountDs(str);
        }

        [Test]
        [TestCase("HELLO", ExpectedResult = true)]
        [TestCase("HEllo", ExpectedResult = false)]
        [TestCase("mArmALadE", ExpectedResult = false)]
        [TestCase("marmalade", ExpectedResult = true)]
        [TestCase("MARMALADE", ExpectedResult = true)]
        [TestCase("ketchUP", ExpectedResult = false)]
        [TestCase("pickle", ExpectedResult = true)]
        [TestCase("MUSTARD", ExpectedResult = true)]
        public static bool SameCase(string str)
        {
            return EdabitExercises.SameCase(str);
        }
    }
}