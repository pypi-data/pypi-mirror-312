class DiscountsUtil:

    def __init__(self, discounts_interval):
        self.discounts_interval = sorted(discounts_interval)

    def apply_visit_discount(self, total_amount, total_purchases):
        discount_percentage = 0
        for visits, discount_percent in self.discounts_interval:
            if total_purchases >= visits:
                discount_percentage = discount_percent
        discount = total_amount * (discount_percentage/100)
        amount_after_discount = total_amount - discount
        return amount_after_discount


    def apply_loyalty_points(self, total_amount, loyalty_points, conversion_rate):
        loyalty_discount_amount = loyalty_points * conversion_rate
        amount_after_discount = total_amount - loyalty_discount_amount
        if amount_after_discount < 0:
            amount_after_discount = total_amount
        return amount_after_discount

