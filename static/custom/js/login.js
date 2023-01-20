

const register_url = window.location.origin + "/api/users/login/"

$( "#login_button" ).click(function() {
  var email = $("#email").val()
  var password = $("#password").val()
  $.ajax({
    method: 'post',
    dataType: "json",
    headers: {
      'Content-Type': 'application/json',
    },
    url: register_url,
    data: JSON.stringify({
      "email": email,
      "password": password,
    }),
    success: function(data){   /* функция которая будет выполнена после успешного запроса.  */
	     alert("SUCCESS. TOKEN IN AUTH"); /* В переменной data содержится ответ от index.php. */

    },
    error: function(data) {
            console.log("error", data.responseJSON.detail);
            alert('error loading from database...');
            }
  })
});