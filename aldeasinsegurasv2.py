import requests

# URL y encabezados necesarios
url = "https://chl-6912d48e-e2ec-4ce4-8a1e-e1ad28ab70ce-aldeas-inseguras-v2.softwareseguro.com.ar/src/ctl/enviar_mercancia.ctl.php"
headers = {
    "Cookie": "_ga=GA1.3.752036958.1743859339; PHPSESSID=594f762006ebdfe4d3980faa9dea3c35",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
}

# IDs de los jugadores y sus recursos
jugadores = [
    {"id": "39bffa01f5b07b2a651fe9d973492e46", "recursos": [4920, 1162, 9752]},
    {"id": "111ccefe3a4a88fbf9a7260547dbc084", "recursos": [4563, 2022, 2453]},
    {"id": "ee2e04b3d8686ef9a055626e762c20be", "recursos": [1311, 2056, 3493]},
    {"id": "97238101b434ef7873b08bd9789b0779", "recursos": [745, 1122, 11621]},
    {"id": "bc4aa16b743a3dfba7b9617b8fcca2a3", "recursos": [4552, 1543, 4340]},
    {"id": "bde44e88ebd3925ff843b2e31bda83d7", "recursos": [3322, 3344, 10483]},
    {"id": "74d2afa3a1f4894c8829c6f80a7a436b", "recursos": [4415, 125, 3177]},
    {"id": "f29ae2207b53b27bc0cfb758b910476f", "recursos": [4018, 1739, 14388]},
    {"id": "f6cb7ff9058fdfe1b6cd21de0dcb4618", "recursos": [1585, 1678, 7819]},
    {"id": "e9432dc2f3f99b5d00fb4144d232efda", "recursos": [2319, 2997, 7503]},
    {"id": "6464c004dfdf96f42bd5d64f8e3f507d", "recursos": [3054, 687, 6498]},
    {"id": "6aca358cf89c4ee1b46cfef0ace4e0bf", "recursos": [2569, 616, 8109]},
    {"id": "d9537eba52bbfccfb912b2bdf64d6142", "recursos": [248, 2440, 7940]},
    {"id": "be637e3073a1e7e5cfb86c5978c9560a", "recursos": [1433, 2620, 13103]},
    {"id": "ac550a1da769ae43f800adbff174e7dc", "recursos": [3592, 123, 9428]},
    {"id": "9fedb91a0f93706d7f09b44d0e5b94c1", "recursos": [4676, 3489, 8519]},
    {"id": "115d2db0ba51ec6f82172a6246551b17", "recursos": [929, 135, 13593]},
    {"id": "b43cb96566fcc52a71287afbcf498900", "recursos": [2208, 1828, 13169]},
    {"id": "d68e1ad7131220df462d00caf7d52001", "recursos": [4029, 2600, 10148]},
    {"id": "40dd93cfc62726d9a10e378d63fe9fb2", "recursos": [3502, 3344, 3471]},
    {"id": "ef257c0254b32357433c5d0dd5388522", "recursos": [1510, 3313, 3881]},
    {"id": "76f5de481543092426ed96456329db54", "recursos": [2532, 2130, 1959]},
    {"id": "ce04175308c38ebe1429f866c2480b57", "recursos": [2984, 3207, 9849]},
    {"id": "932b0abd0550a946a7c9fa77d0b433ab", "recursos": [725, 768, 14753]},
    {"id": "4f20b8ee035e59c931925351eacf7378", "recursos": [1989, 633, 5916]},
    {"id": "8531995b7030121c4440299ffefd65ef", "recursos": [4910, 1631, 2058]},
    {"id": "f2f935dc6e0c1e382f6dd686d1e1e878", "recursos": [2791, 463, 10879]},
    {"id": "e96e7bee778fcec8a26b2e1d824b6dd9", "recursos": [2947, 3046, 3798]},
    {"id": "ef098d1695add0b35b5c65b3827ad3b4", "recursos": [3441, 3493, 9402]},
    {"id": "0cf98521e69e11ba393f944d16ecfa51", "recursos": [4375, 3003, 1180]},
    {"id": "96f6667851fab55af355753e9d806cf3", "recursos": [3658, 3387, 13224]},
    {"id": "c3d53e1df4750f72bd4f66d9d171d947", "recursos": [4728, 1149, 7590]},
    {"id": "5c1e86a6ed413e62b29974ac120ac435", "recursos": [834, 982, 5654]},
    {"id": "4dea77c53155f93a3f87873b412325a7", "recursos": [3164, 658, 12375]},
    {"id": "75d233774458cae7e375bf7f582c213a", "recursos": [3686, 466, 2754]},
    {"id": "4a868daa1f4aa72e01b10e6fee6c736d", "recursos": [2231, 3288, 14594]},
    {"id": "d45e6690027091d238da45f37816342b", "recursos": [3917, 2271, 10383]},
    {"id": "0a3c1c2ca143f24b15ab06eea2a3806b", "recursos": [1893, 3004, 2241]},
    {"id": "42ab06fc9d3f4f885b29528a6fff9e06", "recursos": [2683, 764, 13440]},
    {"id": "98ee51f7953be869c88c256a54d9295d", "recursos": [3079, 2307, 11467]},
    {"id": "20775e3bb85fa3ec2701d374057540de", "recursos": [4438, 3257, 9305]},
    {"id": "146e3839b123364ccf95374c6b2ea63a", "recursos": [3402, 2871, 6049]},
    {"id": "470fcd3ceb3271482e0fa2da791bc7cf", "recursos": [268, 2184, 11599]},
    {"id": "180b65657a46f840a085fe7e4ef880b4", "recursos": [1769, 171, 2363]},
]

