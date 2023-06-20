from models import *
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
]




seedCategories(session)
seedBrands(session)