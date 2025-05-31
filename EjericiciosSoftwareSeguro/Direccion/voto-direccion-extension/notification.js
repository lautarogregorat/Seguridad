
const btnAfirmativo = document.getElementById("afirmativo");
const btnNegativo = document.getElementById("negativo");
const inputClave = document.getElementById("clave");

// Obtener parámetros GET
const params = new URLSearchParams(window.location.search);
const title = params.get("title") || "Sin título";
const body = params.get("body") || "Sin contenido";

// Mostrar en el HTML
document.getElementById("title").textContent = title;
document.getElementById("body").textContent = body;

function fromBase64UrlSafe(input) {
    // Revertimos los cambios URL-safe a base64 estándar
    let base64 = input.replace(/-/g, '+').replace(/_/g, '/');
  
    // Añadimos los signos de igual que se hayan eliminado (padding)
    const padding = 4 - (base64.length % 4);
    if (padding !== 4) {
      base64 += '='.repeat(padding);
    }
  
    // Decodificamos desde base64 a string
    return atob(base64);
}
  
function enviarVoto(afirmativo) {
    const id = params.get("id") || "";
    const base64Url = params.get("url") || "";
    const clave = inputClave.value;
    let url = fromBase64UrlSafe(base64Url);
    fetch(url + "registrar_voto", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ uuid: id, afirmativo: afirmativo, clave: clave })
    })
    .then(response => response.json())
    .then(data => {
        const divMensaje = document.getElementById("mensaje");
        divMensaje.textContent = data['message'];
    })
    .catch(error => {
        console.error("Error al registrar el token:", error);
    });
}

btnAfirmativo.addEventListener("click", function() {
    enviarVoto(true);
});

btnNegativo.addEventListener("click", function() {
    enviarVoto(false);
});