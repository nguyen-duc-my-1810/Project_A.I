from tkinter import ttk
from tkinter import messagebox
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from keras.models import load_model
from keras.utils import img_to_array, load_img
import numpy as np
import Fuzzy_plant 
import Dictionary_AI

# Form window for Irrigation suggestion
def open_Form_window():
    global is_Form_window_opened, Form_window
    global kind_combobox, mois_combobox, temp_spinbox, soil_combobox, stage_combobox
  
    if not is_Form_window_opened:
        Form_window =Toplevel(bg="#e0fcff")
        Form_window.title("Information")
        Form_window.iconbitmap("water2.ico")
        Form_window.geometry(f"+80+{new_window_x}")
        Form_window.resizable(0, 0)

        form_label = Label(Form_window, text="Information for Irrigation suggestion", 
                           font=("Microsoft Yahei UI", 12, "bold"), bg="#e0fcff")
        form_label.pack(pady=5)

        form_frame = Frame(Form_window, bg="#e0fcff")
        form_frame.pack(side=TOP, fill=BOTH, padx=10, pady=10)

        kindofplant = Label(form_frame, text="Kind", font=("Monserrat", 11), bg="#e0fcff")
        kindofplant.grid(row=0, column=0, columnspan=2)
        temp = Label(form_frame, text="Temperature", font=("Monserrat", 11), bg="#e0fcff")
        temp.grid(row=0, column=2, columnspan=2)
        mois = Label(form_frame, text="Moisture", font=("Monserrat", 11), bg="#e0fcff")
        mois.grid(row=0, column=4, columnspan=2)

        kind_combobox = ttk.Combobox(form_frame, values=["Herbaceous", "Wood", "Tải ảnh lên"])
        kind_combobox.configure(font=("Arial", 12), width=12)
        kind_combobox.bind("<<ComboboxSelected>>", handle_image)
        kind_combobox.grid(row=1, column=0, columnspan=2)

        temp_spinbox = Spinbox(form_frame, from_=5, to=45, textvariable=StringVar(value="25"))
        temp_spinbox.grid(row=1, column=2, columnspan=2)
        temp_spinbox.configure(font=("Arial", 12), width=12)
        mois_combobox = ttk.Combobox(form_frame, values=["Dry", "Moist", "Wet"])
        mois_combobox.grid(row=1, column=4, columnspan=2)
        mois_combobox.configure(font=("Arial", 12), width=12)
        
        space_label = Label(form_frame, text=" ", font=("Monserrat", 5, "bold"), bg="#e0fcff")
        space_label.grid(row=2, column=0)

        soil = Label(form_frame, text=" Soil ", font=("Monserrat", 11), bg="#e0fcff")
        soil.grid(row=3, column=1, columnspan=2)
        stage = Label(form_frame, text="Stage", font=("Monserrat", 11), bg="#e0fcff")
        stage.grid(row=3, column=3, columnspan=2)

        soil_combobox = ttk.Combobox(form_frame, values=["Sand", "Alluvium", "Loam", "Clay"])
        soil_combobox.configure(font=("Arial", 12), width=12)
        soil_combobox.grid(row=4, column=1, columnspan=2)
        stage_combobox = ttk.Combobox(form_frame, values=["Germination", "Growing", "Full-growing"])
        stage_combobox.configure(font=("Arial", 12), width=12)
        stage_combobox.grid(row=4, column=3, columnspan=2)

        for widget in form_frame.winfo_children():
            widget.grid_configure(padx=15, pady=5)

        calculate_button = Button(form_frame, text="  Calculate  ", bg="#7ab0e6", command=Fuzzy_model)
        calculate_button.configure(font=("Arial", 12, "bold"))
        calculate_button.grid(row=5, column=2, columnspan=2, pady=15)

        Form_window.protocol("WM_DELETE_WINDOW", close_Form_window)
        is_Form_window_opened = True

        
def close_Form_window():
    global is_Form_window_opened, Form_window
    is_Form_window_opened = False
    Form_window.destroy()


# Using CNN model to identify the plant
def CNN_model(x):
    global result_int

    model = load_model("CNN_plant.h5")

    img_CNN = load_img(x, target_size=(32, 32, 3))
    img_CNN = img_to_array(img_CNN)
    img_CNN = img_CNN.astype("float32")/255
    img_CNN = img_CNN.reshape((1, 32, 32, 3))

    result = np.argmax(model.predict(img_CNN), axis=-1)
    result_int = result.item()

    
# Process images when users choose to upload images
def handle_image(event):
    global kind_input
    if kind_combobox.get() == "Upload image":
        IS_file_path = filedialog.askopenfilename()

        CNN_model(IS_file_path)
        kind_input = Dictionary_AI.CNN_map_kind.get(result_int, "Herbaceous")
    else:
        kind_input = kind_combobox.get()


