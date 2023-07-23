from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, categories, brands, products, coupons, users, orders, chatbot
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(brands.router)
app.include_router(products.router)
app.include_router(coupons.router)
app.include_router(users.router)
app.include_router(orders.router)
app.include_router(chatbot.router)

@app.on_event("startup")
async def startup():
    print("\n # ========== PreDu ========== #")