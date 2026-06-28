from flask import Flask, render_template, request, jsonify
import os
import platform
import subprocess

app = Flask(__name__)
OS_NAME = platform.system()

# Intentamos importar pyautogui para Windows/X11
try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except Exception:
    PYAUTOGUI_AVAILABLE = False

@app.route('/')
def index():
    # Sirve el archivo index.html que crearemos en el siguiente paso
    return render_template('index.html')

@app.route('/comando', methods=['POST'])
def ejecutar_comando():
    data = request.json
    accion = data.get('accion')
    valor = data.get('valor', 0) # Para el contador de apagado

    if accion == 'vol_up':
        if OS_NAME == 'Linux':
            subprocess.run(['wpctl', 'set-volume', '@DEFAULT_AUDIO_SINK@', '5%+'])
        else:
            pyautogui.press('volumeup')
            
    elif accion == 'vol_down':
        if OS_NAME == 'Linux':
            subprocess.run(['wpctl', 'set-volume', '@DEFAULT_AUDIO_SINK@', '5%-'])
        else:
            pyautogui.press('volumedown')
            
    elif accion == 'play_pause':
        if OS_NAME == 'Linux':
            subprocess.run(['playerctl', 'play-pause'])
        else:
            pyautogui.press('playpause')
            
    elif accion == 'next':
        if OS_NAME == 'Linux':
            subprocess.run(['playerctl', 'next'])
        else:
            pyautogui.press('nexttrack')
            
    elif accion == 'prev':
        if OS_NAME == 'Linux':
            subprocess.run(['playerctl', 'previous'])
        else:
            pyautogui.press('prevtrack')
            
    elif accion == 'suspend':
        if OS_NAME == 'Linux':
            os.system('systemctl suspend')
        elif OS_NAME == 'Windows':
            os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
            
    elif accion == 'shutdown':
        minutos = int(valor)
        if OS_NAME == 'Linux':
            os.system(f'shutdown +{minutos}')
        elif OS_NAME == 'Windows':
            os.system(f'shutdown /s /t {minutos * 60}')
            
    elif accion == 'cancel_shutdown':
        if OS_NAME == 'Linux':
            os.system('shutdown -c')
        elif OS_NAME == 'Windows':
            os.system('shutdown /a')

    return jsonify({"status": "ok", "accion": accion})

if __name__ == '__main__':
    # Escucha en todas las interfaces de red (0.0.0.0) en el puerto 5000
    app.run(host='0.0.0.0', port=5000)