# Using Fuzzy model for input values from form
def Fuzzy_model():
    global kind_raw, water, times  
    kind_raw = kind_combobox.get()
    temp_raw = temp_spinbox.get()
    mois_raw = mois_combobox.get()
    soil_raw = soil_combobox.get()
    stage_raw = stage_combobox.get()

    if kind_raw and temp_raw and mois_raw and soil_raw and stage_raw:
        kind_raw = kind_input
        kind = Dictionary_AI.kind_map.get(kind_raw)
        temp = temp_raw
        mois = Dictionary_AI.mois_map.get(mois_raw)()
        soil = Dictionary_AI.soil_map.get(soil_raw)
        stage = Dictionary_AI.stage_map.get(stage_raw)

        Fuzzy_plant.watering.input['kind'] = float(kind)
        Fuzzy_plant.watering.input['temp'] = float(temp)
        Fuzzy_plant.watering.input['mois'] = float(mois)
        Fuzzy_plant.watering.input['soil'] = float(soil)
        Fuzzy_plant.watering.input['stage'] = float(stage)

        Fuzzy_plant.watering.compute()
        water = Fuzzy_plant.watering.output['water']
        times = Fuzzy_plant.watering.output['times']
        times = round(times)

        if water < 0.3:
            water = 0
            times = 0
        elif water > 0.3 and water < 1:
            water = round(water, 2)
            water =  water * 1000
            water = str(water) + "ml"
        else: 
            water = round(water, 1)
            water = str(water) + "l"

        if times <= 1:
            times = str(times) + " time"
        else:
            times = str(times) + " times"
        print('Water', water, 'Time:', times)

        open_IS_window()
    else:
        messagebox.showwarning(title="Warning", message="You must input all values")


