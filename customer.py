# Định nghĩa lớp khách hàng
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

    def load_customers_from_csv(filename):
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