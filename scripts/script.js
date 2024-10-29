document.querySelector('#file-input').addEventListener('change', (event) => {
    let input = event.target;
    let file = input.files[0];
    let name = file.name;

    let btn = document.querySelector('.file-button__text');
    btn.innerHTML = name;

    let cross = document.querySelector('.input__file').querySelector('.close');
    cross.style.display = "block";
});

function resetFile() {
    let btn = document.querySelector('.file-button__text');
    btn.innerHTML = "Выбрать PDF";

    let cross = document.querySelector('.input__file').querySelector('.close');
    cross.style.display = "none";

    document.querySelector('#file-input').value = "";
}

function changeProcent() {
    let input = document.querySelector('#range-input');
    let proc = document.querySelector('.procent');
    proc.innerHTML = input.value + '%';
}

function toggleMode(checkbox) {
    const textInput = document.querySelector('.input__text');
    const fileInput = document.querySelector('.input__file');

    if (checkbox.checked) {
        fileInput.classList.remove('show');
        textInput.classList.add('show');
    } else {
        textInput.classList.remove('show');
        fileInput.classList.add('show');
    }
}

async function handleFormSubmit(event) {
    event.preventDefault();

    const fileInput = document.querySelector('#file-input');
    const outputPanel = document.getElementById('output-panel');
    const overlay = document.getElementById('overlay');
    const rangeInput = document.querySelector('#range-input');
    const file = fileInput.files[0];

    if (file && file.type === "application/pdf") {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('percentage', rangeInput.value);

        outputPanel.innerHTML = "Отправка файла...";
        overlay.style.display = "flex";

        try {
            const response = await fetch('/api', {
                method: 'POST',
                body: formData
            });

            overlay.style.display = "none";

            if (response.ok) {
                const result = await response.json();
                outputPanel.innerHTML = result.result || "Файл успешно обработан";
            } else {
                outputPanel.innerHTML = "Ошибка при обработке файла на сервере";
            }
        } catch (error) {
            overlay.style.display = "none";
            outputPanel.innerHTML = "Ошибка сети или сервера";
            console.error("Ошибка:", error);
        }
    } else {
        outputPanel.innerHTML = "Пожалуйста, выберите PDF файл";
    }
}
