from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from ..types import Invoice
from ..orchestrators import SAPOrchestrator
from ..config.logger import logger


class CustomerOverdueAnalysis:
    """Analysis result for a single customer's overdue invoices"""
    def __init__(self, customer_id: str, customer_name: str, invoices: List[Dict], 
                 total_amount: float, summary: str):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.invoices = invoices
        self.total_overdue_amount = total_amount
        self.summary = summary
        self.count = len(invoices)


class OverdueAnalysis:
    """Result of overdue invoice analysis across multiple customers"""
    def __init__(self, customer_analyses: List[CustomerOverdueAnalysis], 
                 all_invoices: List[Dict], total_amount: float, summary: str):
        self.customer_analyses = customer_analyses
        self.all_invoices = all_invoices
        self.total_overdue_amount = total_amount
        self.summary = summary
        self.total_count = len(all_invoices)
        self.customer_count = len(customer_analyses)


class OverdueCheckerAgent:
    """
    Agent for checking and analyzing overdue invoices across multiple customers.
    
    Integrates with the Synthetic Data Fabricator to:
    1. Fetch invoices from database for multiple customers
    2. Calculate overdue days based on billing_date, due_date, and billing_cycle
    3. Sort by severity (most overdue first) and group by customer
    4. Generate actionable reports per customer and consolidated
    5. Identify customers with highest risk (most overdue invoices)
    """
    
    def __init__(self, orchestrator: Optional[SAPOrchestrator] = None):
        """
        Initialize the overdue checker agent.
        
        Args:
            orchestrator: SAP orchestrator instance for fetching invoice data
        """
        self.orchestrator = orchestrator or SAPOrchestrator()
        logger.info("Overdue Checker Agent initialized for multi-customer analysis")
    
    def calculate_overdue_days(
        self, 
        billing_date: str, 
        due_date: str, 
        billing_cycle: Optional[int] = None
    ) -> Tuple[int, bool]:
        """
        Calculate overdue days for an invoice.
        
        Args:
            billing_date: Billing date in YYYY-MM-DD format
            due_date: Due date in YYYY-MM-DD format
            billing_cycle: Billing cycle in days (optional, for validation)
        
        Returns:
            Tuple of (overdue_days, is_overdue)
        """
        today = datetime.now().date()
        
        # Parse due date
        if isinstance(due_date, str):
            due_date_obj = datetime.strptime(due_date, '%Y-%m-%d').date()
        else:
            due_date_obj = due_date
        
        # Calculate overdue days
        overdue_days = (today - due_date_obj).days
        is_overdue = overdue_days > 0
        
        # Validate billing cycle if provided
        if billing_cycle and billing_date:
            billing_date_obj = datetime.strptime(billing_date, '%Y-%m-%d').date()
            expected_cycle = (due_date_obj - billing_date_obj).days
            
            if abs(expected_cycle - billing_cycle) > 5:  # Allow 5-day tolerance
                logger.warning(
                    f"Billing cycle mismatch: expected ~{billing_cycle} days, "
                    f"actual {expected_cycle} days"
                )
        
        return overdue_days, is_overdue
    
    def check_invoice(self, invoice) -> Optional[Dict]:
        """
        Check a single invoice for overdue status.
        
        Args:
            invoice: Invoice object or dict to check
        
        Returns:
            Dictionary with overdue details if overdue, None otherwise
        """
        # Handle both Invoice objects and dicts
        if isinstance(invoice, dict):
            billing_date = invoice.get('invoice_date') or invoice.get('invoiceDate')
            due_date = invoice.get('due_date') or invoice.get('dueDate')
            invoice_id = invoice.get('id')
            customer_id = invoice.get('customer_id') or invoice.get('customerId')
            amount = invoice.get('amount')
            status = invoice.get('status')
            invoice_number = invoice.get('invoice_number') or invoice.get('invoiceNumber')
            items = invoice.get('items', [])
        else:
            billing_date = invoice.invoice_date
            due_date = invoice.due_date
            invoice_id = invoice.id
            customer_id = invoice.customer_id
            amount = invoice.amount
            status = invoice.status
            invoice_number = invoice.invoice_number
            items = invoice.items
        
        # Calculate billing cycle from dates
        billing_date_obj = datetime.strptime(billing_date, '%Y-%m-%d').date()
        due_date_obj = datetime.strptime(due_date, '%Y-%m-%d').date()
        billing_cycle = (due_date_obj - billing_date_obj).days
        
        overdue_days, is_overdue = self.calculate_overdue_days(
            billing_date, 
            due_date, 
            billing_cycle
        )
        
        if not is_overdue:
            return None
        
        return {
            'id': invoice_id,
            'customer_id': customer_id,
            'invoice_number': invoice_number,
            'billing_date': billing_date,
            'due_date': due_date,
            'billing_cycle': billing_cycle,
            'amount': amount,
            'status': status,
            'overdue_days': overdue_days,
            'overdue_severity': self._calculate_severity(overdue_days),
            'items_count': len(items)
        }
    
    def _calculate_severity(self, overdue_days: int) -> str:
        """Calculate severity level based on overdue days (45-day billing cycle standard)"""
        if overdue_days >= 90:
            return "CRITICAL"
        elif overdue_days >= 60:
            return "HIGH"
        elif overdue_days >= 30:
            return "MEDIUM"
        else:
            return "LOW"
    
    def check_multiple_invoices(self, invoices: List[Invoice], group_by_customer: bool = True) -> OverdueAnalysis:
        """
        Check multiple invoices and sort by overdue days (descending).
        Can group results by customer for multi-customer analysis.
        
        Args:
            invoices: List of Invoice objects or dictionaries
            group_by_customer: If True, group results by customer ID
        
        Returns:
            OverdueAnalysis object with sorted overdue invoices
        """
        logger.info(f"Checking {len(invoices)} invoices for overdue status")
        
        overdue_list = []
        
        for invoice in invoices:
            overdue_info = self.check_invoice(invoice)
            if overdue_info:
                overdue_list.append(overdue_info)
        
        # Sort by overdue days (descending - most overdue first)
        overdue_list.sort(key=lambda x: x['overdue_days'], reverse=True)
        
        # Calculate total overdue amount
        total_amount = sum(inv['amount'] for inv in overdue_list)
        
        if group_by_customer:
            # Group by customer
            customer_groups = {}
            for inv in overdue_list:
                cust_id = inv['customer_id']
                if cust_id not in customer_groups:
                    customer_groups[cust_id] = []
                customer_groups[cust_id].append(inv)
            
            # Create customer analyses
            customer_analyses = []
            for cust_id, cust_invoices in customer_groups.items():
                cust_total = sum(inv['amount'] for inv in cust_invoices)
                cust_name = cust_invoices[0].get('customer_name', cust_id)
                cust_summary = self._generate_customer_summary(cust_id, cust_name, cust_invoices, cust_total)
                
                customer_analyses.append(CustomerOverdueAnalysis(
                    customer_id=cust_id,
                    customer_name=cust_name,
                    invoices=cust_invoices,
                    total_amount=cust_total,
                    summary=cust_summary
                ))
            
            # Sort customers by total overdue amount (highest risk first)
            customer_analyses.sort(key=lambda x: x.total_overdue_amount, reverse=True)
            
            # Generate consolidated summary
            summary = self._generate_multi_customer_summary(customer_analyses, overdue_list, total_amount)
            
            logger.info(f"Found {len(overdue_list)} overdue invoices across {len(customer_analyses)} customers totaling ${total_amount:,.2f}")
            
            return OverdueAnalysis(customer_analyses, overdue_list, total_amount, summary)
        else:
            # Single list without grouping
            summary = self._generate_summary(overdue_list, total_amount)
            
            logger.info(f"Found {len(overdue_list)} overdue invoices totaling ${total_amount:,.2f}")
            
            return OverdueAnalysis([], overdue_list, total_amount, summary)
    
    def _generate_summary(self, overdue_list: List[Dict], total_amount: float) -> str:
        """Generate a summary report of overdue invoices"""
        if not overdue_list:
            return "No overdue invoices found."
        
        severity_counts = {
            'CRITICAL': 0,
            'HIGH': 0,
            'MEDIUM': 0,
            'LOW': 0
        }
        
        for inv in overdue_list:
            severity_counts[inv['overdue_severity']] += 1
        
        summary = f"""
OVERDUE INVOICE ANALYSIS
========================
Total Overdue: {len(overdue_list)} invoices
Total Amount: ${total_amount:,.2f}

Severity Breakdown:
  CRITICAL (90+ days): {severity_counts['CRITICAL']} invoices
  HIGH (60-89 days):   {severity_counts['HIGH']} invoices
  MEDIUM (30-59 days): {severity_counts['MEDIUM']} invoices
  LOW (1-29 days):     {severity_counts['LOW']} invoices

Most Overdue:
  Invoice ID: {overdue_list[0]['id']}
  Days Overdue: {overdue_list[0]['overdue_days']} days
  Amount: ${overdue_list[0]['amount']:,.2f}
"""
        return summary
    
    def _generate_customer_summary(self, customer_id: str, customer_name: str, 
                                   invoices: List[Dict], total_amount: float) -> str:
        """Generate summary for a single customer's overdue invoices"""
        severity_counts = {
            'CRITICAL': 0,
            'HIGH': 0,
            'MEDIUM': 0,
            'LOW': 0
        }
        
        for inv in invoices:
            severity_counts[inv['overdue_severity']] += 1
        
        most_overdue = max(invoices, key=lambda x: x['overdue_days'])
        
        summary = f"""
Customer: {customer_name} (ID: {customer_id})
Overdue Invoices: {len(invoices)}
Total Overdue Amount: ${total_amount:,.2f}
Most Overdue: {most_overdue['overdue_days']} days
Severity: {severity_counts['CRITICAL']} CRITICAL, {severity_counts['HIGH']} HIGH, {severity_counts['MEDIUM']} MEDIUM, {severity_counts['LOW']} LOW
"""
        return summary
    
    def _generate_multi_customer_summary(self, customer_analyses: List[CustomerOverdueAnalysis],
                                        all_invoices: List[Dict], total_amount: float) -> str:
        """Generate consolidated summary for multiple customers"""
        if not customer_analyses:
            return "No overdue invoices found across customers."
        
        severity_counts = {
            'CRITICAL': 0,
            'HIGH': 0,
            'MEDIUM': 0,
            'LOW': 0
        }
        
        for inv in all_invoices:
            severity_counts[inv['overdue_severity']] += 1
        
        # Find customer with highest risk
        highest_risk_customer = max(customer_analyses, key=lambda x: x.total_overdue_amount)
        
        # Find most overdue invoice overall
        most_overdue = max(all_invoices, key=lambda x: x['overdue_days'])
        
        summary = f"""
MULTI-CUSTOMER OVERDUE ANALYSIS
================================
Total Customers with Overdue: {len(customer_analyses)}
Total Overdue Invoices: {len(all_invoices)}
Total Overdue Amount: ${total_amount:,.2f}
Average per Customer: ${total_amount/len(customer_analyses):,.2f}

Overall Severity Breakdown:
  CRITICAL (90+ days): {severity_counts['CRITICAL']} invoices
  HIGH (60-89 days):   {severity_counts['HIGH']} invoices
  MEDIUM (30-59 days): {severity_counts['MEDIUM']} invoices
  LOW (1-29 days):     {severity_counts['LOW']} invoices

Highest Risk Customer:
  Customer: {highest_risk_customer.customer_name}
  ID: {highest_risk_customer.customer_id}
  Overdue Amount: ${highest_risk_customer.total_overdue_amount:,.2f}
  Invoice Count: {highest_risk_customer.count}

Most Overdue Invoice (Overall):
  Invoice ID: {most_overdue['id']}
  Customer ID: {most_overdue['customer_id']}
  Days Overdue: {most_overdue['overdue_days']} days
  Amount: ${most_overdue['amount']:,.2f}

Top 5 Customers by Overdue Amount:
"""
        for idx, cust in enumerate(customer_analyses[:5], 1):
            summary += f"  {idx}. {cust.customer_name}: ${cust.total_overdue_amount:,.2f} ({cust.count} invoices)\n"
        
        return summary
    
    async def fetch_and_analyze_customer_invoices(
        self, 
        customer_id: str
    ) -> OverdueAnalysis:
        """
        Fetch all invoices for a customer and analyze overdue status.
        
        Args:
            customer_id: Customer ID to fetch invoices for
        
        Returns:
            OverdueAnalysis object
        """
        logger.info(f"Fetching invoices for customer {customer_id}")
        
        # This would integrate with the orchestrator to fetch invoices
        # For now, we'll use a placeholder that works with the mock system
        try:
            # In a real implementation, you'd fetch from SAP
            # invoices = await self.orchestrator.get_customer_invoices(customer_id)
            
            # For mock mode, we'll work with provided invoice objects
            logger.warning("Direct invoice fetching not implemented - use check_multiple_invoices() with invoice objects")
            return OverdueAnalysis([], 0.0, "No invoices fetched - integration pending")
        
        except Exception as e:
            logger.error(f"Failed to fetch invoices: {str(e)}")
            raise
    
    def format_report(self, analysis: OverdueAnalysis, detailed: bool = False, 
                     group_by_customer: bool = True) -> str:
        """
        Format overdue analysis into a readable report.
        
        Args:
            analysis: OverdueAnalysis object
            detailed: Whether to include detailed invoice list
            group_by_customer: Whether to group report by customer
        
        Returns:
            Formatted report string
        """
        report = analysis.summary
        
        if detailed:
            if group_by_customer and analysis.customer_analyses:
                report += "\n\nDETAILED REPORT BY CUSTOMER:\n"
                report += "=" * 80 + "\n"
                
                for cust_idx, cust_analysis in enumerate(analysis.customer_analyses, 1):
                    report += f"\n{'='*80}\n"
                    report += f"CUSTOMER #{cust_idx}: {cust_analysis.customer_name}\n"
                    report += f"Customer ID: {cust_analysis.customer_id}\n"
                    report += f"Total Overdue: ${cust_analysis.total_overdue_amount:,.2f} ({cust_analysis.count} invoices)\n"
                    report += f"{'='*80}\n"
                    
                    # Sort customer's invoices by overdue days
                    sorted_invoices = sorted(cust_analysis.invoices, 
                                           key=lambda x: x['overdue_days'], 
                                           reverse=True)
                    
                    for idx, inv in enumerate(sorted_invoices, 1):
                        report += f"\n  Invoice #{idx}:\n"
                        report += f"    ID: {inv['id']}\n"
                        report += f"    Amount: ${inv['amount']:,.2f}\n"
                        report += f"    Billing Date: {inv['billing_date']}\n"
                        report += f"    Due Date: {inv['due_date']}\n"
                        report += f"    Billing Cycle: {inv['billing_cycle']} days\n"
                        report += f"    Overdue Days: {inv['overdue_days']} days\n"
                        report += f"    Severity: {inv['overdue_severity']}\n"
                        report += f"    Status: {inv['status']}\n"
            else:
                # Single list format (original behavior)
                report += "\n\nDETAILED INVOICE LIST (sorted by overdue days):\n"
                report += "=" * 80 + "\n"
                
                for idx, inv in enumerate(analysis.all_invoices, 1):
                    report += f"\n{idx}. Invoice: {inv['id']}\n"
                    report += f"   Customer ID: {inv['customer_id']}\n"
                    report += f"   Amount: ${inv['amount']:,.2f}\n"
                    report += f"   Billing Date: {inv['billing_date']}\n"
                    report += f"   Due Date: {inv['due_date']}\n"
                    report += f"   Billing Cycle: {inv['billing_cycle']} days\n"
                    report += f"   Overdue Days: {inv['overdue_days']} days\n"
                    report += f"   Severity: {inv['overdue_severity']}\n"
                    report += f"   Status: {inv['status']}\n"
        
        return report
