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

    // Some animals.
    var dog = {id: 1, name: 'dog', 'paws': 4};
    var cat = {id: 2, name: 'cat', 'paws': 4};
    var bird = {id: 3, name: 'bird', 'paws': 2};
    var animal_list = [dog, cat, bird];

    self.mydog = {
        name: 'Bob',
        age: 37,
        color: 'brown'
    };

    self.counter = 0;

    self.toggle_plus = function () {
        if (self.vue.is_plus) {
            self.vue.thing_list.push("" + self.counter);
            self.counter += 1;
        } else {
            // Minus
            self.vue.thing_list[2] = 'whale';
        }
        self.vue.is_plus = !self.vue.is_plus;
    };

    // Complete as needed.
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            salutation: 'hello',
            thing_list: ['duck', 'cat', 'cow', 'donkey'],
            animal_list: animal_list,
            is_plus: true
        },
        methods: {
            toggle_plus: self.toggle_plus
        }
    });

    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
