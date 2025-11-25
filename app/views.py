from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from . import appbuilder, db
from .models import (
    BusinessPermission,
    Customer,
    Order,
    OrderItem,
    Product,
    StockItem,
    Supplier,
    Warehouse,
)


class SupplierModelView(ModelView):
    datamodel = SQLAInterface(Supplier)
    list_columns = ["name", "ico", "dic", "city", "country"]
    add_columns = [
        "name",
        "ico",
        "dic",
        "email",
        "phone",
        "address",
        "city",
        "zip_code",
        "country",
    ]
    edit_columns = add_columns

    label_columns = {
        "name": "Název",
        "ico": "IČO",
        "dic": "DIČ",
        "email": "E-mail",
        "phone": "Telefon",
        "address": "Adresa",
        "city": "Město",
        "zip_code": "PSČ",
        "country": "Stát",
    }


class ProductModelView(ModelView):
    datamodel = SQLAInterface(Product)
    list_columns = ["sku", "name", "unit_price", "currency", "vat_rate", "is_active"]
    add_columns = [
        "sku",
        "name",
        "description",
        "unit_price",
        "currency",
        "vat_rate",
        "barcode",
        "supplier",
        "is_active",
    ]
    edit_columns = add_columns

    label_columns = {
        "sku": "Kód",
        "name": "Název",
        "description": "Popis",
        "unit_price": "Cena za jednotku",
        "currency": "Měna",
        "vat_rate": "DPH %",
        "barcode": "Čárový kód",
        "supplier": "Dodavatel",
        "is_active": "Aktivní",
    }


class CustomerModelView(ModelView):
    datamodel = SQLAInterface(Customer)
    list_columns = ["name", "ico", "dic", "email", "phone", "city", "is_active"]
    add_columns = [
        "name",
        "ico",
        "dic",
        "email",
        "phone",
        "billing_address",
        "shipping_address",
        "city",
        "zip_code",
        "country",
        "is_active",
    ]
    edit_columns = add_columns

    label_columns = {
        "name": "Název",
        "ico": "IČO",
        "dic": "DIČ",
        "email": "E-mail",
        "phone": "Telefon",
        "billing_address": "Fakturační adresa",
        "shipping_address": "Doručovací adresa",
        "city": "Město",
        "zip_code": "PSČ",
        "country": "Stát",
        "is_active": "Aktivní",
    }


class WarehouseModelView(ModelView):
    datamodel = SQLAInterface(Warehouse)
    list_columns = ["name", "code", "city", "country", "is_active"]
    add_columns = ["name", "code", "address", "city", "zip_code", "country", "is_active"]
    edit_columns = add_columns

    label_columns = {
        "name": "Název skladu",
        "code": "Kód",
        "address": "Adresa",
        "city": "Město",
        "zip_code": "PSČ",
        "country": "Stát",
        "is_active": "Aktivní",
    }


class StockItemModelView(ModelView):
    datamodel = SQLAInterface(StockItem)
    list_columns = ["warehouse", "product", "quantity", "min_quantity", "updated_at"]
    add_columns = ["warehouse", "product", "quantity", "min_quantity"]
    edit_columns = add_columns

    label_columns = {
        "warehouse": "Sklad",
        "product": "Produkt",
        "quantity": "Množství",
        "min_quantity": "Minimální množství",
        "updated_at": "Aktualizováno",
    }


class OrderItemInlineView(ModelView):
    datamodel = SQLAInterface(OrderItem)
    list_columns = ["product", "quantity", "unit_price", "vat_rate", "total_line"]
    add_columns = ["product", "quantity", "unit_price", "vat_rate", "total_line"]
    edit_columns = add_columns

    label_columns = {
        "product": "Produkt",
        "quantity": "Množství",
        "unit_price": "Cena za jednotku",
        "vat_rate": "DPH %",
        "total_line": "Řádkem celkem",
    }


class OrderModelView(ModelView):
    datamodel = SQLAInterface(Order)
    related_views = [OrderItemInlineView]

    list_columns = ["order_number", "customer", "created_at", "status", "total_amount", "currency"]
    add_columns = [
        "order_number",
        "customer",
        "created_at",
        "due_date",
        "status",
        "total_amount",
        "currency",
        "note",
    ]
    edit_columns = add_columns

    label_columns = {
        "order_number": "Číslo objednávky",
        "customer": "Zákazník",
        "created_at": "Vytvořeno",
        "due_date": "Splatnost",
        "status": "Stav",
        "total_amount": "Celková částka",
        "currency": "Měna",
        "note": "Poznámka",
    }


class BusinessPermissionModelView(ModelView):
    datamodel = SQLAInterface(BusinessPermission)
    list_columns = ["code", "description"]
    add_columns = ["code", "description"]
    edit_columns = add_columns

    label_columns = {
        "code": "Kód oprávnění",
        "description": "Popis",
    }


db.create_all()

appbuilder.add_view(
    ProductModelView,
    "Produkty",
    icon="fa-cube",
    category="Katalog",
)

appbuilder.add_view(
    SupplierModelView,
    "Dodavatelé",
    icon="fa-truck",
    category="Katalog",
)

appbuilder.add_view(
    CustomerModelView,
    "Zákazníci",
    icon="fa-users",
    category="Obchod",
)

appbuilder.add_view(
    WarehouseModelView,
    "Sklady",
    icon="fa-archive",
    category="Logistika",
)

appbuilder.add_view(
    StockItemModelView,
    "Zásoby",
    icon="fa-cubes",
    category="Logistika",
)

appbuilder.add_view(
    OrderModelView,
    "Objednávky",
    icon="fa-file-text-o",
    category="Obchod",
)

appbuilder.add_view(
    BusinessPermissionModelView,
    "Oprávnění (obchod)",
    icon="fa-lock",
    category="Nastavení",
)

