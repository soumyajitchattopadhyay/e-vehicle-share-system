document.addEventListener("DOMContentLoaded", function() {
    const balanceAmountElement = document.getElementById("balanceAmount");

    let currentBalance = parseFloat(localStorage.getItem("currentBalance")) || 30.0;
    
    const paymentAmount = parseFloat(localStorage.getItem("paymentAmount"));

    if (!isNaN(paymentAmount) && paymentAmount > 0) {
        currentBalance -= paymentAmount;
        currentBalance = currentBalance < 0 ? 0 : currentBalance;

        balanceAmountElement.textContent = `${currentBalance.toFixed(1)} GBP`;

        localStorage.setItem("currentBalance", currentBalance.toFixed(1));

        localStorage.removeItem("paymentAmount");
    } else {
        balanceAmountElement.textContent = `${currentBalance.toFixed(1)} GBP`;
    }
});
