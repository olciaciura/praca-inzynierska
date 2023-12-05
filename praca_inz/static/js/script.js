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
        } else if (event.key === 'd') {
            downloadImage();
        } else if (event.key === 'r') {
            clearMeasurement();
        } else if (event.key === 'm') {
            setScale(); //nie działa 
        }});
});

function openFullscreen(imgElement) {
    imgElement.classList.add('fullscreen');
    imgElement.style.zIndex = '1000';
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
    
        var filename = imageUrl.split('/').pop(); //pobranie nazwy pliku
        downloadLink.download = `image_${filename}`;

        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);
    } else {
        console.error('Brak obrazu w trybie pełnoekranowym');
    }
}

let point1 = null;
let point2 = null;
let scale = null;

function handleImageClick(event) {
    const imageWrapper = event.currentTarget;
    const rect = imageWrapper.getBoundingClientRect();
    const x = event.clientX;
    const y = event.clientY;

    if (!point1) {
        point1 = { x, y };
    } else if (!point2) {
        point2 = { x, y };
        displayMeasurementInfo();
        drawOverlay();
    }
}

function displayMeasurementInfo() {
    const measurementInfo = document.getElementById('measurement_info');
    const sizeSpan = document.getElementById('measurement_size');

    if (point1 && point2) {
        const size = calculateDistance(point1, point2);
        sizeSpan.textContent = `${size.toFixed(2)}`;
        measurementInfo.style.display = 'block';
    }
}

function calculateDistance(pointA, pointB) {
    if (!scale) {
        scale = 2
    }

    const dx = pointA.x - pointB.x;
    const dy = pointA.y - pointB.y;

    const distanceInPixels = Math.sqrt(dx * dx + dy * dy);
    const distanceInMillimeters = distanceInPixels * scale;
    return distanceInMillimeters;
}

function drawOverlay() {
    const imageWrapper = document.querySelector('.image_wrapper');
    const overlay = document.querySelector('.overlay');

    const xMarker = document.createElement('div');
    xMarker.className = 'x-marker';
    xMarker.style.position = 'absolute';
    xMarker.style.left = `${point2.x}px`;
    xMarker.style.top = `${point2.y}px`;
    xMarker.innerHTML = '<span style="color: red; font-size: 20px;">X</span>';
    imageWrapper.appendChild(xMarker); 

    const line = document.createElement('div');
    line.className = 'line';
    line.style.position = 'absolute';
    line.style.left = `${point1.x}px`;
    line.style.top = `${point1.y}px`;
    line.style.width = `${point2.x - point1.x}px`;
    line.style.height = `${point2.y - point1.y}px`;
    line.style.border = '1px solid red';
    imageWrapper.appendChild(line);  

    console.log('Point1:', point1);
    console.log('Point2:', point2);
}

function setScale() {
    const scaleInput = document.getElementById('scale_input');
    scale = parseFloat(scaleInput.value);

    if (isNaN(scale) || scale <= 0) {
        alert('Wprowadź poprawną wartość skali (większą od zera).');
        scale = null;
    }
}
function clearMeasurement() {
    point1 = null;
    point2 = null;
    const measurementInfo = document.getElementById('measurement_info');
    measurementInfo.style.display = 'none';

    const x = document.querySelector('.x-marker');
    x.innerHTML = '';

    const line = document.querySelector('.line');
    line.innerHTML = '';
};