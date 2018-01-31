$(document).ready(function(){
    // Checking if the password is of django format
    var passWordBoxSelector = $("input[name='new-password']"),
        retypePassWordBoxSelector = $("input[name='retype-password']");
    $("input[name='new-password'], input[name='retype-password']").on('keyup', function () {
        // Password validation
        var validationRe = /^(?=.*?[a-z]).{8,}$/,
            typedPassWord = passWordBoxSelector.val(),
            messageSpanSelector = $("#message");
        if (typedPassWord.match(validationRe)) {
            messageSpanSelector.addClass("offset-md-2");
            // Checking match pattern
            if (passWordBoxSelector.val() == retypePassWordBoxSelector.val()) {
                messageSpanSelector.html('Passwords matched!').removeClass('text-danger').addClass('text-success');
                $("button[name='submit']").show();
            } else {
                messageSpanSelector.html('Passwords are not matching').removeClass('text-success').addClass('text-danger');
                $("button[name='submit']").hide();
            }
        } else {
            messageSpanSelector.removeClass("offset-md-2");
            messageSpanSelector.html('Password must be of minimum 8 characters with at least one letter').removeClass('text-success').addClass('text-danger');
            $("button[name='submit']").hide();
        }
    });// Keyup events
});