import random
import math
import pandas as pd

class Customer:
    def __init__(self, customer_id, gender, age, annual_income, spending_score):
        self.customer_id = customer_id
        self.gender = gender
        self.age = age
        self.annual_income = annual_income
        self.spending_score = spending_score

    def get_gender(self):
        return self.gender

    def get_age(self):
        return self.age

    def get_annual_income(self):
        return self.annual_income

    def get_spending_score(self):
        return self.spending_score

    def get_customer_id(self):
        return self.customer_id

def Kmean(customers, k):
    #Step 0: Initialize random centroids
    centroids = []
    for i in range(k):
        centroid = [random.randint(0, 1), random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)]
        centroids.append(centroid)

    clusters = [[] for _ in range(k)]
    cluster_counts = {i: 0 for i in range(k)}  # Initialize counts for each cluster

    # Main K-means algorithm loop
    changed = True
    while changed:
        changed = False
        clusters = [[] for _ in range(k)]

        #Step 1: Assign customers to the closest centroid
        for customer in customers:
            closest_centroid_index = 0
            min_distance = float('inf')
            customer_attributes = [
                0 if customer.get_gender() == "Male" else 1, 
                customer.get_age(), 
                customer.get_annual_income(), 
                customer.get_spending_score()
            ]

            for i, centroid in enumerate(centroids):
                distance = 0
                for j in range(len(centroid)):
                    distance += (customer_attributes[j] - centroid[j]) ** 2
                distance = math.sqrt(distance)
                if distance < min_distance:
                    min_distance = distance
                    closest_centroid_index = i

            clusters[closest_centroid_index].append(customer)

        #Step 2: Update centroids
        for i in range(k):
            cluster = clusters[i]
            if cluster:
                new_centroid = [0] * 4
                for customer in cluster:
                    new_centroid[0] += 0 if customer.get_gender() == "Male" else 1
                    new_centroid[1] += customer.get_age()
                    new_centroid[2] += customer.get_annual_income()
                    new_centroid[3] += customer.get_spending_score()

                new_centroid = [x / len(cluster) for x in new_centroid]

                if new_centroid != centroids[i]:
                    centroids[i] = new_centroid
                    changed = True

    # Count customers in each cluster
    for i in range(k):
        cluster_counts[i] = len(clusters[i])

    # Print result
    print(f"{'CustomerID':<12} {'Gender':<6} {'Age':<4} {'Annual Income':<13} {'Spending Score':<14} {'Cluster':<8}")
    for i in range(k):
        for customer in clusters[i]:
            print(f"{customer.get_customer_id():<12} {customer.get_gender():<6} {customer.get_age():<4} {customer.get_annual_income():<13} {customer.get_spending_score():<14} {i + 1:<8}")

    # Print the cluster counts
    print("\nCluster counts:")
    for i in range(k):
        print(f"Cluster {i + 1}: {cluster_counts[i]} customers")

 # Calculate statistics for each cluster
    cluster_stats = []
    for i in range(k):
        cluster = clusters[i]
        if cluster:
            total_files = len(cluster)
            avg_age = sum([customer.get_age() for customer in cluster]) / total_files
            avg_income = sum([customer.get_annual_income() for customer in cluster]) / total_files
            avg_spending_score = sum([customer.get_spending_score() for customer in cluster]) / total_files
            female_count = sum([1 for customer in cluster if customer.get_gender() == "Female"])
            female_ratio = (female_count / total_files) * 100
            cluster_stats.append([total_files, avg_age, avg_income, avg_spending_score, female_ratio])
    print("\n\n\n\n")
    # Convert statistics into a pandas DataFrame
    df = pd.DataFrame(cluster_stats, columns=["Total files", "Average age", "Average annual Income", "Average spending score", "Female ratio"])

    # Add cluster labels
    df.index = [f"Cluster {i+1}" for i in range(k)]

    # Format the 'Female ratio' column to display percentages
    df['Female ratio'] = df['Female ratio'].apply(lambda x: f"{x:.0f}%")

    # Print the table
    print(df)

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