def table_calc(balance,unit,open,type,percentage):
    total_units=round(balance/unit)
    prices=[]
    temp_price=open
    prices.append(temp_price)
    if type=='LONG':
        for x in range(total_units-1):
            
            temp_price=round(temp_price-((temp_price*percentage)/100),3)
            prices.append(temp_price)
    else:
        for x in range(total_units-1):
            
            temp_price=round(temp_price+((temp_price*percentage)/100),3)
            prices.append(temp_price)       

    return prices


def min_max_calc(type,min,max):
    change=0
    if type=='LONG':
        change=(min*100/max)-100
    else:
        change=(max*100/min)-100
    print(change)
    return change
