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

def input_value():
    global types_raw, water, times  
    types_raw = type_entry.get()
    temp_raw = temp_spinbox.get()
    mois_raw = mois_combobox.get()
    soil_raw = soil_combobox.get()
    stage_raw = stage_combobox.get()

    if types_raw and temp_raw and mois_raw and soil_raw and stage_raw:
        types_raw = type_input
        types = Dictionary_AI.type_map.get(types_raw)
        temp = temp_raw
        mois = Dictionary_AI.mois_map.get(mois_raw)()
        soil = Dictionary_AI.soil_map.get(soil_raw)
        stage = Dictionary_AI.stage_map.get(stage_raw)

        Fuzzy_plant.watering.input['kind'] = float(types)
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
        # Fuzzy_plant.water.view(sim=Fuzzy_plant.watering)
        open_IS_window()
    else:
        messagebox.showwarning(title="Warning", message="You must input all values")


def open_IS_window():
    global is_IS_window_opened, IS_window, types_raw
    if not is_IS_window_opened:

        IS_window = Toplevel()
        IS_window.title("Irrigation suggestion")
        IS_window.iconbitmap("water2.ico")
        IS_window.geometry(f"+600+{new_window_x + 35}")

        IS_label = Label(IS_window, text="Irrigation suggestion")
        IS_label.pack()

        IS_frame = Frame(IS_window)
        IS_frame.columnconfigure(0, weight=1, minsize=100)
        IS_frame.columnconfigure(1, weight=1, minsize=200)
        IS_frame.pack(side="bottom", fill="both", expand=True, pady=15)

        infor_frame = Frame(IS_frame)
        infor_frame.columnconfigure(0, weight=1, minsize=65)
        infor_frame.columnconfigure(1, weight=1, minsize=65)
        infor_frame.columnconfigure(2, weight=1, minsize=65)
        infor_frame.columnconfigure(3, weight=1, minsize=65)
        infor_frame.columnconfigure(4, weight=1, minsize=65)
        infor_frame.columnconfigure(5, weight=1, minsize=65)
        infor_frame.columnconfigure(6, weight=1, minsize=65)
        infor_frame.rowconfigure(2, minsize=40)
        infor_frame.grid(row=0, column=0)

        suggest_frame = Frame(IS_frame)
        suggest_frame.grid(row=0, column=1)

        #Label_frame
        img1 = Image.open("plant2.png")
        img1 = img1.resize((50, 50))
        photo_img1 = ImageTk.PhotoImage(img1)
        label1 = Label(infor_frame, image=photo_img1)
        label1.grid(row=0, column=0, columnspan=2)
        label1.image = photo_img1

        img2 = Image.open("cloudy-day.png")
        img2 = img2.resize((50, 50))
        photo_img2 = ImageTk.PhotoImage(img2)
        label2 = Label(infor_frame, image=photo_img2)
        label2.grid(row=0, column=2, columnspan=2)
        label2.image = photo_img2

        img3 = Image.open("soil-analysis.png")
        img3 = img3.resize((50, 50))
        photo_img3 = ImageTk.PhotoImage(img3)
        label3 = Label(infor_frame, image=photo_img3)
        label3.grid(row=0, column=4, columnspan=2)
        label3.image = photo_img3

        type_label = Label(infor_frame, text=type_entry.get(),
                           font=("Monserrat", 15, "bold"))
        type_label.grid(row=1, column=0, columnspan=2)
        temp_label = Label(infor_frame, text=temp_spinbox.get() + "°C",
                           font=("Monserrat", 15, "bold"))
        temp_label.grid(row=1, column=2, columnspan=2)
        mois_label = Label(infor_frame, text=mois_combobox.get(),
                           font=("Monserrat", 15, "bold"))
        mois_label.grid(row=1, column=4, columnspan=2)

        img4 = Image.open("plant1.png")
        img4 = img4.resize((50, 50))
        photo_img4 = ImageTk.PhotoImage(img4)
        label4 = Label(infor_frame, image=photo_img4)
        label4.grid(row=3, column=1, columnspan=2)
        label4.image = photo_img4

        img5 = Image.open("sakura.png")
        img5 = img5.resize((50, 50))
        photo_img5 = ImageTk.PhotoImage(img5)
        label5 = Label(infor_frame, image=photo_img5)
        label5.grid(row=3, column=3, columnspan=2)
        label5.image = photo_img5

        soil_label = Label(infor_frame, text=soil_combobox.get(),
                           font=("Monserrat", 15, "bold"))
        soil_label.grid(row=4, column=1, columnspan=2)

        stage_label = Label(infor_frame, text=stage_combobox.get(),
                            font=("Monserrat", 15, "bold"))
        stage_label.grid(row=4, column=3, columnspan=2)

        img7 = Image.open("right-arrow (1).png")
        img7 = img7.resize((50, 50))
        photo_img7 = ImageTk.PhotoImage(img7)
        label7 = Label(infor_frame, image=photo_img7)
        label7.grid(row=2, column=6, columnspan=2)
        label7.image = photo_img7

        # Suggest_frame
        water_label = Label(suggest_frame, text=water,
                            font=("Monserrat", 25, "bold"), foreground="blue")
        water_label.grid(row=0, column=0)

        time_label = Label(suggest_frame, text=times,
                           font=("Monserrat", 25, "bold"), foreground="red")
        time_label.grid(row=1, column=0)

        img6 = Image.open("watering-plants.png")
        img6 = img6.resize((100, 100))
        photo_img6 = ImageTk.PhotoImage(img6)
        label6 = Label(suggest_frame, image=photo_img6)
        label6.grid(row=0, column=1, rowspan=2)
        label6.image = photo_img6

        for widget in infor_frame.winfo_children():
            widget.grid_configure()

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

    
def CNN_model(x):
    global result_int

    model = load_model("CNN_plant.h5")

    img_CNN = load_img(x, target_size=(32, 32, 3))
    img_CNN = img_to_array(img_CNN)
    img_CNN = img_CNN.astype("float32")/255
    img_CNN = img_CNN.reshape((1, 32, 32, 3))

    result = np.argmax(model.predict(img_CNN), axis=-1)
    result_int = result.item()


