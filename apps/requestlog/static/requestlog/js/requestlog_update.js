var main = function() {
    var process_animation;

    $(document).on('change', 'select', function() {
        // this is an odd way to submit a form,
        // but we need onSubmit event to fire up
        // and form.submit() doesn't do this.
        var button = this.form.ownerDocument.createElement('input');
        button.style.display = 'none';
        button.type = 'submit';
        this.form.appendChild(button).click();
        this.form.removeChild(button);
    });

    $('form').ajaxForm({
        delegation: true,
        dataType:  'json',

        beforeSubmit:  function() {
            $('select').prop('disabled', true);

            $('.process_ongoing').text('Updating data');

            process_animation = setInterval(function() {
                MAX_DOTS = 8;

                status_text = $('.process_ongoing').text();

                // current step
                dots = status_text.match(/\.+$/);
                dots_num = (dots == null ? 0: dots[0].length);

                // next step
                dots_num = ++dots_num % (MAX_DOTS + 1);
                dots = Array(dots_num+1).join('.');

                status_text = status_text.replace(/\.+$/, ''); // clear current dots
                $('.process_ongoing').text(status_text + dots); // place new dots
            }, 200);
        },

        complete: function() {
            // update requests table after priority change
            $.get('/requests/', function(data){
                $('tbody').html(data.table);

                $('select').prop('disabled', false);
                $('.process_ongoing').html('&nbsp');
                clearInterval(process_animation);
            });
        }
    });
}

$(document).ready(main);