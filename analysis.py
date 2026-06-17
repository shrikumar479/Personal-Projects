def analyse_stock(pe, debt_To_Equity):
    valuation = "Unknown"
    if pe:
        if pe < 15:
            valuation = "Undervalued"
        elif pe < 30:
            valuation = "Fairly Valued"
        else:
            valuation = "Overvalued"
            
    risk = "Unknown"
    if debt_To_Equity:
        if debt_To_Equity < 1:
            risk = "Low Leverage"
        else:
            risk = "High Leverage"
            
    return{
        "valuation": valuation,
        "risk_profile": risk
    }
    
    