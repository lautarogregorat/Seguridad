import { initializeApp } from "./firebase/firebase-app.js";
import { getMessaging, getToken, onMessage } from "./firebase/firebase-messaging.js";

const btnGuardar = document.getElementById("guardar");
const urlInput = document.getElementById("url");
const estadoDiv = document.getElementById("estado");

function iniciar() {
  const firebaseConfig = {
      apiKey: "AIzaSyCnjE3Pb__NHFLv9q8iefdRVLDTom6ls88",
      authDomain: "voto-direccion.firebaseapp.com",
      projectId: "voto-direccion",
      storageBucket: "voto-direccion.firebasestorage.app",
      messagingSenderId: "455730454874",
      appId: "1:455730454874:web:bdfd1ff0993a0db616d363"
  };
  initializeApp(firebaseConfig);
  
  const messaging = getMessaging();
    
  // Solicitar permiso y obtener token
  getToken(messaging, {
    vapidKey: "BHFSA2yiYSiSOkWK-cc0WpARJmzaBBUNw51-lMSx5tQeGFv1wPsSDga4Lo33m3NojOux9QV5rQDwKOsydZAvzDo"
  })
    .then((currentToken) => {
      if (currentToken) {
        let configURL = localStorage.getItem("configURL");
        fetch(configURL + "registrar_token", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ token: currentToken })
        })
          .then(response => response.json())
          .then(data => {
            // Paso URL a SW
            navigator.serviceWorker.ready.then(registration => {
              registration.active.postMessage({
                tipo: "URL",
                url: configURL
              });
            });
          })
          .catch(error => {
            console.error("Error al registrar el token:", error);
          });
      } else {
        console.warn("No se obtuvo token. Solicita permisos para notificaciones.");
      }
    })
    .catch((err) => {
      console.error("Error al obtener el token FCM", err.name, err.message);
    });
}


function deshabilitarConfig() {
  const esperaDiv = document.getElementById("espera");

  // Deshabilitar el campo de URL y el botón
  urlInput.disabled = true;
  btnGuardar.disabled = true;

  // Mostrar el mensaje "Listo"
  estadoDiv.textContent = "Listo";
  estadoDiv.style.color = "green";

  esperaDiv.textContent = "Esperando nueva encuesta...";
}

let configURL = localStorage.getItem("configURL");
if (configURL != null) {
  urlInput.value = configURL;
  deshabilitarConfig();
  iniciar();
}



btnGuardar.addEventListener("click", function() {
    const url = urlInput.value.trim();

    const regex = /^(https?:\/\/)(localhost:\d+|([a-zA-Z0-9-]+\.)*softwareseguro\.com\.ar)(:\d+)?(\/[^\s]*)?$/;

    if (regex.test(url)) {
      // Guardar la URL en localStorage o realizar acción
      if (url.endsWith('/')) {
        localStorage.setItem("configURL", url);
        deshabilitarConfig();
        iniciar();
      } else {
        estadoDiv.textContent = "Por favor ingresa una URL válida (con el protocolo y la barra al final).";
        estadoDiv.style.color = "red";
      }
    } else {
      estadoDiv.textContent = "Por favor ingresa una URL válida (con el protocolo y la barra al final).";
      estadoDiv.style.color = "red";
    }
});
