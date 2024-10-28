

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

function togglePdf(elem) {
    if (elem.textContent == "Ввести текст") {
        elem.textContent = "Выбрать PDF"
    } else {
        elem.textContent = "Ввести текст"
    }

    document.querySelector(".input__file").classList.toggle("show");
    document.querySelector(".input__text").classList.toggle("show");

    resetFile()
    document.querySelector(".input__text").querySelector('textarea').value = "";
}