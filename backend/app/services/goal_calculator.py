def calculate_monthly_savings(target_amount: float, months: int) -> float:
    """Basic monthly savings calculation: Target amount / months.
    
    Example: 500,000 / 24 months = 20,833.33 per month.
    """
    if months <= 0:
        raise ValueError("Number of months must be greater than zero.")
    if target_amount <= 0:
        raise ValueError("Target amount must be greater than zero.")
    
    return round(target_amount / months, 2)


def calculate_sip_with_returns(target_amount: float, months: int, annual_return_pct: float = 12.0) -> float:
    """Calculate required monthly SIP assuming an annualized expected compounding rate."""
    if annual_return_pct <= 0:
        return calculate_monthly_savings(target_amount, months)
    
    monthly_rate = (annual_return_pct / 100.0) / 12.0
    # Future Value of SIP formula: FV = P * [((1 + r)^n - 1) / r] * (1 + r)
    factor = (((1 + monthly_rate) ** months - 1) / monthly_rate) * (1 + monthly_rate)
    monthly_sip = target_amount / factor
    return round(monthly_sip, 2)
