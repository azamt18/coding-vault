using CodingTasks.DataStructures.Tree;
using FluentAssertions;
using NUnit.Framework;

namespace CodingTasks.Tests.DataStructures;

[TestFixture]
public class BinaryTreeTraversalTests
{
    [Test]
    public void InOrder_TraversesCorrectly()
    {
        //       4
        //      / \
        //     2   5
        //    / \
        //   1   3
        var root = new TreeNode<int>(4,
            new TreeNode<int>(2, new TreeNode<int>(1), new TreeNode<int>(3)),
            new TreeNode<int>(5));

        var recursive = BinaryTreeTraversal.InOrder(root);
        var iterative = BinaryTreeTraversal.InOrderIterative(root);

        recursive.Should().Equal(1, 2, 3, 4, 5);
        iterative.Should().Equal(1, 2, 3, 4, 5);
    }

    [Test]
    public void InOrder_NullRoot_ReturnsEmpty()
    {
        BinaryTreeTraversal.InOrder<int>(null).Should().BeEmpty();
        BinaryTreeTraversal.InOrderIterative<int>(null).Should().BeEmpty();
    }
}
