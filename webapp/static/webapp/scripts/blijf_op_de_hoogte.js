$(document).ready(function() {
  $('#contact_form').bootstrapValidator({
      // To use feedback icons, ensure that you use Bootstrap v3.1.0 or later
      feedbackIcons: {
          valid: 'glyphicon glyphicon-ok',
          invalid: 'glyphicon glyphicon-remove',
          validating: 'glyphicon glyphicon-refresh'
      },
      fields: {
          first_name: {
              validators: {
                      stringLength: {
                      min: 2,
                      message: 'Vul een voornaam in alstublieft'
                  },
                      notEmpty: {
                      message: 'Vul een geldige voornaam in alstublieft'
                  }
              }
          },
           last_name: {
              validators: {
                   stringLength: {
                      min: 2,
                      message: 'Vul een achternaam in alstublieft'
                  },
                  notEmpty: {
                      message: 'Vul een geldige achternaam in alstublieft'
                  }
              }
          },
          email: {
              validators: {
                  notEmpty: {
                      message: 'Vul een email adres in alstublieft'
                  },
                  emailAddress: {
                      message: 'Vul een geldig email adres in alstublieft'
                  }
              }
          },
          street: {
              validators: {
                   stringLength: {
                      min: 8,
                      message: 'Vul een straatnaam in alstublieft'
                  },
                  notEmpty: {
                      message: 'Vul een geldige straatnaam in alstublieft'
                  }
              }
          },
          house_number: {
              validators: {
                  notEmpty: {
                      message: 'Vul een geldig huisnummer in alstublieft'
                  }
              }
          },
          city: {
              validators: {
                   stringLength: {
                      min: 3,
                      message: 'Vul een gemeente in alstublieft'
                  },
                  notEmpty: {
                      message: 'Vul een geldige gemeente in alstublieft'
                  }
              }
          },
          postcode: {
              validators: {
                  notEmpty: {
                      message: 'Vul een postcode in alstublieft'
                  },
                  zipCode: {
                      country: 'BE',
                      message: 'Vul een geldige postcode in alstublieft'
                  }
              }
          },
        }
      })
      .on('success.form.bv', function(e) {
          $('#success_message').slideDown({ opacity: "show" }, "slow") // Do something ...
              $('#contact_form').data('bootstrapValidator').resetForm();

          // Prevent form submission
          e.preventDefault();

          // Get the form instance
          var $form = $(e.target);

          // Get the BootstrapValidator instance
          var bv = $form.data('bootstrapValidator');

          // Use Ajax to submit form data
          $.post($form.attr('action'), $form.serialize(), function(result) {
              console.log(result);
          }, 'json');
      });
});
