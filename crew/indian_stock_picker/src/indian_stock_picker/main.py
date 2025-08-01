#!/usr/bin/env python
import warnings
import os
from datetime import datetime
from indian_stock_picker.crew import StockPicker

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    module=r"litellm\.llms\.custom_httpx\.async_client_cleanup"
)

def run():
    """
    Run the Indian StockPicker crew.
    """
    inputs = {
        'market': 'India',
        'current_date': str(datetime.now())
    }

    result = StockPicker().crew().kickoff(inputs=inputs)

    print("\n\n=== FINAL DECISION ===\n\n")
    print(result.raw)

if __name__ == "__main__":
    run()
