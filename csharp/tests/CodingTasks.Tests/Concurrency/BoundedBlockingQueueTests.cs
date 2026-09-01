using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using CodingTasks.Concurrency.BoundedBlockingQueue;
using FluentAssertions;
using NUnit.Framework;

namespace CodingTasks.Tests.Concurrency;

[TestFixture]
public class BoundedBlockingQueueTests
{
    [Test]
    public async Task ProducerConsumer_MultipleThreads_ProcessesAllItemsSafely()
    {
        var queue = new BoundedBlockingQueue<int>(capacity: 5);
        const int totalItems = 100;
        var consumedItems = new List<int>();
        var lockObj = new object();

        var producer = Task.Run(async () =>
        {
            for (int i = 1; i <= totalItems; i++)
            {
                await queue.EnqueueAsync(i);
            }
        });

        var consumer = Task.Run(async () =>
        {
            for (int i = 0; i < totalItems; i++)
            {
                var val = await queue.DequeueAsync();
                lock (lockObj)
                {
                    consumedItems.Add(val);
                }
            }
        });

        await Task.WhenAll(producer, consumer);

        consumedItems.Should().HaveCount(totalItems);
        consumedItems.Should().Equal(Enumerable.Range(1, totalItems));
    }
}
