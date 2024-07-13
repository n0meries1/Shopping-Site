document.addEventListener('DOMContentLoaded', function()
{
    const registerForm = document.getElementById('create_new_user');
    const registerFail = document.getElementById('username-taken');

    registerForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const formData = new FormData(registerForm);
        const response = await fetch('/create_new_user', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        if (result.success)
        {
            alert("Account Created!")
            window.location.href = '/login';
        }
        else
        {
            registerFail.style.display = "block";
        }

    });



});