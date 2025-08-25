#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime

from coder.crew import Coder

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

# assignment = 'Write a python program to calculate the first 10,000 terms \
#     of this series, multiplying the total by 4: 1 - 1/3 + 1/5 - 1/7 + ...'

assignment = f"""Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target. \
            You may assume that each input would have exactly one solution, and you may not use the same element twice. \
            You can return the answer in any order. 
            Example 1:
                Input: nums = [2,7,11,15], target = 9
                Output: [0,1]
                Explanation: Because nums[0] + nums[1] == 9, 
                we return [0, 1]."""

def run():
    """
    Run the crew.
    """
    inputs = {
        'assignment': assignment,
    }
    
    result = Coder().crew().kickoff(inputs=inputs)
    print(result.raw)




