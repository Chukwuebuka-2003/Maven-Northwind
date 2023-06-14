import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
    # Load the datasets
    order_details_df = pd.read_csv('order_details.csv', usecols=['orderID', 'productID', 'unitPrice', 'quantity', 'discount', 'revenue'])
    orders_df = pd.read_csv('orders.csv', usecols=['orderID', 'customerID', 'employeeID', 'orderDate', 'requiredDate', 'shippedDate', 'shipperID', 'freight'])
    customers_df = pd.read_csv('customers.csv', usecols=['customerID', 'companyName', 'contactName', 'contactTitle', 'city', 'country'], encoding='ISO-8859-1')
    products_df = pd.read_csv('products.csv', usecols=['productID', 'productName', 'quantityPerUnit', 'unitPrice', 'discontinued', 'categoryID'], encoding='ISO-8859-1')
    shippers_df = pd.read_csv('shippers.csv', usecols=['shipperID', 'companyName'])
    categories_df = pd.read_csv('categories.csv', usecols=['categoryID', 'categoryName', 'description'])
    employees_df = pd.read_csv('employees.csv', usecols=['employeeID', 'employeeName', 'title', 'city', 'country', 'reportsTo'])

    # Create Streamlit app
    st.title('Northwind Traders KPI Dashboard :chart_with_upwards_trend:')

    # Create tabs for each KPI
    tabs = ['Key Metrics', 'Sales Trends', 'Product Performance', 'Key Customers', 'Shipping Costs', 'Key Cities by Sales','Key Countries by Sales', 'Revenue by Category', 'Revenue by Company']
    selected_tab = st.sidebar.selectbox('Select a KPI', tabs)

    if selected_tab == 'Key Metrics':
        # Code for Key Metrics KPI
        calculate_key_metrics(order_details_df, orders_df, products_df, customers_df)

    elif selected_tab == 'Sales Trends':
        # Code for Sales Trends KPI
        calculate_sales_trends(order_details_df, orders_df)

    elif selected_tab == 'Product Performance':
        # Code for Product Performance KPI
        calculate_product_performance(order_details_df, products_df)

    elif selected_tab == 'Key Customers':
        # Code for Key Customers KPI
        calculate_key_customers(orders_df, customers_df, order_details_df)

    elif selected_tab == 'Shipping Costs':
        # Code for Shipping Costs KPI
        calculate_shipping_costs(orders_df, shippers_df)

    elif selected_tab == 'Key Cities by Sales':
        # Code for Key Cities by Sales KPI
        calculate_key_cities_by_sales(orders_df, customers_df, order_details_df)
        
        
    elif selected_tab == 'Key Countries by Sales':
        # Code for Key Cities by Sales KPI
        calculate_key_countries_by_sales(orders_df, customers_df, order_details_df)

    elif selected_tab == 'Revenue by Category':
        # Code for Revenue by Category KPI
        calculate_revenue_by_category(order_details_df, products_df, categories_df)

    elif selected_tab == 'Revenue by Company':
        # Code for Revenue by Company KPI
        calculate_revenue_by_company(order_details_df, orders_df, customers_df)

def calculate_key_metrics(order_details_df, orders_df, products_df, customers_df):
    # Calculate key metrics
    # Calculate revenue
    total_revenue = order_details_df['revenue'].sum()

    # Calculate total freight cost
    total_freight_cost = orders_df['freight'].sum()

    # Calculate total quantity
    total_quantity = order_details_df['quantity'].sum()

    # Get total number of orders
    total_orders = len(orders_df)

    # Get total number of products
    total_products = len(products_df)

    # Get total number of customers
    total_customers = len(customers_df)

    # Display cards
    st.subheader('Key Metrics')

    # Revenue card
    st.metric(label='Revenue', value=f'${total_revenue:.2f}')

    # Freight cost card
    st.metric(label='Freight Cost', value=f'${total_freight_cost:.2f}')

    # Quantity card
    st.metric(label='Quantity', value=total_quantity)

    # Orders card
    st.metric(label='Orders', value=total_orders)

    # Products card
    st.metric(label='Products', value=total_products)

    # Customers card
    st.metric(label='Customers', value=total_customers)
