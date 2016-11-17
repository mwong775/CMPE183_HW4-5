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

    self.play = function(i, j) {
        if (self.vue.board[i * 3 + j] === '') {
            self.vue.$set(self.vue.board, i * 3 + j, self.vue.youare);
            $.post(set_state_url, {p: self.vue.game_name, new_board: JSON.stringify(self.vue.board)});
        }
    };

    // Refresh the game.
    self.refresh = function () {
        $.get(
            get_state_url + '?' + $.param({p: self.vue.game_name}),
            function (data) {
                self.vue.youare = data.youare;
                self.vue.board = data.state.board;
                self.vue.theyare = data.theyare;
                self.vue.playing = data.state.playing;
                self.vue.turn = data.state.turn;
            }
        );
    };

    self.auto_refresh = function () {
        setInterval(
            self.refresh, 2000
        )
    };

    self.start_play = function () {
        self.vue.disable_game_input = true;
        self.refresh();
        self.auto_refresh();
    };

    // Complete as needed.
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            youare: '',
            theyare: '',
            board: ['', '', '', '', '', '', '', '', ''],
            board_string: '',
            turn: '',
            playing: [],
            game_name: '',
            disable_game_input: false
        },
        methods: {
            play: self.play,
            refresh: self.refresh,
            start_play: self.start_play
        }

    });


    $("#vue-div").show();
    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
