import logging
import random
from datetime import date, datetime, timedelta

from app import db
from app.models import (
    Customer,
    Order,
    OrderItem,
    Product,
    StockItem,
    Supplier,
    Warehouse,
)

log = logging.getLogger(__name__)


def reset_business_data():
    """Delete existing business data so we can reseed the DB."""

    try:
        db.session.query(OrderItem).delete()
        db.session.query(Order).delete()
        db.session.query(StockItem).delete()
        db.session.query(Product).delete()
        db.session.query(Supplier).delete()
        db.session.query(Customer).delete()
        db.session.query(Warehouse).delete()
        db.session.commit()
    except Exception as e:  # pragma: no cover - utility script
        log.error("Error when cleaning business data: %s", e)
        db.session.rollback()


def create_suppliers():
    suppliers = [
        Supplier(
            name="TechnoServis s.r.o.",
            ico="12345678",
            dic="CZ12345678",
            email="info@technoservis.cz",
            phone="+420 111 111 111",
            address="Průmyslová 1",
            city="Praha",
            zip_code="19000",
        ),
        Supplier(
            name="KancelPlus a.s.",
            ico="87654321",
            dic="CZ87654321",
            email="obchod@kancelplus.cz",
            phone="+420 222 222 222",
            address="U Kanceláře 5",
            city="Brno",
            zip_code="60200",
        ),
    ]
    db.session.add_all(suppliers)
    db.session.commit()
    return suppliers


def create_products(suppliers):
    products = [
        Product(
            sku="NB-001",
            name="Notebook 15"",
            description="Kancelářský notebook 15"" s SSD diskem.",
            unit_price=18990,
            vat_rate=21.0,
            barcode="1234567890123",
            supplier=suppliers[0],
        ),
        Product(
            sku="MON-001",
            name="Monitor 24"",
            description="LED monitor 24"" vhodný pro kancelář.",
            unit_price=4990,
            vat_rate=21.0,
            barcode="2345678901234",
            supplier=suppliers[0],
        ),
        Product(
            sku="KP-001",
            name="Kancelářský papír A4",
            description="Bílý kancelářský papír A4, balík 500 listů.",
            unit_price=129,
            vat_rate=21.0,
            barcode="3456789012345",
            supplier=suppliers[1],
        ),
        Product(
            sku="PS-001",
            name="Psací souprava",
            description="Souprava kuličkových per, 10 ks.",
            unit_price=89,
            vat_rate=21.0,
            barcode="4567890123456",
            supplier=suppliers[1],
        ),
    ]
    db.session.add_all(products)
    db.session.commit()
    return products


def create_customers():
    customers = [
        Customer(
            name="Alfa Solutions s.r.o.",
            ico="25896314",
            dic="CZ25896314",
            email="info@alfasolutions.cz",
            phone="+420 333 333 333",
            billing_address="Firemní 10",
            shipping_address="Firemní 10",
            city="Ostrava",
            zip_code="70030",
        ),
        Customer(
            name="Město Podlesí",
            ico="00234567",
            dic="CZ00234567",
            email="podatelna@podlesi.cz",
            phone="+420 444 444 444",
            billing_address="Náměstí 1",
            shipping_address="Náměstí 1",
            city="Podlesí",
            zip_code="56301",
        ),
    ]
    db.session.add_all(customers)
    db.session.commit()
    return customers


def create_warehouses():
    warehouses = [
        Warehouse(
            name="Hlavní sklad Praha",
            code="PRG",
            address="Skladová 100",
            city="Praha",
            zip_code="19900",
        ),
        Warehouse(
            name="Regionální sklad Brno",
            code="BRN",
            address="Průmyslová 25",
            city="Brno",
            zip_code="61600",
        ),
    ]
    db.session.add_all(warehouses)
    db.session.commit()
    return warehouses


def create_stock(warehouses, products):
    stock_items = []
    for warehouse in warehouses:
        for product in products:
            quantity = random.randint(5, 50)
            min_quantity = random.randint(1, 5)
            stock_items.append(
                StockItem(
                    warehouse=warehouse,
                    product=product,
                    quantity=quantity,
                    min_quantity=min_quantity,
                    updated_at=datetime.utcnow(),
                )
            )
    db.session.add_all(stock_items)
    db.session.commit()
    return stock_items


def create_orders(customers, products):
    orders = []
    order_items_all = []

    for i in range(3):
        customer = random.choice(customers)
        created_at = datetime.utcnow() - timedelta(days=random.randint(0, 30))
        due_date = date.today() + timedelta(days=14)
        order_number = f"ORD-{datetime.utcnow():%Y%m%d}-{i+1:03d}"

        order = Order(
            order_number=order_number,
            customer=customer,
            created_at=created_at,
            due_date=due_date,
            status=random.choice(["new", "confirmed", "shipped"]),
            currency="CZK",
        )
        db.session.add(order)
        db.session.flush()  # ensure order.id

        total = 0
        for _ in range(random.randint(1, 4)):
            product = random.choice(products)
            qty = random.randint(1, 10)
            unit_price = product.unit_price
            vat_rate = product.vat_rate
            line_total = qty * float(unit_price)

            item = OrderItem(
                order=order,
                product=product,
                quantity=qty,
                unit_price=unit_price,
                vat_rate=vat_rate,
                total_line=line_total,
            )
            db.session.add(item)
            order_items_all.append(item)
            total += line_total

        order.total_amount = total
        orders.append(order)

    db.session.commit()
    return orders, order_items_all


def main():  # pragma: no cover - utility script
    logging.basicConfig(level=logging.INFO)
    log.info("Resetting business data...")
    reset_business_data()

    log.info("Creating suppliers...")
    suppliers = create_suppliers()

    log.info("Creating products...")
    products = create_products(suppliers)

    log.info("Creating customers...")
    customers = create_customers()

    log.info("Creating warehouses...")
    warehouses = create_warehouses()

    log.info("Creating stock items...")
    create_stock(warehouses, products)

    log.info("Creating orders...")
    create_orders(customers, products)

    log.info("Test data successfully created.")


if __name__ == "__main__":  # pragma: no cover
    main()

