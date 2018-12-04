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

    self.open_uploader = function () {
        $("div#uploader_div").show();
        self.vue.is_uploading = true;
    };

    self.close_uploader = function () {
        $("div#uploader_div").hide();
        self.vue.is_uploading = false;
        $("input#file_input").val(""); // This clears the file choice once uploaded.

    };

    self.upload_file = function (event, post_idx) {
        // This function is in charge of:
        // - Creating an image preview
        // - Uploading the image to GCS
        // - Calling another function to notify the server of the final image URL.

        var blog_post_id = post_idx; // TODO: you really have here to do something like:
        // post = self.vue.posts[post_idx];
        // var blog_post_id = post.id;

        // Reads the file.
        var input = event.target;
        var file = input.files[0];
        if (file) {
            // We want to read the image file, and transform it into a data URL.
            var reader = new FileReader();
            // We add a listener for the load event of the file reader.
            // The listener is called when loading terminates.
            // Once loading (the reader.readAsDataURL) terminates, we have
            // the data URL available.
            reader.addEventListener("load", function () {
                // An image can be represented as a data URL.
                // See https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URIs
                // Here, we set the data URL of the image contained in the file to an image in the
                // HTML, causing the display of the file image.
                self.vue.img_url = reader.result;
                $.post(image_post_url, {
                    image_url: reader.result,
                    blog_post_id: blog_post_id // Placeholder for more useful info.
                });
            }, false);
            // Reads the file as a data URL. This triggers above event handler.
            reader.readAsDataURL(file);
        }
    };

    //         // Now we should take care of the upload.
    //         // Gets an upload URL.
    //         console.log("Trying to get the upload url");
    //         $.getJSON('https://upload-dot-luca-teaching.appspot.com/start/uploader/get_upload_url',
    //             function (data) {
    //                 // We now have upload (and download) URLs.
    //                 // The PUT url is used to upload the image.
    //                 // The GET url is used to notify the server where the image has been uploaded;
    //                 // that is, the GET url is the location where the image will be accessible
    //                 // after the upload.  We pass the GET url to the upload_complete function (below)
    //                 // to notify the server.
    //                 var put_url = data['signed_url'];
    //                 var get_url = data['access_url'];
    //                 console.log("Received upload url: " + put_url);
    //                 // Uploads the file, using the low-level interface.
    //                 var req = new XMLHttpRequest();
    //                 // We listen to the load event = the file is uploaded, and we call upload_complete.
    //                 // That function will notify the server of the location of the image.
    //                 req.addEventListener("load", self.upload_complete(get_url));
    //                 // TODO: if you like, add a listener for "error" to detect failure.
    //                 req.open("PUT", put_url, true);
    //                 req.send(file);
    //             });
    //     }
    // };


    // self.upload_complete = function(get_url) {
    //     // Hides the uploader div.
    //     self.vue.show_img = true;
    //     self.close_uploader();
    //     console.log('The file was uploaded; it is now available at ' + get_url);
    //     // TODO: The file is uploaded.  Now you have to insert the get_url into the database, etc.
    // };

    self.get_image = function () {
        $.getJSON(image_get_url,
            {
                blog_post_id: 1,
            },
            function (data) {
                self.vue.received_image = data.image_str;
            }
            )
    };

    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            is_uploading: false,
            img_url: null,
            received_image: null,
            show_img: false,
            self_page: true // Leave it to true, so initially you are looking at your own images.
        },
        methods: {
            open_uploader: self.open_uploader,
            close_uploader: self.close_uploader,
            upload_file: self.upload_file,
            get_image: self.get_image
        }

    });

    $("#vue-div").show();

    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});

