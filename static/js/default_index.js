// This is the js for the default/index.html view.

var app = function() {

    var self = {};

    Vue.config.silent = false; // show all warnings

    // Extends an array
    self.extend = function(a, b) {
        for (var i = 0; i < b.length; i++) {
            a.push(b[i]);
        }
    };

     // Enumerates an array.
    var enumerate = function(v) { var k=0; return v.map(function(e) {e._idx = k++;});};

    self.add_review = function(product_idx) {
        // We disable the button, to prevent double submission.
        $.web2py.disableElement($(".add-review"));
        var r = self.vue.product_list[product_idx];
        console.log("product_idx = " + product_idx);
        var review_list = r._reviews;
        var sent_content = self.vue.review_content;

        $.post(add_review_url, 
            {
                review_content: sent_content,
                product_id: r.id,
                //review_rating: r.__num_stars_display,
            },
            function (data) {
                $.web2py.enableElement($(".add-review"));

                self.vue.review_content=""; // Clears the form??
                // Adds the product to the list of products
                var new_review = {
                    id: data.review_id,
                    review_content: sent_content,
                    review_author: data.review_author,
                    product_id: r.id,
                };
                new_review.rating = r._num_stars_display;
                review_list.unshift(new_review);
                self.process_reviews(product_idx);

                // self.vue.confirm = true;
                // setInterval(
                //     function() {
                //         console.log('interval again');
                //         self.vue.confirm = false;
                //     },
                //     1000
                //     );

                self.show_reviews(product_idx);
                self.get_reviews(product_idx);
                console.log(new_review);
                console.log("r list length:");
                console.log(review_list.length);
            });
    };

    self.confirm = function() {
        console.log("CONFIRMMM");
        self.vue.confirm = true;
        setInterval(
        function() {self.vue.confirm = false},
        1000
        );
    }

    self.process_reviews = function(product_idx) {
        var p = self.vue.product_list[product_idx];
        console.log("before process reviews:");
        console.log(p);
        var review_list = p._reviews;
        console.log(review_list);
        enumerate(review_list);

        review_list.map(function (e) {
            Vue.set(e, '__num_stars_display', e.rating);
        });
        console.log("after process reviews:");
        console.log(review_list);
    };

    self.get_products = function() {
        $.getJSON(get_product_list_url,
            function(data) {
                self.vue.product_list = data.product_list;
                self.process_products();
                console.log("product list below:");
                console.log(self.vue.product_list);
                for(let i = 0; i < self.vue.product_list.length; i++) {
                    console.log("printing a product:");
                    var p = self.vue.product_list[i];
                    console.log(p);
                    console.log("its reviews:");
                    console.log(p._reviews);
                    // console.log("review_list length:" + p._reviews.length);
                }
            });
    };

    self.show_cart = function() {
        self.vue.cart_view = !self.vue.cart_view;
        self.get_cart();
    }

    self.get_cart = function() {
        $.getJSON(get_cart_url,
            function (data) {
                self.vue.order_list = data.order_list;
                console.log("TOTAL:" + data.order_total);
                self.vue.order_total = data.order_total;
            }
        );
        self.process_orders();
    };

    self.add_cart = function(product_idx) {
        console.log("ADDED TO CARTTTTT");
        $.web2py.disableElement($(".add-cart"));
        var r = self.vue.product_list[product_idx];
        console.log("product_idx = " + product_idx);
         var order_quantity = r._order_quantity;
        if(order_quantity > 0) {
            console.log("quantity is at least 1");
            console.log("u want to order " + order_quantity + "of these");
            $.post(add_cart_url,
                {
                    quantity: order_quantity,
                    product_id: r.id,
                },
                function (data) {
                    $.web2py.enableElement($(".add-cart"));

                    r._order_quantity = ""; // Clears the form..?

                    var new_order = {
                        id: data.order_id,
                        quantity: order_quantity,
                        product_id: r.id,
                    };
                    self.vue.order_list.unshift(new_order);
                    self.process_orders();
                    self.get_cart();
                });
        }
        else {
            console.log("pls input quantity"); // no quantity specified
        }
    };

    self.clear_cart = function() {
        $.getJSON(clear_cart_url,
            function (data) {
                self.vue.order_list = data.order_list;
                self.vue.order_total = 0;
            }
        );
        self.hide_cart();
    }

    self.hide_cart = function() {
        self.vue.cart_view = !self.vue.cart_view;
    }

    self.process_orders = function() {
        console.log("before process orders:");
        console.log(self.vue.order_list);
        enumerate(self.vue.order_list);
        // self.vue.order_list.map(function (e) {
            // Vue.set(e, 'quantity', e.quantity);
        // });
        console.log("after process orders:");
        console.log(self.vue.order_list);
    }

    self.process_products = function() {
        console.log("before process products:");
        console.log(self.vue.product_list);

        enumerate(self.vue.product_list);
        // console.log("processing: ");
        // console.log(self.vue.product_list);
        self.vue.product_list.map(function (e) {
            Vue.set(e, '_details', false);
            Vue.set(e, '_reviews', []);
            Vue.set(e, '_order_quantity');
            Vue.set(e, '_show_reviews', false);
            Vue.set(e, '_num_stars_display', 0);
            Vue.set(e, '_set_stars', false);
            Vue.set(e, 'visible', true);
            Vue.set(e, 'rating', e.rating);
        });
        console.log("after process products:");
        console.log(self.vue.product_list);
      
    };

    self.get_reviews = function(product_idx) {
        // self.get_products(product_idx);
        // confirm = false;
        var p = self.vue.product_list[product_idx];
        console.log("product ID: " + p.id);
        self.show_reviews(product_idx);
        $.getJSON(get_reviews_url, {product_id: p.id}, 
            function(data) {
               //self.vue.review_list = data.review_list;
                p._reviews = data.reviews;
               // product_id: p.id;
               // review_content: p.review_content;
               //review_content: review_idx
            });
        self.process_reviews(product_idx);
        p._show_reviews = true; //!p._show_reviews;
        p._details = true; //!p._details;
        for(let i = 0; i < self.vue.product_list.length; i++){
            if(i != product_idx) {
                var q = self.vue.product_list[i];
                q._show_reviews = false;
                q._details = false;
            }
        }

        console.log("# reviews:" + p._reviews.length);
        console.log("get reviews:");
        console.log(p._reviews);
    };

    // Code for getting and displaying the list of reviews?? NOPE
    self.show_reviews = function(product_idx) {
        var p = self.vue.product_list[product_idx];
        // console.log("show reviews:");
        // console.log(p);
        p._show_reviews = true;
        for(let i = 0; i < self.vue.product_list.length; i++){
            if(i != product_idx) {
                var q = self.vue.product_list[i];
                q._show_reviews = false;
                q._details = false;
            }
        }
    };

    self.hide_reviews = function(product_idx) {
        var p = self.vue.product_list[product_idx];
        p._show_reviews = false; 
        p._details = false; ;
        // console.log("hide reviews:");
        // console.log(p);
        self.get_products();
    }

    // Code for star ratings.
    self.stars_out = function (product_idx) {
        // Out of the star rating; set number of visible back to rating.
        var p = self.vue.product_list[product_idx];
        if(!p._set_stars)
            p._num_stars_display = 0;
    };

    self.stars_over = function(product_idx, star_idx) {
        // Hovering over a star; we show that as the number of active stars.
        var p = self.vue.product_list[product_idx];
        p._num_stars_display = star_idx;
    };

    self.set_stars = function(product_idx, star_idx) {
        // The user has set this as the number of stars for the product.
        var p = self.vue.product_list[product_idx];
        //console.log(self.vue.product_list[product_idx]);
        p._set_stars = true;
        p._num_stars_display = star_idx;
        console.log("_num_stars_display: " + p._num_stars_display);
        console.log("SETSTAR # reviews: " + p._reviews.length);
        //Sends the rating to the server.
        $.post(set_stars_url, {
            rating: star_idx,
            product_id: p.id,
        });
    };

    self.do_search = function() {
        // $.getJSON(search_url,
        //     {search_string: self.vue.search_string},
            // function (data) {
                //self.vue.strings = data.strings;
                for(let i = 0; i < self.vue.product_list.length; i++) {
                    let p = self.vue.product_list[i];

                    if(p.product_name.toUpperCase().indexOf(self.vue.searchbar.toUpperCase()) == 0 || self.vue.searchbar == "")
                    {
                        p.visible = true;
                    }
                    else
                    {
                        p.visible = false;
                    }
                };
            };

    // Complete as needed.
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            strings: [],
            searchbar: '',
            product_name: "",
            product_description: "",
            review_content:"",
            order_list: [], // HW5
            order_name: "",
            order_price: "",
            order_quantity: "",
            order_total: 0,
            cart_view: false, // HW5
            rating: "",
            username: "",
            product_list: [],
            confirm: false,
            //review_list: [],
            star_indices: [1,2,3,4,5]
        },
        methods: {
           // do_call: self.do_call,
            //confirm: self.confirm,
            do_search: self.do_search,
            // add_product: self.add_product,
            add_cart: self.add_cart, //HW5
            get_cart: self.get_cart, // HW5
            clear_cart: self.clear_cart, // HW5
            show_cart: self.show_cart, // HW5
            hide_cart: self.hide_cart, // HW5
            //
            add_review: self.add_review,
            //Show/hide reviews?
            get_reviews: self.get_reviews,
            show_reviews: self.show_reviews,
            hide_reviews: self.hide_reviews,
             // Star ratings.
            stars_out: self.stars_out,
            stars_over: self.stars_over,
            set_stars: self.set_stars
        }

    });

    if(is_logged_in) {
        $(".add_review").show();
    }
    self.get_products();
    self.do_search();

    $("#vue-div").show();
    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
