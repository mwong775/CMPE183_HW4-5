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

    self.counter = 0;

    self.toggle_plus = function () {
        if (self.vue.is_plus) {
            self.vue.thing_list.push("" + self.counter);
            self.counter += 1;
        }
        self.vue.is_plus = !self.vue.is_plus;
    };

    self.get_initial_data = function () {
        // The URL is initial_data_url
        $.getJSON(
            initial_data_url,
            function (data) {
                console.log("Reply from the server");
                self.vue.animal_list = data.animals;
                self.vue.thing_list = data.things;
            }
        );
        console.log("I just sent my server request.");
    };

    self.change_salutation = function () {
        console.log("changing salutation");
        if (self.vue.salutation === 'hello') {
            self.vue.salutation = 'ciao';
            self.vue.sal_button = 'English';
        } else {
            self.vue.salutation = 'hello';
            self.vue.sal_button = 'Italian';
        }
    };

    // Complete as needed.
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            salutation: 'hello',
            sal_button: 'Italian',
            thing_list: [],
            animal_list: [],
            is_plus: true
        },
        methods: {
            change_salutation: self.change_salutation,
            toggle_plus: self.toggle_plus
        }
    });

    self.get_initial_data();

    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
