import psycopg2

def fetch_customer(customer_id):
    conn = None
    cur = None
    
    try:
        conn = psycopg2.connect(
            host="34.63.63.212",
            database="customer_inventory",
            user="app-user",
            password="Bhavya@12$",
            port=5432
        )

        cur = conn.cursor()
        cur.execute("""
            SELECT customer_id, customer_name, credit_limit, customer_addr,
                   customer_email, billing_date, due_date, billing_cycle, country
            FROM customers_billing
            WHERE customer_id = %s
        """, (customer_id,))

        result = cur.fetchone()
        
        if result is None:
            print(f"Customer with ID {customer_id} not found.")
        
        return result
        
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# Test the function
if __name__ == "__main__":
    # Replace with an actual customer_id from your database
    customer_id = 'CUST019'
    
    print(f"Fetching customer with ID: {customer_id}")
    customer = fetch_customer(customer_id)
    
    if customer:
        print("\nCustomer Details:")
        print(f"ID: {customer[0]}")
        print(f"Name: {customer[1]}")
        print(f"Credit Limit: {customer[2]}")
        print(f"Address: {customer[3]}")
        print(f"Email: {customer[4]}")
        print(f"Billing Date: {customer[5]}")
        print(f"Due Date: {customer[6]}")
        print(f"Billing Cycle: {customer[7]}")
        print(f"Country: {customer[8]}")
