import pandas as pd
import matplotlib.pyplot as plt
data = pd.read_csv('transactions.csv')

total_transactions = len(data)
total_amount = data["Amount"].sum()
average_amount = data["Amount"].mean()
status_count = data["Status"].value_counts()

plt.figure(figsize=(6, 4))
plt.pie(status_count, labels=status_count.index, autopct="%1.1f%%")
plt.title("Transaction Status Distribution")
plt.show()
payment_method_count = data["Payment Method"].value_counts()
merchant_count = data["Merchant"].value_counts()
location_count = data["Location"].value_counts()
max_amount = data["Amount"].max()
unusual_transactions = data[data["Amount"] > 60000]

print("Number of unusual transactions: ", len(unusual_transactions))
print("Total Transactions: ", total_transactions)
print("Total Amount: ", total_amount)
print("Average Amount: ", average_amount)
print("Max Amount: ", max_amount)
print("Number of unusual transactions: ", len(unusual_transactions))


