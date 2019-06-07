# Here go your api methods.

def get_product_list():
	products = db(db.product).select()
	for p in products:
		stars = db(db.stars.product_id == p.id).select()
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
	return response.json(dict(product_list=products))

@auth.requires_signature()
def get_cart():
	order_list = []
	check_orders = db(db.shopping_cart.user_email == auth.user.email).select()
	num_orders = len(check_orders)
	if num_orders == 0:
		print("NO ORDERS")
		return
	rows = db(db.shopping_cart.user_email == auth.user.email).select()
	# products = 
	sum = 0 # tryna calculate total price of orders
	for row in rows:
		print(row)
		products = db(row.product_id == db.product.id).select()
		for product in products:
			sum += row.quantity * product.product_price
			sum = round(sum, 2) # in case it spontaneously produces super long floats
			order_list.append(dict(
				product_id = row.product_id,
				order_name = product.product_name,
				order_price = product.product_price,
				order_quantity = row.quantity,
				))
		print("ORDERS")
		print(row)

	print("Shopping cart:")
	print(order_list)
	return response.json(dict(order_list=order_list, order_total=sum))

@auth.requires_signature()
def add_cart():
	quantity = int(request.vars.quantity)
	orders = db((db.shopping_cart.product_id == request.vars.product_id) & (db.shopping_cart.user_email == auth.user.email)).select()
	sum = quantity
	for order in orders:
		sum += order.quantity
	print(sum)
	order_id = db.shopping_cart.update_or_insert(
			(db.shopping_cart.user_email == auth.user.email) & (db.shopping_cart.product_id == request.vars.product_id),
		quantity = sum, 
		product_id = request.vars.product_id,
		user_email = auth.user.email,
		)
	return response.json(dict(order_id=order_id))

@auth.requires_signature()
def clear_cart():
	db(db.shopping_cart.user_email == auth.user.email).delete()
	order_list = db(db.shopping_cart.user_email == auth.user.email).select()	
	return response.json(dict(order_list=order_list))

@auth.requires_signature()
def add_review():
	review_id = db.reviews.update_or_insert(
			(db.reviews.user_email == auth.user.email) & (db.reviews.product_id == request.vars.product_id),
		review_content = request.vars.review_content,
		product_id = request.vars.product_id,
		user_email = auth.user.email,
		)
	# rows = db(db.reviews).select()
	# print("ADD REVIEW ROWS: ")
	# for row in rows:
	# 	print(row)
	return response.json(dict(review_id=review_id))

def get_reviews():
	"""Gets the list of reviews for a product??"""
	product_id = int(request.vars.product_id)
	print("requesting product id: ")
	print(product_id)
	review_list = []
	# We get directly the list of all reviews for the product i guess
	review_list = []
	rows = db(db.reviews.product_id == product_id).select(db.reviews.ALL, db.stars.ALL,
		left=[
		db.reviews.on((db.reviews.product_id == db.product.id) & (db.reviews.user_email == db.stars.user_email)),
		db.stars.on((db.stars.user_email == db.reviews.user_email) & (db.stars.product_id == db.product.id)),
		],
		orderby=~db.reviews.review_time)
	for row in rows:
		review_list.append(dict(
			product_id = row.reviews.product_id,
			review_content = row.reviews.review_content,
			review_author = row.reviews.review_author,
			rating = row.stars.rating,
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
		(db.stars.user_email == auth.user.email) & (db.stars.product_id == product_id),
		product_id = product_id,
		user_email = auth.user.email,
		rating = rating
	)
	return "ok" # might be useful in debugging

# MY_PRODUCTS = ['duck', 'cards',]

# @auth.requires_signature(hash_vars=False)
# def search():
#     s = request.vars.search_string or ''
#     res = [t for t in MY_PRODUCTS if s in t]
#     return response.json(dict(strings=res))