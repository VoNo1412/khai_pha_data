import random
import math

def Kmean(customers, k):
    # Initialize random centroids
    centroids = []
    for i in range(k):
        centroid = [random.randint(0, 1), random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)]
        centroids.append(centroid)

    clusters = [[] for _ in range(k)]

    # Main K-means algorithm loop
    changed = True
    while changed:
        changed = False
        clusters = [[] for _ in range(k)]

        # Assign customers to the closest centroid
        for customer in customers:
            closest_centroid_index = 0
            min_distance = float('inf')
            customer_attributes = [0 if customer.get_gender() == "Male" else 1, customer.get_age(), customer.get_annual_income(), customer.get_spending_score()]

            for i, centroid in enumerate(centroids):
                distance = 0
                for j in range(len(centroid)):
                    distance += (customer_attributes[j] - centroid[j]) ** 2
                distance = math.sqrt(distance)
                if distance < min_distance:
                    min_distance = distance
                    closest_centroid_index = i

            clusters[closest_centroid_index].append(customer)

        # Update centroids
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

    # Print result
    print(f"{'CustomerID':<12} {'Gender':<6} {'Age':<4} {'Annual Income':<13} {'Spending Score':<14} {'Cluster':<8}")
    for i in range(k):
        for customer in clusters[i]:
            print(f"{customer.get_customer_id():<12} {customer.get_gender():<6} {customer.get_age():<4} {customer.get_annual_income():<13} {customer.get_spending_score():<14} {i + 1:<8}")