def calculate_kpis(df):

    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    total_orders = df["Order ID"].nunique()
    total_customers = df["Customer Name"].nunique()

    avg_order_value = total_sales / total_orders
    profit_margin = (total_profit / total_sales) * 100

    kpis = {
        "Total Sales": total_sales,
        "Total Profit": total_profit,
        "Total Orders": total_orders,
        "Total Customers": total_customers,
        "Average Order Value": avg_order_value,
        "Profit Margin": profit_margin
    }

    return kpis