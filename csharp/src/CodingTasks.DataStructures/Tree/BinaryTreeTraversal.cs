using System.Collections.Generic;

namespace CodingTasks.DataStructures.Tree;

public class TreeNode<T>
{
    public T Value { get; set; }
    public TreeNode<T>? Left { get; set; }
    public TreeNode<T>? Right { get; set; }

    public TreeNode(T value, TreeNode<T>? left = null, TreeNode<T>? right = null)
    {
        Value = value;
        Left = left;
        Right = right;
    }
}

public static class BinaryTreeTraversal
{
    public static List<T> InOrder<T>(TreeNode<T>? root)
    {
        var result = new List<T>();
        Traverse(root, result);
        return result;

        static void Traverse(TreeNode<T>? node, List<T> acc)
        {
            if (node == null) return;
            Traverse(node.Left, acc);
            acc.Add(node.Value);
            Traverse(node.Right, acc);
        }
    }

    public static List<T> InOrderIterative<T>(TreeNode<T>? root)
    {
        var result = new List<T>();
        if (root == null) return result;

        var stack = new Stack<TreeNode<T>>();
        var current = root;

        while (current != null || stack.Count > 0)
        {
            while (current != null)
            {
                stack.Push(current);
                current = current.Left;
            }

            current = stack.Pop();
            result.Add(current.Value);
            current = current.Right;
        }

        return result;
    }
}
