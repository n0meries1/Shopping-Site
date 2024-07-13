document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById("login_user");
    const loginFail = document.getElementById("login-fail");

    loginForm.addEventListener('submit', async (event) =>
    {
        event.preventDefault();

        const formData = new FormData(loginForm);
        const response = await fetch('/login_user', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        if (result.success)
        {
            window.location.href = '/';
        }
        else
        {
            loginFail.style.display = "block";
        }

    })
})