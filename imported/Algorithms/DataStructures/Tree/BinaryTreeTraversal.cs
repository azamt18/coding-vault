using System;
using System.Collections.Generic;

namespace DataStructures.Tree;

public static class BinaryTreeTraversal
{
    public class TreeNode
    {
        public int Value;
        public TreeNode Left;
        public TreeNode Right;
    }
    
    // In in-order traversal, we visit the left child first, followed by the node itself, and then the right child. This can be visualized as “Left – Root – Right.”
    public static void InOrderTraversal(TreeNode root)
    {
        if (root == null)
            return;

        InOrderTraversal(root.Left);
        Console.Write(root.Value + " ");
        InOrderTraversal(root.Right);
    }
    
    // The idea is to push nodes onto the stack while traversing to the left, and then pop them and move to the right.
    public static void InOrderTraversalNonRecursive(TreeNode root)
    {
        if (root == null)
            return;

        Stack<TreeNode> stack = new Stack<TreeNode>();
        TreeNode current = root;

        while (current != null || stack.Count > 0)
        {
            while (current != null)
            {
                stack.Push(current);
                current = current.Left;
            }

            current = stack.Pop();
            Console.Write(current.Value + " ");
            current = current.Right;
        }
    }
}