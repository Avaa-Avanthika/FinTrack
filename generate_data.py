import random
import csv
from datetime import datetime, timedelta

payment_methods = ['Credit Card', 'Debit Card', 'UPI', 'Bank Transfer', 'Wallet']
merchants = ['Amazon', 'Flipkart', 'Zomato', 'Swiggy', 'Myntra', 'BigBasket', 'BookMyShow', 'Uber', 'Rapido']
categories = ['Electronics', 'Fashion', 'Food', 'Travel', 'Entertainment', 'Groceries']
loations = ['Kochi', 'Trivandrum', 'Kottayam', 'Kozhikode', 'Thrissur', 'Chennai', 'Bangalore', 'Mumbai', 'Delhi', 'Hyderabad']
statuses = ['Success', 'Failed', 'Pending']
customerTypes = ['Regular', 'Premium', 'New']
deviceTypes = ['Mobile', 'Desktop', 'Tablet']
start_date = datetime.now() - timedelta(days=90)
with open("transactions.csv", "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Transaction ID', 'Timestamp', 'Amount', 'Payment Method', 'Merchant', 'Category', 'Location', 'Status', 'Customer Type', 'Device Type'])

    for i in range(10000):
        transaction_ID = f"TXN{i + 1:05d}"
        timestamp = start_date + timedelta(days=random.randint(0, 89), minutes=random.randint(0, 1439))
        amount_type = random.choices(
        ["Small", "Medium", "Large"],
         weights=[70, 25, 5]
        )[0]
        if amount_type == "Small":
            amount = random.randint(200, 5000)
        elif amount_type == "Medium":
            amount = random.randint(5001, 20000)
        else:
            amount = random.randint(20001, 60000)
        if random.random() < 0.005:
            amount = random.randint(60001, 150000)
        payment_method = random.choice(payment_methods)
        merchant = random.choice(merchants)
        category = random.choice(categories)
        location = random.choice(loations)
        status = random.choices(statuses, weights=[94,5,1])[0]
        customerType = random.choice(customerTypes)
        deviceType = random.choice(deviceTypes)

        row = [transaction_ID, timestamp, amount, payment_method, merchant, category, location, status, customerType, deviceType]

        writer.writerow(row)
