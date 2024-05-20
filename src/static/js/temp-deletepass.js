function openConfirmDeleteModal(passwordId) {
    // Open the confirmation dialog
    var confirmDeleteModal = new bootstrap.Modal(document.getElementById('confirmDeleteModal'));
    confirmDeleteModal.show();
    
    // Handle delete button click
    var deleteButton = document.getElementById('confirmDeleteLink');
    deleteButton.addEventListener('click', function() {

        var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        // Send AJAX request to delete the password
        var url = "/deletepass/" + passwordId + "/";
        var xhr = new XMLHttpRequest();
        xhr.open('DELETE', url);
        xhr.setRequestHeader('X-CSRFToken', csrfToken);
        xhr.onload = function() {

            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                if (response.success) {
                // Handle successful response
                console.log("Password deleted successfully.");

                // Close the confirmation dialog
                confirmDeleteModal.hide();

                // Reload the home page or perform any necessary actions
                location.reload();
                } else {
                // Handle error response
                console.log("Error deleting password.");
                }
            } else {
                // Handle error response
                console.log("Error deleting password.");
            }
        };
        xhr.send();
    });
  }


  