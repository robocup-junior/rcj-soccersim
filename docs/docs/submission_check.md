# Check of the ZIP submission

Before you upload the code for your robots, you can check below whether
the submission conforms to the required structure and contains necessary data.

<form action="#">
    <label for="zipinput">Choose ZIP file</label>
    <input type="file" id="zipinput" name="zipinput" accept=".zip">
</form>

<div id="zip-error" style="color: red; margin-top: 30px;"></div>
<div id="zip-success" style="color: green;"></div>

<script src="https://robocupjuniortc.github.io/rcj-soccer-sim/js/zip.min.js"></script>
<script src="https://robocupjuniortc.github.io/rcj-soccer-sim/js/submission_check.js"></script>
<script>
    function init() {
        var fileInput = document.getElementById("zipinput");
        fileInput.addEventListener("change", function(event) {
            const reader = new zip.ZipReader(new zip.BlobReader(fileInput.files[0]));

            var zip_error = document.getElementById("zip-error");
            var zip_success = document.getElementById("zip-success");
            zip_error.innerHTML = "";
            zip_success.innerHTML = "";

            reader.getEntries().then(function(entries) {
                var errors = get_submission_errors(reader.reader.size, entries);

                if (errors.length > 0) {
                    var error_msg = "<ul>";
                    for (var i = 0; i < errors.length; i++) {
                        error_msg += "<li>" + errors[i] + "</li>";
                    }
                    error_msg += "</ul>";
                    zip_error.innerHTML = error_msg;
                } else {
                   zip_success.innerHTML = "Your ZIP file looks OK!" 
                }
            }).catch(function(e) {
                zip_error.innerHTML = "Failed to load your submission. Check whether it is correct ZIP file!";
            });
        });
    }

    window.addEventListener("load", init, false);
</script>
