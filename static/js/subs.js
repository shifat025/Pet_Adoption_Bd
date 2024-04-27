document.getElementById('subscriptionButton').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent default link behavior
    
    // Show toast notification
    showToast('Subscription Successful!', 'success');
    
    // Optionally, redirect after showing the toast
    setTimeout(function() {
        window.location.href = event.target.href;
    }, 3000); // Redirect after 3 seconds (adjust as needed)
});

function showToast(message, type) {
    // Your toast implementation logic goes here
    // This is a simple example, you can use libraries like Bootstrap Toast or create your own custom toast
    alert(message); // Example: Alert box, replace with your toast implementation
}