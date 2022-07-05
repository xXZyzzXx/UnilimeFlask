import csv
from typing import Generator

from database.crud import create_product, create_review, get_product_by_asin


def get_file_data(filename: str) -> Generator:
    """Returns a generator object of file"""
    with open(filename, "r") as file_to_parse:
        reader = csv.DictReader(file_to_parse)
        for row_data in reader:
            yield row_data


def parse_products_file():
    """Create a Product from file data"""
    products_filename = "parsing_files/products.csv"
    file_generator_object: Generator = get_file_data(filename=products_filename)
    for rows_data in file_generator_object:
        title = rows_data.get("Title")
        asin = rows_data.get("Asin")  # noqa
        create_product(title=title, asin=asin)


def parse_reviews_file():
    """Create a Review from file data"""
    reviews_filename = "parsing_files/reviews.csv"
    file_generator_object: Generator = get_file_data(filename=reviews_filename)
    for rows_data in file_generator_object:
        review = rows_data.get("Review")
        title = rows_data.get("Title")
        asin = rows_data.get("Asin")  # noqa
        product = get_product_by_asin(asin=asin)  # We can add cache here
        create_review(product=product, title=title, review=review)
