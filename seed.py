from models import *
from services.auth import get_password_hash
from sqlalchemy.orm import Session
from database import create_session

session = create_session()

# ===== CATEGORIES ===== #
categories = [
    {
        "name": "education",
        "description": "Educational Products"
    },
    {
        "name": "entertainment",
        "description": "Entertainment Products"
    },
    {
        "name": "office",
        "description": "Products for Office uses"
    }
]

def seedCategories(session: Session):
    for category in categories:
        existed_category = session.query(Category).filter_by(name=category["name"]).first()
        if not existed_category:
            new_category = Category(name=category["name"], description=category["description"])
            session.add(new_category)
    session.commit()



# ===== BRANDS ===== #
brands = [
    {
        "name": "netflix",
        "description": "Popular Streaming Service"
    },
    {
        "name": "spotify",
        "description": "The best Music Subscription"
    },
    {
        "name": "chegg",
        "description": "Student's Best Friend"
    },
    {
        "name": "bartleby",
        "description": "Education is important"
    },
    {
        "name": "canva",
        "description": "Draw to your hearts desire"
    },
]

def seedBrands(session: Session):
    for brand in brands:
        existed_brand = session.query(Brand).filter_by(name=brand["name"]).first()
        if not existed_brand:
            new_brand = Brand(name=brand["name"], description=brand["description"])
            session.add(new_brand)
    session.commit()



# ===== PRODUCTS ===== #
products = [
    {
        "category_id": 2,
        "brand_id": 1,
        "name": "Netflix 1 Month Combo",
        "description": "For 1 User, 1 Month",
        "cost_per_unit": 69000,
        "image": "https://drive.google.com/uc?export=view&id=1TXT-Tv-vYtTVvXAxVLxXfBEizRyjDWhY",
        "stock_quantity": 200
    },
    {
        "category_id": 2,
        "brand_id": 1,
        "name": "Netflix 3 Month Combo",
        "description": "For 1 User, 3 Month",
        "cost_per_unit": 169000,
        "image": "https://drive.google.com/uc?export=view&id=1TXT-Tv-vYtTVvXAxVLxXfBEizRyjDWhY",
        "stock_quantity": 200
    },
    {
        "category_id": 2,
        "brand_id": 1,
        "name": "Netflix 6 Month Combo",
        "description": "For 1 User, 6 Month",
        "cost_per_unit": 299000,
        "image": "https://drive.google.com/uc?export=view&id=1TXT-Tv-vYtTVvXAxVLxXfBEizRyjDWhY",
        "stock_quantity": 200
    },
    {
        "category_id": 1,
        "brand_id": 3,
        "name": "Chegg 1 Month Combo",
        "description": "For 1 User, 1 Month",
        "cost_per_unit": 49000,
        "image": "https://drive.google.com/uc?export=view&id=1KxuyShsGXEq0Bj7Ala1Nyn-TmwjVlg5b",
        "stock_quantity": 200
    },
    {
        "category_id": 1,
        "brand_id": 3,
        "name": "Chegg 3 Month Combo",
        "description": "For 1 User, 3 Month",
        "cost_per_unit": 129000,
        "image": "https://drive.google.com/uc?export=view&id=1KxuyShsGXEq0Bj7Ala1Nyn-TmwjVlg5b",
        "stock_quantity": 200
    },
    {
        "category_id": 1,
        "brand_id": 3,
        "name": "Chegg 6 Month Combo",
        "description": "For 1 User, 6 Month",
        "cost_per_unit": 239000,
        "image": "https://drive.google.com/uc?export=view&id=1KxuyShsGXEq0Bj7Ala1Nyn-TmwjVlg5b",
        "stock_quantity": 200
    },
    {
        "category_id": 2,
        "brand_id": 2,
        "name": "Spotify 3 Month Combo",
        "description": "For 1 User, 3 Month",
        "cost_per_unit": 69000,
        "image": "https://drive.google.com/uc?export=view&id=1VgKhAMK-30kMZY6pF4g0ag39-EXe2n2S",
        "stock_quantity": 200
    },
    {
        "category_id": 2,
        "brand_id": 2,
        "name": "Spotify 6 Month Combo",
        "description": "For 1 User, 6 Month",
        "cost_per_unit": 119000,
        "image": "https://drive.google.com/uc?export=view&id=1VgKhAMK-30kMZY6pF4g0ag39-EXe2n2S",
        "stock_quantity": 200
    },
    {
        "category_id": 2,
        "brand_id": 2,
        "name": "Spotify Family Combo",
        "description": "For 3 User, 6 Month",
        "cost_per_unit": 299000,
        "image": "https://drive.google.com/uc?export=view&id=1VgKhAMK-30kMZY6pF4g0ag39-EXe2n2S",
        "stock_quantity": 200
    },
    {
        "category_id": 1,
        "brand_id": 4,
        "name": "Bartleby 1 Month Combo",
        "description": "For 1 User, 1 Month",
        "cost_per_unit": 59000,
        "image": "https://drive.google.com/uc?export=view&id=1ndEiq9Gi4cuxlxHQN0ARd9GFOoH-JEF9",
        "stock_quantity": 200
    },
    {
        "category_id": 1,
        "brand_id": 4,
        "name": "Bartleby 3 Month Combo",
        "description": "For 1 User, 3 Month",
        "cost_per_unit": 159000,
        "image": "https://drive.google.com/uc?export=view&id=1ndEiq9Gi4cuxlxHQN0ARd9GFOoH-JEF9",
        "stock_quantity": 200
    },
    {
        "category_id": 1,
        "brand_id": 4,
        "name": "Bartleby 6 Month Combo",
        "description": "For 1 User, 6 Month",
        "cost_per_unit": 259000,
        "image": "https://drive.google.com/uc?export=view&id=1ndEiq9Gi4cuxlxHQN0ARd9GFOoH-JEF9",
        "stock_quantity": 200
    },
    {
        "category_id": 3,
        "brand_id": 5,
        "name": "Canva 1 Month",
        "description": "For 1 User, 1 Month",
        "cost_per_unit": 29000,
        "image": "https://drive.google.com/uc?export=view&id=1Mgvd3WZ6RKDTJU75zzFKJ-4XRIzUH0ay",
        "stock_quantity": 200
    },
    {
        "category_id": 3,
        "brand_id": 5,
        "name": "Canva 2 Month",
        "description": "For 1 User, 2 Month",
        "cost_per_unit": 49000,
        "image": "https://drive.google.com/uc?export=view&id=1Mgvd3WZ6RKDTJU75zzFKJ-4XRIzUH0ay",
        "stock_quantity": 200
    },
    {
        "category_id": 3,
        "brand_id": 5,
        "name": "Canva 3 Month",
        "description": "For 1 User, 4 Month",
        "cost_per_unit": 59000,
        "image": "https://drive.google.com/uc?export=view&id=1Mgvd3WZ6RKDTJU75zzFKJ-4XRIzUH0ay",
        "stock_quantity": 200
    },
]

