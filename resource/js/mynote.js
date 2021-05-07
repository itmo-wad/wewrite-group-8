function showLogin() {
    $("#login").addClass("active");
    $("#reg").removeClass("active");
    $("#find").removeClass("active");
    $("#loginpanel").addClass("active");
    $("#regpanel").removeClass("active");
    $("#findpanel").removeClass("active");
    $('#mymodal').modal('show');
}

function showReg() {
    $("#login").removeClass("active");
    $("#reg").addClass("active");
    $("#find").removeClass("active");
    $("#loginpanel").removeClass("active");
    $("#regpanel").addClass("active");
    $("#findpanel").removeClass("active");
    $('#mymodal').modal('show');
}



function doSendMail(obj) {
    var email = $.trim($("#regname").val());
    if (!email.match(/.+@.+\..+/)) {
        bootbox.alert({title:"Error message", message:"The email address format is incorrect."});
        $("#regname").focus();
        return false;
    }
    $.post('/ecode', 'email=' + email, function (data) {
        if (data == 'email-invalid') {
             bootbox.alert({title:"Error message", message:"The email address format is incorrect."});
            $("#regname").focus();
            return false;
        }
        if (data == 'send-pass') {
            bootbox.alert({title:"Error message", message:"The email verification code has been successfully sent, please check."});
            $("#regname").attr('disabled', true);
            $(obj).attr('disabled', true);
            return false;
        }
        else {
            bootbox.alert({title:"Error message", message:"The email verification code was not sent successfully."});
            return false;
        }
    })
}

function doReg(e) {
    if (e != null && e.keyCode != 13) {
        return false;
    }

    var regname = $.trim($("#regname").val());
    var regpass = $.trim($("#regpass").val());
    var regcode = $.trim($("#regcode").val());

    if (!regname.match(/.+@.+\..+/) || regpass.length < 5) {
        bootbox.alert({title:"Error message", message:"Incorrect email address or password less than 5 characters."});
        return false;
    }
    else {
        param = "username=" + regname;
        param += "&password=" + regpass;
        param += "&ecode=" + regcode;
        $.post('/user', param, function (data) {
            if (data == "ecode-error") {
                bootbox.alert({title:"Error message", message:"Invalid verification code."});
                $("#regcode").val('');
                $("#regcode").focus();
            }
            else if (data == "up-invalid") {
                bootbox.alert({title:"Error message", message:"Incorrect email address or password less than 5 characters."});
            }
            else if (data == "user-repeated") {
                bootbox.alert({title:"Error message", message:"The user name has already been registered."});
                $("#regname").focus();
            }
            else if (data == "reg-pass") {
                bootbox.alert({title:"message", message:"Congratulations, you have successfully registered."});
                setTimeout('location.reload();', 1000);

            }
            else if (data == "reg-fail") {
                bootbox.alert({title:"Error message", message:"Registration failed, please contact administrator."});
            }
        });
    }
}

function doLogin(e) {
    if (e != null && e.keyCode != 13) {
        return false;
    }

    var loginname = $.trim($("#loginname").val());
    var loginpass = $.trim($("#loginpass").val());
    var logincode = $.trim($("#logincode").val());

    if (loginname.length < 5 || loginpass.length < 5) {
        bootbox.alert({title:"Error message", message:"The user name and password are less than 5 characters."});
        return false;
    }
    else {
        var param = "username=" + loginname;
        param += "&password=" + loginpass;
        param += "&vcode=" + logincode;
        $.post('/login', param, function (data) {
            if (data == "vcode-error") {
                bootbox.alert({title:"Error message", message:"Invalid verification code."});
                $("#logincode").val('');
                $("#logincode").focus();
            }
            else if (data == "login-pass") {
                bootbox.alert({title:"message", message:"Congratulations! Login successfully."});
                setTimeout('location.reload();', 1000);

            }
            else if (data == "login-fail") {
                bootbox.alert({title:"Error message", message:"Logon failed, please contact administrator."});
            }
        });
    }
}



$(document).ready(function () {
    $.get('/loginfo', function (data) {
        content = '';
        if (data == null) {
            content += '<a class="nav-item nav-link" href="#" onclick="showLogin()"> login</a>';
            content += '<a class="nav-item nav-link" href="#" onclick="showReg()">registered</a>';
        }
        else {
            content += '<a class="nav-item nav-link" href="/ucenter">You are welcome：' + data["nickname"] + '</a>&nbsp;&nbsp;&nbsp;';
            if (data['role'] == 'admin') {
                content += '<a class="nav-item nav-link" href="/admin">System management</a>&nbsp;&nbsp;&nbsp;';
            }
            else {
                content += '<a class="nav-item nav-link" href="/ucenter">The user center</a>&nbsp;&nbsp;&nbsp;';
            }
            content += '<a class="nav-item nav-link" href="/logout">logout</a>';
        }
        $("#loginmenu").append(content);
    });
});