def calculate_sales_trends(order_details_df, orders_df):
    # Merge order_details_df and orders_df
    merged_df = pd.merge(order_details_df, orders_df, on='orderID')

    # Convert the 'orderDate' column to datetime data type with the correct format
    merged_df['orderDate'] = pd.to_datetime(merged_df['orderDate'], format='%Y-%m-%d')

    # Set the 'orderDate' column as the index
    merged_df.set_index('orderDate', inplace=True)

    # Calculate monthly revenue
    monthly_revenue = merged_df['revenue'].resample('M').sum()

    # Calculate quarterly revenue
    quarterly_revenue = merged_df['revenue'].resample('Q').sum()

    # Calculate yearly revenue
    yearly_revenue = merged_df['revenue'].resample('Y').sum()

    # Calculate sales growth rate
    sales_growth_rate = yearly_revenue.pct_change()

    # Create a line chart for monthly revenue
    st.subheader('Monthly Revenue')
    st.line_chart(monthly_revenue)

    # Create a bar chart for quarterly revenue
    st.subheader('Quarterly Revenue')
    st.bar_chart(quarterly_revenue)

    # Create a line chart for yearly revenue
    st.subheader('Yearly Revenue')
    st.line_chart(yearly_revenue)

    # Create a line chart for sales growth rate
    st.subheader('Sales Growth Rate')
    st.line_chart(sales_growth_rate)

def calculate_product_performance(order_details_df, products_df):
    # Code for Product Performance KPI
    # Calculate total units sold by product
    units_sold = order_details_df.groupby('productID')['quantity'].sum().reset_index()
    units_sold = pd.merge(units_sold, products_df[['productID', 'productName']], on='productID')

    # Calculate revenue by product
    revenue = pd.merge(order_details_df, products_df, on='productID')
    revenue['total_revenue'] = revenue['quantity'] * revenue['unitPrice_x']
    revenue_by_product = revenue.groupby('productID')['total_revenue'].sum().reset_index()
    revenue_by_product = pd.merge(revenue_by_product, products_df[['productID', 'productName']], on='productID')

    # Visualize product performance
    st.subheader('Total Units Sold by Product')
    st.bar_chart(units_sold.set_index('productName'))
    st.subheader('Revenue by Product')
    st.bar_chart(revenue_by_product.set_index('productName'))

    # Identify the best-selling products
    best_selling_products = revenue_by_product.nlargest(5, 'total_revenue')

    # Create a pie chart for best-selling products
    st.subheader('Best-Selling Products')
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.pie(best_selling_products['total_revenue'], labels=best_selling_products['productName'], autopct='%1.1f%%')
    ax.set_title('Best-Selling Products')
    st.pyplot(fig)

def calculate_key_customers(orders_df, customers_df, order_details_df):
    # Code for Key Customers KPI
    # Calculate total revenue per customer
    customer_revenue = pd.merge(orders_df, customers_df, on='customerID')
    customer_revenue = pd.merge(customer_revenue, order_details_df, on='orderID')  # Merge with order_details_df
    total_revenue_per_customer = customer_revenue.groupby('customerID')['revenue'].sum().reset_index()

    # Calculate customer retention rate
    customer_retention = orders_df.groupby('customerID')['orderID'].nunique().reset_index()
    customer_retention['retention_rate'] = customer_retention['orderID'] / customer_retention['orderID'].max()
    customer_retention = customer_retention.sort_values('retention_rate', ascending=False)


    # Identify key customers
    key_customers = total_revenue_per_customer[total_revenue_per_customer['revenue'] > 10000]
    key_customers = key_customers.sort_values('revenue', ascending=False)

    # Visualize key customer insights
    st.subheader('Total Revenue per Customer')
    st.bar_chart(total_revenue_per_customer.set_index('customerID'))

    # Display customer retention rate
    st.subheader('Customer Retention Rate')
    retention_rate_formatted = customer_retention.set_index('customerID')['retention_rate'].apply(lambda x: "{:.2%}".format(x))
    st.write(retention_rate_formatted)
    
    
    # Display key customers
    st.subheader('Key Customers')
    st.dataframe(key_customers)


