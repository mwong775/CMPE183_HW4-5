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

    self.edit_toggle = function (is_edit) {
        if (is_edit) {
            self.vue.is_editing = true;
        } else {
            // Save the value, e.g. sending it to the server.
            console.log("The user saved value " + self.vue.my_string);
            self.vue.save_pending = true;
            $.post(edit_url,
                {my_string: self.vue.my_string},
                function (data) {
                    self.vue.save_pending = false;
                    self.vue.is_editing = false;
                });
        }
    };

    // Complete as needed.
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            my_string: "Some initial string",
            is_editing: false,
            save_pending: false
        },
        methods: {
            edit_toggle: self.edit_toggle
        }

    });


    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
