## Setup
* Create a `.env` file in the project directory with the following contents
```
OPENAI_API_KEY=<YOUR UNIQUE OPEN AI API KEY>
``` 

## Tips
* Enter `exit` to end the program
* I recommend restarting every so often to lower AI token usage. This is because it resets the chat history.
* You can remove problems from the `problems.json` file if you don't want them to show up.
* Whenever you get a question correct, it is progressively less likely to appear in the future.

## Example
```
Assistant > Ready to be quizzed on a random NeetCode/LeetCode problem? (Yes / No)

====================
User > yes

[AI is thinking...]
====================
Assistant > Great — here's your problem:

Binary Tree Postorder Traversal

Problem: Given the root of a binary tree, return the postorder traversal of its nodes' values (i.e., visit left subtree,
then right subtree, then the node).

Input: a binary tree root.
Output: an array/list of node values in postorder.

Example:
- Input: root = [1, null, 2, 3]
- Output: [3, 2, 1]

Task for you:
1) Describe, at a high level, how you would implement postorder traversal. Mention at least the standard recursive approach
and one iterative approach (briefly explain how the iterative version works).
2) For each approach you mention, give the time and space complexity (Big-O).

Give your answer when ready. After your explanation I’ll give feedback and adjust your knowledge level for this problem.

====================
User > This can be done in O(n) time and O(h) memory for both recursion and iteration. Recursion solution is trivial. For
iteration you can use two stacks that are always kept at the same size. One is for storing nodes that need to be revisted,
and the other is a stack of booleans for keeping track of which nodes' left side has already been explored. This lets you
jump back up the tree and know when youce already gone left at a node. You traverse as far left as possible, adding nodes
to the stack as you go, with a true. Then you jump back and readd the node but mark it false and go right, repeat. when
jumping back to a node marked false, you can add it to the answer and pop it for good.

[AI is thinking...]
====================
Assistant > Nice — good answer.

What you said is correct:
- Recursive postorder is straightforward (DFS: recurse left, recurse right, visit node). Time O(n), space O(h) for the recursion
stack (h = tree height; worst-case O(n) for a skewed tree).
- Your iterative idea (explicit stack + boolean visited flag) correctly simulates the recursion. That runs in O(n) time and uses
O(h) extra space for the stacks/flags (again worst-case O(n)). Your algorithm description of traversing left, pushing nodes with
a flag, then revisiting and switching to the right subtree is a valid approach.

Small notes / alternatives you can mention in interviews:
- Clarify worst-case vs. typical: say O(h) space, with h up to n in the worst case.
- Other common iterative approaches:
  - Use a single stack plus a "prev" pointer to track whether you came up from the left or right child.
  - Or use a modified preorder (root, right, left) pushing nodes in that order and then reverse the output to get left, right,
root — also O(n) time and O(h) space.
- If counting the output array, that adds O(n) space as well (but usually we exclude the required output).

I increased your knowledge level for this problem — nice work. Want another random problem? (Yes / No)

====================
User > exit
```
