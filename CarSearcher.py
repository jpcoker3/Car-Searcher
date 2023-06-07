import tkinter as tk
from tkinter import ttk

import webbrowser
import string
import sys
import json
import os

import requests
from bs4 import BeautifulSoup

import pandas as pd

#bs4
#pandas


file_path = 'data.json'

make = ""
model = ""
year = ""
zip_code = ""
car_dict = {}
    
def save_dict_to_json():
    with open(file_path, 'w') as file:
        json.dump(car_dict, file)
        print(car_dict)

def load_dict_from_json():
    if not os.path.exists(file_path):
        get_makes_and_models() # if no file esists, create it
    else:
        global car_dict
        with open(file_path, 'r') as file:
            car_dict = json.load(file)
            print(car_dict)

# get data from GUI and search for cars
def search(make_var, model_var, year_var, zip_code_):
    make = make_var.get()
    model = model_var.get()
    year = year_var.get()
    zip_code = zip_code_.get()

    print("Selected values:")
    print("Make:", make)
    print("Model:", model)
    print("Year:", year)
    print("zip_code:", zip_code)
    
    search_autotempest(make, model, year, zip_code)
    #search_fb_marketplace(make, model, year, zip_code)  #NOT WORKING YET
    
def search_autotempest(make, model, year, zip_code = "90210"):
    #clean variables for link. 
    make = make.replace(" ", "")
    make = make.lower()
    
    model = model.replace(" ", "")
    model = model.lower()
    
    #example link
    #https://www.autotempest.com/results?make=toyota&model=mr2spyder&zip=39211&localization=any&domesticonly=0
    
    url = ("https://www.autotempest.com/results?make="+ make +
                "&model="+model+ 
                "&zip="+str(zip_code) +
                "&localization=any&domesticonly=0")
    if year != "":
        url += "&minyear=" + year+ "&maxyear=" + year

    webbrowser.open(url, new=0, autoraise=True)
    
def search_fb_marketplace(make, model, year, zip_code = "90210"):
    #clean variables for link. 
    make = make.replace(" ", "-")
    make = make.lower()
    
    model = model.replace(" ", "-")
    model = model.lower()

    
    #example link
    #https://www.facebook.com/marketplace/category/acura-legend
    
    url = ("https://www.facebook.com/marketplace/category/"+ make + "-" + model)
    
    webbrowser.open(url, new=0, autoraise=True)
    
def get_makes_and_models():
    global car_dict

    car_makes_first_letter = "ABCDEFGHIJKLMNOPRSTV"
        
    for page in car_makes_first_letter:
        url = "https://www.kbb.com/car-make-model-list/used/"+page+"/make/"
        data = requests.get(url)
    
        
        soup = BeautifulSoup(data.text, 'html.parser')
        chart = soup.find(class_="css-1q107tk ee33uo30")
        list_of_all = chart.find_all(class_="css-irk93x ee33uo33")
        
        each_row = [None, None]
        for index, element in enumerate(list_of_all):
            # Get the index within the group of three elements
            group_index = index % 3
            # make list of row for easier processing later
            if group_index == 0:
                each_row = [None, None]

            if group_index == 0:
                # Process the model element
                model = element
                #print("Model:", model.text)
                each_row[1] = string.capwords(model.text)
            elif group_index == 1:
                # Process the make element
                make = element
                #print("Make:", make.text)
                each_row[0] = string.capwords(make.text)
            elif group_index == 2:
                # Process the years element
                years = element
                #print("Years:", years.text)
                each_row.append(years.text)
            
            # when list for row is complete, add to dictionary
            if group_index == 2:
                make = each_row[0]
                model = each_row[1]
                
                if make not in car_dict:
                    car_dict[make] = {}
                
                car_dict[make][model] = []
                
                for each_year in range(2, len(each_row)):
                    year = each_row[each_year]
                
                    car_dict[make][model].append(year)
                
    save_dict_to_json()
    
