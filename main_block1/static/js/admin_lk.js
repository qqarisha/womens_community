document.addEventListener('DOMContentLoaded', function() {
    // Переключение вкладок
    const tabButtons = document.querySelectorAll('.nav-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Удаляем активный класс у всех кнопок и вкладок
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Добавляем активный класс к текущей кнопке
            button.classList.add('active');
            
            // Находим соответствующую вкладку и делаем её активной
            const tabId = button.getAttribute('data-tab') + '-tab';
            document.getElementById(tabId).classList.add('active');
            
            // Если это вкладка статистики, инициализируем графики
            if (tabId === 'stats-tab') {
                initCharts();
            }
        });
    });
    
    // Обработка загрузки изображения
    const imageInput = document.getElementById('event-image');
    const imagePreview = document.getElementById('image-preview');
    const fileNameSpan = document.querySelector('.file-name');
    
    if (imageInput) {
        imageInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                fileNameSpan.textContent = file.name;
                
                const reader = new FileReader();
                reader.onload = function(e) {
                    imagePreview.innerHTML = `<img src="${e.target.result}" alt="Превью">`;
                    imagePreview.style.display = 'block';
                }
                reader.readAsDataURL(file);
            } else {
                fileNameSpan.textContent = 'Файл не выбран';
                imagePreview.style.display = 'none';
                imagePreview.innerHTML = '';
            }
        });
    }
    
    // Инициализация графиков (заглушка)
    function initCharts() {
        console.log('Инициализация графиков...');
        // Здесь будет код для инициализации Chart.js или другой библиотеки
    }
    
    // Обработка формы
    const eventForm = document.getElementById('create-event-form');
    if (eventForm) {
        eventForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Здесь будет код для отправки формы
            alert('Мероприятие успешно создано!');
            eventForm.reset();
            fileNameSpan.textContent = 'Файл не выбран';
            imagePreview.style.display = 'none';
            imagePreview.innerHTML = '';
        });
    }
});