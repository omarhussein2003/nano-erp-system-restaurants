# Simple Restaurant ERP (FastAPI)

An MVP ERP for restaurants with modules for POS, Inventory, CRM/Delivery, Reporting, and Admin. Built with FastAPI, SQLModel (SQLite), and Jinja2 templates. Simple dashboard UI with icons.

## Features (MVP)
- POS: open/close shift, cash-in/out, create order, split payments (stubs), receipt preview.
- Inventory: items, categories, suppliers, purchase orders, stock movements, recipes/BOM (basic).
- CRM/Delivery: customers, addresses, driver assignment flow (queued → out → delivered).
- Reporting: daily Z, sales by category, payment mix, inventory valuation (basic queries).
- Admin: menus, taxes, service charge, printers, tables/floors, roles & permissions (lightweight).

## Getting Started (Windows)
1. Create and activate a virtual environment:
   ```powershell
   py -3 -m venv .venv
   .\.venv\Scripts\activate
   ```
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Run the app:
   ```powershell
   uvicorn app.main:app --reload
   ```
4. Open http://127.0.0.1:8000 in your browser.

## Project Structure
```
app/
  main.py
  db.py
  models.py
  routers/
    pos.py
    inventory.py
    crm.py
    reporting.py
    admin.py
  templates/
    base.html
    index.html
    pos/index.html
    inventory/index.html
    crm/index.html
    reporting/index.html
    admin/index.html
  static/
    css/styles.css
    img/* (placeholders)
```

## Notes
- The database is a local SQLite file `erp.db`. On first run, tables are created and some demo data is seeded.
- Authentication is simplified for MVP (role field only). Add proper auth later.
- Reporting is first cut; refine as you add real data.

## Next Steps
- Flesh out POS flows (modifiers, split bills, refunds) with UI forms.
- Add barcode/PLU support for items.
- Add printable receipt templates and printer configuration.
- Implement real auth (OAuth2 + password) and per-branch permissions.
