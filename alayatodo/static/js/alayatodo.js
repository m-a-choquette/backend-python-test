// Function called when the add button is clicked.
// Checks if the description and alert the user if it's not valid.
function validateDescription() {
    if ($('#new-todo-description').val().split(' ').join('').length == 0) {
        alert('you must enter a valid description');
    }
}

// Function that triggers form submit when complete checkbox is checked
$('.todo-complete-checkbox').on('change', function() {
    $(this).parent('form').submit();
});


// Function to hide flash confirmation message when todos are created/deleted
$( document ).ready(function() {
    $('.alert.alert-warning.alert-dismissible.fade.in').delay(1000).hide([2000])
});
