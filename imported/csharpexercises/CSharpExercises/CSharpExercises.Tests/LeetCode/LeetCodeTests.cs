using CSharpExercises.Arrays;
using CSharpExercises.Strings;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CSharpExercises.Tests.LeetCode
{
    [TestFixture]
    public class LeetCodeTests
    {
        [Test]
        [TestCase("leetcode", 2)]
        [TestCase("abbcccddddeeeeedcba", 5)]
        public void _1446ConsecutiveCharacters(string input, int expected)
        {
            Assert.That(Consecutive.MaxPower(input), Is.EqualTo(expected));
        }

        [Test]
        [TestCase(new int[] { 0 }, 0)]
        [TestCase(new int[] { 1 }, 1)]
        [TestCase(new int[] { 1, 1, 0, 1, 1, 1 }, 3)]
        [TestCase(new int[] { 1, 0, 1, 1, 0, 1 }, 2)]
        public void _485MaxConsecutiveOnes(int[] input, int expected)
        {
            Assert.That(Consecutive.FindMaxConsecutiveOnes(input), Is.EqualTo(expected));
        }

        [Test]
        [TestCase("anagram", "anagram", true)]
        [TestCase("anagram", "nagaram", true)]
        [TestCase("rat", "car", false)]
        [TestCase("aa", "a", false)]
        public void _242ValidAnagram(string s, string t, bool expected)
        {
            Assert.That(ArraysAndHashing.IsAnagram(s, t), Is.EqualTo(expected));
        }

    }
}
