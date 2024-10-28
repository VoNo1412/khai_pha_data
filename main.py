import tkinter as tk
from tkinter import messagebox
import pandas as pd
import random
import math
import matplotlib.pyplot as plt

# Define Customer class
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
    # Step 0: Initialize random centroids
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

        # Step 1: Assign customers to the closest centroid
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

        # Step 2: Update centroids
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

    # Return the calculated counts and stats
    return cluster_counts, cluster_stats, clusters, centroids


# GUI class for the K-means application
class KMeansApp:
    def __init__(self, root):
        self.root = root
        self.root.title("K-means Clustering")
        self.root.geometry("800x500")

        # Input fields
        tk.Label(root, text="Number of Clusters (k):").pack()
        self.k_entry = tk.Entry(root)
        self.k_entry.pack()

        # Button to load data and run K-means
        self.run_button = tk.Button(root, text="Run K-means", command=self.run_kmeans)
        self.run_button.pack()

        # Results display area
        self.result_label = tk.Label(root, text="Results", font=("Arial", 12))
        self.result_label.pack()

        self.result_text = tk.Text(root, wrap='word', height=15, width=400)
        self.result_text.pack()

    def run_kmeans(self):
        # Validate k input
        try:
            k = int(self.k_entry.get())
            if k <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid positive integer for the number of clusters.")
            return

        # Load data and perform K-means clustering
        try:
            customers = self.load_customers('raw_customers.csv')
            cluster_counts, cluster_stats, clusters, centroids = Kmean(customers, k)
            self.display_results(cluster_counts, cluster_stats)
            self.plot_clusters(clusters, centroids)
        except FileNotFoundError:
            messagebox.showerror("File Not Found", "The file 'raw_customers.csv' was not found.")
    
    def load_customers(self, filename):
        customers = []
        with open(filename, mode='r') as file:
            next(file)  # Skip header
            for line in file:
                row = line.strip().split(",")
                customerId = int(row[0])
                gender = row[1]
                age = int(row[2])
                annualIncome = int(row[3])
                spendingScore = int(row[4])
                customer = Customer(customerId, gender, age, annualIncome, spendingScore)
                customers.append(customer)
        return customers

    def display_results(self, cluster_counts, cluster_stats):
        # Clear previous results
        self.result_text.delete("1.0", tk.END)

        # Display cluster counts
        result = "Cluster Counts:\n"
        for cluster_id, count in cluster_counts.items():
            result += f"Cluster {cluster_id + 1}: {count} customers\n"
        result += "\n"

        # Display statistics for each cluster
        result += "Cluster Statistics:\n"
        result += f"{'Cluster':<10}{'Total':<10}{'Avg Age':<10}{'Avg Income':<15}{'Avg Score':<12}{'Female Ratio':<15}\n"
        for i, stats in enumerate(cluster_stats):
            result += f"{i + 1:<10}{stats[0]:<10}{stats[1]:<10.2f}{stats[2]:<15.2f}{stats[3]:<12.2f}{stats[4]:<15}\n"
        
        self.result_text.insert(tk.END, result)

    def plot_clusters(self, clusters, centroids):
        # Create a scatter plot for the clusters
        plt.figure(figsize=(10, 6))

        colors = ['r', 'g', 'b', 'y', 'c', 'm']  # Extend colors as needed
        for i, cluster in enumerate(clusters):
            if cluster:  # Check if the cluster is not empty
                ages = [customer.get_age() for customer in cluster]
                incomes = [customer.get_annual_income() for customer in cluster]
                plt.scatter(ages, incomes, color=colors[i % len(colors)], label=f'Cluster {i + 1}')

        # Plot centroids
        centroid_ages = [centroid[1] for centroid in centroids]
        centroid_incomes = [centroid[2] for centroid in centroids]
        plt.scatter(centroid_ages, centroid_incomes, color='black', marker='X', s=200, label='Centroids')

        plt.title("K-means Clustering Results")
        plt.xlabel("Age")
        plt.ylabel("Annual Income")
        plt.legend()
        plt.grid()
        plt.show()

# Initialize the main application window
root = tk.Tk()
app = KMeansApp(root)
root.mainloop()
