#!/usr/bin/env python3
"""
Fix invoices - Create invoices for existing paid orders
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db import get_session
from app import models as m
from app.services import FinanceIntegrationService
from sqlmodel import select

def fix_invoices():
    """Create invoices for all paid orders that don't have invoices"""
    session = next(get_session())
    
    try:
        # Get all paid orders
        paid_orders = session.exec(
            select(m.Order).where(m.Order.status == m.OrderStatus.paid)
        ).all()
        
        print(f"Found {len(paid_orders)} paid orders")
        
        created_count = 0
        for order in paid_orders:
            # Check if invoice already exists
            existing_invoice = session.exec(
                select(m.Invoice).where(m.Invoice.order_id == order.id)
            ).first()
            
            if not existing_invoice:
                try:
                    print(f"Creating invoice for order {order.id} ({order.order_no})...")
                    FinanceIntegrationService.create_order_transaction(session, order)
                    created_count += 1
                    print(f"✅ Created invoice for order {order.id}")
                except Exception as e:
                    print(f"❌ Error creating invoice for order {order.id}: {e}")
            else:
                print(f"Invoice already exists for order {order.id}")
        
        print(f"\n🎉 Created {created_count} new invoices!")
        
        # Verify results
        total_invoices = session.exec(select(m.Invoice)).all()
        print(f"Total invoices in database: {len(total_invoices)}")
        
    except Exception as e:
        print(f"Error: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    fix_invoices()
