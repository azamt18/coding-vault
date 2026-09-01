using Algorithmics.ArraysAndHashing;
using FluentAssertions;
using NUnit.Framework;

namespace CodingTasks.Tests.ArraysAndHashing;

[TestFixture]
public class GroupAnagramsSolutionTests
{
    private GroupAnagramsSolution _sut = null!;

    [SetUp]
    public void SetUp()
    {
        _sut = new GroupAnagramsSolution();
    }

    [Test]
    public void GroupAnagrams_StandardInput_GroupsCorrectly()
    {
        // Arrange
        string[] input = ["eat", "tea", "tan", "ate", "nat", "bat"];

        // Act
        var result = _sut.GroupAnagrams(input);

        // Assert: order of groups or items within groups may vary, so check equivalence
        result.Should().HaveCount(3);
        result.Should().ContainEquivalentOf(new[] { "eat", "tea", "ate" });
        result.Should().ContainEquivalentOf(new[] { "tan", "nat" });
        result.Should().ContainEquivalentOf(new[] { "bat" });
    }

    [Test]
    public void GroupAnagrams_SingleEmptyString_ReturnsSingleEmptyGroup()
    {
        // Arrange
        string[] input = [""];

        // Act
        var result = _sut.GroupAnagrams(input);

        // Assert
        result.Should().HaveCount(1);
        result[0].Should().Equal(new[] { "" });
    }

    [Test]
    public void GroupAnagrams_SingleCharacter_ReturnsSingleGroup()
    {
        // Arrange
        string[] input = ["a"];

        // Act
        var result = _sut.GroupAnagrams(input);

        // Assert
        result.Should().HaveCount(1);
        result[0].Should().Equal(new[] { "a" });
    }

    [Test]
    public void GroupAnagrams_NoAnagrams_EachInItsOwnGroup()
    {
        // Arrange
        string[] input = ["abc", "def", "ghi"];

        // Act
        var result = _sut.GroupAnagrams(input);

        // Assert
        result.Should().HaveCount(3);
        result.Should().ContainEquivalentOf(new[] { "abc" });
        result.Should().ContainEquivalentOf(new[] { "def" });
        result.Should().ContainEquivalentOf(new[] { "ghi" });
    }
}
