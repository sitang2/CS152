import random
import string
from datetime import datetime, timedelta
from app import app, db, Review, Business

def generate_review_code():
    """Generate a random 6-character review code with letters and digits."""
    characters = string.ascii_letters + string.digits
    review_code = ''.join(random.choice(characters) for _ in range(6))
    return review_code

def insert_review(business_id):
    """Insert a new review into the database and return the review code."""
    with app.app_context():
        try:
            # Check if the business_id exists
            if not db.session.query(db.exists().where(Business.id == business_id)).scalar():
                raise ValueError(f"Business with ID {business_id} does not exist.")
            
            review_code = generate_review_code()
            expiry_date = datetime.now() + timedelta(hours=24)
            new_review = Review(expiry_date=expiry_date, review_code=review_code, business_id=business_id)
            db.session.add(new_review)
            db.session.commit()
            return review_code
        except ValueError as ve:
            print(f"Error: {ve}")
            db.session.rollback()
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            db.session.rollback()
        return None

if __name__ == "__main__":
    business_id = 1  # Change this ID to match an existing business
    review_code = insert_review(business_id)
    if review_code:
        print(f"Generated review code: {review_code}")
    else:
        print("Failed to generate review code. Please check the logs for details.")
