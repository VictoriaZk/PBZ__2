$(document).ready(function() {

    $('#submit').on('click', function(e) {
        e.preventDefault();
        var form = $('#a-submit-form');
        form.attr("method", "post");
        form.submit();
    });
});
