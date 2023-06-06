import tkinter as tk
from tkinter import ttk
from selenium import webdriver

from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager 

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
    #set url
    url = "https://www.carvana.com/cars"
    
    #set options
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--headless=new")
    
    #create driver
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=options) 

    
    driver.get(url)
    
    '''
    wait = WebDriverWait(driver, 10)
    models = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-qa="filters.expandfacet-make-model-headerButton"]')))
    print(models.text)
    # models.click()


    wait = WebDriverWait(driver, 5)
    show_more = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-qa="filters.toggle-all-makes-button"]')))
    print(show_more.text)
    # show_more.click()
'''

    

    #get the html
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    
    

    
    results = soup.find(id="__next")
    makes_and_models = results.find_all("div", class_= "grid gap-16 p-32")[0]
    
    result_dict = {}
    current_key = None
    current_values = []
    
    for makes_and_model in makes_and_models.find_all("input"):
        id = makes_and_model.get("id")
        
        #get make as key
        if id.startswith("make-"):
            if current_key:
                result_dict[current_key] = current_values
                current_values = []
            current_key = id.replace("make-", "")
        #get model as value
        elif id.startswith("model-") and current_key:
            current_values.append(id.replace("model-", ""))

    if current_key:
        result_dict[current_key] = current_values
    
    global car_dict
    car_dict = result_dict
    
    
    
    
def create_window():
    pad_x = 10
    pad_y = 10
    # Create the main window
    window = tk.Tk()
    window.title("Car Selector")

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

    make_combo = ttk.Combobox(window, textvariable=make_var)
    make_combo['values'] = list(car_dict.keys())
    make_combo.grid(row=0, column=1, sticky=tk.W+tk.E, padx=pad_x, pady=pad_y)

    # Create the model dropdown
    model_label = ttk.Label(window, text="Model:")
    model_label.grid(row=1, column=0, sticky=tk.W, padx=pad_x, pady=pad_y)

    model_combo = ttk.Combobox(window, textvariable=model_var)
    model_combo.grid(row=1, column=1, sticky=tk.W+tk.E, padx=pad_x, pady=pad_y)

    def update_models(event):
        selected_make = make_var.get()
        if selected_make in car_dict:
            models = car_dict[selected_make]
            model_combo['values'] = models
            model_var.set('')  # Clear the selected models option
        else:
            model_combo['values'] = ()

    make_combo.bind("<<ComboboxSelected>>", update_models)

    # Create the year dropdown
    year_label = ttk.Label(window, text="Year:")
    year_label.grid(row=2, column=0, sticky=tk.W, padx=pad_x, pady=pad_y)

    year_combo = ttk.Combobox(window, textvariable=year_var)
    year_combo['values'] = ('Test Year 1', 'Test Year 2', 'Test Year 3')
    year_combo.grid(row=2, column=1, sticky=tk.W+tk.E, padx=pad_x, pady=pad_y)

    # Create the sort dropdown
    sort_label = ttk.Label(window, text="Sort:")
    sort_label.grid(row=3, column=0, sticky=tk.W, padx=pad_x, pady=pad_y)

    sort_combo = ttk.Combobox(window, textvariable=sort_var)
    sort_combo['values'] = ('Test Sort 1', 'Test Sort 2', 'Test Sort 3')
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

