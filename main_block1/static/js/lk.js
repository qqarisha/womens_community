async function sha256(str) {
    const buf = new TextEncoder().encode(str);
    const digest = await crypto.subtle.digest('SHA-256', buf);
    return Array.from(new Uint8Array(digest))
      .map(b => b.toString(16).padStart(2, '0'))
      .join('');
}

document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Сброс сообщений об ошибках
    document.querySelectorAll('.error-message').forEach(el => {
        el.style.display = 'none';
    });
    
    // Валидация
    let isValid = true;
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();
    
    if (!email.includes('@') || !email.includes('.')) {
        document.getElementById('emailError').textContent = 'Введите корректный email';
        document.getElementById('emailError').style.display = 'block';
        isValid = false;
    }
    
    if (password.length < 6) {
        document.getElementById('passwordError').textContent = 'Пароль должен содержать минимум 6 символов';
        document.getElementById('passwordError').style.display = 'block';
        isValid = false;
    }
    
    if (isValid) {
        // Здесь можно добавить AJAX-запрос дя авторизации
        alert('Вход выполнен успешно!');
        let hash = await sha256(password);
        let request_body = {"email": email, "password": hash};
        const request_properties = {
            method : 'POST',
            headers : {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body : JSON.stringify(request_body)
        }
        
        const response = await window.fetch("http://127.0.0.1:5000/api/register", request_properties)
        .then((response) => { 
            response.json().then(res => console.log(res));
            window.location.href = 'profile.html'; // Перенаправление после успешного входа
        })
        .catch((err) => console.error(err));
    }
});