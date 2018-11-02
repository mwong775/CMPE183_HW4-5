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

    self.edit_title = function () {
        self.vue.is_title_editable = true;
    };

    self.end_edit_title = function () {
        self.vue.is_title_editable = false;
        // We send the title.
        $.post(set_title_url, 
            {title: self.vue.title}
            );
    };

    self.get_title = function () {
        $.getJSON(get_title_url, function(data) {
            self.vue.title = data.title
        }
        );
    };

    // Complete as needed.
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            is_logged_in: is_logged_in,
            title: "",
            is_title_editable: false,
        },
        methods: {
            edit_title: self.edit_title,
            end_edit_title: self.end_edit_title
        }

    });

    // Let's get the info. 
    self.get_title();

    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