def create_window():
    pad_x = 10
    pad_y = 10
    # Create the main window
    window = tk.Tk()
    window.title("Car Selector")
    window.geometry('600x400')

    # Scale up the font size
    style = ttk.Style()
    style.configure('TLabel', font=('Arial', 16))  # Adjust the font size for labels
    style.configure('TCombobox', font=('Arial', 16))  # Adjust the font size for comboboxes

    # Set the margin around the window
    window.configure(padx=20, pady=20)

    # Create variables to store selected values
    make_var = tk.StringVar()
    model_var = tk.StringVar()
    year_var = tk.StringVar()
    zip_code_var = tk.StringVar()

    # Create the make dropdown
    make_label = ttk.Label(window, text="Make: *")
    make_label.grid(row=0, column=0, sticky=tk.W, padx=pad_x, pady=pad_y)

    make_combo = ttk.Combobox(window, textvariable=make_var, state='readonly')
    make_combo['values'] = list(car_dict.keys())
    make_combo.grid(row=0, column=1, sticky=tk.W+tk.E, padx=pad_x, pady=pad_y)


    # Create the model dropdown
    model_label = ttk.Label(window, text="Model: *")
    model_label.grid(row=1, column=0, sticky=tk.W, padx=pad_x, pady=pad_y)

    model_combo = ttk.Combobox(window, textvariable=model_var, state='readonly')
    model_combo.grid(row=1, column=1, sticky=tk.W+tk.E, padx=pad_x, pady=pad_y)

    def update_models(event):
        selected_make = make_var.get()

        if selected_make not in car_dict:
            model_combo['values'] = ()
            year_var.set('')  # Clear the selected years option
            year_combo['values'] = () # reset year
        else:
            models = car_dict[selected_make].keys()
            model_combo['values'] = list(models)
            model_var.set('')  # Clear the selected models option
            year_var.set('')  # Clear the selected years option
            year_combo['values'] = () # reset years
            


                    
    def update_years(event):
        selected_make = make_var.get()
        selected_model = model_var.get()

        if selected_make in car_dict and selected_model in car_dict[selected_make]:
            years = car_dict[selected_make][selected_model]
            # years is taken from the website as a string "1990, 1991, 1992, " etc. this splits it into a list
            print(str(years))
            #years = years.strip('[]')
            years = years[0].split(', ')
            year_combo['values'] = years  # Unpack the years list
            year_var.set('')  # Clear the selected years option
        else:
            year_combo['values'] = ()



    make_combo.bind("<<ComboboxSelected>>", update_models)
    model_combo.bind("<<ComboboxSelected>>", update_years)
    # Create the year dropdown
    year_label = ttk.Label(window, text="Year:")
    year_label.grid(row=2, column=0, sticky=tk.W, padx=pad_x, pady=pad_y)

    year_combo = ttk.Combobox(window, textvariable=year_var, state='readonly')
    year_combo['values'] = ('')
    year_combo.grid(row=2, column=1, sticky=tk.W+tk.E, padx=pad_x, pady=pad_y)

    # Create the zip_code label
    zip_code_label = ttk.Label(window, text="Zip Code:")
    zip_code_label.grid(row=3, column=0, sticky=tk.W, padx=pad_x, pady=pad_y)

    # Create the zip_code entry
    zip_code_entry = tk.Entry(window, textvariable=zip_code_var)
    zip_code_entry.grid(row=3, column=1, sticky=tk.W+tk.E, padx=pad_x, pady=pad_y)

    

    # Create the button to get selected values
    def search_command():
        search(make_var, model_var, year_var, zip_code_var)

    button = ttk.Button(window, text="Search", command=search_command)
    button.grid(row=4, columnspan=2, pady=10)
    
    # Disable the button initially
    button['state'] = 'disabled'

    # Validate the option selection to enable/disable the button
    def validate_options(*args):
        if make_var.get() and model_var.get():
            button['state'] = 'normal'
        else:
            button['state'] = 'disabled'

    # Validate whenever an option changes
    make_var.trace('w', validate_options)
    model_var.trace('w', validate_options)
    year_var.trace('w', validate_options)
    zip_code_var.trace('w', validate_options)

    # Configure grid weights to make the dropdowns scale with window resizing
    window.grid_columnconfigure(1, weight=1)
    window.grid_rowconfigure(4, weight=1)

    # Start the main event loop
    window.mainloop()

def main():
    
    load_dict_from_json()
    create_window()
    
if __name__ == '__main__':
    main()
