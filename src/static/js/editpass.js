function openConfirmPinModal2(passwordId) {
    // Open the confirmation dialog
    var confirmPinModal2 = new bootstrap.Modal(document.getElementById('confirmPinModal2'));
    confirmPinModal2.show();
    console.log("part 01");
  
    // Cursor movement
    var inputBoxes = document.querySelectorAll('#confirmPinModal2 .pin-input input');
  
    inputBoxes.forEach(function(input, index) {
      input.addEventListener('input', function() {
        if (input.value.length === input.maxLength) {
          if (index < inputBoxes.length - 1) {
            inputBoxes[index + 1].focus();
          }
        }
      });
    });
  
    // Handle confirm button click
    var confirmButton = document.querySelector('#confirmPinModal2 button[type="submit"]');
    confirmButton.addEventListener('click', function(event) {
      event.preventDefault();
  
      // Retrieve the entered Quick PIN
      var digit1 = document.querySelector('#confirmPinModal2 input[name="digit1"]').value;
      var digit2 = document.querySelector('#confirmPinModal2 input[name="digit2"]').value;
      var digit3 = document.querySelector('#confirmPinModal2 input[name="digit3"]').value;
      var digit4 = document.querySelector('#confirmPinModal2 input[name="digit4"]').value;
      var quickPin = digit1 + digit2 + digit3 + digit4;
      console.log("part 02");
  
      // Send AJAX request to validate the Quick PIN and view the password
      var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
      var url = "/checkpin/";
      var xhr = new XMLHttpRequest();
      xhr.open('POST', url);
      xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
      xhr.setRequestHeader('X-CSRFToken', csrfToken);
      console.log("part 03");
      xhr.onload = function() {
        console.log("part 03.1");
        if (xhr.status === 200) {
          console.log("part 04");
          var response = JSON.parse(xhr.responseText);
          if (response.success) {
            // Handle successful response
            console.log("Password viewed successfully.");
            // Close the confirmation dialog
            confirmPinModal2.hide();
            console.log("part 05");
  
            // Redirect to the viewpass.html page
            var redirectUrl = "/editpass/" + passwordId + "/?quickPin=" + encodeURIComponent(quickPin);
            window.location.href = redirectUrl;
            console.log("part 07");
          } else {
            // Handle error response
            console.log("Error viewing password.");
            var errorMessageElement = document.getElementById('error-message2');
            errorMessageElement.textContent = 'Invalid Quick PIN !!';
          }
        } else {
          // Handle error response
          console.log("Error viewing password.");
        }
      };
      var data = "quick_pin=" + encodeURIComponent(quickPin);
      xhr.send(data);
    });
  }
  