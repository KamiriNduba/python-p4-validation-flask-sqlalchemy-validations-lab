from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)  # Ensure all authors have a unique name
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Validator for ensuring author name is not empty
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Author name must not be empty")
        # Ensure that no two authors have the same name
        if Author.query.filter_by(name=name).first() is not None:
            raise ValueError("Author name must be unique")
        return name

    # Validator for ensuring phone number is exactly ten digits (if provided)
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if phone_number and (not phone_number.isdigit() or len(phone_number) != 10):
            raise ValueError("Phone number must be exactly ten digits")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'


class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Validator for ensuring post title contains clickbait keywords
    @validates('title')
    def validate_title(self, key, title):
        clickbait_keywords = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(keyword in title for keyword in clickbait_keywords):
            raise ValueError("Post title must contain one of: 'Won't Believe', 'Secret', 'Top', 'Guess'")
        return title

    # Validator for ensuring post content is at least 250 characters long
    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Post content must be at least 250 characters long")
        return content

    # Validator for ensuring post summary is maximum 250 characters long (if provided)
    @validates('summary')
    def validate_summary(self, key, summary):
        if summary and len(summary) > 250:
            raise ValueError("Post summary must be a maximum of 250 characters")
        return summary

    # Validator for ensuring post category is either Fiction or Non-Fiction
    @validates('category')
    def validate_category(self, key, category):
        if category not in ["Fiction", "Non-Fiction"]:
            raise ValueError("Post category must be either Fiction or Non-Fiction")
        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
