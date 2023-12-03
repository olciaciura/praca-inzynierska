// script.js
document.addEventListener('DOMContentLoaded', function () {
    var images = document.querySelectorAll('.image_wrapper img');

    images.forEach(function (imgElement) {
        imgElement.addEventListener('click', function () {
            openFullscreen(imgElement);
        });
    });

    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape') {
            closeFullscreen();
        }
    });

    document.addEventListener('keydown', function (event) {
        if (event.key === 'd') {
            downloadImage();
        }
    });

});

function openFullscreen(imgElement) {
    imgElement.classList.add('fullscreen');
    var overlay = imgElement.nextElementSibling;
    overlay.classList.add('active');
    var overlayButtons = overlay.querySelector('.overlay_buttons');
    overlayButtons.style.display = 'block';
}

function closeFullscreen() {
    var fullscreenImg = document.querySelector('.image_wrapper img.fullscreen');
    var activeOverlay = document.querySelector('.overlay.active');

    if (fullscreenImg) {
        fullscreenImg.classList.remove('fullscreen');
    }

    if (activeOverlay) {
        activeOverlay.classList.remove('active');
        var overlayButtons = activeOverlay.querySelector('.overlay_buttons');

        if (overlayButtons) {
            overlayButtons.style.display = 'none';
        }
    }
}

function downloadImage() {
    var fullscreenImg = document.querySelector('.image_wrapper img.fullscreen');

    if (fullscreenImg) {
        var imageUrl = fullscreenImg.src;

        var downloadLink = document.createElement('a');
        downloadLink.href = imageUrl;

        // Pobierz nazwę pliku z URL
        var filename = imageUrl.split('/').pop();
        downloadLink.download = `image_${filename}`;

        // Dodaj link do dokumentu
        document.body.appendChild(downloadLink);

        // Kliknij w link, aby rozpocząć pobieranie
        downloadLink.click();

        // Usuń link z dokumentu po pobraniu
        document.body.removeChild(downloadLink);
    } else {
        console.error('Brak obrazu w trybie pełnoekranowym');
    }
}

function setScale() {
    // Kod do ustawienia skali
}