def open_CR_window():
    global is_CR_window_opened, CR_window, file_path
    if not is_CR_window_opened:
 
        file_path = filedialog.askopenfilename()
        CNN_model(file_path)

        img = Image.open(file_path)
        img = img.resize((200, 200))

        CR_window = Toplevel(bg="#FEF0EA")
        CR_window.title("Crop recognition")
        CR_window.iconbitmap("leave.ico")
        CR_window.geometry(f"780x650+{new_window_y}+80")

        CR_label = Label(CR_window, text="Crop recognition", 
                         font=("Monserrat", 15, "bold"), bg="#FEF0EA")
        CR_label.pack(side="top", pady=10)

        CR_frame = Frame(CR_window, bg="#FEF0EA")
        CR_frame.pack(side="top", fill="both", expand=True)

        scrollbar = Scrollbar(CR_frame)
        scrollbar.pack(side="right", fill="y")

        description = Text(CR_frame, wrap="word", yscrollcommand=scrollbar.set, borderwidth=0, 
                           selectbackground="#96f8ff", selectforeground="#000000", bg="#FEF0EA")  # "#ddf0ff"
        description.configure(state="normal")

        description.insert("1.0", "    ")
        photo_img = ImageTk.PhotoImage(img)
        description.image_create("end", image=photo_img)
        description.image = photo_img

        description.tag_config("name", font=("Microsoft Yahei UI", 20, "bold")) #30
        description.tag_config("title", font=("Microsoft Yahei UI", 16, "bold"))
        description.tag_config("text", font=("Microsoft Yahei UI", 14), foreground="#0A3715")

        content = Dictionary_AI.CNN_map_content.get(result_int, "None")

        description.insert("end", "        ")
        description.insert("end", Dictionary_AI.CNN_map_title.get(result_int, "None"), "name")
        description.insert("end", "\n")

        description.insert("end", content[0], "title")
        description.insert("end", content[1], "text")
        description.insert("end", content[2], "title")
        description.insert("end", content[3], "text")
        description.insert("end", content[4], "title")
        description.insert("end", content[5], "text")
        description.insert("end", content[6], "title")
        description.insert("end", content[7], "text")

        description.configure(state="disabled")
        description.pack(side="left", fill="both", expand=True, pady=10, padx=25)

        scrollbar.config(command=description.yview)

        CR_window.protocol("WM_DELETE_WINDOW", close_CR_window)
        is_CR_window_opened = True


def close_CR_window():
    global is_CR_window_opened, CR_window
    is_CR_window_opened = False
    CR_window.destroy()
    

def handle_image(event):
    global type_input
    if type_entry.get() == "Tải ảnh lên":
        IS_file_path = filedialog.askopenfilename()
        CNN_model(IS_file_path)
        type_input = Dictionary_AI.CNN_map_type.get(result_int, "Herbaceous")
    else:
        type_input = type_entry.get()


