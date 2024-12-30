document.getElementById("loginForm").addEventListener("submit", function (e) {
    e.preventDefault();

    // Get the form data
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const role = document.getElementById("role").value;
    const rememberMe = document.getElementById("rememberMe").checked;

    // Log the data (for now, you can replace this with an API request)
    console.log("Username:", username);
    console.log("Password:", password);
    console.log("Role:", role);
    console.log("Remember Me:", rememberMe);

    // You can make an API call here to send this data to your backend
    // Example:
    // fetch('/your-api-endpoint', {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify({ username, password, role, rememberMe })
    // });

    // Reset the form fields
    document.getElementById("loginForm").reset();
});
