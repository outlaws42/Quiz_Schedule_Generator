#! /usr/bin/env python3
# -*- coding: utf-8 -*-
try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gio, GdkPixbuf
    import os, subprocess
    import sys
    import pickle
    import configparser
    import logging
    logging.basicConfig(filename='qsg.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    import xlsx_export as exp
except(ImportError) as e:
    print("This module is required  " + str(e))
    logging.info('This module is required  ' + str(e))

      
class MainWindow(Gtk.Window):
    version = "0.8.5.1"
    def __init__(self):
        Gtk.Window.__init__(self,title="Quiz Schedule Generator    " + self.version)

        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(10) # Give some space around the border
        self.set_default_size(700,500)
        if os.name == 'posix':
            self.set_icon_from_file(self.get_resource_path("images/logo.png"))
        elif os.name == 'nt':
            self.set_icon_from_file("images/logo.png")
            
        self.open_file()
        self.team_info()
        self.convert_to_list()
        self.tree_settings()
        self.menu_bar()
        self.nav_buttons()
        

    def get_resource_path(self,rel_path):
        dir_of_py_file = os.path.dirname(__file__)
        rel_path_to_resource = os.path.join(dir_of_py_file, rel_path)
        abs_path_to_resource = os.path.abspath(rel_path_to_resource)
        return abs_path_to_resource


        
    def open_file(self):
        """
            read python dict back from the file. If it doesn't exist then it creates it.
        """
        try:
            if os.name == 'posix':
                with open(self.get_resource_path('teams.qs'), 'rb') as file_:
                    self.teams_present = pickle.load(file_)
            elif os.name == 'nt':
                with open('teams.qs', 'rb') as file_:
                    self.teams_present = pickle.load(file_)
            
        except(FileNotFoundError) as e:
            print( str(e) + " Creating")
            logging.info(str(e) + " Creating")
            self.teams_present = {
                    "COLUMBIA CITY": "CC",
                    "COLUMBIA CITY 2": "CC2",
                    "COLLEGE 1ST": "CF",
                    "COLLEGE 1ST 2": "CF2",
                    "SUGAR GROVE": "SG",
                    "SUGAR GROVE 2": "SG2",
                    "OAK GROVE": "OG",
                    "OAK GROVE 2": "OG2",
                    "SYRACUSE": "SY",
                    "SYRACUSE 2": "SY2",
                    "TRIER RIDGE": "TR"
                }
            if os.name == 'posix':
                with open(self.get_resource_path('teams.qs'), 'wb') as file_:
                    pickle.dump(self.teams_present, file_)
            elif os.name == 'nt':
                with open('teams.qs', 'wb') as file_:
                    pickle.dump(self.teams_present, file_)
                
        self.team_info()

    def save_file(self):
        output = open('teams.qs', 'wb')
        pickle.dump(self.teams_present, output)
        output.close()
        self.team_info()

    def team_info(self):
        self.teams = [x for x in self.teams_present.values()]
        self.rooms = int(len(self.teams) / 3)
        self.teams_capacity = self.rooms * 3
        
        
    def convert_to_list(self):
        temp = []
        self.teams_ = []
        for key, value in self.teams_present.items():
            temp = [key,value]
            self.teams_.append(temp)
        self.teams_.sort()
        
        
    #############################################
    # Navigation                                #
    #############################################    
    def menu_bar(self):
        #self.main_menu_bar = uimanager.get_widget("/MenuBar")
        self.menu_bar = Gtk.MenuBar()
        
        # File menu
        file_menu = Gtk.Menu()
        file_menu_dropdown = Gtk.MenuItem("File")
        file_menu_dropdown.set_submenu(file_menu)
        
        # File menu items
        file_gen = Gtk.MenuItem("Generate Schedule")
        file_menu.append(file_gen)
        file_settings = Gtk.MenuItem("Settings")
        file_menu.append(file_settings)
        file_exit = Gtk.MenuItem("Exit")
        file_menu.append(file_exit)
        
        # Help menu
        help_menu = Gtk.Menu()
        help_menu_dropdown = Gtk.MenuItem("Help")
        help_menu_dropdown.set_submenu(help_menu)
        
        # Help menu items
        help_about = Gtk.MenuItem("About")
        help_menu.append(help_about)


        # Append menus to menubar
        self.menu_bar.append(file_menu_dropdown)
        self.menu_bar.append(help_menu_dropdown)

        # Menu signals
        file_gen.connect("activate",self.gen_sch)
        file_settings.connect("activate",self.setting_call)
        file_exit.connect("activate",self.exit_app)
        help_about.connect("activate",self.about_dia)

        #self.toolbar = uimanager.get_widget("/ToolBar")
        #box.pack_start(toolbar, False, False, 0)
        
    def nav_buttons(self):
        
        self.add_button = Gtk.Button()
        if os.name == 'posix':
            img_add = Gtk.Image.new_from_file(self.get_resource_path("images/add.png"))
        elif os.name == 'nt':
            img_add = Gtk.Image.new_from_file("images/add.png")
        self.add_button.set_image(img_add)
        self.add_button.set_tooltip_text("Adds a team to the list")
        self.add_button.connect("clicked",self.add_row)
        
        self.remove_button = Gtk.Button()
        if os.name == 'posix':
            img_rem = Gtk.Image.new_from_file(self.get_resource_path("images/remove.png"))
        elif os.name == 'nt':
            img_rem = Gtk.Image.new_from_file("images/remove.png")
            
        self.remove_button.set_image(img_rem)
        self.remove_button.set_tooltip_text("Removes the highlighted team from the list")
        self.remove_button.connect("clicked",self.remove_row)

        self.generate_button = Gtk.Button()
        if os.name == 'posix':
            img_gen = Gtk.Image.new_from_file(self.get_resource_path("images/gen.png"))
        elif os.name == 'nt':
            img_gen = Gtk.Image.new_from_file("images/gen.png")
        self.generate_button.set_image(img_gen)
        self.generate_button.set_tooltip_text("Generates the quiz schedule")
        self.generate_button.connect("clicked",self.gen_sch)
        
        self.window_layout()
        

    def window_layout(self):
        self.set_border_width(10) # Give some space around the border
       
        # Creating Items putting each row in a box
        # Menu bar/Treeview
        box_1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing =5)
        self.add(box_1)
        box_1.pack_start(self.menu_bar, False, False, 0)        
        box_1.pack_start(self.treeview, True, True, 0)

        # Add/Remove/Generate buttons
        box_2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing =0)
        box_1.add(box_2)
        box_2.pack_start(self.add_button, False, False, 5)
        box_2.pack_start(self.remove_button, False, False, 5)
        box_2.pack_start(self.generate_button, False, False, 5)
    
    #############################################
    # Liststore/Treeview/Cell Renderer settings #
    #############################################
    def tree_settings(self):
        
        #Convert data to ListStore (list that TreeView can display)
        self.liststore = Gtk.ListStore(str,str) # have to tell what type of data
        for item in self.teams_:
            self.liststore.append(list(item)) # append items to the ListStore
            
        renderer = []
        for i in range(2):
            i = Gtk.CellRendererText()
            renderer.append(i)
            
        # TreeView is the item that is displayed
        self.treeview = Gtk.TreeView(self.liststore)
        for i, col_title in enumerate(["Teams","Team Abbreviation"]):
            renderer[i].set_property("editable", True)
            column = Gtk.TreeViewColumn(col_title, renderer[i], text=i)
            column.set_sort_column_id(i)
            column.set_min_width(250)
            column.set_resizable(True)  
            column.set_alignment(0.5)  # Sets alignment for the column header
            renderer[i].set_alignment(0.5, 0.5)  # Sets the alignment for the data  (xaling, yalign)
            self.treeview.append_column(column)
        self.treeview.set_rules_hint( True )
        #new_item = ["test","t"]
        # Handle selection
        #selected_row = self.treeview.get_selection()
        #selected_row.connect("changed", self.item_selected)
        #self.liststore.append(new_item)
        
        # Add TreeView to main layout
        #self.window_layout()
        
        # Handle editing
        renderer[0].connect("edited", self.team_edited)
        renderer[1].connect("edited", self.team_abr_edited)
        
    def add_row(self,button):
        new_item = ["TEAM","T"]
        self.liststore.append(new_item)
                
        self.teams_present["TEAM"] = "T"
        self.save_file()

    def team_edited(self, widget, path, text):
        old_text = self.liststore[path][0]
        old_text_u = old_text.upper()
        text_upper = text.upper()
        self.liststore[path][0] = text_upper  # Updates the list store
        self.teams_present[text_upper] = self.teams_present.pop(old_text_u)  # Update the dictionary with edit. and del old key
        #del self.teams_present[old_text_u]  # del old entry in dictionary
        self.save_file()
        #for k in sorted(self.teams_present):#Sorts in alphebetical order and loops through the dictionary
        #    print(k, ':', self.teams_present[k])#At each loop we print the key(k) :  We print the  value(teams_present[k])
    

    def team_abr_edited(self, widget, path, text):
        
        team_text = self.liststore[path][0]
        team_text_up = team_text.upper()
        new_value = text.upper()
        self.liststore[path][1] = new_value  # Updates the list store
        self.teams_present[team_text_up] = new_value  # Update the dictionary with edit. and del old key
        #del self.teams_present[old_text_u]  # del old entry in dictionary
        self.save_file()
        #for k in sorted(self.teams_present):#Sorts in alphebetical order and loops through the dictionary
         #   print(k, ':', self.teams_present[k])#At each loop we print the key(k) :  We print the  value(teams_present[k])

    def remove_row(self, button):
     
        # Get the TreeView selected row(s)
        selection = self.treeview.get_selection()
        
        # get_selected_rows() returns a tuple
        # The first element is a ListStore
        # The second element is a list of tree paths
        # of all selected rows
        #model, paths = selection.get_selected_rows()

        # Get info from list what team was selected
        model, row = selection.get_selected()
        team = str(model[row][0]) # Get team that was deleted from liststore to delete from Dictitonary
        
        # Get the TreeIter instance for each path
        #for path in paths:
         #   iter = model.get_iter(path)
        # Remove the ListStore row referenced by iter
        model.remove(row)
        del self.teams_present[team]
        self.save_file()
        #for k in sorted(self.teams_present):#Sorts in alphebetical order and loops through the dictionary
        #    print(k, ':', self.teams_present[k])#At each loop we print the key(k) :  We print the  value(teams_present[k])
            
    #############################################
    # Popup dialogs                             #
    #############################################
    def about_dia(self,widget):
        about = Gtk.AboutDialog()
        if os.name == 'posix':
            about.set_icon_from_file(self.get_resource_path("images/logo.png"))
        elif os.name == 'nt':
            about.set_icon_from_file("images/logo.png")
        #about.set_transient_for(MainWindow)
        about.set_modal(MainWindow)
        about.set_program_name("Quiz Schedule Generator")
        about.set_version("Version:  " + str(self.version))
        about.set_copyright("Copyright (C) 2016 ")
        about.set_comments("Takes a list of teams and generates a quiz schedule")
        try:
            about.set_logo(GdkPixbuf.Pixbuf.new_from_file(self.get_resource_path("images/logo_64.png")))
        except:
            pass
        about.set_authors(["Troy Franks"])
        about.set_artists(["Nizips", "sixsixfive"])
        about.set_license_type(Gtk.License.GPL_3_0)
        #about.set_wrap_license(True)
        about.run()
        about.destroy()

    def message_dia(self,filename):
        main_text = "Schedule Info"
        message_text = """Your schedule is at %s\n
        This schedule will have %d rooms and %d team(s)
        on break each quiz""" %(filename, self.rooms, int(len(self.teams) - self.teams_capacity))
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK, main_text)
        dialog.set_modal(MainWindow)
        dialog.format_secondary_text(message_text)
        dialog.run()
        dialog.destroy()
        
    def save_dia(self):
        dialog = Gtk.FileChooserDialog("Save Schedule As", self,
                                       Gtk.FileChooserAction.SAVE,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_SAVE, Gtk.ResponseType.ACCEPT))
        dialog.set_default_size(480, 320)

        self.add_filters(dialog)
        response = dialog.run()

        Gtk.FileChooser.set_do_overwrite_confirmation(dialog, True)

        #self.user_edited_new_document = True

        #if( self.user_edited_new_document ):
        #    Gtk.FileChooser.set_current_name(dialog, "Untitled document")
        #else:
         #   Gtk.FileChooser.set_filename(filename)
            
        if response == Gtk.ResponseType.ACCEPT:

            self.filename = Gtk.FileChooser.get_filename(dialog)
            if not self.filename.endswith('.xlsx'):
                self.filename += '.xlsx'
            self.save_path_file(self.filename)
            dialog.destroy()
            self.message_dia(self.filename)
            self.call_external()
            self.auto_open(self.filename,)
            #return filename
            
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()

    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Excel spread sheet")
        filter_text.add_pattern("*.xlsx")
        filter_text.add_mime_type("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        dialog.add_filter(filter_text)
    
    
    #############################################
    # Actions                                   #
    #############################################
    def exit_app(self,widget):
        Gtk.main_quit()
    
    def save_path_file(self,filename):
        with open('path.txt', 'w') as output:
            output.write(filename)

    def config_read(self):
        config = configparser.SafeConfigParser()
        if os.name == 'posix':
            config.read(self.get_resource_path('settings.cfg'))
        elif os.name == 'nt':
            config.read('settings.cfg')
        self.a_open = config.getboolean('schedule', 'auto_open')
        self.b_open = config.get('schedule', 'auto_open')
        self.header_title = config.get('schedule', 'header_title')
        self.header_on = config.getboolean('schedule', 'header_on')
        self.header_on_b = config.get('schedule', 'header_on')
        self.quiz_morn = config.get('schedule', 'quizes_morning')
        self.quiz_aft = config.get('schedule', 'quizes_after')
        self.font_title_fc =  config.get('schedule','title_font_face')
        self.font_title_sz =  config.get('schedule','title_font_size')
        self.font_title_comb = self.font_title_fc + " " + self.font_title_sz
        self.font_head_fc =  config.get('schedule','head_font_face')
        self.font_head_sz =  config.get('schedule','head_font_size')
        self.font_head_comb = self.font_head_fc + " " + self.font_head_sz
        self.font_abr_fc =  config.get('schedule','abr_font_face')
        self.font_abr_sz =  config.get('schedule','abr_font_size')
        self.font_abr_comb = self.font_abr_fc + " " + self.font_abr_sz
        
    def auto_open(self,filename):
        self.config_read()
        if self.a_open == True:
            if sys.platform.startswith('darwin'):
                subprocess.call(('open', filename))
            elif os.name == 'nt':
                os.startfile(filename)
            elif os.name == 'posix':
                subprocess.call(('xdg-open', filename))
        else:
            pass


    #############################################
    # class calls                               #
    #############################################
    def setting_call(self,button):
        self.pref = SettingsDia()
        self.pref.run()
          
    def gen_sch(self,button):
        """
            Calls the class for the excel generate
        """
        self.save_dia()
        
    def call_external(self):
        self.sch = exp.ExportXlsx()
        
        
        
class SettingsDia(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.main = MainWindow()
        self.set_default_size(500,300)
        self.set_title("Settings")
        self.set_border_width(10) # Give some space around the border
        if os.name == 'posix':
            self.set_icon_from_file(self.main.get_resource_path("images/logo.png"))
        elif os.name == 'nt':
            self.set_icon_from_file("images/logo.png")
        
        self.set_modal(MainWindow)
        self.add_button("CLOSE", Gtk.ResponseType.CLOSE)
        #self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.connect("response", self.button_settings)
        self.config_items()

    def config_items(self):
        
        # Read config file
        self.main.config_read()
        
        # List box
        listbox = Gtk.ListBox() # Create a Listbox
        listbox.set_selection_mode(Gtk.SelectionMode.NONE) # Weather you can select or not.
        self.vbox.add(listbox) # Add the Listbox

        # Section header
        schedule_row = Gtk.ListBoxRow() 
        schedule_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing =100)
        schedule_row.add(schedule_box)
        label = Gtk.Label()
        label.set_markup("<b>Schedule</b>")
        label.set_alignment(0, 0.5)
        schedule_box.pack_start(label, True, True, 0)
        listbox.add(schedule_row)

        # Row 1 checkbutton to set weather it auto opens the schedule after creation
        auto_open_row = Gtk.ListBoxRow() 
        auto_open_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing =50)
        auto_open_row.add(auto_open_box)
        check_auto_open = Gtk.CheckButton(label="Open quiz schedule after creation")
        check_auto_open.set_tooltip_text("When on, the quiz schedule will auto open in the default application for excel files")
        check_auto_open.set_active(self.main.a_open)
        check_auto_open.connect("toggled", self.auto_open_check)
        auto_open_box.pack_start(check_auto_open, False, False, 0)
        listbox.add(auto_open_row)

        # row 2 checkbutton show schedule title
        title_on_row = Gtk.ListBoxRow() 
        title_on_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing =50)
        title_on_row.add(title_on_box)
        check_title_on = Gtk.CheckButton(label="Show quiz schedule title")
        check_title_on.set_tooltip_text("Title shows on the schedule, 'On or Off'")
        check_title_on.set_active(self.main.header_on)
        check_title_on.connect("toggled", self.title_check)
        title_on_box.pack_start(check_title_on, False, False, 0)
        listbox.add(title_on_row)
        
        # Row 3 title entry for schedule
        row_2 = Gtk.ListBoxRow() 
        box_2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing =115)
        row_2.add(box_2)
        label = Gtk.Label("Quiz schedule title:")
        label.set_alignment(0, 0.5)
        entry_title = Gtk.Entry()
        entry_title.set_input_purpose(Gtk.InputPurpose.FREE_FORM)
        entry_title.set_text(self.main.header_title)
        try:
            entry_title.set_max_width_chars(45) # Sets the length of the text box itself
        except(AttributeError) as e:
            print(str(e))
            pass
        entry_title.set_max_length(55) # sets how many characters your tex string can be.
        entry_title.set_tooltip_text("Hit the 'ENTER' key to save the title")
        entry_title.connect("activate", self.on_entry_activated)
        box_2.pack_start(label, False, False, 0)
        box_2.pack_start(entry_title, False, False, 0)
        listbox.add(row_2)

        # Row 4 Spin button for afternoon quizzes
        morn_quiz_row = Gtk.ListBoxRow() 
        morn_quiz_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing =20)
        morn_quiz_row.add(morn_quiz_box)
        label = Gtk.Label("Number of quizzes before lunch (Default 6):")
        label.set_alignment(0, 0.5)
        adjustment = Gtk.Adjustment(value=int(self.main.quiz_morn),
                                            lower=3,upper=7,
                                            step_increment=1,
                                            page_increment=1,
                                            page_size=0)
        morn_quiz = Gtk.SpinButton(adjustment=adjustment)
        morn_quiz.set_numeric(True)
        morn_quiz.set_tooltip_text("Use the + or - buttons or enter a valid number then press 'ENTER'. (Max 7)")
        morn_quiz.connect("value-changed", self.on_morn_quiz_changed)
        morn_quiz_box.pack_start(label, False, False, 0)
        morn_quiz_box.pack_start(morn_quiz, False, False, 0)
        listbox.add(morn_quiz_row)

        # Row 5 Spin button for afternoon quizzes
        after_quiz_row = Gtk.ListBoxRow() 
        after_quiz_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing =30)
        after_quiz_row.add(after_quiz_box)
        label = Gtk.Label("Number of quizzes after lunch (Default 6):")
        label.set_alignment(0, 0.5)
        adjustment = Gtk.Adjustment(value=int(self.main.quiz_aft),
                                            lower=3,upper=7,
                                            step_increment=1,
                                            page_increment=1,
                                            page_size=0)
        aftr_quiz = Gtk.SpinButton(adjustment=adjustment)
        aftr_quiz.set_numeric(True)
        aftr_quiz.set_tooltip_text("Use the + or - buttons or enter a valid number then press 'ENTER'. (Max 7)")
        aftr_quiz.connect("value-changed", self.on_aftr_quiz_changed)
        after_quiz_box.pack_start(label, False, False, 0)
        after_quiz_box.pack_start(aftr_quiz, False, False, 0)
        listbox.add(after_quiz_row)

        # Row 6 font for title schedule
        font_row_1 = Gtk.ListBoxRow() 
        font_box_1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing =155)
        font_row_1.add(font_box_1)
        label = Gtk.Label("Title font and size:")
        label.set_alignment(0, 0.5)
        self.font_ = Gtk.FontButton(title="Title font and size")
        self.font_.set_font_name(self.main.font_title_comb)
        self.font_.connect("font-set", self.font_title_changed)
        font_box_1.pack_start(label, False, False, 0)
        font_box_1.pack_start(self.font_, False, False, 0)
        listbox.add(font_row_1)

        # Row 7 font for title schedule
        font_row_2 = Gtk.ListBoxRow() 
        font_box_2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing =47)
        font_row_2.add(font_box_2)
        label = Gtk.Label("Room/Legend headings font and size:")
        label.set_alignment(0, 0.5)
        self.font_ = Gtk.FontButton(title="Room headings font and size")
        self.font_.set_font_name(self.main.font_head_comb)
        self.font_.connect("font-set", self.font_head_changed)
        font_box_2.pack_start(label, False, False, 0)
        font_box_2.pack_start(self.font_, False, False, 0)
        listbox.add(font_row_2)
        
        # Row 8 font for base schedule
        font_row_3 = Gtk.ListBoxRow() 
        font_box_3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing =80)
        font_row_3.add(font_box_3)
        label = Gtk.Label("Team abbreviation font and size:")
        label.set_alignment(0, 0.5)
        self.font_ = Gtk.FontButton(title="Quiz font and size")
        self.font_.set_font_name(self.main.font_abr_comb)
        self.font_.connect("font-set", self.font_abr_changed)
        font_box_3.pack_start(label, False, False, 0)
        font_box_3.pack_start(self.font_, False, False, 0)
        listbox.add(font_row_3)
        
        # Last saved values
        #self.open_=self.main.b_open  # set self.open for when state is not changed
        #self.entry_text = self.main.header_title
        #self.entry_on = self.main.header_on_b
        #self.morn = self.main.quiz_morn
        #self.aftr = self.main.quiz_aft
        #self.title_font_face = self.main.title_font_fc
        #self.title_font_size = self.main.title_font_sz
        #self.head_font_face = self.main.font_head_fc
        #self.head_font_size = self.main.font_head_sz
        #self.abr_font_face = self.main.font_abr_fc
        #self.abr_font_size = self.main.font_abr_sz
        
        
        self.show_all()
        
    #############################################
    # signal calls                               #
    #############################################
    def font_seperate(self,font):
        font_list = list(font.get_font_name())
        font_size_list = list(font.get_font_name())
        font_size_list[:-2] = []  # slice list size
        if font_size_list[0] == " ":
            font_size_list[:-1] = []  # slice list size
            for i in range(2):
                font_list.pop()
        else:
            for i in range(3):
                font_list.pop()
        font_face = "".join(font_list)
        font_size = "".join(font_size_list)
        return [font_face, font_size]

    def font_title_changed(self,font):
        font_ = self.font_seperate(font)
        self.main.font_title_fc = font_[0]
        self.main.font_title_sz = font_[1]
        self.set_config()

    def font_head_changed(self,font):
        font_ = self.font_seperate(font)
        self.main.font_head_fc = font_[0]
        self.main.font_head_sz = font_[1]
        self.set_config()

    def font_abr_changed(self,font):
        font_ = self.font_seperate(font)
        self.main.font_abr_fc = font_[0]
        self.main.font_abr_sz = font_[1]
        self.set_config()
        
    def auto_open_check(self, check):
        self.main.b_open = self.on_toggled(check)
        self.set_config()

    def title_check(self, check):
        self.main.header_on_b = self.on_toggled(check)
        self.set_config()
                
    def on_toggled(self, check):
        if check.get_active():
            output = "yes"
        else:
            output = "no"
        return output

    def on_entry_activated(self, entry):
        self.main.header_title = entry.get_text()
        self.set_config()

    def on_morn_quiz_changed(self, spinbutton):
        self.main.quiz_morn = str(spinbutton.get_value_as_int())
        self.set_config()

    def on_aftr_quiz_changed(self, spinbutton):
        self.main.quiz_aft = str(spinbutton.get_value_as_int())
        self.set_config()
        
    #############################################
    # config calls                               #
    #############################################    
    def set_config(self):
        self.values()
        self.config_write(*self.test)
        print(*self.test)
            
    def values(self):
        self.test = (self.main.b_open,
                    self.main.header_title,
                    self.main.header_on_b,
                    self.main.quiz_morn,
                    self.main.quiz_aft,
                    self.main.font_title_fc,
                    self.main.font_title_sz,
                    self.main.font_head_fc,
                    self.main.font_head_sz,
                    self.main.font_abr_fc,
                    self.main.font_abr_sz
                    )
                            
    def config_write(self,*args):
        config = configparser.SafeConfigParser()
        config['schedule'] = {}
        config['schedule']['auto_open'] = str(args[0])
        config['schedule']['header_title'] = str(args[1])
        config['schedule']['header_on'] = str(args[2])
        config['schedule']['Quizes_morning'] = str(args[3])
        config['schedule']['Quizes_After'] = str(args[4])
        config['schedule']['title_font_face'] = str(args[5])
        config['schedule']['title_font_size'] = str(args[6])
        config['schedule']['head_font_face'] = str(args[7])
        config['schedule']['head_font_size'] = str(args[8])
        config['schedule']['abr_font_face'] = str(args[9])
        config['schedule']['abr_font_size'] = str(args[10])
        if os.name == 'posix':
            with open(self.main.get_resource_path('settings.cfg'), 'w') as configfile:
                config.write(configfile)
        elif os.name == 'nt':
            with open('settings.cfg', 'w') as configfile:
                config.write(configfile)
            
                
    def button_settings(self,dialog,response):
            dialog.destroy()
    

    
window = MainWindow()
window.connect('delete-event',Gtk.main_quit)
window.show_all()
Gtk.main()
