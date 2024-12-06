class DiscountsUtil:

    def __init__(self, discounts_interval, loyalty_interval):
        self.discounts_interval = sorted(discounts_interval)
        self.loyalty_interval = sorted(loyalty_interval)

    def apply_visit_discount(self, total_amount, total_purchases):
        discount_percentage = 0
        for min_visits, max_visits, discount_percent in self.discounts_interval:
            if min_visits <= total_purchases <= max_visits:
                discount_percentage = discount_percent
        discount = total_amount * (discount_percentage/100)
        amount_after_discount = total_amount - discount
        return amount_after_discount


    def getLoyaltyPoints(self, total_amount):
        loyalty_percentage = 0
        for min_amount, max_amount, loyalty_percent in self.loyalty_interval:
            if min_amount <= total_amount <= max_amount:
                loyalty_percentage = loyalty_percent
        loyalty_points = total_amount * (loyalty_percentage / 100)
        return loyalty_points

