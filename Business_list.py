from app import app, db, Business

def populate_businesses():
    with app.app_context():  # Ensure that the code runs within the application context
        # Sample businesses
        businesses = [
            {'name': 'Joe\'s Coffee Shop'},
            {'name': 'The Gourmet Bistro'},
            {'name': 'Tech Haven'},
            {'name': 'Urban Fitness Center'},
            {'name': 'The Book Nook'},
            {'name': 'Green Leaf Organic Market'},
        ]

        for business in businesses:
            # Check if business already exists
            if not Business.query.filter_by(name=business['name']).first():
                new_business = Business(name=business['name'])
                db.session.add(new_business)
        
        # Commit the changes
        db.session.commit()
        print("Businesses have been added to the database.")

if __name__ == '__main__':
    populate_businesses()
