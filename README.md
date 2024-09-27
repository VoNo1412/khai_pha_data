py main.py

# Tại sao phải tạo cụm(cluster) ?
    - Một cluster tổng có thể chia thành nhiều cluster con
    - Phân cụm để xử lý những data lớn như triệu bản ghi chẳng hạn thay vì xử lý data nhỏ lẻ ta gom chúng thành cụm
    - Để gọm cụm ta gom những data tương đồng giống nhau khác với các bản ghi ở cụm khác
    - đặc trưng giống nhau ở đây được đo bằng khoảng cách
    - khoảng cách càng gần nhau thì nó càng tương đồng nhau
    - vd: Khoảng cách từ A đến B gần hơn so với A đến C => A và B tương đồng nhau => A,B được gọm lại thành 1 cluster


