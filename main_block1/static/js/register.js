document.getElementById('registrationForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Сброс сообщений об ошибках
    document.querySelectorAll('.error-message').forEach(el => {
        el.style.display = 'none';
    });
    
    // Валидация
    let isValid = true;
    const fullName = document.getElementById('fullName').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    
    if (fullName.length < 3) {
        document.getElementById('fullNameError').textContent = 'Введите полное имя';
        document.getElementById('fullNameError').style.display = 'block';
        isValid = false;
    }
    
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        document.getElementById('emailError').textContent = 'Введите корректный email';
        document.getElementById('emailError').style.display = 'block';
        isValid = false;
    }
    
    if (password.length < 6) {
        document.getElementById('passwordError').textContent = 'Пароль должен содержать минимум 6 символов';
        document.getElementById('passwordError').style.display = 'block';
        isValid = false;
    }
    
    if (password !== confirmPassword) {
        document.getElementById('confirmPasswordError').textContent = 'Пароли не совпадают';
        document.getElementById('confirmPasswordError').style.display = 'block';
        isValid = false;
    }
    
    if (isValid) {
        // Здесь добавить отправку формы на сервер
        alert('Регистрация успешна!');
        window.fetch("http://127.0.0.1:5000").then(function(response) { 
            alert(response.text());
        });
        // window.location.href = 'profile.html';
    }
});