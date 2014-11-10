var main = function() {
    var process_animation;

    // style datepicker widget
    $('input#id_birth').removeClass('form-control')
                       .removeAttr('readonly');

    $('form').ajaxForm({
        dataType:  'json',

        beforeSubmit:  function() {
            $('form :input').prop('disabled', true);
            $('form .glyphicon-calendar').parent().hide();
            $('form a').hide();
            $('.person_form_errors').hide(350);
            $('.errors_content').empty();

            $('.person_form_status').text('Updating data')
                                    .removeClass('process_success process_error')
                                    .addClass('process_ongoing');

            process_animation = setInterval(function() {
                MAX_DOTS = 8;

                status_text = $('.person_form_status').text();

                // current step
                dots = status_text.match(/\.+$/);
                dots_num = (dots == null ? 0: dots[0].length);

                // next step
                dots_num = ++dots_num % (MAX_DOTS + 1);
                dots = Array(dots_num+1).join('.');

                status_text = status_text.replace(/\.+$/, ''); // clear current dots
                $('.person_form_status').text(status_text + dots); // place new dots
            }, 200);
        },

        complete: function() {
            $('form :input').prop('disabled', false);
            $('form .glyphicon-calendar').parent().show();
            $('form a').show();

            clearInterval(process_animation);
        },

        success: function(data) {
            $('.person_form_status').text('Data updated')
                                    .removeClass('process_ongoing')
                                    .addClass('processsuccess');

            // reset photo name
            $('#id_photo').wrap('<form>').closest('form').get(0).reset();
            $('#id_photo').unwrap();
            // if photo was cleared, update page accordingly
            if ($('#photo-clear_id').prop('checked')) {
                $('.photo').attr('src', STATIC_URL + 'person/img/no_photo_available.jpg');
            }

        },

        error: function(response) {
            data = JSON.parse(response.responseText);

            // show errors form errors on page
            $.each(data.errors, function(field_name, field_errors) {
                $('<p>').addClass('labels').text(field_name)
                        .appendTo($('.errors_content'));

                $ul = $('<ul>').addClass('errorlist');

                $.each(field_errors, function(index, error) {
                    $('<li>').text(error).appendTo($ul);
                });

                $('.errors_content').append($ul);
            });

            $('.person_form_errors').show(350);
            $('.person_form_status').text('Failed to update. See errors below')
                                    .removeClass('process_ongoing')
                                    .addClass('process_error');
        }
    });
}

$(document).ready(main);