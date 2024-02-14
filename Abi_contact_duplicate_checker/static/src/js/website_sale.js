odoo.define('your_module.check_email_popup', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var ajax = require('web.ajax');
    var Dialog = require('web.Dialog');

    publicWidget.registry.EmailCheckPopup = publicWidget.Widget.extend({
        selector: '.oe_website_sale', // Use the class or ID of your form
        events: {
            'submit': '_onSubmit',
        },

        _onSubmit: function (event) {
            event.preventDefault();
            var $form = $(event.currentTarget);
            var data = this._serializeFormData($form);
            var self = this;

            ajax.jsonRpc('/shop/address', 'call', data)
                .then(function (result) {
                    if (result.error) {
                        self._displayPopupError(result.error);
                    } else {
                        // If no error, proceed with form submission
                        $form.off('submit').submit();
                    }
                });
        },

        _serializeFormData: function ($form) {
            return $form.serializeArray().reduce(function (data, { name, value }) {
                data[name] = value;
                return data;
            }, {});
        },

        _displayPopupError: function (message) {
            new Dialog(this, {
                title: _t("Error"),
                size: 'medium',
                $content: $('<div/>').text(message),
                buttons: [
                    {text: _t("OK"), close: true}
                ],
            }).open();
        },
    });
});
