var main = function() {

    $('#id_photo').change(function() {
        if (this.files && this.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $('.photo').attr('src', e.target.result);
            }

            reader.readAsDataURL(this.files[0]);

            $('#photo-clear_id').prop('checked',  false);
        }
    });
}

$(document).ready(main);
