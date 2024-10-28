import pandas as pd
import random
import math

def Kmean(customers, k):
    # Step 0: khởi tạo cluster và random centroids(tâm điểm) 
    clusters = []
    centroids = []

    for i in range(k):
        # thứ tự lần lượt random là gender, age, annual_income, spending_score
        centroid = [random.randint(0, 1), random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)]
        centroids.append(centroid)


    # Step 1: Hàm xử lý chính k-mean
    changed = True
    while changed:
        changed = False
        clusters = [[] for _ in range(k)]

        # Step 1.1: Gán khách hàng cho tâm điểm có vị trị gần nhất 
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
                    distance += (customer_attributes[j] - centroid[j]) ** 2 # bình phương x^2
                distance = math.sqrt(distance)
                if distance < min_distance:
                    min_distance = distance
                    closest_centroid_index = i

            clusters[closest_centroid_index].append(customer)

        # Step 1.2: Cập nhật cetroids(tâm điểm) dựa trên trung bình các thuộc tính của khách hàng 
        # cho đến khi centroid không thay đổi nữa là kết thúc thuật toán
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

    # Step 2: Đếm số khách hàng trong mỗi cluster
    cluster_counts = {i: 0 for i in range(k)}  # khởi tạo đếm số lượng của mỗi cluster(cụm)
    for i in range(k):
        cluster_counts[i] = len(clusters[i])

    # Step 3: tính toán số lượng thống kê và phân tích cho từng cluster
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


    return cluster_counts, cluster_stats, clusters, centroids
