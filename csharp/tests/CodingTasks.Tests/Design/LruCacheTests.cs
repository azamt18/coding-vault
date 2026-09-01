using CodingTasks.Design.LruCache;
using FluentAssertions;
using NUnit.Framework;

namespace CodingTasks.Tests.Design;

[TestFixture]
public class LruCacheTests
{
    [Test]
    public void LruCache_GetAndPut_FollowsLruEvictionPolicy()
    {
        var cache = new LruCache<int, int>(2);

        cache.Put(1, 1);
        cache.Put(2, 2);

        cache.TryGet(1, out var val1).Should().BeTrue();
        val1.Should().Be(1);

        cache.Put(3, 3); // evicts key 2 (key 1 was recently accessed)

        cache.TryGet(2, out _).Should().BeFalse();
        cache.TryGet(3, out var val3).Should().BeTrue();
        val3.Should().Be(3);

        cache.Put(4, 4); // evicts key 1 (key 3 was recently accessed)

        cache.TryGet(1, out _).Should().BeFalse();
        cache.TryGet(3, out _).Should().BeTrue();
        cache.TryGet(4, out var val4).Should().BeTrue();
        val4.Should().Be(4);
    }
}
