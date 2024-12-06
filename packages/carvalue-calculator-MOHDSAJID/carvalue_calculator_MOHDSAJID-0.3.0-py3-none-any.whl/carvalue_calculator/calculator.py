# src/carvalue_calculator/calculator.py
class CarValueCalculator:
    """Simple calculator for car valuations"""
    
    @staticmethod
    def calculate_market_value(base_price, year, mileage):
        """
        Calculate adjusted market value based on year and mileage
        
        Args:
            base_price (float): Original price of the car
            year (int): Year of manufacture
            mileage (int): Current mileage
            
        Returns:
            float: Adjusted market value
        """
        current_year = 2024
        age = current_year - year
        
        # Age adjustment (5% depreciation per year)
        age_adjustment = 1 - (age * 0.05)
        
        # Mileage adjustment (reduction by 0.01 for every 1000 miles)
        mileage_adjustment = 1 - ((mileage / 1000) * 0.01)
        
        # Calculate final value
        adjusted_value = base_price * max(age_adjustment, 0.3) * max(mileage_adjustment, 0.3)
        
        return round(max(adjusted_value, base_price * 0.1), 2)
    
    @staticmethod
    def calculate_monthly_cost(price, down_payment, interest_rate, months):
        """
        Calculate monthly payment for car financing
        
        Args:
            price (float): Car price
            down_payment (float): Down payment amount
            interest_rate (float): Annual interest rate (percentage)
            months (int): Loan term in months
            
        Returns:
            float: Monthly payment amount
        """
        loan_amount = price - down_payment
        monthly_rate = (interest_rate / 100) / 12
        
        if monthly_rate == 0:
            return round(loan_amount / months, 2)
            
        monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate)**months) / ((1 + monthly_rate)**months - 1)
        return round(monthly_payment, 2)