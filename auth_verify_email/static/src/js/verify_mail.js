odoo.define('auth_verify_email.verify_mail', function (require) {
    'use strict';

    $(document).ready(function() {
        $('.verify_email_btn').click(function() {
            $("#uEmail").text($("#aEmail").val());
            $("#modalVerifyEmail").modal('show');
        });

        $('.askmelater').click(function() {
            $("#modalVerifyEmail").modal('hide');
            const now = new Date();
            const item = {
                expiry: now.getTime() + 3600 * 1000, // Expiry in 1 hour
            };
            localStorage.setItem("hideverifymodal", JSON.stringify(item));
        });

        $("#subbtn").click(function(ev) {
            ev.preventDefault();
            $.ajax({
                type: "POST",
                url: "/verify/email",
                data: $("#verifyemail").serialize(),
                beforeSend: function() {
                    $("#o_loader").removeClass("d-none");
                },
                success: function(data, textStatus, jqXHR) {
                    $("#o_loader").addClass("d-none");
                    // Check if the response is HTML
                    if (typeof data === "string" && data.trim().startsWith('<!DOCTYPE html>')) {
                        // The response is an HTML page, not the expected JSON
                        console.error('Expected JSON, but got HTML. User might not be authenticated.');
                        // Redirect to the login page or show an error message
                        window.location.href = "/web/login";
                    } else {
                        // Assuming the response is JSON
                        try {
                            var payload = JSON.parse(data); // Parsing JSON data
                            $("#otp").removeClass("d-none");
                            $("#subbtn").val("Verify OTP");
                            if (payload && payload['reload'] === true) {
                                window.location.reload();
                            }
                        } catch (e) {
                            console.error("Error parsing response as JSON:", e);
                            // Handle parsing error here
                        }
                    }
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    $("#o_loader").addClass("d-none");
                    console.error("AJAX error: ", textStatus, ", Details: ", errorThrown);
                    // Handle AJAX error here, such as displaying an error message to the user
                }
            });
        });

        function _checkEmailAddress() {
            let showMailModal = localStorage.getItem("hideverifymodal");
            let show = true;
            if (showMailModal) {
                const item = JSON.parse(showMailModal);
                const now = new Date();
                if (now.getTime() < item.expiry) {
                    show = false;
                } else {
                    localStorage.removeItem("hideverifymodal");
                }
            }
            if (show) {
                var verified = $("#authmailverified").val();
                var email = $("#authmail").val();
                if (verified !== 'True' && email !== '') {
                    $("#uEmail").text(email);
                    $("#modalVerifyEmail").modal('show');
                    return false;
                }
            }
            return true;
        }

        _checkEmailAddress();
    });
});
