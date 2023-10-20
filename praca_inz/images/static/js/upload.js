const fileInput = document.getElementById('file');
        const imagePreview = document.getElementById('preview');

        fileInput.addEventListener('change', (event) => {
            const selectedFile = event.target.files[0];
            if (selectedFile) {
                const fileReader = new FileReader();
                fileReader.onload = function () {
                    imagePreview.src = fileReader.result;
                };
                fileReader.readAsDataURL(selectedFile);
            }
        });
