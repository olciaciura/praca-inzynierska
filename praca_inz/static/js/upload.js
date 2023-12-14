document.getElementById('file').addEventListener('change', function (event) {
    handleFileSelect(event, placeholderImagePath);
});

function handleFileSelect(event, placeholderImagePath) {
    var preview = document.getElementById('preview-container');
    preview.innerHTML = '';

    var files = event.target.files;

    if (files.length > 0) {
        for (var i = 0; i < files.length; i++) {
            var file = files[i];

            var reader = new FileReader();

            reader.onload = function (e) {
                var img = new Image();
                img.src = e.target.result;
                img.className = 'preview';
                preview.appendChild(img);
            };

            reader.readAsDataURL(file);
        }
    } else {
        var img = new Image();
        img.src = placeholderImagePath;
        img.className = 'preview-image';
        preview.appendChild(img);
    }
}
