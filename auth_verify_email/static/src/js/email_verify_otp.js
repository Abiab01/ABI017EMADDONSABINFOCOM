odoo.define('auth_verify_email.verify_mail_otp', function(require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var ajax = require('web.ajax');

    publicWidget.registry.OtpButton = publicWidget.Widget.extend({
        selector: '.oe_signup_form',
        events: {
            'click .send_otp_button': '_onSendOtpClick',
            'click .resend_otp_button': '_onResendOtpClick',
            'submit': '_onFormSubmit',  // This will capture the submit event of the form
        },

        start: function() {
            this._super.apply(this, arguments);
            this.failedAttempts = 0;  // Initialize the counter for failed attempts
            //this.$otpInput = this.$("input[name='otp']");
            this.$emailInput = this.$("input[name='login']");
            this.$sendOtpBtn = this.$(".send_otp_button");
            this.$resendOtpBtn = this.$(".resend_otp_button").hide();  // Hide the resend button initially
            this.$('.oe_login_buttons').hide();
            this.$('.oe_login_auth').hide();
            this.$otpInput = this.$("input[name='otp']").hide();

        },

        _onSendOtpClick: function(ev) {
            ev.preventDefault();
            var email = this.$emailInput.val();
            if (email) {
                this.$sendOtpBtn.prop('disabled', true); // Disable the send OTP button right after clicking
                this._sendOrResendOtp(email);
            } else {
                alert('Please enter your email address.'); // Consider updating this to a message on the page instead of an alert
            }
            this.$('.oe_login_buttons').show();
            this.$('.oe_login_auth').show();
            this.$otpInput.show();
        },

        _sendOrResendOtp: function(email) {
            var self = this;
            ajax.jsonRpc("/user/send_otp", 'call', {
                email: email,
            }).then((result) => {
                var $otpMessageContainer = this.$('.otp-message-container'); // Make sure this selector targets the correct element
                if (result.status === 'success') {
                    $otpMessageContainer.text(result.message).css('color', 'green').show();
                    // The button remains disabled. Do not re-enable it here.
                } else {
                    // In case of error, you might want to allow the user to try again.
                    // Consider your logic here, whether you want to re-enable the button or not.
                    $otpMessageContainer.text(result.message).css('color', 'red').show();
                    self.$sendOtpBtn.prop('disabled', false); // Optionally re-enable the button in case of failure
                }
            });
        },


        _onResendOtpClick: function(ev) {
            ev.preventDefault();
            var email = this.$emailInput.val();
            if (email) {
                this._sendOrResendOtp(email);
            } else {
                alert('Please enter your email address.');
            }
        },

        _onFormSubmit: function(ev) {
            ev.preventDefault(); // Prevent the form from submitting until OTP is validated

            var self = this;
            var email = this.$emailInput.val();
            var otp = this.$otpInput.val();
            var $submitButton = this.$el.find('button[type="submit"]');
            var $otpMessageContainer = this.$('.otp-message-container'); // Select the message container

            if (!email || !otp) {
                $otpMessageContainer.text('Please enter your email address and OTP.').css('color', 'red').show();
                return;
            }

            // Disable the submit button to prevent multiple submissions
            $submitButton.prop('disabled', true);

            ajax.jsonRpc("/user/validate_otp", 'call', {
                email: email,
                otp_provided: otp,
            }).then((result) => {
                if (result.status === 'success') {
                    // If OTP is valid, display a success message and trigger the form submission
                    $otpMessageContainer.text("Successfully verified email OTP.").css('color', 'green').show();
                    self.failedAttempts = 0; // Reset the counter on success
                    self.$resendOtpBtn.hide(); // Hide the resend button on success
                    self.$sendOtpBtn.show(); // Show the send button on success
                    // Submit the form after a slight delay to allow the user to see the message
                    setTimeout(function() { self.$el.get(0).submit(); }, 1000);
                } else {
                    // Increment the counter on failure
                    self.failedAttempts++;
                    // Check if failed attempts are less than 3
                    if (self.failedAttempts < 3) {
                        // Display an error message with the attempt count
                        var attemptText = self.failedAttempts + (self.failedAttempts === 1 ? "st" : self.failedAttempts === 2 ? "nd" : "rd");
                        $otpMessageContainer.text(attemptText + " attempt Wrong OTP, please enter the valid OTP.").css('color', 'red').show();
                    } else {
                        // After the third failed attempt, prompt to resend the OTP
                        $otpMessageContainer.text("Please resend OTP.").css('color', 'red').show();
                        self.$resendOtpBtn.show(); // Show the resend button
                        self.$sendOtpBtn.hide(); // Hide the send button
                    }
                    self.$otpInput.val(''); // Clear the OTP input field
                }
            }, (error) => {
                // Handle any errors here, such as network errors or server issues
                $otpMessageContainer.text("An error occurred while validating the OTP.").css('color', 'red').show();
            }).then(() => {
                // Re-enable the submit button
                $submitButton.prop('disabled', false);
            });
        },
    });
});
