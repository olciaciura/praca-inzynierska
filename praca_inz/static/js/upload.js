document.addEventListener('DOMContentLoaded', function() {
  const fileInput = document.getElementById('file');
  const imagePreview = document.getElementById('preview');

  fileInput.addEventListener('change', (e) => {
      const file = e.target.files[0];

      if (file) {
          const reader = new FileReader();
          reader.onload = (event) => {
              imagePreview.src = event.target.result;
          };
          reader.readAsDataURL(file);
      } else {
          imagePreview.src = '/static/images/image_placeholder.png';
      }
  });
});

// TODO obsługa wysyłania zdjecia - w tym napisanie endpointu - czeka na response w którem jest ramka
