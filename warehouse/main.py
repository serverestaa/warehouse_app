from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

redis = get_redis_connection(
    host='redis-11115.c283.us-east-1-4.ec2.redns.redis-cloud.com',
    port="11115",
    password='iYsOZ5QcmDsBTvfwOP8x2PJa7OBZzh9w',
    decode_responses=True
)


class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


@app.post('/product', tags=['warehouse'])
def create(product: Product):
    return product.save()


@app.get('/product/{pk}', tags=['warehouse'])
def get(pk: str):
    return Product.get(pk)


@app.get('/products', tags=['warehouse'])
def all():
    # return Product.all_pks()
    return [format(pk) for pk in Product.all_pks()]


def format(pk: str):
    product = Product.get(pk)
    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }


@app.delete('/product/{pk}', tags=['warehouse'])
def delete(pk: str):
    return Product.delete(pk)
