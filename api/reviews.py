from flask import Blueprint, request, jsonify
from flask_paginate import get_page_parameter

from database.crud import get_product_by_id, get_reviews_by_product, create_review
from utils.cache import cache

reviews_blueprint = Blueprint('product_reviews', __name__, url_prefix='/product_reviews')


@reviews_blueprint.route("/<product_id>", methods=["GET"])
@cache.cached(timeout=50, query_string=True)
def product_reviews_endpoint(product_id: str):
    """Returns related reviews and Product data by id"""
    page = request.args.get(get_page_parameter(), type=int, default=1)
    product = get_product_by_id(product_id=product_id)
    if not product:
        err_msg = {"detail": "No Product in database with this id"}
        return err_msg
    product_reviews: list = get_reviews_by_product(product=product, page=page)
    result_data: dict = {
        "product": product.serialized_data,
        "reviews": [review.serialized_data for review in product_reviews] if product_reviews else [],
    }
    return jsonify(result_data)


@reviews_blueprint.route("/<product_id>", methods=["PUT"])
def add_review_to_product(product_id: str):
    """Add a new review for Product"""
    review_data: dict = request.json
    product = get_product_by_id(product_id=product_id)
    title = review_data.get("Title") or review_data.get("title")
    review_text = review_data.get("Review") or review_data.get("review")
    if not any([title, review_text]):
        return "Invalid data provided"
    review = create_review(product=product, title=title, review=review_text)
    return f"Successfully created review with id: {review.id}"
