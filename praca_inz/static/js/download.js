document.addEventListener("DOMContentLoaded", function () {
  // Poczekaj, aż cały dokument zostanie załadowany

  var downloadButton = document.getElementById("download_button");
  downloadButton.addEventListener("click", function () {
      // Obsłuż kliknięcie przycisku "download_button"

      var imageElement = document.getElementById("preview");
      var imageUrl = imageElement.getAttribute("src");

      // Utwórz tymczasowy link do pobierania
      var downloadLink = document.createElement("a");
      downloadLink.href = imageUrl;

      // Pobierz nazwę pliku z URL
      var filename = imageUrl.split("/").pop();
      downloadLink.download = filename;

      // Kliknij w link, aby rozpocząć pobieranie
      downloadLink.click();
  });
});
