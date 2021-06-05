
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
$(function () {

    $('.contactme-main .next-btn').click(function () {
        console.log('next-btn clicked');
        // $('.contactme-main .contactme-info').hide();
        var empty = false;
        $('.contactme-main .contactme-form input').not('[type="file"]').each(function () {
            if ($(this).val() == '' || $(this).val() == undefined) {
                empty = true;
                $(this).addClass('message-missing');
            }

        });
        if (!empty) {
            console.log('not empty');
            $('.contactme-main .contactme-form .contactme-info').fadeOut();
            $(this).fadeOut();
            $('.contactme-main .prev-btn').fadeIn();
            $('.contactme-main .submit-btn').fadeIn();


        }
    });
    $('.contactme-main .prev-btn').click(function () {
        $('.contactme-main .contactme-form .contactme-info').fadeIn();
        $(this).fadeOut();
        $('.contactme-main .next-btn').fadeIn()

    });
    $('.contactme-main .submit-btn').click(function () {
        $('.contactme-main .contactme-form .contactme-message').fadeOut();

        const csrftoken = getCookie('csrftoken');

        $('.contactme-main .contactme-btn').fadeOut()
        $.ajax({
            type: 'GET',
            url: $('.contactme-form').data('action'),
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function (data) {
                $('.contactme-main  svg').animate({
                    opacity: '1'
                }, function () {
                    $('.contactme-main .tags').fadeIn()
                });

                $(this).fadeOut();
                console.log(data.count)
                console.log(data.total)
            },

        });

    });
    $('.contactme-main .contactme-form input').on('input', function () {
        $(this).removeClass('message-missing');
    });

});