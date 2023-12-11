// script.js
document.addEventListener('DOMContentLoaded', function () {

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

let point1 = null;
let point2 = null;
let scale = null;


function displayMeasurementInfo() {
    const measurementInfo = document.getElementById('measurementInfo');
    const sizeSpan = document.getElementById('measurementSize');

    if (point1 && point2) {
        const size = calculateDistance(point1, point2);
        sizeSpan.textContent = `${size.toFixed(2)}`;
        measurementInfo.style.display = 'block';
    }
}

function openFullscreen(imgElement) {
	if(document.querySelector('.image_wrapper').classList.contains('full')){
		const imageWrapper = event.currentTarget;
		const rect = imageWrapper.getBoundingClientRect();
		const x = event.clientX;
		const y = event.clientY;
		if (!point1) {
			point1 = { x, y };
			
            const imageWrapper = document.querySelector('.image_wrapper');

            const xMarker = document.createElement('div');
            xMarker.className = 'x-marker';
            xMarker.style.position = 'absolute';
            xMarker.style.left = `${point1.x - 6}px`;
            xMarker.style.top = `${point1.y -5}px`;
            xMarker.innerHTML = '<span style="color: red; font-size: 20px;">X</span>';
            imageWrapper.appendChild(xMarker); 
                    
		} else if (!point2) {
			point2 = { x, y };
			
			
            const imageWrapper = document.querySelector('.image_wrapper');

            const xMarker = document.createElement('div');
            xMarker.className = 'y-marker';
            xMarker.style.position = 'absolute';
            xMarker.style.left = `${point2.x - 6}px`;
            xMarker.style.top = `${point2.y - 5}px`;
            xMarker.innerHTML = '<span style="color: red; font-size: 20px;">X</span>';
            imageWrapper.appendChild(xMarker); 
			
			displayMeasurementInfo();
			drawOverlay();
		}
	} else {
		document.querySelector('.image_wrapper').classList.add('full');
		document.querySelector('.actions').classList.add('show');	
        
	}
 
}

function closeFullscreen() {
	document.querySelector('.image_wrapper').classList.remove('full');
	document.querySelector('.actions').classList.remove('show');
    clearMeasurement();
}

function downloadImage() {
    var fullscreenImg = document.querySelector('.image_wrapper.full img');

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

function calculateDistance(pointA, pointB) {
    if (!scale) {
        alert('Wprowadź poprawną wartość skali (większą od zera).');
        scale = null;
    }

    const dx = pointA.x - pointB.x;
    const dy = pointA.y - pointB.y;

    const distanceInPixels = Math.sqrt(dx * dx + dy * dy);
    const distanceInMillimeters = distanceInPixels * scale;
    return distanceInMillimeters;
}

function setScale() {
    const scaleInput = document.getElementById('scaleInput');
    scale = parseFloat(scaleInput.value);

    if (isNaN(scale) || scale <= 0) {
        alert('Wprowadź poprawną wartość skali (większą od zera).');
        scale = null;
    }
}
function clearMeasurement() {
    point1 = null;
    point2 = null;
    const measurementInfo = document.getElementById('measurementInfo');
    measurementInfo.style.display = 'none';

    const x = document.querySelector('.x-marker');
    x.innerHTML = '';

    const y = document.querySelector('.y-marker');
    y.innerHTML = '';
};