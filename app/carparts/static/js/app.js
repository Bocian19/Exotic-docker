
$(document).ready(function(){

    // console.log($("#django_instagram_media_wall"));

    $('[data-toggle="tooltip"]').tooltip();

  $('.carousel').on('click', 'a#load_more', function(e) {


        const colums_to_show = $('#carousel-col.show-1');
        if (colums_to_show[4].nextElementSibling.nextElementSibling) {
            console.log(colums_to_show[4].nextElementSibling.nextElementSibling);
            const column_target = colums_to_show[4].nextElementSibling.nextElementSibling
            const page = column_target.getAttribute('data-page');

            $.ajax({
                method: "GET",
                url: '/load/' + page,
                success: function (result) {
                    $(`div[data-page="${page}"]`).html($(`div[data-page="${page}"]`, result).html());
                }
            });


            colums_to_show[4].nextElementSibling.classList.remove('hide');
            colums_to_show[0].classList.add('hide');
            colums_to_show[0].classList.remove('show-1');
            colums_to_show[4].nextElementSibling.classList.add('show-1');
            e.preventDefault();
        } else {
            return false;
        }
      });


      $('.carousel').on('click', 'a#load-back', function (e) {

          const colums_to_show = $('#carousel-col.show-1');
          if (colums_to_show[0].previousElementSibling) {
              colums_to_show[0].previousElementSibling.classList.remove('hide');
              colums_to_show[4].classList.add('hide');
              colums_to_show[0].previousElementSibling.classList.add('show-1');
              colums_to_show[4].classList.remove('show-1');
              e.preventDefault();
          }
          return false;

      });

// creating border on clicked thumbnail
      $('div#small-thumbnail').on('click', function () {

          $('div#large-thumbnail')[0].innerHTML = this.innerHTML;

          const active = document.querySelector('.active-thumbnail');
          if (active) {
              active.classList.remove('active-thumbnail');
          }
          this.firstChild.classList.add('active-thumbnail');
          $('#large-thumbnail')[0].firstChild.classList.add('product-thumbnail');
      });

      $(document).on('click', 'label[id=brand-label]', function () {
          this.style.backgroundColor = "#a9a9a9";
          const active = $("input[name=brand]:checked");
          if (active) {
              console.log(active);
          }
          this.previousElementSibling.setAttribute('checked', "checked");
          $('#form-filter').submit();
      })
      $('.myCarousel').carousel({
          interval: 2000
      })

      $(document).on('click', '#collapse-starter', function () {
          $('div.delivery-info').slideToggle();
      })
      $(document).on('click', '#collapse-starter-2', function () {
          $('div.part-number-info').slideToggle();
      })

      $(document).on('click', '#collapse-starter-3', function () {
          $('div.order').slideToggle();
      })

      $(function () {
          $(".pulse").hover(function () {
              $(this).removeClass("pulse");
          }, function () {
              $(this).addClass("pulse");
          });
      });
      $(document).on('click', '.all-contacts', function () {
          const myDiv = $('#all-contact-types');
          if (myDiv.hasClass('show')) {
              myDiv.removeClass('show');
          } else
              myDiv.addClass('show');
      })

      function validateEmail(email) {
  const re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(email);
}

function validate(go) {
          go.preventDefault();
  const $result = $("#result");
  const email = $("#id_email-subscr").val();
  $result.text("");

  if (validateEmail(email)) {
      const target_url = $('form#only-email').attr("action");
      const token = $('input[name="csrfmiddlewaretoken"]').attr('value');
        $.ajax({
                method: "POST",
                url: target_url,
                data: { csrfmiddlewaretoken: token },
                success: function () {
                    $('#only-email').submit();
                }
            });
            $result.css("color", "green");
            $result.text(" Ссылка для активации отправлена");


  } else {
    $result.text(email + " не является правильным :(");
    $result.css("color", "red");
  }
  return false;

}

$("#validate").on("click", validate);

       // $("#django_instagram_media_wall").click(function(e) {
       //      e.preventDefault();
       //  });

});

