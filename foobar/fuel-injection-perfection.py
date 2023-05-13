"""
Fuel Injection Perfection=========================

Commander Lambda has asked for your help to refine the automatic quantum antimatter fuel injection system for the LAMBCHOP doomsday device. It's a great chance for you to get a closer look at the LAMBCHOP -- and maybe sneak in a bit of sabotage while you're at it -- so you took the job gladly. Quantum antimatter fuel comes in small pellets, which is convenient since the many moving parts of the LAMBCHOP each need to be fed fuel one pellet at a time. However, minions dump pellets in bulk into the fuel intake. You need to figure out the most efficient way to sort and shift the pellets down to a single pellet at a time. The fuel control mechanisms have three operations: 1) Add one fuel pellet2) Remove one fuel pellet3) Divide the entire group of fuel pellets by 2 (due to the destructive energy released when a quantum antimatter pellet is cut in half, the safety controls will only allow this to happen if there is an even number of pellets)Write a function called solution(n) which takes a positive integer as a string and returns the minimum number of operations needed to transform the number of pellets to 1. The fuel intake control panel can only display a number up to 309 digits long, so there won't ever be more pellets than you can express in that many digits.For example:solution(4) returns 2: 4 -> 2 -> 1solution(15) returns 5: 15 -> 16 -> 8 -> 4 -> 2 -> 1Quantum antimatter fuel comes in small pellets, which is convenient since the many moving parts of the LAMBCHOP each need to be fed fuel one pellet at a time. However, minions dump pellets in bulk into the fuel intake. You need to figure out the most efficient way to sort and shift the pellets down to a single pellet at a time. The fuel control mechanisms have three operations: 1) Add one fuel pellet2) Remove one fuel pellet3) Divide the entire group of fuel pellets by 2 (due to the destructive energy released when a quantum antimatter pellet is cut in half, the safety controls will only allow this to happen if there is an even number of pellets)Write a function called solution(n) which takes a positive integer as a string and returns the minimum number of operations needed to transform the number of pellets to 1. The fuel intake control panel can only display a number up to 309 digits long, so there won't ever be more pellets than you can express in that many digits.For example:solution(4) returns 2: 4 -> 2 -> 1solution(15) returns 5: 15 -> 16 -> 8 -> 4 -> 2 -> 1

Languages=========
To provide a Python solution, edit solution.py
To provide a Java solution, edit Solution.java

Test cases==========
Your code should pass the following test cases.Note that it may also be run against hidden test cases not shown here.

-- Python cases --
Input:solution.solution('15')Output:    5

Input:solution.solution('4')Output:    2
-- Java cases --
Input:Solution.solution('15')Output:    5

Input:Solution.solution('4')Output:    2
"""


# Let's solve this iteratively
# Found an algo that explained all odd numbers can be incremented or decremented by 1
# to be divisible by 4
# algo:
# 1. base case is n == 1
# 2. if the number is even, divide by 2
# 3. if the number is odd, find modulus of 4 and increment/decrement accordingly
#    e.g. if n % 4 = 3 then increment so it is divisible by 4
# 3 is a rogue case because it actually takes longer with the above algo than if you
# just subtract twice

def solution(n):
    num = int(n)
    count = 0
    while num != 1:
        if num % 2 == 0:
            num = num // 2
        elif num % 4 == 1 or num == 3:
            num -= 1
        else:
            num += 1
        count += 1
    return count

