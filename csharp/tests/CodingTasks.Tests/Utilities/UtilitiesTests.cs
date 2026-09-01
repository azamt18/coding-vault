using CodingTasks.Utilities.AddressToPost;
using CodingTasks.Utilities.Hashing;
using CodingTasks.Utilities.Renamer;
using FluentAssertions;
using NUnit.Framework;

namespace CodingTasks.Tests.Utilities;

[TestFixture]
public class UtilitiesTests
{
    [Test]
    public void LevenshteinDistance_CalculatesCorrectDistance()
    {
        LevenshteinDistance.Compute("kitten", "sitting").Should().Be(3);
        LevenshteinDistance.Compute("aunt", "ant").Should().Be(1);
        LevenshteinDistance.Compute("same", "same").Should().Be(0);
    }

    [Test]
    public void LevenshteinDistance_CalculatesSimilarity()
    {
        LevenshteinDistance.CalculateSimilarity("same", "same").Should().Be(1.0);
        LevenshteinDistance.CalculateSimilarity("a", "b").Should().Be(0.0);
    }

    [Test]
    public void Sha3Hasher_ComputesSha256Successfully()
    {
        var hash = Sha3Hasher.ComputeSha256("hello world");
        hash.Should().Be("b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9");
    }

    [Test]
    public void StringAggregator_JoinsNonEmptyStrings()
    {
        var result = StringAggregator.JoinNonEmpty(" ", "a", "", "b", "c");
        result.Should().Be("a b c");
    }

    [Test]
    public void StringAggregator_CountsOccurrences()
    {
        var items = new[] { "apple", "banana", "apple", "orange", "banana", "apple" };
        var counts = StringAggregator.CountOccurrences(items);

        counts["apple"].Should().Be(3);
        counts["banana"].Should().Be(2);
        counts["orange"].Should().Be(1);
    }
}