def calculate_shipping_costs(orders_df, shippers_df):
    # Code for Shipping Costs KPI
    # Calculate average shipping cost per order
    avg_shipping_cost = orders_df.groupby('orderID')['freight'].mean().reset_index()

    # Calculate shipping cost by shipper
    shipping_cost_by_shipper = pd.merge(orders_df, shippers_df, on='shipperID')
    shipping_cost_by_shipper = shipping_cost_by_shipper.groupby('companyName')['freight'].sum().reset_index()

    # Visualize shipping cost insights
    st.subheader('Average Shipping Cost per Order')
    st.bar_chart(avg_shipping_cost.set_index('orderID'))
    st.subheader('Shipping Cost by Shipper')
    st.bar_chart(shipping_cost_by_shipper.set_index('companyName'))

def calculate_key_cities_by_sales(orders_df, customers_df, order_details_df):
    # Code for Key Cities by Sales KPI
    # Calculate total sales by city
    # Merge orders and customers DataFrames
    merged_df = pd.merge(orders_df, customers_df, on='customerID')
    merged_df = pd.merge(merged_df, order_details_df, on='orderID')

    # Calculate total sales by city
    sales_by_city = merged_df.groupby('city')['revenue'].sum().reset_index()

    # Identify key cities by sales
    key_cities = sales_by_city.nlargest(5, 'revenue')

    # Visualize key cities by sales
    st.subheader('Key Cities by Sales')
    st.bar_chart(key_cities.set_index('city'))

    # Analysis of key cities
    st.subheader('Key Cities Analysis')
    st.write("The top 5 cities with the highest sales are:")
    st.table(key_cities)
    st.write("These cities contribute significantly to the company's revenue and should be a focus for sales and marketing strategies.")
    
    
def calculate_key_countries_by_sales(orders_df, customers_df, order_details_df):
    # Code for Key Cities by Sales KPI
    # Calculate total sales by city
    # Merge orders and customers DataFrames
    merged_df = pd.merge(orders_df, customers_df, on='customerID')
    merged_df = pd.merge(merged_df, order_details_df, on='orderID')

    # Calculate total sales by city
    sales_by_city = merged_df.groupby('country')['revenue'].sum().reset_index()

    # Identify key cities by sales
    key_cities = sales_by_city.nlargest(5, 'revenue')

    # Visualize key cities by sales
    st.subheader('Key Cities by Sales')
    st.bar_chart(key_cities.set_index('country'))

    # Analysis of key cities
    st.subheader('Key Countries Analysis')
    st.write("The top 5 countries with the highest sales are:")
    st.table(key_cities)
    st.write("These countries contribute significantly to the company's revenue and should be a focus for sales and marketing strategies.")


def calculate_revenue_by_category(order_details_df, products_df, categories_df):
    # Merge the DataFrames
    merged_df = pd.merge(order_details_df, products_df, on='productID')
    merged_df = pd.merge(merged_df, categories_df, on='categoryID')

    # Calculate revenue by category
    revenue_by_category = merged_df.groupby('categoryName')['revenue'].sum().reset_index()
    revenue_by_category = revenue_by_category.sort_values('revenue', ascending=False)

    # Display revenue by category
    st.subheader('Revenue by Category')
    st.dataframe(revenue_by_category)    

def calculate_revenue_by_company(order_details_df, orders_df, customers_df):
    # Code for Revenue by Company KPI
    # Merge order_details, orders, and customers DataFrames
    merged_df = pd.merge(pd.merge(order_details_df, orders_df, on='orderID'), customers_df, on='customerID')

    # Calculate revenue by company
    revenue_by_company = merged_df.groupby('companyName')['revenue'].sum().reset_index()

    # Identify top revenue-generating companies
    top_companies = revenue_by_company.nlargest(5, 'revenue')

    # Visualize revenue by company
    st.subheader('Revenue by Company')
    st.bar_chart(revenue_by_company.set_index('companyName'))

    # Analysis of top revenue-generating companies
    st.subheader('Top Revenue-Generating Companies')
    st.write("The top 5 companies with the highest revenue are:")
    st.table(top_companies)
    st.write("These companies contribute significantly to the company's overall revenue and should be nurtured as key customers.")

# Run the app
if __name__ == '__main__':
    main()
