from database import create_session

from services.coupons import get_all_coupons

session = create_session

success, data = get_all_coupons(session)

print(len(data))