def open_Form_window():
    global is_Form_window_opened, Form_window
    global type_entry, mois_combobox, temp_spinbox, soil_combobox, stage_combobox
  
    if not is_Form_window_opened:
        Form_window =Toplevel()
        Form_window.title("Information")
        Form_window.iconbitmap("water2.ico")
        Form_window.geometry(f"+80+{new_window_x + 35}")
        Form_window.resizable(0, 0)

        form_label = Label(Form_window, text="Information for Irrigation suggestion")
        form_label.pack(pady=10)

        form_frame = Frame(Form_window)
        form_frame.pack(side=TOP, fill=BOTH, padx=10, pady=10)

        typeofplant = Label(form_frame, text="Type")
        typeofplant.grid(row=0, column=0, columnspan=2)
        temp = Label(form_frame, text="Temperature")
        temp.grid(row=0, column=2, columnspan=2)
        mois = Label(form_frame, text="Moisture")
        mois.grid(row=0, column=4, columnspan=2)

        type_entry = ttk.Combobox(form_frame, values=["Herbaceous", "Wood", "Tải ảnh lên"], width=12)
        type_entry.configure(font=("Arial", 12))
        type_entry.bind("<<ComboboxSelected>>", handle_image)
        type_entry.grid(row=1, column=0, columnspan=2)

        temp_spinbox = Spinbox(form_frame, from_=5, to=45, textvariable=StringVar(value="25"), width=12)
        temp_spinbox.grid(row=1, column=2, columnspan=2)
        temp_spinbox.configure(font=("Arial", 12))
        mois_combobox = ttk.Combobox(form_frame, values=["Dry", "Moist", "Wet"], width=12)
        mois_combobox.grid(row=1, column=4, columnspan=2)
        mois_combobox.configure(font=("Arial", 12))
        
        space_label = Label(form_frame, text=" ")
        space_label.grid(row=2, column=0)

        soil = Label(form_frame, text=" Soil ")
        soil.grid(row=3, column=1, columnspan=2)
        stage = Label(form_frame, text="Stage")
        stage.grid(row=3, column=3, columnspan=2)

        soil_combobox = ttk.Combobox(form_frame, values=["Sand", "Alluvium", "Loam", "Clay"], width=12)
        soil_combobox.configure(font=("Arial", 12))
        soil_combobox.grid(row=4, column=1, columnspan=2)
        stage_combobox = ttk.Combobox(form_frame, values=["Germination", "Growing", "Full-growing"], width=12)
        stage_combobox.configure(font=("Arial", 12))
        stage_combobox.grid(row=4, column=3, columnspan=2)

        for widget in form_frame.winfo_children():
            widget.grid_configure(padx=15, pady=5)

        submit = Button(form_frame, text="  clickkkk  ", command=input_value)
        submit.grid(row=5, column=2, columnspan=2, pady=15)

        Form_window.protocol("WM_DELETE_WINDOW", close_Form_window)
        is_Form_window_opened = True

        
def close_Form_window():
    global is_Form_window_opened, Form_window
    is_Form_window_opened = False
    Form_window.destroy()


is_Form_window_opened = False
is_CR_window_opened = False
is_IS_window_opened = False


window = Tk()
window.title('Crop recognition and Irrigation suggestion system ')
window.iconbitmap('plant.ico')
window.configure(bg="#C1D9BF") #9effae  #BFD8BD #98C9A3 #94C79F #B5D2B2
window.geometry("450x250+80+80")
window.resizable(0, 0)

window_width = window.winfo_width()
window_height = window.winfo_height()
window_x = window.winfo_rootx()
window_y = window.winfo_rooty()

label = Label(window, text="Hello!", 
              font=("Monserrat", 19, "bold"),bg="#C1D9BF")
label.pack(pady=15)

frame = Frame(bg="#C1D9BF")
frame.pack(padx=15, fill="both", expand=True)

new_window_x = window_height + window_x
new_window_y = window_width + window_y
button1 = Button(frame, text="Crop\nrecognition",
                 font=("Monserrat", 19, "bold"), command=open_CR_window)
button2 = Button(frame, text="Irrigation\nsuggestion",
                 font=("Monserrat", 19, "bold"), command=open_Form_window)

button1.pack(padx=20, pady=30, side="left", fill="both", expand=True)
button2.pack(padx=20, pady=30, side="right", fill="both", expand=True)

window.mainloop()

