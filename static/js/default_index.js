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

    function get_tracks_url(start_idx, end_idx) {
        var pp = {
            start_idx: start_idx,
            end_idx: end_idx
        };
        return tracks_url + "?" + $.param(pp);
    }

    self.get_tracks = function () {
        $.getJSON(get_tracks_url(0, 20), function (data) {
            self.vue.tracks = data.tracks;
            self.vue.has_more = data.has_more;
            self.vue.logged_in = data.logged_in;
            enumerate(self.vue.tracks);
        })
    };

    self.get_more = function () {
        var num_tracks = self.vue.tracks.length;
        $.getJSON(get_tracks_url(num_tracks, num_tracks + 50), function (data) {
            self.vue.has_more = data.has_more;
            self.extend(self.vue.tracks, data.tracks);
            enumerate(self.vue.tracks);
        });
    };

    self.add_track_button = function () {
        // The button to add a track has been pressed.
        self.vue.is_adding_track = !self.vue.is_adding_track;
    };

    self.add_track = function () {
        // The submit button to add a track has been added.
        $.post(add_track_url,
            {
                artist: self.vue.form_artist,
                title: self.vue.form_track,
                album: self.vue.form_album,
                duration: self.vue.form_duration
            },
            function (data) {
                $.web2py.enableElement($("#add_track_submit"));
                self.vue.tracks.unshift(data.track);
                enumerate(self.vue.tracks);
            });
    };

    var enumerate = function(v) { var k=0; return v.map(function(e){e._idx = k++;});};

    self.delete_track = function(track_id) {
        $.post(del_track_url,
            {
                track_id: track_id
            },
            function () {
                var idx = null;
                for (var i = 0; i < self.vue.tracks.length; i++) {
                    if (self.vue.tracks[i].id === track_id) {
                        // If I set this to i, it won't work, as the if below will
                        // return false for items in first position.
                        idx = i + 1;
                        break;
                    }
                }
                if (idx) {
                    self.vue.tracks.splice(idx - 1, 1);
                    enumerate(self.vue.tracks);
                }
            }
        )
    };

    self.select_track = function(track_idx) {
        var track = self.vue.tracks[track_idx];
        self.vue.selected_idx = track_idx;
        self.vue.selected_id = track.id;
        self.vue.selected_url = track.track_url;
    };

    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            is_adding_track: false,
            tracks: [],
            logged_in: false,
            has_more: false,
            form_artist: null,
            form_track: null,
            form_album: null,
            form_duration: null,
            selected_id: -1,  // Track selected to play.
            selected_idx: null,
            selected_url: null
        },
        methods: {
            get_more: self.get_more,
            add_track_button: self.add_track_button,
            add_track: self.add_track,
            delete_track: self.delete_track,
            select_track: self.select_track
        }

    });

    self.get_tracks();
    $("#vue-div").show();


    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
