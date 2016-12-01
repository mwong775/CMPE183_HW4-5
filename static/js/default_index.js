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
    var enumerate = function(v) {
        var k=0;
        return v.map(function(e) {e._idx = k++;});
    };

    self.get_info = function () {
        $.getJSON(get_info_url, function (data) {
            self.vue.image_list = data.image_list;
            enumerate(self.vue.image_list);
        });
    };

    self.mouse_over = function (img_idx, star_idx) {
        self.vue.image_list[img_idx].num_stars_display = star_idx;
    };

    // Complete as needed.
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            image_list: [],
            is_logged_in: is_logged_in,
            star_indices: [1, 2, 3, 4, 5]
        },
        methods: {
            mouse_over: self.mouse_over
        }

    });

    self.get_info();
    $("#vue-div").show();

    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
