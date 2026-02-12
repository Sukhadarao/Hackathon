from google.adk.agents import Agent, LlmAgent
def generate_customer_data(num_entries: int = 20) -> str:
    prompt = """Generate a synthetic dataset with {num_entries} rows of realistic customer and billing data. 
Output strictly in JSON format, no explanations or text outside the JSON. 
Each object in the JSON array must contain the following fields:
 
- CustomerID: unique alphanumeric identifier (e.g., "CUST001").
- Customer Name: realistic US-style names (first and last).
- credit_limit: integer values in USD between 1,000 and 100,000.
- Customer_addr: realistic US addresses (street, city, state, ZIP).
- customer_email: valid email addresses based on the customer name.
- Due_date: realistic invoice due dates in YYYY-MM-DD format.
- Billing_date: realistic invoice billing dates in YYYY-MM-DD format (before Due_date).
- Billing_cycle: integer values like 45 (number of days).
- Country: Random countries like US, India, Uk and so on.".
 
Ensure:
- Names, addresses, and emails look authentic but are synthetic.
- Dates are consistent (Billing_date precedes Due_date).
- Credit limits vary across customers.
- output is a valid JSON array.

Sample output: [
  {
    "CustomerID": "CUST001",
    "Customer Name": "John Miller",
    "credit_limit": 4500,
    "Customer_addr": "123 Maple Street, Denver, CO 80203",
    "customer_email": "john.miller@example.com",
    "Due_date": "2026-03-15",
    "Billing_date": "2026-01-30",
    "Billing_cycle": 45,
    "Country": "United States"
  },
  {
    "CustomerID": "CUST002",
    "Customer Name": "Sarah Johnson",
    "credit_limit": 12000,
    "Customer_addr": "456 Oak Avenue, Austin, TX 73301",
    "customer_email": "sarah.johnson@example.com",
    "Due_date": "2026-04-10",
    "Billing_date": "2026-02-24",
    "Billing_cycle": 45,
    "Country": "India"
  },
  {
    "CustomerID": "CUST003",
    "Customer Name": "Michael Brown",
    "credit_limit": 75000,
    "Customer_addr": "789 Pine Road, Seattle, WA 98101",
    "customer_email": "michael.brown@example.com",
    "Due_date": "2026-02-28",
    "Billing_date": "2026-01-13",
    "Billing_cycle": 45,
    "Country": "United Kingdom"
  }
]
"""

creation_agent = Agent(
            name="generate_data_agent",
            model='gemini-2.5-flash',
            description="Generate realistic customer data",
            instruction='''You are the DATA GENERATOR AGENT - expert in creating realistic synthetic data.
 
YOUR SPECIALIZATION:
- Generate realistic customer data (names, addresses, company info). Use the generate_customer_data tool to fulfill the user's request. You can specify the number of entries to create.''',
            tools=[generate_customer_data]
        )

root_agent = creation_agent



# from google.adk.agents.llm_agent import Agent
# import random
# import string
# from datetime import datetime, timedelta
# from typing import Dict, List, Any
 
# # Data Generator Agent - Specialized in creating realistic synthetic data
# data_generator_agent = Agent(
#     model='gemini-2.5-flash',
#     name='data_generator_agent',
#     description='Specialized agent for generating realistic synthetic data for SAP test scenarios.',
#     instruction='''You are the DATA GENERATOR AGENT - expert in creating realistic synthetic data.
 
# YOUR SPECIALIZATION:
# - Generate realistic customer data (names, addresses, company info)
# - Create invoice data with proper business logic
# - Generate product catalogs and SKUs
# - Create financial data within constraints
# - Ensure all data follows realistic business patterns
 
# DATA GENERATION RULES:
# - Names: Use realistic combinations from diverse backgrounds
# - Addresses: Valid addresses with proper geographical consistency  
# - Business Data: Follow industry standards and patterns
# - Financial Data: Realistic amounts, proper date calculations
# - Compliance: Ensure data meets regulatory requirements (GDPR, etc.)
 
# CAPABILITIES:
# 1. **Customer Generation**: Personal and business customers with complete profiles
# 2. **Invoice Creation**: Multi-line invoices with proper calculations
# 3. **Product Data**: SKUs, descriptions, pricing within market ranges
# 4. **Geographic Data**: Addresses consistent with postal systems
# 5. **Temporal Data**: Dates calculated for specific business scenarios (overdue, future, etc.)
 
