from database import create_session
from models import *

from services.coupons import get_all_coupons

session = create_session()

new_brand = Brand(name="Mailchimp", description="API Service")
session.add(new_brand)
session.flush()
print(new_brand.id)

session.commit()