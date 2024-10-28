# Lý do tại sao dùng K-MEAN mà không dùng thuật toán phân cụm khác như Hierarchical Clustering ?
    + Khả năng mở rộng với dữ liệu lớn:
    K-means có độ phức tạp tính toán thấp hơn nhiều so với Hierarchical Clustering, khiến nó thích hợp cho các tập dữ liệu lớn. Hierarchical Clustering có độ phức tạp tính toán cao hơn

    + Hiệu suất tính toán:
    K-means là một thuật toán lặp, chỉ cần vài bước tính toán chính (gán điểm vào cụm và cập nhật centroid), giúp nó chạy nhanh hơn so với quá trình phân cấp của Hierarchical Clustering.
    Hierarchical Clustering cần xây dựng một cây phân cấp đầy đủ, dẫn đến chi phí tính toán cao.
 
# Tại sao phải cập nhật lại centroid (tâm cụm) ?
    + Quá trình cập nhật này giúp cải thiện độ chính xác của cụm bằng cách đảm bảo rằng centroid luôn đại diện tốt nhất cho tất cả các điểm dữ liệu trong cụm, từ đó tạo ra các nhóm chặt chẽ hơn và nhất quán hơn.
    + Centroid mới này sẽ dịch chuyển đến vị trí gần hơn với trung tâm của các điểm dữ liệu đã gán vào cụm, giúp tinh chỉnh các cụm qua từng vòng lặp