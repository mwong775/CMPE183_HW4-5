// This is the js for the default/index.html view.

var app = function () {

    var self = {};

    Vue.config.silent = false; // show all warnings

    // Extends an array
    self.extend = function (a, b) {
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
        })
    };

    self.get_more = function () {
        var num_tracks = self.vue.tracks.length;
        $.getJSON(get_tracks_url(num_tracks, num_tracks + 50), function (data) {
            self.vue.has_more = data.has_more;
            self.extend(self.vue.tracks, data.tracks);
        });
    };

    self.add_track_button = function () {
        // The button to add a track has been pressed.
        self.vue.is_adding_track = !self.vue.is_adding_track;
        self.vue.is_adding_track_from_spotify = false;

    };

    self.add_track_from_spotify_button = function () {
        // The button to add a track has been pressed.
        self.vue.is_adding_track_from_spotify = !self.vue.is_adding_track_from_spotify;
        self.vue.is_adding_track = false;

    };

    self.add_track = function () {
        console.log("Tracks: " + data.track)
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
            });
    };

    self.add_track_from_spotify = function () {
        // The submit button to add a track has been added.
        $.post(add_track_from_spotify_url,
            {
                artist: self.vue.form_artist,
            },
            function (data) {
                $.web2py.enableElement($("#add_track_from_spotify_submit"));
                for (i = 0; i < data.tracks.length; i++) {
                    self.vue.tracks.unshift(data.tracks[i]);
                }
            });
    };

    self.delete_track = function (track_id) {
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
                }
            }
        )
    };

    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            is_adding_track: false,
            is_adding_track_from_spotify: false,
            tracks: [],
            logged_in: false,
            has_more: false,
            form_artist: null,
            form_track: null,
            form_album: null,
            form_duration: null
        },
        methods: {
            get_more: self.get_more,
            add_track_button: self.add_track_button,
            add_track_from_spotify_button: self.add_track_from_spotify_button,
            add_track: self.add_track,
            add_track_from_spotify: self.add_track_from_spotify,
            delete_track: self.delete_track
        }

    });

    self.get_tracks();
    $("#vue-div").show();


    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function () {
    APP = app();
});
