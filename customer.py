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