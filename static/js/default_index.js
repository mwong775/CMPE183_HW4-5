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
        console.log(post_idx);
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
            }, false);
            // Reads the file as a data URL. This triggers above event handler.
            reader.readAsDataURL(file);

            // Now we should take care of the upload.
            // Gets an upload URL.
            console.log("Trying to get the upload url");
            $.getJSON(get_upload_url, // Signed
                function (data) {
                    // We now have upload (and download) URLs.
                    // The PUT url is used to upload the image.
                    // The GET url is used to notify the server where the image has been uploaded;
                    // that is, the GET url is the location where the image will be accessible
                    // after the upload.  We pass the GET url to the upload_complete function (below)
                    // to notify the server.
                    var put_url = data['signed_url'];
                    var image_name = data['image_name'];
                    console.log("Received upload url: " + put_url);
                    // Uploads the file, using the low-level interface.
                    var req = new XMLHttpRequest();
                    // We listen to the load event = the file is uploaded, and we call upload_complete.
                    // That function will notify the server of the location of the image.
                    req.addEventListener("load", self.upload_complete(image_name));
                    // TODO: if you like, add a listener for "error" to detect failure.
                    req.open("PUT", put_url, true);
                    req.send(file);
                });
        }
    };


    self.upload_complete = function(image_name) {
        // Hides the uploader div.
        self.vue.show_img = true;
        self.close_uploader();
        console.log('The file was uploaded; its name is: ' + image_name);
        // The file is uploaded.  We have to let the server know.
        $.post(upload_notification_url,
            {
                image_name: image_name,
                post_id: 1, // This is a stand-in for any kind of data you need to associate
                // with the image.
            },
            function () {
                // Here you can for instance show a notification icon.
            }
        );
    };

    self.get_image = function () {
        // TODO: We need to first ask the server what's the image name,
        // and then we need to ask the server to give us a GET URL for an image of that name.
        $.getJSON(get_image_url, // https://host/app/api/get_image_url?post_id=4
            {
                post_id: 1,
            },
            function (data) {
                self.vue.received_image = data.image_url;
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

