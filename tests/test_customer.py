import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from customer import Customer, Rate

def test_add_rate_increases_rate_count():
    customer = Customer("Test Co")
    rate = Rate("MEL", "SHA", "20GP", 800, 400, 200, 300, 35, 30, "COLLECT", "14 Days")

    assert len(customer.rates) == 0
    customer.add_rate(rate)
    assert len(customer.rates) == 1