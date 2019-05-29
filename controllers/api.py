# Here go your api methods.


# @auth.requires_signature()
# def add_product():
# 	product_id = db.product.insert(
# 		product_name = request.vars.product_name,
# 		product_description = request.vars.product_description,
# 		product_price = request.vars.product_price
# 		) 
# 	rows = db(db.product).select()
# 	for row in rows:
# 		print(row)

# 		# return the id of the new product?, so we can insert along all the others.
# 	return response.json(dict(rows=rows))#product_id=product_id))

def get_product_list():
	# rows = db().select(db.product.ALL, db.reviews.ALL, db.stars.ALL,
	# 	 left=[
	# 	 	db.reviews.on((db.reviews.product_id == db.product.id)),# & (db.reviews.user_email == db.stars.user_email)),
	# 	 	db.stars.on((db.stars.product_id == db.product.id))# & (db.stars.product_id == db.product.id))
	# 	 	],
	# 		)
	# products = db(db.product).select().as_list()
	products = db(db.product).select()
	for p in products:
		stars = db(db.stars.product_id == p.id).select()#.as_list()
		# print("PRODUCT RATINGS: ")
		# print(stars)
		sum = 0
		# num = 0
		rating = 0 #if row.stars.id is None else row.stars.rating,
		num = len(stars)
		if num == 0:
			continue
		# print("# RATINGS")
		# print(num)
		for star in stars:
			sum += star.rating
		# print("SUMMMM")
		# print(sum)
		rating = sum / num
		# print("AVG: ")
		# print(rating)
		p.avg_rating = rating
		print("AVERAGE: ")
		print(p.avg_rating)

		# results.append(dict(
		# 	id = row.product.id,
		# 	product_name = row.product.product_name,
		# 	product_description = row.product.product_description,
		# 	product_price = row.product.product_price,
		# 	rating = 0 if row.stars.id is None else row.stars.rating,
		# 	))
	return response.json(dict(product_list=products))#, rating = rating))

@auth.requires_signature()
def add_review():
	#rating = int(request.vars.review_rating)
	review_id = db.reviews.update_or_insert(
			(db.reviews.user_email == auth.user.email) & (db.reviews.product_id == request.vars.product_id),
		review_content = request.vars.review_content,
		#review_author = auth.user.first_name + " " + auth.user.last_name, #request.vars.review_author,
		product_id = request.vars.product_id,
		user_email = auth.user.email,
		)
	rows = db(db.reviews).select()
	print("ADD REVIEW ROWS: ")
	for row in rows:
		print(row)

	return response.json(dict(review_id=review_id))

def get_reviews():
	"""Gets the list of reviews for a product??"""
	product_id = int(request.vars.product_id)
	print("requesting product id: ")
	print(product_id)
	review_list = []
	# We get directly the list of all reviews for the product i guess
	#rows = db(db.reviews.product_id == product_id).select(db.reviews.user_email)
	# review_list = [r.user_email for r in rows]
	# review_list.sort()
	# print(review_list)
	review_list = []
	rows = db(db.reviews.product_id == product_id).select(db.reviews.ALL, db.stars.ALL,
		left=[
		#db.product.on(db.reviews.product_id == db.product.id),
		db.reviews.on((db.reviews.product_id == db.product.id) & (db.reviews.user_email == db.stars.user_email)),
		db.stars.on((db.stars.user_email == db.reviews.user_email) & (db.stars.product_id == db.product.id)),
		],
		orderby=~db.reviews.review_time)
	for row in rows:
		review_list.append(dict(
			product_id = row.reviews.product_id,
			review_content = row.reviews.review_content,
			review_author = row.reviews.review_author,
			rating = row.stars.rating,#None if row.stars.id is None else row.stars.rating,
			))

	print("ADD REVIEW ROWS: ")
	for row in rows:
		print(row)
	print("ADD REVIEW RESULTS:")
	print(review_list)

	return response.json(dict(reviews=review_list))

@auth.requires_signature(hash_vars=False)
def set_stars():
	product_id = int(request.vars.product_id)
	#review_id = int(request.vars.review_id)
	rating = int(request.vars.rating)
	db.stars.update_or_insert(
		(db.stars.user_email == auth.user.email) & (db.stars.product_id == request.vars.product_id),
		product_id = product_id,
		user_email = auth.user.email,
		rating = rating
	)
	return "ok" # mighht be useful in debugging

# MY_PRODUCTS = ['duck', 'cards',]

# @auth.requires_signature(hash_vars=False)
# def search():
#     s = request.vars.search_string or ''
#     res = [t for t in MY_PRODUCTS if s in t]
#     return response.json(dict(strings=res))