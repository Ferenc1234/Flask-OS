import datetime

from flask_appbuilder import Model
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship


class Supplier(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True, nullable=False)
    ico = Column(String(20), nullable=True)
    dic = Column(String(20), nullable=True)
    email = Column(String(120), nullable=True)
    phone = Column(String(40), nullable=True)
    address = Column(String(255), nullable=True)
    city = Column(String(120), nullable=True)
    zip_code = Column(String(20), nullable=True)
    country = Column(String(120), nullable=False, default="Česká republika")

    products = relationship("Product", back_populates="supplier")

    def __repr__(self):
        return self.name or "Supplier"  # pragma: no cover


class Product(Model):
    id = Column(Integer, primary_key=True)
    sku = Column(String(64), unique=True, nullable=False)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    unit_price = Column(Numeric(12, 2), nullable=False, default=0)
    currency = Column(String(3), nullable=False, default="CZK")
    vat_rate = Column(Float, nullable=False, default=21.0)
    is_active = Column(Boolean, nullable=False, default=True)
    barcode = Column(String(64), nullable=True)

    supplier_id = Column(Integer, ForeignKey("supplier.id"), nullable=True)
    supplier = relationship("Supplier", back_populates="products")

    stock_items = relationship("StockItem", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")

    def __repr__(self):
        return f"{self.sku} - {self.name}"


class Customer(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    ico = Column(String(20), nullable=True)
    dic = Column(String(20), nullable=True)
    email = Column(String(120), nullable=True)
    phone = Column(String(40), nullable=True)
    billing_address = Column(String(255), nullable=True)
    shipping_address = Column(String(255), nullable=True)
    city = Column(String(120), nullable=True)
    zip_code = Column(String(20), nullable=True)
    country = Column(String(120), nullable=False, default="Česká republika")
    is_active = Column(Boolean, nullable=False, default=True)

    orders = relationship("Order", back_populates="customer")

    def __repr__(self):
        return self.name


class Warehouse(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True, nullable=False)
    code = Column(String(50), unique=True, nullable=True)
    address = Column(String(255), nullable=True)
    city = Column(String(120), nullable=True)
    zip_code = Column(String(20), nullable=True)
    country = Column(String(120), nullable=False, default="Česká republika")
    is_active = Column(Boolean, nullable=False, default=True)

    stock_items = relationship("StockItem", back_populates="warehouse")

    def __repr__(self):
        return self.name


class StockItem(Model):
    __tablename__ = "stock_item"
    __table_args__ = (
        UniqueConstraint("warehouse_id", "product_id", name="uq_stock_warehouse_product"),
    )

    id = Column(Integer, primary_key=True)
    warehouse_id = Column(Integer, ForeignKey("warehouse.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    min_quantity = Column(Integer, nullable=False, default=0)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    warehouse = relationship("Warehouse", back_populates="stock_items")
    product = relationship("Product", back_populates="stock_items")

    def __repr__(self):
        return f"{self.warehouse} / {self.product} ({self.quantity})"


class Order(Model):
    id = Column(Integer, primary_key=True)
    order_number = Column(String(64), unique=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    due_date = Column(Date, nullable=True)
    status = Column(String(32), nullable=False, default="new")
    total_amount = Column(Numeric(12, 2), nullable=False, default=0)
    currency = Column(String(3), nullable=False, default="CZK")
    note = Column(Text, nullable=True)

    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    def __repr__(self):
        return self.order_number


class OrderItem(Model):
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("order.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Numeric(12, 2), nullable=False, default=0)
    vat_rate = Column(Float, nullable=False, default=21.0)
    total_line = Column(Numeric(12, 2), nullable=False, default=0)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

    def __repr__(self):
        return f"{self.order} / {self.product}"


class BusinessPermission(Model):
    id = Column(Integer, primary_key=True)
    code = Column(String(64), unique=True, nullable=False)
    description = Column(String(255), nullable=True)

    def __repr__(self):
        return self.code