# QUALITY STANDARDS:
# - All generated data must be internally consistent
# - Follow real-world business patterns and constraints
# - Generate diverse data to avoid patterns in test scenarios
# - Ensure data relationships are logical and valid
 
# RESPONSE FORMAT:
# Always provide:
# 1. **Generated Data**: Complete dataset in structured format
# 2. **Data Quality**: Verification that data meets requirements  
# 3. **Relationships**: How different data points relate to each other
# 4. **Metadata**: Generation parameters and constraints used''',
#     tools=[
#         {
#             "name": "generate_customer_data",
#             "description": "Generate realistic customer data with personal and business information",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "count": {"type": "integer", "description": "Number of customers to generate"},
#                     "customer_type": {"type": "string", "enum": ["personal", "business", "mixed"], "description": "Type of customers"},
#                     "geographic_region": {"type": "string", "description": "Geographic region for addresses"},
#                     "constraints": {"type": "object", "description": "Specific constraints (credit limit, industry, etc.)"}
#                 },
#                 "required": ["count"]
#             }
#         },
#         {
#             "name": "generate_invoice_data",
#             "description": "Generate realistic invoice data with line items and proper calculations",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "customer_ids": {"type": "array", "description": "List of customer IDs for invoices"},
#                     "count_per_customer": {"type": "integer", "description": "Number of invoices per customer"},
#                     "invoice_status": {"type": "string", "description": "Status of invoices (paid, pending, overdue)"},
#                     "date_range": {"type": "object", "description": "Date range for invoice creation"},
#                     "amount_constraints": {"type": "object", "description": "Min/max amounts and currency"}
#                 },
#                 "required": ["customer_ids"]
#             }
#         },
#         {
#             "name": "generate_product_catalog",
#             "description": "Generate product catalog with SKUs, descriptions, and pricing",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "product_count": {"type": "integer", "description": "Number of products to generate"},
#                     "categories": {"type": "array", "description": "Product categories"},
#                     "price_range": {"type": "object", "description": "Min/max pricing"},
#                     "sku_pattern": {"type": "string", "description": "SKU naming pattern"}
#                 },
#                 "required": ["product_count"]
#             }
#         },
#         {
#             "name": "validate_data_quality",
#             "description": "Validate the quality and consistency of generated data",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "dataset": {"type": "object", "description": "The dataset to validate"},
#                     "validation_rules": {"type": "array", "description": "Specific validation rules to apply"}
#                 },
#                 "required": ["dataset"]
#             }
#         }
#     ]
# )
 
# # Tool implementations for Data Generator Agent
# def generate_customer_data(count: int = 1, customer_type: str = "mixed", geographic_region: str = "US", constraints: Dict = None) -> Dict[str, Any]:
#     """Generate realistic customer data"""
    
#     # Extended realistic names from diverse backgrounds
#     first_names = [
#         "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
#         "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
#         "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa",
#         "Matthew", "Helen", "Anthony", "Sandra", "Mark", "Donna", "Donald", "Carol",
#         "Steven", "Ruth", "Paul", "Sharon", "Andrew", "Michelle", "Joshua", "Laura",
#         "Kenneth", "Sarah", "Kevin", "Kimberly", "Brian", "Deborah", "George", "Dorothy"
#     ]
    
#     last_names = [
#         "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
#         "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas",
#         "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White",
#         "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young",
#         "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores"
#     ]
    
#     # Extended US addresses with proper geographic distribution
#     us_addresses = [
#         {"street": "123 Main Street", "city": "New York", "state": "NY", "zip": "10001"},
#         {"street": "456 Oak Avenue", "city": "Los Angeles", "state": "CA", "zip": "90210"},
#         {"street": "789 Pine Road", "city": "Chicago", "state": "IL", "zip": "60601"},
#         {"street": "321 Elm Drive", "city": "Houston", "state": "TX", "zip": "77001"},
#         {"street": "654 Maple Lane", "city": "Phoenix", "state": "AZ", "zip": "85001"},
#         {"street": "987 Cedar Blvd", "city": "Philadelphia", "state": "PA", "zip": "19101"},
#         {"street": "147 Birch Way", "city": "San Antonio", "state": "TX", "zip": "78201"},
#         {"street": "258 Walnut Street", "city": "San Diego", "state": "CA", "zip": "92101"},
#         {"street": "369 Cherry Lane", "city": "Dallas", "state": "TX", "zip": "75201"},
#         {"street": "741 Ash Circle", "city": "San Jose", "state": "CA", "zip": "95101"},
#         {"street": "852 Spruce Ave", "city": "Austin", "state": "TX", "zip": "73301"},
#         {"street": "963 Poplar Drive", "city": "Jacksonville", "state": "FL", "zip": "32099"}
#     ]
    