# Transferencia para el recurso 1 (normal)
for i in range(len(jugadores) - 1):
    id_jugador_origen = jugadores[i]["id"]
    id_jugador_destino = jugadores[i + 1]["id"]
    cantidad = jugadores[i]["recursos"][0]  # Recurso 1 (oro)

    # Acumular los recursos en el jugador destino
    jugadores[i + 1]["recursos"][0] += cantidad
    jugadores[i]["recursos"][0] = 0  # El jugador origen queda con 0 del recurso transferido

    # Datos del formulario
    data = {
        "id_jugador_origen": id_jugador_origen,
        "select_jugador_destino": id_jugador_destino,
        "select_recurso": 1,
        "txt_cantidad": cantidad
    }

    # Realizar la solicitud POST
    response = requests.post(url, headers=headers, data=data)

    # Verificar el resultado
    if response.status_code == 200:
        print(f"Transferencia exitosa de recurso 1 ({cantidad}) de {id_jugador_origen} a {id_jugador_destino}")
    else:
        print(f"Error en la transferencia de recurso 1 de {id_jugador_origen} a {id_jugador_destino}: {response.status_code}")

# Transferencia para los recursos 2 y 3 (todos los recursos al ID específico)
id_jugador_destino = "bdbcc9b006186e87657912bbb0411a37"  # ID fijo del jugador destino

for recurso in [2, 3]:  # Recurso 2 y 3
    for jugador in jugadores:
        id_jugador_origen = jugador["id"]
        cantidad = jugador["recursos"][recurso - 1]  # Obtener la cantidad total del recurso

        if cantidad > 0:  # Solo transferir si hay recursos disponibles
            # Datos del formulario
            data = {
                "id_jugador_origen": id_jugador_origen,
                "select_jugador_destino": id_jugador_destino,
                "select_recurso": recurso,
                "txt_cantidad": 50
            }

            # Realizar la solicitud POST
            response = requests.post(url, headers=headers, data=data)

            # Verificar el resultado
            if response.status_code == 200:
                print(f"Transferencia exitosa de recurso {recurso} ({cantidad}) de {id_jugador_origen} a {id_jugador_destino}")
            else:
                print(f"Error en la transferencia de recurso {recurso} de {id_jugador_origen} a {id_jugador_destino}: {response.status_code}")

            # Actualizar los recursos del jugador origen
            jugador["recursos"][recurso - 1] = 0  # El jugador origen queda con 0 del recurso transferido