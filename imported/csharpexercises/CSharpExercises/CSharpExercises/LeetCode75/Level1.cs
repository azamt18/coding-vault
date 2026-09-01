using System;

namespace CSharpExercises.LeetCode75
{
    public class Level1
    {
        static void Main(string[] args)
        {
            var nodes = new int[] { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 };

            for (var i = 0; i < nodes.Length; i++)
            {
                ListNode next = null;
                if (i + 1 <= nodes.Length)
                    next = new ListNode(nodes[i + 1]); 

                var node = new ListNode(nodes[i], next);
            }
            
            var head = new ListNode(nodes[0]);
            for (var i = 1; i <= nodes.Length - 1; i++)
            {
                ListNode nextNode = null;
                if (i + 1 <= nodes.Length)
                {
                    //nextNode = new ListNode(nodes[i], );
                }

                var node = new ListNode(nodes[i], nextNode);
            }

            //SplitListToParts()
            PivotIndex(new int[] { 1, 7, 3, 6, 5, 6 });
            RunningSum(new int[] { 1, 2, 3, 4 });

            Console.ReadLine();
        }

        /**
         * Definition for singly-linked list.
         * public class ListNode {
         *     public int val;
         *     public ListNode next;
         *     public ListNode(int val=0, ListNode next=null) {
         *         this.val = val;
         *         this.next = next;
         *     }
         * }
         */
        public class ListNode
        {
            public int value;
            public ListNode next;

            public ListNode(int value, ListNode next = null)
            {
                this.value = value;
                this.next = next;
            }
        }

        public static ListNode[] SplitListToParts(ListNode head, int k)
        {
            // get length
            int length = 0;
            ListNode current = head;
            if (current.next != null)
            {
                current = current.next;
                length += length + 1;
            }

            // subnode properties
            int width = length / k, remainder = length % k;
            
            ListNode[] result = new ListNode[k];
            
            // create result
            for (int i = 0; i < k; i++)
            {
                ListNode root = new ListNode(0);
                ListNode write = root;
                for (int j = 0; j < width + (i < remainder ? 1 : 0); ++j)
                {
                    write.next = new ListNode(current.value);
                    write = write.next;

                    if (current != null) 
                        current = current.next;
                }
                
                result[i] = head.next;
            }

            return result;
        }

        public static int PivotIndex(int[] nums)
        {
            int sum = 0, leftSum = 0, pivotIndex = -1;

            for (var i = 0; i < nums.Length; i++)
            {
                sum += nums[i];
            }

            for (var i = 0; i < nums.Length; i++)
            {
                if (leftSum == sum - leftSum - nums[i])
                {
                    return i;
                }

                leftSum += nums[i];
            }

            return pivotIndex;
        }

        public static int[] RunningSum(int[] nums)
        {
            int[] results = new int[nums.Length];
            int sum = nums[0];
            results[0] = sum;

            for (var i = 1; i <= nums.Length - 1; i++)
            {
                sum += nums[i];
                results[i] = sum;
            }

            return results;
        }
    }
}