document.querySelector('#file-input').addEventListener('change', (event) => {
    let input = event.target;
    console.log(input)
    let file = input.files[0];
    let name = file.name;

    let btn = document.querySelector('.file-button__text');

    btn.innerHTML = name;

    let cross = document.querySelector('.input__file').querySelector('.close')
    cross.style.display = "";
    cross.style.display = "block";


})

function resetFile() {
    let btn = document.querySelector('.file-button__text');

    btn.innerHTML = "Выбрать PDF";

    let cross = document.querySelector('.input__file').querySelector('.close')
    cross.style.display = "";
    cross.style.display = "none";

    document.querySelector('#file-input').value = "";
}

function changeProcent() {
    let input = document.querySelector('#range-input');

    let proc = document.querySelector('.procent');

    let value = input.value;
    proc.innerHTML = value + '%';
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

