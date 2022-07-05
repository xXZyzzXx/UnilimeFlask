from flask import Blueprint, request, jsonify
from flask_paginate import get_page_parameter

from database.crud import get_product_by_id, get_reviews_by_product

reviews_blueprint = Blueprint('product_reviews', __name__)


@reviews_blueprint.route("/<product_id>")
def product_reviews_endpoint(product_id: str):
    """Returns related reviews and Product data by id"""
    page = request.args.get(get_page_parameter(), type=int, default=1)
    product = get_product_by_id(product_id=product_id)
    if not product:
        err_msg = {"detail": "No Products in database"}
        return err_msg
    product_reviews: list = get_reviews_by_product(product=product, page=page)
    result_data: dict = {
        "product": product.serialized_data,
        "reviews": [review.serialized_data for review in product_reviews],
    }
    return jsonify(result_data)
