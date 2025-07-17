
document.getElementById("cardForm").addEventListener("submit", function(event) {
    event.preventDefault();

    // Get the payment amount entered by the user
    const paymentAmount = parseFloat(document.getElementById("paymentAmount").value);

    // Validate the payment amount
    if (isNaN(paymentAmount) || paymentAmount <= 0) {
        alert("Please enter a valid payment amount.");
        return;
    }

    // Send payment amount to the server to update the balance
    fetch("{% url 'add_money' %}", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "{{ csrf_token }}"
        },
        body: JSON.stringify({ amount: paymentAmount })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Balance updated successfully!");
            window.location.href = "{% url 'vehiclerent' %}"; // Redirect to the vehicle selection page
        } else {
            alert("Failed to update balance. Please try again.");
        }
    });
});