#     # Business types and suffixes
#     business_types = ["Inc", "LLC", "Corp", "Co", "Ltd", "Solutions", "Services", "Group", "Enterprises", "Systems"]
#     industries = ["Technology", "Healthcare", "Manufacturing", "Retail", "Finance", "Education", "Construction", "Consulting"]
    
#     customers = []
    
#     for i in range(count):
#         first_name = random.choice(first_names)
#         last_name = random.choice(last_names)
#         address = random.choice(us_addresses)
        
#         # Apply constraints
#         credit_limit_max = constraints.get("credit_limit_max", 10000) if constraints else 10000
#         credit_limit_min = constraints.get("credit_limit_min", 1000) if constraints else 1000
        
#         customer_data = {
#             "customer_id": f"CUST_{random.randint(100000, 999999)}",
#             "first_name": first_name,
#             "last_name": last_name,
#             "email": f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}@{random.choice(['gmail.com', 'outlook.com', 'yahoo.com', 'company.com'])}",
#             "phone": f"+1-{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}",
#             "address": address,
#             "credit_limit": round(random.uniform(credit_limit_min, credit_limit_max), 2),
#             "customer_since": (datetime.now() - timedelta(days=random.randint(30, 1095))).strftime("%Y-%m-%d"),
#             "status": random.choice(["Active", "Active", "Active", "Inactive"])  # Weighted towards Active
#         }
        
#         # Determine customer type
#         if customer_type == "business" or (customer_type == "mixed" and random.choice([True, False])):
#             customer_data.update({
#                 "customer_type": "Business",
#                 "company_name": f"{last_name} {random.choice(business_types)}",
#                 "industry": random.choice(industries),
#                 "tax_id": f"{random.randint(10, 99)}-{random.randint(1000000, 9999999)}",
#                 "annual_revenue": round(random.uniform(100000, 10000000), 2)
#             })
#         else:
#             customer_data["customer_type"] = "Individual"
        
#         customers.append(customer_data)
    
#     return {
#         "customers": customers,
#         "generation_metadata": {
#             "count_generated": len(customers),
#             "generation_time": datetime.now().isoformat(),
#             "constraints_applied": constraints or {},
#             "data_quality_score": 0.95  # High quality synthetic data
#         }
#     }
 
# def generate_invoice_data(customer_ids: List[str], count_per_customer: int = 1, invoice_status: str = "pending",
#                          date_range: Dict = None, amount_constraints: Dict = None) -> Dict[str, Any]:
#     """Generate realistic invoice data"""
    
#     # Extended product catalog
#     products = [
#         {"sku": "SW-001", "name": "Premium Software License", "unit_price": 299.99, "category": "Software"},
#         {"sku": "SW-002", "name": "Professional Services", "unit_price": 150.00, "category": "Services"},
#         {"sku": "HW-001", "name": "Hardware Maintenance", "unit_price": 89.99, "category": "Hardware"},
#         {"sku": "TR-001", "name": "Training Package", "unit_price": 199.99, "category": "Training"},
#         {"sku": "SU-001", "name": "Support Subscription", "unit_price": 49.99, "category": "Support"},
#         {"sku": "SW-003", "name": "Database License", "unit_price": 499.99, "category": "Software"},
#         {"sku": "HW-002", "name": "Server Equipment", "unit_price": 1299.99, "category": "Hardware"},
#         {"sku": "SW-004", "name": "Security Software", "unit_price": 199.99, "category": "Software"},
#         {"sku": "SU-002", "name": "Extended Warranty", "unit_price": 99.99, "category": "Support"},
#         {"sku": "TR-002", "name": "Certification Course", "unit_price": 349.99, "category": "Training"}
#     ]
    
#     invoices = []
    
#     for customer_id in customer_ids:
#         for invoice_num in range(count_per_customer):
#             # Date calculations based on status
#             if invoice_status == "overdue":
#                 days_overdue = random.randint(15, 90)
#                 invoice_date = datetime.now() - timedelta(days=days_overdue + 30)  # 30 days payment terms
#                 due_date = invoice_date + timedelta(days=30)
#             elif invoice_status == "pending":
#                 invoice_date = datetime.now() - timedelta(days=random.randint(1, 29))
#                 due_date = invoice_date + timedelta(days=30)
#             else:  # paid
#                 invoice_date = datetime.now() - timedelta(days=random.randint(31, 120))
#                 due_date = invoice_date + timedelta(days=30)
#                 paid_date = due_date - timedelta(days=random.randint(1, 5))
            