def seedProducts(session: Session):
    for product in products:
        existed_product = session.query(Product).filter_by(name=product["name"]).first()
        if not existed_product:
            new_product = Product(category_id=product["category_id"], brand_id=product["brand_id"], name=product["name"],
                                    description=product["description"], cost_per_unit=product["cost_per_unit"], image=product["image"],
                                    stock_quantity=product["stock_quantity"])
            session.add(new_product)
    session.commit()



# ===== USERS ===== #
def seedUsers(session: Session):
    admin = session.query(User).filter_by(username="admin").first()
    if  not admin:
        admin = User(username="admin", firstname="admin", lastname="admin", password=get_password_hash("admin"), 
                     phone="0911223333", email="admin@mail.com", location="Admin Home", role="admin")
        session.add(admin)
        session.commit()
    
    user = session.query(User).filter_by(username="user").first()
    if  not user:
        user = User(username="user", firstname="user", lastname="user", password=get_password_hash("user"), 
                    phone="0944556666", email="user@mail.com", location="User Home", role="user")
        session.add(user)
        session.commit()



# ===== COUPONS ===== #
coupons = [
    {
        "code": "WELCOMEPREDU",
        "type": "percentage", # 1 = fixed, 2 = percentage, 3 = both
        "value": 10,
        "min_order_required": 100000,
        "max_discount_applicable": 15000,
        "stock_quantity": 10,
        "limit_per_user": 10,
        "is_active": True
    },
    {
        "code": "PREDU20K",
        "type": "fixed", # 1 = fixed, 2 = percentage, 3 = both
        "value": 20000,
        "min_order_required": 200000,
        "max_discount_applicable": 20000,
        "stock_quantity": 10,
        "limit_per_user": 5,
        "is_active": True
    }
]

def seedCoupons(session: Session):
    for coupon in coupons:
        existed_coupon = session.query(Coupon).filter_by(code=coupon["code"]).first()
        if not existed_coupon:
            new_coupon = Coupon(code=coupon["code"], type=coupon["type"], value=coupon["value"], 
                                min_order_required=coupon["min_order_required"],
                                max_discount_applicable=coupon["max_discount_applicable"], 
                                stock_quantity=coupon["stock_quantity"], limit_per_user=coupon["limit_per_user"], 
                                is_active=coupon["is_active"],)
            session.add(new_coupon)
    session.commit()



seedCategories(session)
seedBrands(session)
seedProducts(session)
seedCoupons(session)
seedUsers(session)