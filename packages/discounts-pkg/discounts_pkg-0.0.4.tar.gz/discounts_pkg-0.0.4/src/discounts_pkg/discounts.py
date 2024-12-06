class DiscountsUtil:
    discounts_interval = [
        {
            "min_visits": 5,
            "max_visits": 10,
            "discount_percent": 5
        },
        {
            "min_visits": 11,
            "max_visits": 15,
            "discount_percent": 10
        },
        {
            "min_visits": 16,
            "max_visits": 20,
            "discount_percent": 15
        }
    ]

    loyalty_interval = [
        {
            "min_amount": 100,
            "max_amount": 150,
            "loyalty_percent": 5
        },
        {
            "min_amount": 151,
            "max_amount": 200,
            "loyalty_percent": 10
        },
        {
            "min_amount": 201,
            "max_amount": 250,
            "loyalty_percent": 15
        },
        {
            "min_amount": 251,
            "max_amount": 300,
            "loyalty_percent": 20
        },
        {
            "min_amount": 301,
            "max_amount": 350,
            "loyalty_percent": 25
        },
        {
            "min_amount": 351,
            "max_amount": 400,
            "loyalty_percent": 30
        },
        {
            "min_amount": 401,
            "max_amount": 450,
            "loyalty_percent": 32
        },
        {
            "min_amount": 451,
            "max_amount": 500,
            "loyalty_percent": 35
        },
        {
            "min_amount": 501,
            "max_amount": 550,
            "loyalty_percent": 40
        }
    ]

    def apply_visit_discount(self, total_amount, total_purchases):
        discount_percentage = 0
        for discount in DiscountsUtil.discounts_interval:
            min_visits = discount["min_visits"]
            max_visits = discount["max_visits"]
            discount_percent = discount["discount_percent"]
            if min_visits <= total_purchases <= max_visits:
                discount_percentage = discount_percent
        discount = total_amount * (discount_percentage/100)
        amount_after_discount = total_amount - discount
        return amount_after_discount


    def getLoyaltyPoints(self, total_amount):
        loyalty_percentage = 0
        for loyalty in DiscountsUtil.loyalty_interval:
            min_amount = loyalty["min_amount"]
            max_amount = loyalty["max_amount"]
            loyalty_percent = loyalty["loyalty_percent"]
            if min_amount <= total_amount <= max_amount:
                loyalty_percentage = loyalty_percent
        loyalty_points = total_amount * (loyalty_percentage / 100)
        return loyalty_points

