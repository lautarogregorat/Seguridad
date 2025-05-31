// Copyright 2023 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     https://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

/*eslint no-unused-vars: ["error", { "varsIgnorePattern": "subscribeUserVisibleOnlyFalse" }]*/

const APPLICATION_SERVER_PUBLIC_KEY = 'BGNyxYYIdQPc5sr7ns-ZjWWciSwrErvGXVt9uISkgd6SX1gRxZbmDiqLFEboVjAM6y2Hwuz6RF9a9yLnJqhq0N0';
let targetDomainNotificationClick = null;

async function subscribeUserVisibleOnlyFalse() {
  const applicationServerKey = urlB64ToUint8Array(
    APPLICATION_SERVER_PUBLIC_KEY
  );
  try {
    let subscriptionData = await self.registration.pushManager.subscribe({
      // With our new change[1], this can be set to false. Before it must
      // always be set to true otherwise an error will be thrown about
      // permissions denied.
      userVisibleOnly: false,
      applicationServerKey: applicationServerKey
    });
    console.log('[Service Worker] Extension is subscribed to push server.');
    logSubscriptionDataToConsole(subscriptionData);
  } catch (error) {
    console.error('[Service Worker] Failed to subscribe, error: ', error);
  }
}

function logSubscriptionDataToConsole(subscription) {
  // The `subscription` data would normally only be know by the push server,
  // but for this sample we'll print it out to the console so it can be pasted
  // into a testing push notification server (at
  // https://web-push-codelab.glitch.me/) to send push messages to this
  // endpoint (extension).
  console.log(
    '[Service Worker] Subscription data to be pasted in the test push' +
    'notification server: '
  );
  console.log(JSON.stringify(subscription));
}

// Push message event listener.
self.addEventListener('push', function (event) {
  let notificationData = event.data.json();
  let notification = notificationData.data;

  if (notification.level === "high") {
    const notificationOptions = {
      body: notification.preview,
      data: {
        id: notification.id,
        title: notification.title,
        body: notification.body
      }
    };

    event.waitUntil(
      self.registration.showNotification('Título de la notificación', notificationOptions)
    );
  }
});

self.addEventListener('notificationclick', function (event) {
  event.notification.close();
  let notification = event.notification;
  
  if (notification.data != null) {
    const promise = new Promise((resolve, reject) => {
      const request = indexedDB.open("MiBD", 1);
  
      request.onerror = () => {
        console.error("Error al abrir IndexedDB");
        reject();
      };
  
      request.onsuccess = () => {
        const db = request.result;
        const tx = db.transaction("urls", "readonly");
        const store = tx.objectStore("urls");
  
        const getRequest = store.get(1); // Cambia por la clave que necesites
  
        getRequest.onsuccess = () => {
          const resultado = getRequest.result;
          if (resultado && resultado.dominio) {
            const notificationParams = {
              id: notification.data.id,
              title: notification.data.title,
              body: notification.data.body,
              url: resultado.dominio
            }
            const urlSearchParams = new URLSearchParams(notificationParams).toString();
            const targetUrl = "notification.html?" + urlSearchParams + "#";
            resolve(clients.openWindow(targetUrl));
          } else {
            console.error("No se encontró el valor en IndexedDB");
            reject();
          }
        };
  
        getRequest.onerror = () => {
          console.error("Error al leer datos de IndexedDB");
          reject();
        };
      };
    });
    event.waitUntil(promise);
  }
});

self.addEventListener("message", event => {
  console.log("event", event)
  const data = event.data;
  if (data.tipo === "URL") {

    let domain = toBase64UrlSafe(data.url);
    guardarURL(domain)
      .then(() => console.log("Dominio guardado en IndexedDB:", domain))
      .catch((err) => console.error("Error guardando dominio:", err));
  }
});

function toBase64UrlSafe(input) {
  const base64 = btoa(input); // Codifica a base64
  return base64.replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, ""); // URL-safe
}

// Inicializar IndexedDB
function openDatabase() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open("MiBD", 1);
    request.onerror = (event) => {
      console.error("Error abriendo la base de datos", event);
      reject(event);
    };
    request.onsuccess = (event) => {
      resolve(event.target.result);
    };
    request.onupgradeneeded = (event) => {
      const db = event.target.result;
      db.createObjectStore("urls", { keyPath: "id", autoIncrement: true });
    };
  });
}

// Guardar URL
async function guardarURL(dominio) {
  const db = await openDatabase();
  const tx = db.transaction("urls", "readwrite");
  const store = tx.objectStore("urls", { keyPath: 'id' });
  store.put({ id: 1, dominio });
  await tx.complete?.catch(() => { }); // algunos navegadores necesitan esto
}

// Helper method for converting the server key to an array that is passed
// when subscribing to a push server.
function urlB64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - (base64String.length % 4)) % 4);
  const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/');

  const rawData = atob(base64);
  const outputArray = new Uint8Array(rawData.length);

  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
}

// [1]: https://chromiumdash.appspot.com/commit/f6a8800208dc4bc20a0250a7964983ce5aa746f0