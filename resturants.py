from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Restaurant(Base):
    __tablename__ ='restaurants'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)

    reviews = relationship('Review', back_populates='resturant')

    @classmethod
    def fanciest(cls, session):
        return session.query(cls).order_by(cls.price.desc()).first()
    
    def all_reviews(self):
        return [f"Review for {self.name} by {reviewer.name()}: {review.rating} stars" for review in self.review]
    

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

    reviews = relationship('Review', back_populates='customer')

    def name(self):
        return f"{self.first_name}{self.last_name}"
    
    def fav_resturant(self):
        highest_rating = -1
        fav = None
        for review in self.reviews:
            if review.rating > highest_rating:
                highest_rating = review.rating
                fav = review.resturant
        return fav
    
    def add_review(self, resturant, rating):
        new_review = Review(customer = self, resturant=resturant, rating=rating)
        return new_review
    
    def delete_review(self, resturant):
        for review in self.reviews:
            if review.resturant == resturant:
                self.reviews.remove(review)

class Review(Base):
    __tablename__ ='reviews'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    resturant_id = Column(Integer, ForeignKey('resturants.id'))
    star_rating = Column(Integer)

    customer = relationship('Customer', back_populates='reviews')
    resturant = relationship('Restaurant', back_populates='reviews')

    def customer(self):
        return self.customer
    
    def resturant(self):
        return self.resturant
    
    def full_reviews(self):
        return [f"Review for {self.resturant.name} by {self.customer.name()}: {self.star_rating} stars" for review in self.resturant.reviews]
    

engine = create_engine('sqlite:///resturant_reviews.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()