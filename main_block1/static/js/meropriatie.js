document.addEventListener('DOMContentLoaded', function() {
    // Получаем элементы
    const modal = document.getElementById('registrationModal');
    const openButtons = document.querySelectorAll('.register-button, #openModal');
    const closeButton = document.querySelector('.close');
    
    // Функция открытия модального окна
    function openModal() {
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden';
        document.body.style.position = 'fixed'; // Фиксируем позицию
        document.body.style.width = '100%'; // Сохраняем ширину
    }
    
    // Функция закрытия модального окна
    function closeModal() {
        modal.style.display = 'none';
        document.body.style.overflow = '';
        document.body.style.position = '';
    }
    
    // Назначаем обработчики для всех кнопок открытия
    openButtons.forEach(btn => {
        btn.addEventListener('click', openModal);
    });
    
    // Обработчик для кнопки закрытия
    closeButton.addEventListener('click', closeModal);
    
    // Закрытие при клике вне окна
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            closeModal();
        }
    });
    
    // Дополнительно: закрытие по ESC
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && modal.style.display === 'block') {
            closeModal();
        }
    });
});