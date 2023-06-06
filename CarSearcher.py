import tkinter as tk
from tkinter import ttk


import requests
from bs4 import BeautifulSoup
#requires 
#pip3 install -U selenium
#pip3 install webdriver-manager
#bs4




make = ""
model = ""
year = ""
sort = ""
car_dict = {}


def get_selected_values(make_var, model_var, year_var, sort_var):
    make = make_var.get()
    model = model_var.get()
    year = year_var.get()
    sort = sort_var.get()

    print("Selected values:")
    print("Make:", make)
    print("Model:", model)
    print("Year:", year)
    print("Sort:", sort)



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
                each_row[1] = model.text
            elif group_index == 1:
                # Process the make element
                make = element
                #print("Make:", make.text)
                each_row[0] = make.text
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
                
    print(car_dict)
    
    
    
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
    sort_var = tk.StringVar()

    # Create the make dropdown
    make_label = ttk.Label(window, text="Make:")
    make_label.grid(row=0, column=0, sticky=tk.W, padx=pad_x, pady=pad_y)

    make_combo = ttk.Combobox(window, textvariable=make_var, state='readonly')
    make_combo['values'] = list(car_dict.keys())
    make_combo.grid(row=0, column=1, sticky=tk.W+tk.E, padx=pad_x, pady=pad_y)


    # Create the model dropdown
    model_label = ttk.Label(window, text="Model:")
    model_label.grid(row=1, column=0, sticky=tk.W, padx=pad_x, pady=pad_y)

    model_combo = ttk.Combobox(window, textvariable=model_var, state='readonly')
    model_combo.grid(row=1, column=1, sticky=tk.W+tk.E, padx=pad_x, pady=pad_y)

    def update_models(event):
        selected_make = make_var.get()

        if selected_make not in car_dict:
            model_combo['values'] = ()
        else:
            models = car_dict[selected_make].keys()
            model_combo['values'] = list(models)
            model_var.set('')  # Clear the selected models option
            year_combo['values'] = () # reset years


                    
    def update_years(event):
        selected_make = make_var.get()
        selected_model = model_var.get()

        if selected_make in car_dict and selected_model in car_dict[selected_make]:
            years = car_dict[selected_make][selected_model]
            # years is taken from the website as a string "1990, 1991, 1992, " etc. this splits it into a list
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

    # Create the sort dropdown
    sort_label = ttk.Label(window, text="Sort:")
    sort_label.grid(row=3, column=0, sticky=tk.W, padx=pad_x, pady=pad_y)

    sort_combo = ttk.Combobox(window, textvariable=sort_var, state='readonly')
    sort_combo['values'] = ('Price', 'Mileage', 'Year')
    sort_combo.grid(row=3, column=1, sticky=tk.W+tk.E, padx=pad_x, pady=pad_y)

    # Create the button to get selected values
    def search_command():
        get_selected_values(make_var, model_var, year_var, sort_var)

    button = ttk.Button(window, text="Search", command=search_command)
    button.grid(row=4, columnspan=2, pady=10)
    
    # Disable the button initially
    button['state'] = 'disabled'

    # Validate the option selection to enable/disable the button
    def validate_options(*args):
        if make_var.get() and model_var.get() and year_var.get() and sort_var.get():
            button['state'] = 'normal'
        else:
            button['state'] = 'disabled'

    # Validate whenever an option changes
    make_var.trace('w', validate_options)
    model_var.trace('w', validate_options)
    year_var.trace('w', validate_options)
    sort_var.trace('w', validate_options)

    # Configure grid weights to make the dropdowns scale with window resizing
    window.grid_columnconfigure(1, weight=1)
    window.grid_rowconfigure(4, weight=1)

    # Start the main event loop
    window.mainloop()

   

def main():
    
    get_makes_and_models()
    create_window()
    
if __name__ == '__main__':
    main()

