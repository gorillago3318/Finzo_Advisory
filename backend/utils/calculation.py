# backend/utils/calculation.py

import math

def calculate_savings(loan_amount, loan_tenure_years, current_repayment, new_interest_rate_annual):
    """
    Calculates the savings from refinancing a loan.

    Parameters:
    - loan_amount (float): The original loan amount.
    - loan_tenure_years (int): The original loan tenure in years.
    - current_repayment (float): The current monthly repayment amount.
    - new_interest_rate_annual (float): The new annual interest rate after refinancing.

    Returns:
    dict: A dictionary containing the new monthly repayment, monthly saving, annual saving,
          total saving, and years saved.
    """
    r = new_interest_rate_annual / 100 / 12  # Monthly interest rate
    n = loan_tenure_years * 12  # Total number of payments

    if r == 0:
        new_repayment = loan_amount / n
    else:
        new_repayment = (loan_amount * r * (1 + r) ** n) / ((1 + r) ** n - 1)

    monthly_saving = current_repayment - new_repayment
    annual_saving = monthly_saving * 12
    total_saving = monthly_saving * n

    if current_repayment > 0:
        years_saved = total_saving / (current_repayment * 12)
    else:
        years_saved = 0.0

    return {
        'new_monthly_repayment': round(new_repayment, 2),
        'monthly_saving': round(monthly_saving, 2),
        'annual_saving': round(annual_saving, 2),
        'total_saving': round(total_saving, 2),
        'years_saved': years_saved
    }

def format_years_saved(years):
    """
    Formats the years saved into a readable string.

    Parameters:
    - years (float): The number of years saved.

    Returns:
    str: A formatted string representing years and months saved.
    """
    years_int = int(years)
    months = int(round((years - years_int) * 12))
    
    if years_int > 0 and months > 0:
        return f"{years_int} year(s) and {months} month(s)"
    elif years_int > 0:
        return f"{years_int} year(s)"
    elif months > 0:
        return f"{months} month(s)"
    else:
        return "0 months"
