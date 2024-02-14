odoo.define('patient_intake_configuration.FieldZip', function (require) {
    "use strict";

    var basic_fields = require('web.basic_fields');
    var registry = require('web.field_registry');

    var FieldZip = basic_fields.InputField.extend({
        className: 'o_field_zip',
        supportedFieldTypes: ['char'],

        events: _.extend({}, basic_fields.InputField.prototype.events, {
            'input': '_onInput',
            'keypress': '_onKeyPress',
        }),

        _onInput: function (event) {
            var inputVal = event.target.value;
            if (inputVal.length > 6) {
                event.target.value = inputVal.slice(0, 6);
            }
        },

        _onKeyPress: function (event) {
            var charCode = (event.which) ? event.which : event.keyCode;
            if (charCode > 31 && (charCode < 48 || charCode > 57)) {
                event.preventDefault();
            }
        },
    });

    registry.add('zip', FieldZip);

    return {
        FieldZip: FieldZip,
    };
});


