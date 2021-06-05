$(function () {
    checkNav();
    // clicking in navbar
    // showing description in 1. section


    $('nav li a').click(function (e) {

        var thisEl = $(this).parent();
        if ($(this).data('scroll') != null) {
            e.preventDefault();
            console.log($(this).data('scroll') + ' clicked');

            $('html,body').animate({
                scrollTop: ($('#' + $(this).data('scroll')).offset().top - $('nav').height() * 0.5) // to make  h2 appear
            }, function () {

                // console.log('a clicked')
                $(thisEl).addClass('active').parent().siblings().each(function () {
                    $(this).children().removeClass('active');
                }
                );

            });
            $(window).scroll(function () {
                // console.log('nav scrolling')
            })
        }
    });

    // for navbar check to see if hidden
    var count = 0,
        count2 = 0,
        scrollTop2 = $(window).scrollTop();
    $('.nav-btn').click(function () {


        if ($(this).hasClass('left')) {

            $('nav ').addClass('hidden');
            count = 0;
        } else {
            // console.log('right clicked');
            $('nav ').removeClass('hidden');
            var btn = $(this);
            $('nav ').animate({
                marginLeft: '0px'
            }, 700, function () {
            });
            $(btn).fadeOut(200, function () {
                $(this).children().children().removeClass('fa-chevron-right').addClass('fa-chevron-left');
                $(this).fadeIn(200);
                $(this).removeClass('right').addClass('left');
            })
        }


    });
    // end of clicking

    color_list = ['gold', '#44bd32', '#00a8ff', '#e84118', '#273c75', '#353b48', '#4cd137', '#7f8fa6', '#8c7ae6', '#44bd32']
    var activeSection = 0;
    $(window).scroll(checkNav);
    // window.onerror = function () {
    //   console.log('errrrrorrrrr')
    // }
    // window.addEventListener('error', function (e) {
    //   console.log('errror');
    // }, true);
    function checkNav() {
        $('.section').each(function () {
            var sectionID = $(this).attr('id');

            if ($(window).scrollTop() >= $(this).offset().top - 50 - $('nav').height()) {
                $('#' + sectionID).addClass('active').siblings().each(function () {
                    $(this).removeClass('active');
                });;
                $('nav li a[data-scroll="' + sectionID + '"]').addClass('active').parent().siblings().each(function () {
                    $(this).children().removeClass('active');
                });
                if (sectionID == 4) {
                    $('.animated-progress span').each(function () {
                        $(this).animate({
                            width: $(this).data('progress') + '%'
                        }, 1000, function () {
                            $(this).text($(this).data('progress') + '%')
                        });
                    });
                }
            }

        });



        var st = $(window).scrollTop();
        if (scrollTop2 > st) {

            count = 0;

        } else if (scrollTop2 < st) {
            // } else if (scrollTop2 < st && $(window).width() < 780) {


            var height = $('nav ul').height(),
                btn = $('.nav-btn');

            // count to check if nav bar is hidden once
            if (count < 1 && !$('nav ').hasClass('hidden')) {
                // console.log(count + '   ' + $('nav ').hasClass('hidden'))

                $('nav ').addClass('hidden');
                $('nav ').animate({

                    marginLeft: '-100%'
                }, 1000);
                $(btn).fadeOut(200, function () {
                    $(this).removeClass('left').addClass('right');

                    $(this).children().children().removeClass('fa-chevron-left').addClass('fa-chevron-right');
                    $(this).fadeIn(200);

                });
                count = 0;
                count2 = 1;
            }

        }
        scrollTop2 = st

    }

});