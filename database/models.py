from database.db import db


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    asin = db.Column(db.String(100), nullable=False)
    reviews = db.relationship("Review", back_populates="product")

    @property
    def serialized_data(self) -> dict:
        model_data: dict = {
            "title": self.title,
            "asin": self.asin,
        }
        return model_data

    def __repr__(self):
        return f"Product ({self.id})"


class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship("Product", back_populates="reviews")
    title = db.Column(db.String(255), nullable=False)
    asin = db.Column(db.String(100), nullable=False)
    review = db.Column(db.Text, nullable=False)

    @property
    def serialized_data(self) -> dict:
        model_data: dict = {
            "title": self.title,
            "review": self.review,
        }
        return model_data

    def __repr__(self):
        return f"Review ({self.id})"
