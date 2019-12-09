(function($) {

	"use strict";


    /*------------------------------------------
        = Slicknav
    -------------------------------------------*/

    function slicknav() {
      $('#menu').slicknav();  
    }


    /*------------------------------------------
        = HIDE PRELOADER
    -------------------------------------------*/
    function preloader() {
        if($('.preloader').length) {
            $('.preloader').delay(100).fadeOut(500, function() {

                //active wow
                wow.init();

            });
        }
    }


    // Parallax background
    function bgParallax() {
        if ($(".parallax").length) {
            $(".parallax").each(function() {
                var height = $(this).position().top;
                var resize     = height - $(window).scrollTop();
                var parallaxSpeed = $(this).data("speed");
                var doParallax = -(resize / parallaxSpeed);
                var positionValue   = doParallax + "px";
                var img = $(this).data("bg-image");

                $(this).css({
                    backgroundImage: "url(" + img + ")",
                    backgroundPosition: "50%" + positionValue,
                    backgroundSize: "cover"
                });

                if ( window.innerWidth < 780) {
                    $(this).css({
                        backgroundPosition: "center center"
                    });
                }
            });
        }
    }



    /*------------------------------------------
        = Roboto Slider SETTING
    -------------------------------------------*/

    // roboto slider background setting
    function sliderBgSetting() {
        if ($(".roboto-slider .slide").length) {
            $(".roboto-slider .slide").each(function() {
                var $this = $(this);
                var img = $this.find(".slider-bg").attr("src");

                $this.css({
                    backgroundImage: "url("+ img +")",
                    backgroundSize: "cover",
                    backgroundPosition: "center center"
                })
            });
        }
    }


    //Setting roboto slider
    function robotoSlider() {
        if ($(".roboto-slider").length) {
            $(".roboto-slider").slick({
                arrows: true,
                prevArrow: '<button type="button" class="slick-prev">Previous</button>',
                nextArrow: '<button type="button" class="slick-next">Next</button>',
                dots: true,
                fade: true,
                cssEase: 'linear',
                autoplay: true,
                autoplaySpeed: 6000
            });
        }
    }

    /*------------------------------------------
        = WOW ANIMATION SETTING
    -------------------------------------------*/
    var wow = new WOW({
        boxClass:     'wow',      // default
        animateClass: 'animated', // default
        offset:       0,          // default
        mobile:       true,       // default
        live:         true        // default
    });



    /*------------------------------------------
        = OWL CAROUSEL SLIDER
    -------------------------------------------*/

    //owl-Carousel-OneColumn
    $('.owl-column1').owlCarousel({
        loop:true,
        autoplay: 5000,
        autoplayHoverPause:false,
        smartSpeed: 700,
        items: 1,
        margin:15,
        dots: true,
        nav:true,
        navText: [
          '<i class="fa fa-angle-left"></i>',
          '<i class="fa fa-angle-right"></i>'
        ]
    });

    //owl-Carousel-TwoColumn
    $('.owl-column2').owlCarousel({
        loop:true,
        autoplay: 5000,
        autoplayHoverPause:false,
        smartSpeed: 700,
        items: 2,
        margin:30,
        dots: true,
        nav:true,
        navText: [
          '<i class="fa fa-angle-left"></i>',
          '<i class="fa fa-angle-right"></i>'
        ],
        responsive:{
          0:{
            items:1
          },
          480:{
            items:1
          },
          600:{
            items:2
          },
          800:{
            items:2
          },
          1024:{
            items:2
          },
          1200:{
            items:2
          }
        }
    });

    //owl-Carousel-TwoColumn
    $('.owl-column3').owlCarousel({
        loop:true,
        autoplay: 5000,
        autoplayHoverPause:false,
        smartSpeed: 700,
        items: 3,
        margin:30,
        dots: true,
        nav:true,
        navText: [
          '<i class="fa fa-angle-left"></i>',
          '<i class="fa fa-angle-right"></i>'
        ],
        responsive:{
          0:{
            items:1
          },
          480:{
            items:1
          },
          600:{
            items:1
          },
          800:{
            items:2
          },
          1024:{
            items:2
          },
          1200:{
            items:3
          }
        }
    });


    /*----------------------
    Client
    ------------------------*/
    $('.owl-client').owlCarousel({
        loop:true,
        autoplay: 5000,
        autoplayHoverPause:false,
        smartSpeed: 700,
        items: 3,
        margin:30,
        dots: true,
        nav:false,
        navText: [
          '<i class="fa fa-angle-left"></i>',
          '<i class="fa fa-angle-right"></i>'
        ],
        responsive: {
            0: {
                items: 2
            },
            480: {
                items: 3
            },
            760: {
                items: 4
            },
            1024: {
                items: 4
            },
            1920: {
                items: 5
            }
        }
    });

    /*----------------------
    Counter
    ------------------------*/
    function counterUpFunfact() {

        $('.counter').counterUp({
            delay: 10,
            time: 1000
        });        
    }


    /*----------------------
    Masonary
    ------------------------*/
    $('.gallery-content').imagesLoaded(function() {

        var $grid = $('.gallery-content').isotope({
            itemSelector: '.gallery_item',
            percentPosition: true,
            masonry: {
                columnWidth: '.gallery_item',
            }
        });

        // filter items on button click
        $('.filter-button-group').on( 'click', 'button', function() {
          var filterValue = $(this).attr('data-filter');
          $grid.isotope({ filter: filterValue });
        });

        $('.project-menu button').on('click', function(event) {
             $(this).siblings('.active').removeClass('active');
             $(this).addClass('active');
             event.preventDefault();
         });
        
    });


    /*------------------------------------------
        = Magnific Popup
    -------------------------------------------*/


    // gallery link setting
    $('.gallery-content').magnificPopup({
      delegate: 'a', // child items selector, by clicking on it popup will open
      type: 'image',
      gallery:{
        enabled:true
      }
    });

    // video popup  setting
    $('.video-popup').magnificPopup({
        type: 'iframe',
        gallery: {
            enabled: true
        }

    });

/*------------------------------------------
        = BACK TO TOP BTN SETTING
    -------------------------------------------*/
    $("body").prepend("<a href='#'' class='back-to-top hvr-pulse-grow animated'><i class='fa fa-long-arrow-up'></i></a>");

    function toggleBackToTopBtn() {
        var amountScrolled = 300;
        if ($(window).scrollTop() > amountScrolled) {
            $("a.back-to-top").fadeIn("slow");
        } else {
            $("a.back-to-top").fadeOut("slow");
        }
    }

    $(".back-to-top").on("click", function() {
        $("html,body").animate({
            scrollTop: 0
        }, 700);
        return false;
    })



    /*==========================================================================
        WHEN DOCUMENT LOADING
    ==========================================================================*/
    $(window).on('load', function() {

        preloader();
        sliderBgSetting();
        robotoSlider();

     });

    /*==========================================================================
        WHEN WINDOW READY
    ==========================================================================*/
    $(document).on('ready', function() {

        slicknav();
        counterUpFunfact();
        bgParallax();

    });


    /*==========================================================================
        WHEN WINDOW SCROLL
    ==========================================================================*/
    $(window).on("scroll", function() {

        toggleBackToTopBtn();
        bgParallax();

    });

    /*==========================================================================
        WHEN WINDOW RESIZE
    ==========================================================================*/
    $(window).on("resize", function() {

    });

})(window.jQuery);