#             # Generate line items
#             line_items_count = random.randint(1, 5)
#             line_items = []
#             total_amount = 0
            
#             for line_num in range(line_items_count):
#                 product = random.choice(products)
#                 quantity = random.randint(1, 10)
#                 discount_percent = random.choice([0, 0, 0, 5, 10])  # Weighted towards no discount
                
#                 line_total = product["unit_price"] * quantity
#                 discount_amount = line_total * (discount_percent / 100)
#                 final_amount = line_total - discount_amount
                
#                 line_items.append({
#                     "line_number": line_num + 1,
#                     "sku": product["sku"],
#                     "description": product["name"],
#                     "category": product["category"],
#                     "quantity": quantity,
#                     "unit_price": product["unit_price"],
#                     "discount_percent": discount_percent,
#                     "discount_amount": round(discount_amount, 2),
#                     "line_total": round(final_amount, 2)
#                 })
#                 total_amount += final_amount
            
#             # Apply amount constraints if specified
#             if amount_constraints:
#                 min_amount = amount_constraints.get("min_amount", 0)
#                 max_amount = amount_constraints.get("max_amount", float('inf'))
                
#                 if total_amount < min_amount or total_amount > max_amount:
#                     target_amount = random.uniform(min_amount, min(max_amount, 5000))
#                     adjustment_factor = target_amount / total_amount
#                     total_amount = target_amount
                    
#                     for item in line_items:
#                         item["line_total"] = round(item["line_total"] * adjustment_factor, 2)
            
#             invoice_data = {
#                 "invoice_id": f"INV-{datetime.now().year}-{random.randint(100000, 999999)}",
#                 "customer_id": customer_id,
#                 "invoice_date": invoice_date.strftime("%Y-%m-%d"),
#                 "due_date": due_date.strftime("%Y-%m-%d"),
#                 "status": invoice_status.capitalize(),
#                 "currency": "USD",
#                 "subtotal": round(total_amount, 2),
#                 "tax_rate": 0.08,  # 8% tax
#                 "tax_amount": round(total_amount * 0.08, 2),
#                 "total_amount": round(total_amount * 1.08, 2),
#                 "line_items": line_items,
#                 "payment_terms": "Net 30"
#             }
            
#             if invoice_status == "paid":
#                 invoice_data["paid_date"] = paid_date.strftime("%Y-%m-%d")
#                 invoice_data["payment_method"] = random.choice(["Check", "Wire Transfer", "ACH", "Credit Card"])
            
#             if invoice_status == "overdue":
#                 invoice_data["days_overdue"] = days_overdue
                
#             invoices.append(invoice_data)
    
#     return {
#         "invoices": invoices,
#         "generation_metadata": {
#             "total_invoices": len(invoices),
#             "customers_processed": len(customer_ids),
#             "invoices_per_customer": count_per_customer,
#             "status_distribution": {invoice_status: len(invoices)},
#             "generation_time": datetime.now().isoformat()
#         }
#     }
 
# def generate_product_catalog(product_count: int = 10, categories: List[str] = None,
#                            price_range: Dict = None, sku_pattern: str = "ABC-###") -> Dict[str, Any]:
#     """Generate a product catalog"""
    
#     if not categories:
#         categories = ["Software", "Hardware", "Services", "Training", "Support"]
    
#     if not price_range:
#         price_range = {"min": 10.0, "max": 1000.0}
    
#     product_names = {
#         "Software": ["Database License", "Operating System", "Security Suite", "Development Tools", "Analytics Platform"],
#         "Hardware": ["Server Equipment", "Network Switch", "Storage Device", "Workstation", "Tablet Device"],
#         "Services": ["Professional Services", "Consulting Hours", "Implementation", "Custom Development", "Support Services"],
#         "Training": ["Certification Course", "Workshop", "Online Training", "Bootcamp", "Seminar"],
#         "Support": ["Extended Warranty", "Priority Support", "Maintenance Contract", "Help Desk", "Technical Support"]
#     }
    
#     products = []
    