# Irrigation suggestion window
def open_IS_window():
    global is_IS_window_opened, IS_window, kind_raw
    if not is_IS_window_opened:

        IS_window = Toplevel(bg="#e0fcff")
        IS_window.title("Irrigation suggestion")
        IS_window.iconbitmap("water2.ico")
        IS_window.geometry(f"+{new_window_y}+370")

        IS_button_bar = Frame(IS_window, bg="#e0fcff")
        IS_button_bar.pack()

        reopen_IS_button = Button(IS_button_bar, text="Irrigation suggestion", 
                         font=("Monserrat", 15, "bold"), bg="#7ab0e6", command=close_IS_window)
        reopen_IS_button.pack(padx= 10, pady=10, side="left")

        Exit_IS_button = Button(IS_button_bar, text="Exit", 
                         font=("Monserrat", 15, "bold"), bg="#919191", command=close_IS)
        Exit_IS_button.pack(padx= 10, pady=10, side="right")

        IS_frame = Frame(IS_window, bg="#e0fcff")
        IS_frame.columnconfigure(0, weight=1, minsize=100)
        IS_frame.columnconfigure(1, weight=1, minsize=200)
        IS_frame.pack(side="bottom", fill="both", expand=True, pady=15)

        infor_frame = Frame(IS_frame, bg="#e0fcff")
        infor_frame.columnconfigure(0, weight=1, minsize=65)
        infor_frame.columnconfigure(1, weight=1, minsize=65)
        infor_frame.columnconfigure(2, weight=1, minsize=65)
        infor_frame.columnconfigure(3, weight=1, minsize=65)
        infor_frame.columnconfigure(4, weight=1, minsize=65)
        infor_frame.columnconfigure(5, weight=1, minsize=65)
        infor_frame.columnconfigure(6, weight=1, minsize=65)
        infor_frame.rowconfigure(2, minsize=40)
        infor_frame.grid(row=0, column=0)

        suggest_frame = Frame(IS_frame, bg="#e0fcff")
        suggest_frame.grid(row=0, column=1)

        # Infor_frame
        # Row 0
        kind_IS_img = Image.open("plant2.png")
        kind_IS_img = kind_IS_img.resize((50, 50))
        kind_IS_photo = ImageTk.PhotoImage(kind_IS_img)
        kind_IS_img_label = Label(infor_frame, image=kind_IS_photo, bg="#e0fcff")
        kind_IS_img_label.grid(row=0, column=0, columnspan=2)
        kind_IS_img_label.image = kind_IS_photo

        temp_IS_img = Image.open("cloudy-day.png")
        temp_IS_img = temp_IS_img.resize((50, 50))
        temp_IS_photo = ImageTk.PhotoImage(temp_IS_img)
        temp_IS_img_label = Label(infor_frame, image=temp_IS_photo, bg="#e0fcff")
        temp_IS_img_label.grid(row=0, column=2, columnspan=2)
        temp_IS_img_label.image = temp_IS_photo

        mois_IS_img = Image.open("soil-analysis.png")
        mois_IS_img = mois_IS_img.resize((50, 50))
        mois_IS_photo = ImageTk.PhotoImage(mois_IS_img)
        mois_IS_img_label = Label(infor_frame, image=mois_IS_photo, bg="#e0fcff")
        mois_IS_img_label.grid(row=0, column=4, columnspan=2)
        mois_IS_img_label.image = mois_IS_photo

        # Row 1
        kind_label = Label(infor_frame, text=kind_input, bg="#e0fcff",
                           font=("Monserrat", 15, "bold"))
        kind_label.grid(row=1, column=0, columnspan=2)
        temp_label = Label(infor_frame, text=temp_spinbox.get() + "°C", bg="#e0fcff",
                           font=("Monserrat", 15, "bold"))
        temp_label.grid(row=1, column=2, columnspan=2)
        mois_label = Label(infor_frame, text=mois_combobox.get(), bg="#e0fcff",
                           font=("Monserrat", 15, "bold"))
        mois_label.grid(row=1, column=4, columnspan=2)

        # Row 2
        arrow_IS_img = Image.open("right-arrow (1).png")
        arrow_IS_img = arrow_IS_img.resize((50, 50))
        arrow_IS_photo = ImageTk.PhotoImage(arrow_IS_img)
        arrow_IS_img_label = Label(infor_frame, image=arrow_IS_photo, bg="#e0fcff")
        arrow_IS_img_label.grid(row=2, column=6, columnspan=2)
        arrow_IS_img_label.image = arrow_IS_photo

        # Row 3
        soil_IS_img = Image.open("plant1.png")
        soil_IS_img = soil_IS_img.resize((50, 50))
        soil_IS_photo = ImageTk.PhotoImage(soil_IS_img)
        soil_IS_img_label = Label(infor_frame, image=soil_IS_photo, bg="#e0fcff")
        soil_IS_img_label.grid(row=3, column=1, columnspan=2)
        soil_IS_img_label.image = soil_IS_photo

        stage_IS_img = Image.open("sakura.png")
        stage_IS_img = stage_IS_img.resize((50, 50))
        stage_IS_photo = ImageTk.PhotoImage(stage_IS_img)
        stage_IS_img_label = Label(infor_frame, image=stage_IS_photo, bg="#e0fcff")
        stage_IS_img_label.grid(row=3, column=3, columnspan=2)
        stage_IS_img_label.image = stage_IS_photo

        # Row 4
        soil_label = Label(infor_frame, text=soil_combobox.get(), bg="#e0fcff",
                           font=("Monserrat", 15, "bold"))
        soil_label.grid(row=4, column=1, columnspan=2)

        stage_label = Label(infor_frame, text=stage_combobox.get(), bg="#e0fcff",
                            font=("Monserrat", 15, "bold"))
        stage_label.grid(row=4, column=3, columnspan=2)

        # Suggest_frame
        water_label = Label(suggest_frame, text=water,
                            font=("Monserrat", 25, "bold"), foreground="#4d93f0", bg="#e0fcff")
        water_label.grid(row=0, column=0)

        time_label = Label(suggest_frame, text=times,
                           font=("Monserrat", 25, "bold"), foreground="#eb3b3b", bg="#e0fcff")
        time_label.grid(row=1, column=0)

        watering_IS_img = Image.open("watering-plants.png")
        watering_IS_img = watering_IS_img.resize((100, 100))
        watering_IS_photo = ImageTk.PhotoImage(watering_IS_img)
        watering_IS_img_label = Label(suggest_frame, image=watering_IS_photo, bg="#e0fcff")
        watering_IS_img_label.grid(row=0, column=1, rowspan=2)
        watering_IS_img_label.image = watering_IS_photo

        for widget in suggest_frame.winfo_children():
            widget.grid_configure(padx=20, pady=15)

        for widget in IS_frame.winfo_children():
            widget.grid_configure(padx= 10, pady=15)

        IS_window.protocol("WM_DELETE_WINDOW", close_IS_window)
        is_IS_window_opened = True


def close_IS_window():
    global is_IS_window_opened, IS_window
    is_IS_window_opened = False
    IS_window.destroy()


# Close both IS window and Form window
def close_IS():
    close_IS_window()
    close_Form_window()


