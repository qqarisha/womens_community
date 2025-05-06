
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
    }
});