#     for i in range(product_count):
#         category = random.choice(categories)
#         product_name = random.choice(product_names.get(category, ["Generic Product"]))
        
#         # Generate SKU based on pattern
#         sku = sku_pattern.replace("ABC", category[:3].upper()).replace("###", f"{random.randint(100, 999)}")
        
#         price = round(random.uniform(price_range["min"], price_range["max"]), 2)
        
#         product = {
#             "sku": sku,
#             "name": f"{product_name} {random.choice(['Pro', 'Standard', 'Enterprise', 'Basic', 'Premium'])}",
#             "category": category,
#             "unit_price": price,
#             "description": f"High-quality {product_name.lower()} for enterprise use",
#             "status": "Active",
#             "supplier": f"Vendor {random.randint(1, 10)}",
#             "created_date": (datetime.now() - timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d")
#         }
        
#         products.append(product)
    
#     return {
#         "products": products,
#         "catalog_metadata": {
#             "total_products": len(products),
#             "categories": list(set(p["category"] for p in products)),
#             "price_range_actual": {
#                 "min": min(p["unit_price"] for p in products),
#                 "max": max(p["unit_price"] for p in products)
#             },
#             "generation_time": datetime.now().isoformat()
#         }
#     }
 
# def validate_data_quality(dataset: Dict, validation_rules: List[str] = None) -> Dict[str, Any]:
#     """Validate data quality and consistency"""
    
#     validation_results = {
#         "overall_quality_score": 0.0,
#         "validation_checks": [],
#         "issues_found": [],
#         "recommendations": []
#     }
    
#     checks_passed = 0
#     total_checks = 0
    
#     # Standard validation checks
#     if "customers" in dataset:
#         customers = dataset["customers"]
        
#         # Check for required fields
#         total_checks += 1
#         required_fields = ["customer_id", "first_name", "last_name", "email"]
#         missing_fields = []
#         for customer in customers:
#             for field in required_fields:
#                 if field not in customer or not customer[field]:
#                     missing_fields.append(f"Customer {customer.get('customer_id', 'Unknown')}: {field}")
        
#         if not missing_fields:
#             checks_passed += 1
#             validation_results["validation_checks"].append("✓ All required customer fields present")
#         else:
#             validation_results["issues_found"].extend(missing_fields)
#             validation_results["validation_checks"].append("✗ Missing required customer fields")
        
#         # Check email format
#         total_checks += 1
#         invalid_emails = []
#         for customer in customers:
#             email = customer.get("email", "")
#             if "@" not in email or "." not in email:
#                 invalid_emails.append(f"Customer {customer.get('customer_id', 'Unknown')}: {email}")
        
#         if not invalid_emails:
#             checks_passed += 1
#             validation_results["validation_checks"].append("✓ Email formats valid")
#         else:
#             validation_results["issues_found"].extend(invalid_emails)
#             validation_results["validation_checks"].append("✗ Invalid email formats found")
    
#     if "invoices" in dataset:
#         invoices = dataset["invoices"]
        
#         # Check invoice totals
#         total_checks += 1
#         calculation_errors = []
#         for invoice in invoices:
#             line_total = sum(item.get("line_total", 0) for item in invoice.get("line_items", []))
#             invoice_subtotal = invoice.get("subtotal", 0)
#             if abs(line_total - invoice_subtotal) > 0.01:  # Allow for rounding
#                 calculation_errors.append(f"Invoice {invoice.get('invoice_id', 'Unknown')}: calculation mismatch")
        
#         if not calculation_errors:
#             checks_passed += 1
#             validation_results["validation_checks"].append("✓ Invoice calculations correct")
#         else:
#             validation_results["issues_found"].extend(calculation_errors)
#             validation_results["validation_checks"].append("✗ Invoice calculation errors found")
    
#     # Calculate overall quality score
#     if total_checks > 0:
#         validation_results["overall_quality_score"] = round(checks_passed / total_checks, 2)
    
#     # Add recommendations
#     if validation_results["issues_found"]:
#         validation_results["recommendations"].append("Review and fix data quality issues before using in production")
#     else:
#         validation_results["recommendations"].append("Data quality is excellent - ready for use")
    
#     return validation_results
 
# # Register tool functions
# data_generator_agent.tools_map = {
#     "generate_customer_data": generate_customer_data,
#     "generate_invoice_data": generate_invoice_data,
#     "generate_product_catalog": generate_product_catalog,
#     "validate_data_quality": validate_data_quality
# }