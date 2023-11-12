import tkinter as tk
import customtkinter
import re
import csv
import numpy as np

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Tsugite: Custom shelter generator")
        self.iconbitmap("New Project.ico")
        self.geometry(f"{1000}x{580}")

        # configure grid layout (3x14)
        self.sidebar_frame = customtkinter.CTkFrame(self, width=240, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, padx = 10, pady = 10, rowspan=16, columnspan=1, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,16), weight=1)
        
        # Create title
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Earthquake Shelter Generator", font=customtkinter.CTkFont(size=18, weight="bold"), anchor="w")
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 5))
        self.logo_label.configure(anchor="s")
        self.logo_label.configure(justify="left")
        
        # Create subtitle
        self.label_subtitle = customtkinter.CTkLabel(master=self.sidebar_frame, text="Fill in your information and draw your desired plan \nto create your own custom shelter!", font=customtkinter.CTkFont(size=10))
        self.label_subtitle.grid(row=1, column=0, columnspan=1, padx=20, pady= (5, 10), sticky= "w")
        self.label_subtitle.configure(anchor="n")
        self.label_subtitle.configure(justify="left")

        # create entries for peoples information
        self.entry_name = customtkinter.CTkEntry(self.sidebar_frame, width=225, placeholder_text="Name")
        self.entry_name.grid(row=2, column=0, columnspan=1, padx=20, pady=(10, 5))

        self.entry_email = customtkinter.CTkEntry(self.sidebar_frame, width=225, placeholder_text="Email")
        self.entry_email.grid(row=3, column=0, columnspan=1, padx=20, pady=5)

        self.entry_phonenumber = customtkinter.CTkEntry(self.sidebar_frame, width=225, placeholder_text="Phonenumber")
        self.entry_phonenumber.grid(row=4, column=0, columnspan=1, padx=20, pady=5)

        self.entry_adress = customtkinter.CTkEntry(self.sidebar_frame, width=225, placeholder_text="Adress")
        self.entry_adress.grid(row=5, column=0, columnspan=1, padx=20, pady= 5)
        
        #amount of people
        self.amount_of_people = customtkinter.CTkComboBox(self.sidebar_frame, width =225, values=["How many people need shelter?"] + [str(i) for i in range(1, 11)])
        self.amount_of_people.grid(row=6, column=0, padx=20, pady=5)

        #amount of people
        self.stories = customtkinter.CTkComboBox(self.sidebar_frame, width =225, values=["How many stories?"] + [str(i) for i in range(1, 3)])
        self.stories.grid(row=7, column=0, padx=20, pady=5)

        #create an error label when someone fills in something incorrectly
        self.error_label = customtkinter.CTkLabel(self.sidebar_frame, text="Please fill in everything before drawing", font=customtkinter.CTkFont(size=10), text_color="grey")
        self.error_label.grid(row=8, column=0, columnspan=1, padx=20, pady=0)

		#submit button to send over their information to an cvs file
        self.submit_button = customtkinter.CTkButton(self.sidebar_frame, command=self.save_personal_info, text="Submit")
        self.submit_button.grid(row=10, column=0, padx=20, pady=(5,40))
        
		#button to change theme to dark or light etc.
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="s")
        self.appearance_mode_label.grid(row=11, column=0, padx=20, pady= 0)

        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], width= 225, command=self.change_appearance_mode_event, anchor = "s")
        self.appearance_mode_optionemenu.grid(row=12, column=0, padx=20, pady=0)
        
		#scaling of the page
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="Scale window:", anchor="s")
        self.scaling_label.grid(row=14, column=0, padx=20, pady= 0)

        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["100%", "110%", "120%", "130%"], width=225, command=self.change_scaling_event, anchor="s")
        self.scaling_optionemenu.grid(row=15, column=0, padx=20, pady=(0, 20))

        #create canvas for drawing
        self.canvas_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.canvas_frame.grid(row=0, column=1, padx=10, pady=10, rowspan=16, columnspan=2, sticky="nsew")

        self.canvas = tk.Canvas(self.canvas_frame, width=400, height=400, bg="white")
        self.canvas.grid(row=11, column=1, rowspan = 11, columnspan=2, padx=20, pady=0)
        
        #create background grid on canvas
        for i in range(0, 400, 40):
            self.canvas.create_line(i, 0, i, 400, fill="lightgray")
            self.canvas.create_line(0, i, 400, i, fill="lightgray")

        self.drawing = False
        self.coords = []
        self.final_points = []
        self.center_coords = []

        self.canvas.bind('<Button-1>', self.draw)
        self.canvas.pack()

        #create an error label when someone fills in something incorrectly
        self.error_label2 = customtkinter.CTkLabel(self, text="Draw your own plan here:", font=customtkinter.CTkFont(size=10), text_color="grey", bg_color="grey86", anchor="s")
        self.error_label2.grid(row=11, column=1, columnspan=2, padx=20, pady=0)
        
        #clear canvas
        self.clear_button = customtkinter.CTkButton(self, text="Clear Canvas", command=self.clear_canvas, bg_color="grey86")
        self.clear_button.grid(row=12, column=1, columnspan=2, padx=10, pady=5)
        
        #send over the point to generate 3D model
        self.render = customtkinter.CTkButton(self, text="Render", command=self.save_to_csv, bg_color="grey86")
        self.render.grid(row=13, column=1, rowspan = 1, columnspan=2, padx=10, pady=(0, 10))
        self.render.configure(state="disabled")
        
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        scaled_width = int(1000 * new_scaling_float)  # Scale the width of the main window
        scaled_height = int(580 * new_scaling_float)  # Scale the height of the main window
        self.geometry(f"{scaled_width}x{scaled_height}")  # Set new dimensions for the main window
        customtkinter.set_widget_scaling(new_scaling_float)

    def is_valid_name(self, name):
        pattern = r'^[a-zA-Z- ]+$'
        return re.match(pattern, name) is not None
    
    def is_valid_email(self, email):
        # Regular expression to validate email format
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(pattern, email) is not None
    
    def is_valid_phonenumber(self, phonenumber):
        # Regular expression to validate phone number format (only digits)
        pattern = r'^\d+$'
        return re.match(pattern, phonenumber) is not None

    def is_valid_address(self):
        # Split the address into components
        components = self.entry_adress.get().split(',')

        # Check if all required components are present
        if len(components) >= 4:
            street = components[0].strip()
            house_number = components[1].strip()
            town = components[2].strip()
            country = components[3].strip()

            # Check if each component is not empty
            if street and house_number and town and country:
                return True

        return False

    def save_personal_info(self):
        name = self.entry_name.get()
        email = self.entry_email.get()
        phonenumber = self.entry_phonenumber.get()
        address = self.entry_adress.get()
        people = self.amount_of_people.get()
        stories = self.stories.get()

        # Check if everything is provided
        if (
            name
            and email
            and phonenumber
            and address
            and people != "How many people need shelter?"
            and stories != "How many stories?"
            and self.is_valid_name(name)
            and self.is_valid_email(email)
            and self.is_valid_phonenumber(phonenumber)
            and self.is_valid_address()
        ):
            # Open the CSV file in append mode and write the information
            with open('data.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["name", "email", "phonenumber", "address", "people", "stories"])
                writer.writerow([name, email, phonenumber, address, people, stories])
                print(f"Saved {name}, {email}, {phonenumber}, {address}, {people}, {stories} to data.csv")
            # Reset error message if it was previously displayed
            self.error_label.configure(text="Information successfully saved!", text_color="green")
            self.render.configure(state="normal")
        else:
            if not self.is_valid_name(name):
               self.error_label.configure(text="Please give a valid name", text_color="red")
            elif not self.is_valid_email(email):
               self.error_label.configure(text="Please give a valid email adress", text_color="red")
            elif not self.is_valid_phonenumber(phonenumber):
               self.error_label.configure(text="Please give a valid phonenumber (061234567)", text_color="red") 
            elif not self.is_valid_address():
               self.error_label.configure(text="Please give adress like: street, housenumber, town, country", text_color="red")
            else:
               self.error_label.configure(text="Please fill in all the boxes correctly", text_color="red")

    def center_of_rectangle(self, x, y):
        return x + 20, y + 20

    def save_to_csv(self):
        global square_generated
        num_squares = len(self.center_coords)  # Number of squares generated
        total_area = num_squares  # Area covered by squares

        if not square_generated:
            self.error_label2.configure(text="Please draw a plan first.", text_color="red")
        elif (int(self.amount_of_people.get()) * 6) > total_area:
            print ((int(self.amount_of_people.get()) * 6), total_area)
            self.error_label2.configure(text="Area is too small for the specified number of people.", text_color="red")
        else:
            with open('points.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["X", "Y"])  # Header
                writer.writerows(self.center_coords)
                print("saved")
            self.error_label2.configure(text="Information successfully saved!", text_color="green")

    def draw(self, event):
        global square_generated
        x = (event.x // 40) * 40
        y = (event.y // 40) * 40

        points_to_add = [(x, y), (x, y + 40), (x + 40, y), (x + 40, y + 40)]

        for point in points_to_add:
            if point not in self.coords:
                self.coords.append(point)
                self.canvas.create_oval(point[0] - 2, point[1] - 2, point[0] + 2, point[1] + 2, fill="blue")

        self.canvas.create_rectangle(x, y, x + 40, y + 40, outline="black")
        self.coords.append((x, y))

        center = self.center_of_rectangle(x, y)
        if center not in self.center_coords:
            self.center_coords.append(center)
        
        square_generated = True
        return square_generated

    def generate_grid(self):
        if len(self.coords) > 1:
            x_coords, y_coords = zip(*self.coords)

            x_points = np.array(x_coords)
            y_points = np.array(y_coords)
            np.unique(x_points)
            np.unique(y_points)

            spacing = 40

            x_final = x_points
            y_final = y_points
            z_final = np.zeros_like(x_final)

            i = 0
            while i < len(x_final):
                self.final_points.append((int(x_final[i] / 40), int(y_final[i] / 40), int(z_final[i] / 40)))
                i += 1
            print(self.final_points)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.coords = []
        self.center_coords = []
        for i in range(0, 400, 40):
            self.canvas.create_line(i, 0, i, 400, fill="lightgray")
            self.canvas.create_line(0, i, 400, i, fill="lightgray")
 
        with open('points.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["X", "Y"]) 
   
if __name__ == "__main__":
    app = App()
    app.mainloop()