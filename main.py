from customer import Customer
from kmean import Kmean

try:
    customers = []
    with open('raw_customers.csv', mode='r') as file:
        next(file)  # Skip header
        for line in file:
            row = line.strip().split(",")  # Remove any trailing newline characters and split by commas
            customerId = int(row[0])
            gender = row[1]
            age = int(row[2])
            annualIncome = int(row[3])  # Ensure it is an integer
            spendingScore = int(row[4])  # Ensure it is an integer

            customer = Customer(customerId, gender, age, annualIncome, spendingScore)
            customers.append(customer)

    # KMeans classification
    k = 3
    kmean = Kmean(customers, k)  # Create an instance of Kmean class

except FileNotFoundError:
    print("The file was not found. Please check the file path.")

print("Check size of customers: ", len(customers))
