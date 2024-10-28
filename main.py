import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from customer import Customer
from kmean import Kmean

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

        # Button to display the plot
        self.plot_button = tk.Button(root, text="Show Clusters", command=self.show_plot)
        self.plot_button.pack()

        # To store clusters and centroids for plotting later
        self.clusters = []
        self.centroids = []

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
            customers = Customer.load_customers_from_csv('raw_customers.csv')
            cluster_stats, self.clusters, self.centroids = Kmean(customers, k)
            self.display_results(cluster_stats)
        except FileNotFoundError:
            messagebox.showerror("File Not Found", "The file 'raw_customers.csv' was not found.")

    def display_results(self, cluster_stats):
        # Clear previous results
        self.result_text.delete("1.0", tk.END)

        # # Display cluster counts
        result = ""
    
        # Display statistics for each cluster
        result += "Cluster Statistics:\n"
        result += f"{'Cluster':<10}| {'Total':<10}| {'Avg Age':<10}| {'Avg Income':<15}| {'Avg Score':<12}| {'Female Ratio':<15}\n"
        result += "-" * 85 + "\n"  # Add a line separator
        for i, stats in enumerate(cluster_stats):
            result += f"{i + 1:<10}| {stats[0]:<10}| {stats[1]:<10.2f}| {stats[2]:<15.2f}| {stats[3]:<12.2f}| {stats[4]:<15}\n"
        
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

    def show_plot(self):
        if self.clusters and self.centroids:  # Check if clusters and centroids are available
            self.plot_clusters(self.clusters, self.centroids)
        else:
            messagebox.showwarning("No Data", "Please run K-means first to generate clusters.")

# Initialize the main application window
root = tk.Tk()
app = KMeansApp(root)
root.mainloop()
