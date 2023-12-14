// document.addEventListener("DOMContentLoaded", function () {
//   // Poczekaj, aż cały dokument zostanie załadowany

//   var downloadButton = document.getElementById("download_button");
//   downloadButton.addEventListener("click", function () {
//       // Obsłuż kliknięcie przycisku "download_button"

//       var imageElement = document.getElementById("preview");
//       var imageUrl = imageElement.getAttribute("src");

//       // Utwórz tymczasowy link do pobierania
//       var downloadLink = document.createElement("a");
//       downloadLink.href = imageUrl;

//       // Pobierz nazwę pliku z URL
//       var filename = imageUrl.split("/").pop();
//       downloadLink.download = filename;

//       // Kliknij w link, aby rozpocząć pobieranie
//       downloadLink.click();
//   });
// });


document.addEventListener("DOMContentLoaded", function () {
  // Poczekaj, aż cały dokument zostanie załadowany

  var downloadButton = document.getElementById("download_button");
  downloadButton.addEventListener("click", function () {
      // Obsłuż kliknięcie przycisku "download_button"

      var imageElements = document.querySelectorAll(".image_wrapper img");
      
      // Utwórz tymczasowy link do pobierania dla każdego obrazu
      imageElements.forEach(function (imageElement, index) {
          var imageUrl = imageElement.getAttribute("src");

          var downloadLink = document.createElement("a");
          downloadLink.href = imageUrl;

          // Pobierz nazwę pliku z URL
          var filename = imageUrl.split("/").pop();
          downloadLink.download = `image_${index + 1}_${filename}`;

          // Kliknij w link, aby rozpocząć pobieranie
          downloadLink.click();
      });
  });
});

document.addEventListener("DOMContentLoaded", function () {
  console.log("Skrypt jest załadowany");

  var downloadButton = document.getElementById("download_button_small");

  if (downloadButton) {
    console.log("Przycisk został znaleziony");

    if (downloadButton.addEventListener) {
      // Sprawdź, czy addEventListener jest dostępne
      downloadButton.addEventListener("click", function () {
        console.log("Przycisk został kliknięty");
      });
    } else if (downloadButton.attachEvent) {
      // Dla starszych wersji IE, które obsługują attachEvent
      downloadButton.attachEvent("onclick", function () {
        console.log("Przycisk został kliknięty (IE)");
      });
    } else {
      console.error("Brak obsługi dla addEventListener lub attachEvent");
    }
  } else {
    console.error("Nie znaleziono przycisku o ID 'download_button_small'");
  }
});
