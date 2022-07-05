import os
from typing import Optional, Union

from database.db import db
from database.models import Product, Review

ITEMS_PER_PAGE = os.environ.get('ITEMS_PER_PAGE', 2)


def create_product(title: str, asin: str) -> None:
    product = Product(title=title, asin=asin)
    _add_object_to_database(model_object=product)


def create_review(product: Product, title: str, review: str, asin: str) -> None:
    review = Review(product=product, title=title, review=review, asin=asin)
    _add_object_to_database(model_object=review)


def get_product_by_id(product_id: Union[str, int]) -> Optional[Product]:
    product = Product.query.get(product_id)
    return product


def get_product_by_asin(asin: str) -> Optional[Product]:
    product = Product.query.filter_by(asin=asin).first()
    return product


def get_reviews_by_product(product: Product, page: int) -> Optional[list]:
    reviews = Review.query.filter_by(product=product).paginate(page=page, per_page=ITEMS_PER_PAGE).items
    return reviews


def _add_object_to_database(model_object) -> None:  # noqa
    db.session.add(model_object)
    db.session.commit()
