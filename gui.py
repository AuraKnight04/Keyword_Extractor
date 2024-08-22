import PySimpleGUI as sg

def main():
    layout = [
        [sg.Text("Enter your name:")],
        [sg.InputText(key="name")],
        [sg.Text("Enter your age:")],
        [sg.InputText(key="age")],
        [sg.Button("Submit")],
        [sg.Text("", key="output")]
    ]

    window = sg.Window("Test GUI", layout)

    while True:
        event, values = window.read()
        if event == "Submit":
            name = values["name"]
            age = values["age"]
            output = f"Hello, {name}! You are {age} years old."
            window["output"].update(output)
        elif event == sg.WINDOW_CLOSED:
            break

    window.close()

if __name__ == "__main__":
    main()