from datetime import timedelta
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(200), nullable=False)
    password = Column(String(1000), nullable=False)
    fullname = Column(String(200), nullable=False)
    is_admin = Column(Boolean, nullable=False)
    is_active = Column(Boolean, nullable=False) 
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    orders = relationship('Order', back_populates='user')
    used_coupons = relationship('Coupon', back_populates='user')


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    products = relationship('Product', back_populates="category")


class Brand(Base):
    __tablename__ = 'brands'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    products = relationship('Product', back_populates="brand")


class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    brand_id = Column(Integer, ForeignKey('brands.id'))
    name = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=False)
    cost_per_unit = Column(Float, nullable=False)
    image = Column(String(1000), nullable=False)
    stock_quantity = Column(Integer, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    category = relationship('Category')
    brand = relationship('Brand')
    ordered_products = relationship('OrderedProduct', back_populates="product")


class Coupon(Base):
    __tablename__ = 'coupons'

    id = Column(Integer, primary_key=True)
    code = Column(String(1000), nullable=False)
    type = Column(Integer, nullable=False) # 1 = fixed, 2 = percentage, 3 = both
    fixed_amount = Column(Float, nullable=False)
    percentage_amount = Column(Float, nullable=False)
    minimum_order = Column(Float, nullable=False)
    maximum_discount = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    orders = relationship('Order', back_populates='coupon')
    used_coupons = relationship("UsedCoupon", back_populates='coupon')


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True) 
    status = Column(Integer, nullable=False) # 1 = pending, 2 = completed, 3 = cancelled
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    applied_coupon = Column(Boolean, nullable=False) 
    coupon_id = Column(Integer, ForeignKey('coupons.id'))
    raw_total_cost = Column(Float, nullable=False)
    discounted_amount = Column(Float, nullable=False)
    final_total_cost = Column(Float, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship('User')
    coupon = relationship('Coupon')
    used_coupon = relationship('UsedCoupon')
    ordered_products = relationship('OrderedProduct', back_populates='order')


class OrderedProduct(Base):
    __tablename__ = 'ordered_products'

    id = Column(Integer, primary_key=True) 
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_cost = Column(Float, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    order = relationship('Order')
    product = relationship('Product')


class UsedCoupon(Base):
    __tablename__ = 'used_coupons'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    coupon_id = Column(Integer, ForeignKey('coupons.id'), nullable=False)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    coupon = relationship('Coupon')
    user = relationship('User')
    order = relationship('Order')


class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(String(2000), nullable=False)
    image = Column(String(200))