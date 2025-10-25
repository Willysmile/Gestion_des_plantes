import PySimpleGUI as sg
from app.api_client import api_client

sg.theme('DarkBlue3')

def create_main_window():
    layout = [
        [sg.Text('🌱 Plant Manager v2', font=('Any', 20), justification='center')],
        [sg.Text('Loading...', key='-STATUS-', font=('Any', 12))],
        [sg.Button('Test API'), sg.Button('Exit', size=(10, 1))]
    ]
    return sg.Window('Plant Manager', layout, finalize=True)

def main():
    window = create_main_window()
    
    if api_client.health_check():
        window['-STATUS-'].update("✅ Connected to backend")
    else:
        window['-STATUS-'].update("❌ Backend not responding")
    
    while True:
        event, values = window.read()
        
        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break
        
        if event == 'Test API':
            if api_client.health_check():
                sg.popup('✅ API is working!')
            else:
                sg.popup('❌ API connection failed!')
    
    window.close()

if __name__ == '__main__':
    main()
