from datetime import timedelta
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean, VARCHAR
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(200), nullable=False)
    password = Column(String(1000), nullable=False)
    firstname = Column(String(200), nullable=False)
    lastname = Column(String(200), nullable=False)
    phone = Column(VARCHAR(10), nullable=False)
    email = Column(VARCHAR(100), nullable=False)
    location = Column(VARCHAR(200), nullable=False)
    role = Column(VARCHAR(10), nullable=False) # admin / user

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    orders = relationship('Order', back_populates='user')
    used_coupons = relationship('UsedCoupon', back_populates='user')


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    products = relationship("Product", back_populates="category")


class Brand(Base):
    __tablename__ = 'brands'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    products = relationship("Product", back_populates="brand")


class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    brand_id = Column(Integer, ForeignKey("brands.id"))
    name = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=False)
    cost_per_unit = Column(Float, nullable=False)
    image = Column(String(1000), nullable=False)
    stock_quantity = Column(Integer, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    category = relationship("Category", back_populates="products")
    brand = relationship("Brand", back_populates="products")
    ordered_products = relationship('OrderedProduct', back_populates="product")


class Coupon(Base):
    __tablename__ = 'coupons'

    id = Column(Integer, primary_key=True)
    code = Column(String(1000), nullable=False)
    type = Column(String(20), nullable=False)
    value = Column(Float, nullable=False)
    min_order_required = Column(Float, nullable=False)
    max_discount_applicable = Column(Float, nullable=False)
    stock_quantity = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False)
    limit_per_user = Column(Integer)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    used_coupons = relationship("UsedCoupon", back_populates='coupon')


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True) 
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user_firstname = Column(String(200), nullable=False)
    user_lastname = Column(String(200), nullable=False)
    user_phone = Column(VARCHAR(10), nullable=False)
    user_email = Column(VARCHAR(100), nullable=False)
    user_location = Column(VARCHAR(200), nullable=False)

    status = Column(String(20), nullable=False) # processing / cancled / completed
    applied_coupon = Column(Boolean, nullable=False)
    raw_total_cost = Column(Float, nullable=False)
    final_total_cost = Column(Float, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship('User', back_populates="orders")
    ordered_products = relationship('OrderedProduct', back_populates='order')
    used_coupon = relationship('UsedCoupon', back_populates='order')


class OrderedProduct(Base):
    __tablename__ = 'ordered_products'

    id = Column(Integer, primary_key=True) 
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    
    name = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=False)
    cost_per_unit = Column(Float, nullable=False)
    
    quantity = Column(Integer, nullable=False)
    total_cost = Column(Float, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    order = relationship('Order', back_populates="ordered_products")
    product = relationship('Product', back_populates="ordered_products")


class UsedCoupon(Base):
    __tablename__ = 'used_coupons'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    coupon_id = Column(Integer, ForeignKey('coupons.id'), nullable=False)
    
    code = Column(String(100), nullable=False)
    type = Column(String(20), nullable=False)
    value = Column(Float, nullable=False)
    applied_value = Column(Float, nullable=False)
    min_order_required = Column(Float, nullable=False)
    max_discount_applicable = Column(Float, nullable=False)
    limit_per_user = Column(Integer)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship('User', back_populates="used_coupons")
    coupon = relationship('Coupon', back_populates="used_coupons")
    order = relationship('Order', back_populates="used_coupon")


