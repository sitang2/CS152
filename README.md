How to run the code

1) make sure to install Flask and Flask Migrate to for web developing.
2) run init_db.py to create a database table
3) run Business_list.py to insert example business lists
4) run code_generator.py to get a access code
5) In code_generator.py at line
   "business_id = 1  # Change this ID to match an existing business"
    changing the id will change the business 

   id     1    {'name': 'Joe\'s Coffee Shop'},
   id     2    {'name': 'The Gourmet Bistro'},
   id     3    {'name': 'Tech Haven'},
   id     4    {'name': 'Urban Fitness Center'},
   id     5    {'name': 'The Book Nook'},
   id     6    {'name': 'Green Leaf Organic Market'},

For exampe, if id 3 code generated, that code can only by valid for "Tech Haven" business.

6) run app.py then click on the local link to start the web.
7) Register then login
8) If code is invalid, the review will not go through.
9) To test another access code, close app.py and generate another code, then start app.py again.
