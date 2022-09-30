from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def printout(head: Optional[ListNode]):
    arr = []
    current = head
    while current:
        # print(current)
        arr.append(current.val)
        current = current.next
    print(arr)


class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        current = head
        nodeCount = 0  # num of nodex
        while current:
            nodeCount += 1
            current = current.next
        targetIndex = nodeCount - n
        if nodeCount <= 1:
            return None
        current = head
        count = 0
        tmp = None
        while current:
            if targetIndex == 0:
                return head.next
            elif count+1 == targetIndex:
                current.next = current.next.next
                count += 1
            else:
                current = current.next
                count += 1
        return head


if __name__ == '__main__':
    # # [1, 2, 3, 4, 5]
    # target = 2
    # tail = ListNode(5)
    # four = ListNode(4, tail)
    # three = ListNode(3, four)
    # two = ListNode(2, three)
    # head = ListNode(1, two)

    target = 2
    two = ListNode(2)
    head = ListNode(1, two)

    runner = Solution()
    current = head
    printout(current)

    newHead = runner.removeNthFromEnd(head, target)

    printout(newHead)
