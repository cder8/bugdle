import json
import os
from pathlib import Path
from zipfile import ZipFile

PUZZLE_DIR = Path("puzzles")
PUZZLE_DIR.mkdir(exist_ok=True)

puzzles = [
    {
        "id": 1,
        "title": "Sum List",
        "description": "The function should return the sum of all elements, but there’s a bug.",
        "snippet": "def sum_list(nums):\n    total = 0\n    for i in range(1, len(nums)):\n        total += nums[i]\n    return total",
        "fix_line": 2,
        "tests": [
            "assert sum_list([1,2,3]) == 6",
            "assert sum_list([10,20]) == 30",
            "assert sum_list([]) == 0"
        ],
        "difficulty": "Easy",
        "explanation": "The loop starts at 1 instead of 0, so the first element is skipped."
    },
    {
        "id": 2,
        "title": "Find Maximum",
        "description": "Fix the function to correctly find the maximum number in a list.",
        "snippet": "def find_max(nums):\n    max_val = nums[0]\n    for n in nums:\n        if n < max_val:\n            max_val = n\n    return max_val",
        "fix_line": 3,
        "tests": [
            "assert find_max([3, 5, 2, 9, 1]) == 9",
            "assert find_max([-1, -5, -3]) == -1",
            "assert find_max([7]) == 7"
        ],
        "difficulty": "Medium",
        "explanation": "The comparison is backwards: use `>` instead of `<` to find the max."
    },
    {
        "id": 3,
        "title": "First Even Number",
        "description": "Find the first even number in the list. Watch out for edge cases.",
        "snippet": "def first_even(nums):\n    for n in nums:\n        if n % 2 == 0:\n            return n\n    return nums[0]",
        "fix_line": 4,
        "tests": [
            "assert first_even([1,3,4,5]) == 4",
            "assert first_even([2,3,4]) == 2",
            "assert first_even([1,3,5]) == None"
        ],
        "difficulty": "Medium",
        "explanation": "The function returns nums[0] when no even numbers exist. It should return None."
    },
    {
        "id": 4,
        "title": "Reverse String",
        "description": "The function should reverse a string but has a subtle bug.",
        "snippet": "def reverse_string(s):\n    result = ''\n    for i in range(len(s)):\n        result += s[i]\n    return result",
        "fix_line": 3,
        "tests": [
            "assert reverse_string('abc') == 'cba'",
            "assert reverse_string('') == ''",
            "assert reverse_string('hello') == 'olleh'"
        ],
        "difficulty": "Easy",
        "explanation": "It should use `s[len(s)-1-i]` or `reversed(s)`; currently it returns the original string."
    },
    {
        "id": 5,
        "title": "Count Vowels",
        "description": "Count the number of vowels in a string, but there’s a bug.",
        "snippet": "def count_vowels(s):\n    vowels = 'aeiou'\n    count = 0\n    for c in s:\n        if c in vowels.upper():\n            count += 1\n    return count",
        "fix_line": 4,
        "tests": [
            "assert count_vowels('hello') == 2",
            "assert count_vowels('HELLO') == 2",
            "assert count_vowels('xyz') == 0"
        ],
        "difficulty": "Easy",
        "explanation": "The check is against `vowels.upper()` only, missing lowercase letters."
    },
    {
        "id": 6,
        "title": "Fibonacci",
        "description": "Return the nth Fibonacci number, but the implementation is off.",
        "snippet": "def fib(n):\n    if n == 0:\n        return 0\n    if n == 1:\n        return 1\n    return fib(n-1) + fib(n-2) + 1",
        "fix_line": 5,
        "tests": [
            "assert fib(0) == 0",
            "assert fib(1) == 1",
            "assert fib(5) == 5"
        ],
        "difficulty": "Medium",
        "explanation": "The `+1` is wrong; remove it to get the correct Fibonacci sequence."
    },
    {
        "id": 7,
        "title": "Palindrome Check",
        "description": "Check if a string is a palindrome, but there’s a subtle bug.",
        "snippet": "def is_palindrome(s):\n    return s == s[::-1].lower()",
        "fix_line": 1,
        "tests": [
            "assert is_palindrome('racecar') == True",
            "assert is_palindrome('Racecar') == True",
            "assert is_palindrome('hello') == False"
        ],
        "difficulty": "Easy",
        "explanation": "You’re only lowercasing the reversed string. You should lowercase both strings before comparing."
    },
    {
        "id": 8,
        "title": "Remove Duplicates",
        "description": "Remove duplicates from a list, but the result has a bug.",
        "snippet": "def remove_duplicates(lst):\n    res = []\n    for x in lst:\n        if x in res:\n            res.append(x)\n    return res",
        "fix_line": 3,
        "tests": [
            "assert remove_duplicates([1,2,2,3]) == [1,2,3]",
            "assert remove_duplicates([]) == []"
        ],
        "difficulty": "Medium",
        "explanation": "The condition is inverted. It should be `if x not in res`."
    },
    {
        "id": 9,
        "title": "Merge Dictionaries",
        "description": "Merge two dictionaries but the code doesn’t work correctly.",
        "snippet": "def merge_dicts(a, b):\n    for k in a:\n        b[k] = a[k]\n    return b",
        "fix_line": 3,
        "tests": [
            "assert merge_dicts({'x':1},{'y':2}) == {'x':1,'y':2}"
        ],
        "difficulty": "Medium",
        "explanation": "Iterating over `a` and assigning to `b` works, but it's safer to return a new dict or update `b` correctly."
    },
    {
        "id": 10,
        "title": "List Flatten",
        "description": "Flatten a list of lists, but the code has a bug.",
        "snippet": "def flatten(lst):\n    res = []\n    for l in lst:\n        res.append(l)\n    return res",
        "fix_line": 3,
        "tests": [
            "assert flatten([[1,2],[3,4]]) == [1,2,3,4]"
        ],
        "difficulty": "Medium",
        "explanation": "You need to extend the result, not append each sublist: `res.extend(l)`."
    },
    {
        "id": 11,
        "title": "Dictionary Keys",
        "description": "Return keys of a dictionary, but the code is wrong.",
        "snippet": "def dict_keys(d):\n    return d.values()",
        "fix_line": 1,
        "tests": [
            "assert dict_keys({'a':1,'b':2}) == ['a','b']"
        ],
        "difficulty": "Easy",
        "explanation": "Should return `d.keys()` instead of `d.values()`."
    },
    {
        "id": 12,
        "title": "String Repeat",
        "description": "Repeat a string n times, but it’s buggy.",
        "snippet": "def repeat(s,n):\n    return s*n-1",
        "fix_line": 1,
        "tests": [
            "assert repeat('a',3) == 'aaa'"
        ],
        "difficulty": "Easy",
        "explanation": "Subtracting 1 is wrong; just use `s*n`."
    },
    {
        "id": 13,
        "title": "Square Numbers",
        "description": "Return a list of squares but there’s a bug.",
        "snippet": "def squares(lst):\n    return [x*2 for x in lst]",
        "fix_line": 1,
        "tests": [
            "assert squares([1,2,3]) == [1,4,9]"
        ],
        "difficulty": "Medium",
        "explanation": "Should be `x**2` instead of `x*2`."
    },
    {
        "id": 14,
        "title": "Filter Negative",
        "description": "Remove negative numbers but the code is buggy.",
        "snippet": "def filter_neg(lst):\n    return [x for x in lst if x>0]",
        "fix_line": 1,
        "tests": [
            "assert filter_neg([-1,0,1,2]) == [0,1,2]"
        ],
        "difficulty": "Medium",
        "explanation": "The comparison misses zero; should be `x >= 0`."
    },
    {
        "id": 15,
        "title": "Capitalize Words",
        "description": "Capitalize words in a sentence but the code fails.",
        "snippet": "def capitalize_words(s):\n    return ' '.join([w.lower() for w in s.split()])",
        "fix_line": 1,
        "tests": [
            "assert capitalize_words('hello world') == 'Hello World'"
        ],
        "difficulty": "Easy",
        "explanation": "You are lowercasing instead of capitalizing: use `w.capitalize()`."
    },
    {
        "id": 16,
        "title": "Check Prime",
        "description": "Check if a number is prime but there’s a bug.",
        "snippet": "def is_prime(n):\n    for i in range(2,n):\n        if n % i == 0:\n            return False\n    return False",
        "fix_line": 4,
        "tests": [
            "assert is_prime(2) == True",
            "assert is_prime(4) == False"
        ],
        "difficulty": "Medium",
        "explanation": "Function always returns False at the end; it should return True if no divisors found."
    },
    {
        "id": 17,
        "title": "List Index",
        "description": "Return the index of an element, buggy code.",
        "snippet": "def find_index(lst, x):\n    for i, val in enumerate(lst):\n        if val == x:\n            return i+1\n    return -1",
        "fix_line": 3,
        "tests": [
            "assert find_index([10,20,30],20) == 1"
        ],
        "difficulty": "Easy",
        "explanation": "Should return `i`, not `i+1`."
    },
    {
        "id": 18,
        "title": "Power Function",
        "description": "Compute x to the power n, buggy implementation.",
        "snippet": "def power(x,n):\n    result = 0\n    for i in range(n):\n        result *= x\n    return result",
        "fix_line": 1,
        "tests": [
            "assert power(2,3) == 8"
        ],
        "difficulty": "Medium",
        "explanation": "Initialize `result=1` instead of 0; multiplication works correctly then."
    },
    {
        "id": 19,
        "title": "Merge Sorted Lists",
        "description": "Merge two sorted lists but code is buggy.",
        "snippet": "def merge(a,b):\n    return a+b",
        "fix_line": 1,
        "tests": [
            "assert merge([1,3,5],[2,4,6]) == [1,2,3,4,5,6]"
        ],
        "difficulty": "Medium",
        "explanation": "Simply adding lists does not maintain order; you need a merge algorithm."
    },
    {
        "id": 20,
        "title": "List Rotation",
        "description": "Rotate a list to the right by n, buggy code.",
        "snippet": "def rotate(lst,n):\n    return lst[n:] + lst[:n]",
        "fix_line": 1,
        "tests": [
            "assert rotate([1,2,3,4],1) == [4,1,2,3]"
        ],
        "difficulty": "Medium",
        "explanation": "The slicing is reversed; should use `lst[-n:] + lst[:-n]`."
    }
]



# Write individual JSON files
for p in puzzles:
    filename = f"{p['id']}.json"
    with open(PUZZLE_DIR / filename, "w") as f:
        json.dump(p, f, indent=4)

# Create a zip archive
with ZipFile("bugdle_puzzles.zip", "w") as zipf:
    for file in PUZZLE_DIR.glob("*.json"):
        zipf.write(file, arcname=file.name)

print("Generated JSON puzzles and created bugdle_puzzles.zip")