# Crop recognition window
def open_CR_window():
    global is_CR_window_opened, CR_window
    if not is_CR_window_opened:
 
        CR_file_path = filedialog.askopenfilename()
        CNN_model(CR_file_path)

        img = Image.open(CR_file_path)
        img = img.resize((200, 200))

        CR_window = Toplevel(bg="#FEF0EA")
        CR_window.title("Crop recognition")
        CR_window.iconbitmap("leave.ico")
        CR_window.geometry(f"780x650+{new_window_y}+30")

        CR_button_frame = Frame(CR_window, bg="#FEF0EA")
        CR_button_frame.pack()

        reopen_CR_button = Button(CR_button_frame, text="Crop recognition", 
                         font=("Monserrat", 15, "bold"), bg="#bde3ba", command=reopen_CR_window)
        reopen_CR_button.pack(padx= 10, pady=10, side="left")

        Exit_CR = Button(CR_button_frame, text="Exit", 
                         font=("Monserrat", 15, "bold"), bg="#919191", command=close_CR_window)
        Exit_CR.pack(padx= 10, pady=10, side="right")

        CR_frame = Frame(CR_window, bg="#FEF0EA")
        CR_frame.pack(side="top", fill="both", expand=True)

        scrollbar = Scrollbar(CR_frame)
        scrollbar.pack(side="right", fill="y")

        infor = Text(CR_frame, wrap="word", yscrollcommand=scrollbar.set, borderwidth=0, 
                           selectbackground="#96f8ff", selectforeground="#000000", bg="#FEF0EA")
        infor.configure(state="normal")

        infor.insert("1.0", "    ")
        photo_img = ImageTk.PhotoImage(img)
        infor.image_create("end", image=photo_img)
        infor.image = photo_img

        infor.tag_config("name", font=("Microsoft Yahei UI", 25, "bold"))
        infor.tag_config("title", font=("Microsoft Yahei UI", 16, "bold"))
        infor.tag_config("text", font=("Microsoft Yahei UI", 14), foreground="#0A3715")

        content = Dictionary_AI.CNN_map_content.get(result_int, "None")

        infor.insert("end", "        ")
        infor.insert("end", Dictionary_AI.CNN_map_title.get(result_int, "None"), "name")
        infor.insert("end", "\n")

        infor.insert("end", content[0], "title")
        infor.insert("end", content[1], "text")
        infor.insert("end", content[2], "title")
        infor.insert("end", content[3], "text")
        infor.insert("end", content[4], "title")
        infor.insert("end", content[5], "text")
        infor.insert("end", content[6], "title")
        infor.insert("end", content[7], "text")

        infor.configure(state="disabled")
        infor.pack(side="left", fill="both", expand=True, pady=10, padx=25)

        scrollbar.config(command=infor.yview)

        CR_window.protocol("WM_DELETE_WINDOW", close_CR_window)
        is_CR_window_opened = True


def close_CR_window():
    global is_CR_window_opened, CR_window
    is_CR_window_opened = False
    CR_window.destroy()
    

def reopen_CR_window():
    close_CR_window()
    open_CR_window()

is_Form_window_opened = False
is_CR_window_opened = False
is_IS_window_opened = False

# Main window------------------------------------------------------
main_window = Tk()
main_window.title('Crop recognition and Irrigation suggestion system ')
main_window.iconbitmap('plant.ico')
main_window.configure(bg="#c4edc0") 

main_window.geometry("550x380+50+30") 
main_window.resizable(0, 0)

window_width = main_window.winfo_width()
window_height = main_window.winfo_height()
window_x = main_window.winfo_rootx()
window_y = main_window.winfo_rooty()
new_window_x = window_height + window_x
new_window_y = window_width + window_y

main_img_frame = Frame(main_window, bg="#c4edc0")
main_img_frame.pack(fill="both", expand=True)

main_img = Image.open("window_image.png")
main_img = main_img.resize((350, 200))
main_photo = ImageTk.PhotoImage(main_img)

label_main_img = Label(main_img_frame, image=main_photo, bg="#c4edc0")
label_main_img.pack(padx=20)

main_button_frame = Frame(main_window, bg="#c4edc0")
main_button_frame.pack(padx=15, fill="both", expand=True, side="bottom")

CR_button_img = Image.open("CR_button.png")
CR_button_img = CR_button_img.resize((188, 100))
CR_photo_img = ImageTk.PhotoImage(CR_button_img)

IS_button_img = Image.open("IS_button.png")
IS_button_img = IS_button_img.resize((188, 100))
IS_button_img = ImageTk.PhotoImage(IS_button_img)

button_CR = Button(main_button_frame, text="Crop\nrecognition", image=CR_photo_img, 
                 compound="center", bg="#c4edc0", font=("Monserrat", 19, "bold"),
                 borderwidth=0, activebackground="#c4edc0", command=open_CR_window)
button_CR.pack(padx=20, pady=15, side="left", fill="both", expand=True)

button_IS = Button(main_button_frame, text="Irrigation\nsuggestion", image=IS_button_img, 
                 compound="center", bg="#c4edc0", font=("Monserrat", 19, "bold"),
                 borderwidth=0, activebackground="#c4edc0", command=open_Form_window)
button_IS.pack(padx=20, pady=15, side="right", fill="both", expand=True)

main_window.mainloop()

