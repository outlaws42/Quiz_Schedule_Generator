#! /usr/bin/env python3
# -*- coding: utf-8 -*-
try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gio, GdkPixbuf
    import os, subprocess
    import sys
    import configparser
    import logging
    logging.basicConfig(filename='qsg.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    import pickle
except(ImportError) as e:
    logging.info('This module is required  ' + str(e))

# External imports
try:
    import xlsx_export as exp
    import pdf_export as pdf
except(ImportError) as e:
    logging.info('External imports  ' + str(e))

class MainWindow(Gtk.Window):
    version = '1.3.5'
    def __init__(self):
        Gtk.Window.__init__(self,title='Quiz Schedule Generator    ' + self.version)

        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(10) # Give some space around the border
        self.set_default_size(700,500)
        if os.name == 'posix':
            self.set_icon_from_file(self.get_resource_path('images/logo.png'))
        elif os.name == 'nt':
            self.set_icon_from_file('images/logo.png')
            
        self.open_file()
        self.team_info()
        self.convert_to_list()
        self.tree_settings()
        self.menu_bar()
        self.nav_buttons()
        

    def get_resource_path(self,rel_path):
        dir_of_py_file = os.path.dirname(sys.argv[0])
        rel_path_to_resource = os.path.join(dir_of_py_file, rel_path)
        abs_path_to_resource = os.path.abspath(rel_path_to_resource)
        return abs_path_to_resource


        
    def open_file(self):
        """
            read python dict back from the file. If it doesn't exist then it creates it.
        """
        try:
            with open(self.get_resource_path('teams.qs'), 'rb') as file_:
                    self.teams_present = pickle.load(file_)
            
        except(FileNotFoundError) as e:
            logging.info(str(e) + ' Creating')
            self.teams_present = {
                    'COLUMBIA CITY': 'CC',
                    'COLUMBIA CITY 2': 'CC2',
                    'COLLEGE 1ST': 'CF',
                    'COLLEGE 1ST 2': 'CF2',
                    'SUGAR GROVE': 'SG',
                    'SUGAR GROVE 2': 'SG2',
                    'OAK GROVE': 'OG',
                    'OAK GROVE 2': 'OG2',
                    'SYRACUSE': 'SY',
                    'SYRACUSE 2': 'SY2',
                    'TRIER RIDGE': 'TR'
                }
            with open(self.get_resource_path('teams.qs'), 'wb') as file_:
                pickle.dump(self.teams_present, file_)
                
        self.team_info()

    def save_file(self):
        with open(self.get_resource_path('teams.qs'), 'wb') as file_:
                pickle.dump(self.teams_present, file_)
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
        #self.main_menu_bar = uimanager.get_widget('/MenuBar')
        self.menu_bar = Gtk.MenuBar()
        
        # File menu
        file_menu = Gtk.Menu()
        file_menu_dropdown = Gtk.MenuItem('File')
        file_menu_dropdown.set_submenu(file_menu)
        
        # File menu items
        file_gen_ex = Gtk.MenuItem('Generate As Excel')
        file_menu.append(file_gen_ex)
        file_gen_pdf = Gtk.MenuItem('Generate As PDF')
        file_menu.append(file_gen_pdf)
        file_settings = Gtk.MenuItem('Settings')
        file_menu.append(file_settings)
        file_exit = Gtk.MenuItem('Exit')
        file_menu.append(file_exit)
        
        # Help menu
        help_menu = Gtk.Menu()
        help_menu_dropdown = Gtk.MenuItem('Help')
        help_menu_dropdown.set_submenu(help_menu)
        
        # Help menu items
        help_doc = Gtk.MenuItem('Documetation')
        help_menu.append(help_doc)
        help_about = Gtk.MenuItem('About')
        help_menu.append(help_about)


        # Append menus to menubar
        self.menu_bar.append(file_menu_dropdown)
        self.menu_bar.append(help_menu_dropdown)

        # Menu signals
        file_gen_ex.connect('activate',self.gen_sch)
        file_gen_pdf.connect('activate',self.gen_pdf)
        file_settings.connect('activate',self.setting_call)
        file_exit.connect('activate',self.exit_app)
        help_about.connect('activate',self.about_dia)
        help_doc.connect('activate',self.help_doc)

    def nav_buttons(self):
        
        self.add_button = Gtk.Button()
        img_add = Gtk.Image.new_from_file(self.get_resource_path('images/add.png'))
        self.add_button.set_image(img_add)
        tooltip = 'Adds a team to the list'
        self.add_button.set_tooltip_text(tooltip)
        self.add_button.connect('clicked',self.team_add)
        
        self.remove_button = Gtk.Button()
        img_rem = Gtk.Image.new_from_file(self.get_resource_path('images/remove.png'))
        self.remove_button.set_image(img_rem)
        tooltip = 'Removes the highlighted team from the list'
        self.remove_button.set_tooltip_text(tooltip)
        self.remove_button.connect('clicked',self.team_remove)

        self.edit_button = Gtk.Button()
        img_ed = Gtk.Image.new_from_file(self.get_resource_path('images/edit.png'))
        self.edit_button.set_image(img_ed)
        tooltip = 'Edit teams'
        self.edit_button.set_tooltip_text(tooltip)
        self.edit_button.connect('clicked',self.team_edit)

        self.generate_button = Gtk.Button()
        img_gen = Gtk.Image.new_from_file(self.get_resource_path('images/spread.png'))
        self.generate_button.set_image(img_gen)
        tooltip = 'Generates the quiz schedule in \'Microsoft Excel\' format'
        self.generate_button.set_tooltip_text(tooltip)
        self.generate_button.connect("clicked",self.gen_sch)

        self.generate_button_pdf = Gtk.Button()
        img_gen_pdf = Gtk.Image.new_from_file(self.get_resource_path('images/pdf.png'))
        self.generate_button_pdf.set_image(img_gen_pdf)
        tooltip = 'Generates the quiz schedule in \'PDF\' format'
        self.generate_button_pdf.set_tooltip_text(tooltip)
        self.generate_button_pdf.connect('clicked',self.gen_pdf)
        
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
        box_2.pack_start(self.edit_button, False, False, 5)
        box_2.pack_start(self.generate_button, False, False, 5)
        box_2.pack_start(self.generate_button_pdf, False, False, 5)
    
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
        for i, col_title in enumerate(['Teams','Team Abbreviation']):
            renderer[i].set_property('editable', False)
            column = Gtk.TreeViewColumn(col_title, renderer[i], text=i)
            column.set_sort_column_id(i)
            column.set_min_width(250)
            column.set_resizable(True)  
            column.set_alignment(0.5)  # Sets alignment for the column header
            renderer[i].set_alignment(0.5, 0.5)  # Sets the alignment for the data  (xaling, yalign)
            self.treeview.append_column(column)
        self.treeview.set_rules_hint( True )

    def team_add(self, widget):
        if len(self.teams)< 17:
            self.add_dia = AddTeamDia(self)
            response = self.add_dia.run()

            if response == Gtk.ResponseType.OK:
            
                if self.add_dia.entry_team.get_text().upper() != '' and self.add_dia.entry_abr.get_text().upper() != '':
                    if self.add_dia.entry_team.get_text().upper() not in self.teams_present and self.add_dia.entry_abr.get_text().upper() not in self.teams_present.values():  
                        new_team_upper = self.add_dia.entry_team.get_text().upper()
                        new_abr_upper = self.add_dia.entry_abr.get_text().upper()
                        new_item = [new_team_upper, new_abr_upper]
                        self.liststore.append(new_item)
                        self.teams_present[new_team_upper] = new_abr_upper
                        self.save_file()
                    
                    else:
                        main_text = 'Team  or Team Abbreviation is already in the list'
                        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                        Gtk.ButtonsType.OK, main_text)
                        dialog.set_modal(widget)
                        dialog.run()
                        dialog.destroy()
                else:
                    main_text = 'Team or Team Abbreviation can\'t be empty'
                    dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                    Gtk.ButtonsType.OK, main_text)
                    dialog.set_modal(widget)
                    dialog.run()
                    dialog.destroy()
           
            
            elif response == Gtk.ResponseType.CANCEL:
                pass

            self.add_dia.destroy()
        else:
            main_text = 'The maximum number of teams is 17'
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
            Gtk.ButtonsType.OK, main_text)
            dialog.set_modal(widget)
            dialog.run()
            dialog.destroy()
        
    def team_edit(self, widget):
        # Get the selected row
        selection = self.treeview.get_selection()
        model, row = selection.get_selected()
        # Get selected team
        team = str(model[row][0])
        # Get selected team abr. 
        abr = str(model[row][1]) # Get team that was
        # Make a copy of self.teams_present
        teams_temp = {key:value for key,value in self.teams_present.items()}
        # Remove the selected team from the temporary dictionary.
        teams_temp.pop(team)
        self.save_edit_file(team,abr)
        self.edit_dia = EditTeamDia(self)
        response = self.edit_dia.run()
        if response == Gtk.ResponseType.OK:
            if self.edit_dia.entry_team.get_text().upper() != '' and self.edit_dia.entry_abr.get_text().upper() != '':
                if self.edit_dia.entry_team.get_text().upper() not in teams_temp.keys() and self.edit_dia.entry_abr.get_text().upper() not in teams_temp.values():
                    model[row][0] = self.edit_dia.entry_team.get_text().upper()
                    model[row][1] = self.edit_dia.entry_abr.get_text().upper()
                    self.teams_present[model[row][0]] = self.teams_present.pop(team)
                    self.teams_present[model[row][0]] = model[row][1]
                    self.save_file()

                else:
                    main_text = 'Team or Team Abbreviation is already in the list of teams'
                    dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                    Gtk.ButtonsType.OK, main_text)
                    dialog.set_modal(widget)
                    dialog.run()
                    dialog.destroy()
                
            else:
                main_text = 'Team or Team Abbreviation can\'t be empty'
                dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                Gtk.ButtonsType.OK, main_text)
                dialog.set_modal(widget)
                dialog.run()
                dialog.destroy()
            
        elif response == Gtk.ResponseType.CANCEL:
            pass

        self.edit_dia.destroy()

    def team_remove(self, button):
            self.del_dia = DelTeamDia(self)
            response = self.del_dia.run()
            if response == Gtk.ResponseType.OK:
                selection = self.treeview.get_selection()
                model, row = selection.get_selected()
                team = str(model[row][0]) 
                model.remove(row)
                del self.teams_present[team]
                self.save_file()
            else:
                pass
            self.del_dia.destroy()
            
    #############################################
    # Popup dialogs                             #
    #############################################
    def about_dia(self,widget):
        about = Gtk.AboutDialog()
        about.set_position(Gtk.WindowPosition.CENTER)
        about.set_icon_from_file(self.get_resource_path('images/logo.png'))
        about.set_modal(MainWindow)
        about.set_program_name('Quiz Schedule Generator')
        about.set_version('Version:  ' + str(self.version))
        about.set_copyright('Copyright (C) 2016 ')
        about.set_comments('Takes a list of teams and generates a quiz schedule')
        try:
            about.set_logo(GdkPixbuf.Pixbuf.new_from_file(self.get_resource_path('images/logo_64.png')))
        except:
            pass
        about.set_authors(['Troy Franks'])
        about.set_documenters (['Troy Franks','Cara Franks'])
        about.set_artists(['Nizips', 'sixsixfive'])
        about.set_license_type(Gtk.License.GPL_3_0)
        #about.set_wrap_license(True)
        about.run()
        about.destroy()

    def message_dia(self,filename):
        main_text = 'Schedule Info'
        message_text = """Your schedule is at %s\n
        This schedule will have %d rooms and %d team(s)
        on break each quiz""" %(filename, self.rooms, int(len(self.teams) - self.teams_capacity))
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK, main_text)
        dialog.set_modal(MainWindow)
        dialog.format_secondary_text(message_text)
        dialog.run()
        dialog.destroy()
        
    def save_dia(self, set_name, text_pattern, mime_type, ext):
        dialog = Gtk.FileChooserDialog('Save Schedule As', self,
                                       Gtk.FileChooserAction.SAVE,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_SAVE, Gtk.ResponseType.ACCEPT))
        dialog.set_default_size(480, 320)

        self.add_filters(dialog, set_name, text_pattern, mime_type)
        response = dialog.run()

        Gtk.FileChooser.set_do_overwrite_confirmation(dialog, True)
            
        if response == Gtk.ResponseType.ACCEPT:

            self.filename = Gtk.FileChooser.get_filename(dialog)
            if not self.filename.endswith(ext):
                self.filename += ext
            self.save_path_file(self.filename)
            dialog.destroy()
            self.message_dia(self.filename)
            if ext == '.xlsx':
                self.call_ex()
            else:
                self.call_pdf()
            self.config_read()
            if self.a_open == True:
                self.auto_open(self.filename)
            else:
                pass
            
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()

    def add_filters(self, dialog, set_name, text_pattern, mime_type):
        filter_text = Gtk.FileFilter()
        filter_text.set_name(set_name)
        filter_text.add_pattern(text_pattern)
        filter_text.add_mime_type(mime_type)
        dialog.add_filter(filter_text)

    #############################################
    # Actions                                   #
    #############################################
    def exit_app(self,widget):
        Gtk.main_quit()
    
    def save_path_file(self,filename):
        with open('path.txt', 'w') as output:
            output.write(filename)
            
    def save_edit_file(self,team, abr):
        with open('edit.txt', 'w') as output:
            output.write(team + '\n' + abr)
            
        
    def config_read(self):
        config = configparser.SafeConfigParser()
        config.read(self.get_resource_path('settings.cfg'))
        self.a_open = config.getboolean('schedule', 'auto_open')
        self.b_open = config.get('schedule', 'auto_open')
        self.header_title = config.get('schedule', 'header_title')
        self.header_on = config.getboolean('schedule', 'header_on')
        self.header_on_b = config.get('schedule', 'header_on')
        self.quiz_morn = config.get('schedule', 'quizes_morning')
        self.quiz_aft = config.get('schedule', 'quizes_after')
        self.quiz_start_time = config.get('schedule', 'quiz_start')
        self.quiz_lunch_length = config.get('schedule', 'lunch_length')
        

    def help_doc(self,button):
        doc = self.get_resource_path('Documents/docs.html')
        self.auto_open(doc)
        
    def auto_open(self,filename):
        if sys.platform.startswith('darwin'):
            subprocess.call(('open', filename))
        elif os.name == 'nt':
            os.startfile(filename)
        elif os.name == 'posix':
            subprocess.call(('xdg-open', filename))


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
        self.save_dia('Excel spread sheet', '*.xlsx', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', '.xlsx')
        
    def gen_pdf(self,button):
        """
            Calls the class for the excel generate
        """
        self.save_dia('PDF Document', '*.pdf', 'application/pdf', '.pdf')
        #pass
    def call_ex(self):
        self.sch = exp.ExportXlsx()

    def call_pdf(self):
        self.sch_pdf = pdf.ExportPdf()
        
        
        
        
class SettingsDia(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.main = MainWindow()
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_default_size(550,325)
        self.set_title('Settings')
        # Give some space around the border
        self.set_border_width(10) 
        self.set_icon_from_file(self.main.get_resource_path('images/logo.png'))
        
        self.set_modal(MainWindow)
        self.add_button('CLOSE', Gtk.ResponseType.CLOSE)
        #self.add_button('Cancel', Gtk.ResponseType.CANCEL)
        self.connect('response', self.button_settings)
        self.config_items()

    def config_items(self):
        
        # Read config file
        self.main.config_read()
        
        outer_box =Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing = 5) 
        self.vbox.add(outer_box)
        
        # Section header
        #schedule_row = Gtk.ListBoxRow()
        schedule_vbox =Gtk.Box(orientation=Gtk.Orientation.VERTICAL)  
        schedule_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing =100)
        schedule_vbox.add(schedule_box)
        label = Gtk.Label()
        label.set_markup('<b>Schedule</b>')
        label.set_alignment(0, 0.5)
        schedule_box.pack_start(label, True, True, 0)
        outer_box.add(schedule_vbox)

        # Row 1 checkbutton to set weather it auto opens the schedule after creation
        #auto_open_row = Gtk.ListBoxRow()
        auto_open_vbox =Gtk.Box(orientation=Gtk.Orientation.VERTICAL)  
        auto_open_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing =50)
        auto_open_vbox.add(auto_open_box)
        check_auto_open = Gtk.CheckButton(label='Open quiz schedule after creation')
        tooltip = 'When on, the quiz schedule will auto open in the default application for xlsx or pdf files'
        check_auto_open.set_tooltip_text(tooltip)
        check_auto_open.set_active(self.main.a_open)
        check_auto_open.connect('toggled', self.auto_open_check)
        auto_open_box.pack_start(check_auto_open, False, False, 0)
        outer_box.add(auto_open_vbox)

        # row 2 checkbutton show schedule title
        title_on_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL) 
        title_on_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing =50)
        title_on_vbox.add(title_on_box)
        check_title_on = Gtk.CheckButton(label='Show quiz schedule title')
        check_title_on.set_tooltip_text('Title shows on the schedule, \'On or Off\'')
        check_title_on.set_active(self.main.header_on)
        check_title_on.connect('toggled', self.title_check)
        title_on_box.pack_start(check_title_on, False, False, 0)
        outer_box.add(title_on_vbox)
        
        # Row 3 title entry for schedule
        vbox_2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box_2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing =115)
        vbox_2.add(box_2)
        label = Gtk.Label('Quiz schedule title:')
        label.set_alignment(0, 0.5)
        entry_title = Gtk.Entry()
        entry_title.set_input_purpose(Gtk.InputPurpose.FREE_FORM)
        entry_title.set_text(self.main.header_title)
        try:
            # Sets the length of the text box itself
            entry_title.set_max_width_chars(45) 
        except(AttributeError) as e:
            pass
        # sets how many characters your tex string can be.
        entry_title.set_max_length(55) 
        entry_title.set_tooltip_text('Hit the ENTER key to save the title')
        entry_title.connect('activate', self.on_entry_activated)
        box_2.pack_start(label, False, False, 0)
        box_2.pack_start(entry_title, False, False, 0)
        outer_box.add(vbox_2)

        # Row 4 Spin button for morning quizzes
        morn_quiz_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL) 
        morn_quiz_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing =20)
        morn_quiz_vbox.add(morn_quiz_box)
        label = Gtk.Label('Number of quizzes before lunch (Default 6):')
        label.set_alignment(0, 0.5)
        adjustment = Gtk.Adjustment(value=int(self.main.quiz_morn),
                                            lower=5,upper=7,
                                            step_increment=1,
                                            page_increment=1,
                                            page_size=0)
        morn_quiz = Gtk.SpinButton(adjustment=adjustment)
        morn_quiz.set_numeric(True)
        morn_quiz.set_tooltip_text('Use the + or - buttons or enter a valid number then press ENTER. (Max 7)')
        morn_quiz.connect('value-changed', self.on_morn_quiz_changed)
        morn_quiz_box.pack_start(label, False, False, 0)
        morn_quiz_box.pack_start(morn_quiz, False, False, 0)
        outer_box.add(morn_quiz_vbox)

        # Row 5 Spin button for afternoon quizzes
        after_quiz_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL) 
        after_quiz_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing =30)
        after_quiz_vbox.add(after_quiz_box)
        label = Gtk.Label('Number of quizzes after lunch (Default 6):')
        label.set_alignment(0, 0.5)
        adjustment = Gtk.Adjustment(value=int(self.main.quiz_aft),
                                            lower=4,upper=7,
                                            step_increment=1,
                                            page_increment=1,
                                            page_size=0)
        aftr_quiz = Gtk.SpinButton(adjustment=adjustment)
        aftr_quiz.set_numeric(True)
        aftr_quiz.set_tooltip_text('Use the + or - buttons or enter a valid number then press ENTER. (Max 7)')
        aftr_quiz.connect('value-changed', self.on_aftr_quiz_changed)
        after_quiz_box.pack_start(label, False, False, 0)
        after_quiz_box.pack_start(aftr_quiz, False, False, 0)
        outer_box.add(after_quiz_vbox)

        # Row 6 comboboxtext for start time
        quiz_start_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL) 
        quiz_start_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing =180)
        quiz_start_vbox.add(quiz_start_box)
        label = Gtk.Label('Schedule start time:')
        label.set_alignment(0, 0.5)
        quiz_start_combo = Gtk.ComboBoxText()
        quiz_start_combo.append('09:30', '09:30')
        quiz_start_combo.append('09:40', '09:40')
        quiz_start_combo.set_active_id(self.main.quiz_start_time)
        quiz_start_combo.connect("changed", self.on_quiz_start_changed)
        quiz_start_box.pack_start(label, False, False, 0)
        quiz_start_box.pack_start(quiz_start_combo, False, False, 0)
        outer_box.add(quiz_start_vbox)

        # Row 7 comboboxtext for lunch length
        quiz_lunch_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL) 
        quiz_lunch_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing =160)
        quiz_lunch_vbox.add(quiz_lunch_box)
        label = Gtk.Label('Schedule lunch length:')
        label.set_alignment(0, 0.5)
        quiz_lunch_combo = Gtk.ComboBoxText()
        quiz_lunch_combo.append('40', '40 Min')
        quiz_lunch_combo.append('60', '60 Min')
        quiz_lunch_combo.set_active_id(self.main.quiz_lunch_length)
        quiz_lunch_combo.connect("changed", self.on_quiz_lunch_changed)
        quiz_lunch_box.pack_start(label, False, False, 0)
        quiz_lunch_box.pack_start(quiz_lunch_combo, False, False, 0)
        outer_box.add(quiz_lunch_vbox)
        
        self.show_all()
        
    #############################################
    # signal calls                               #
    #############################################
        
    def auto_open_check(self, check):
        self.main.b_open = self.on_toggled(check)
        self.set_config()

    def title_check(self, check):
        self.main.header_on_b = self.on_toggled(check)
        self.set_config()
                
    def on_toggled(self, check):
        if check.get_active():
            output = 'yes'
        else:
            output = 'no'
        return output

    def on_entry_activated(self, entry):
        self.main.header_title = entry.get_text()
        self.set_config()

    def on_quiz_start_changed(self, quiz_start_item):
           self.main.quiz_start_time = quiz_start_item.get_active_text()
           self.set_config()

    def on_quiz_lunch_changed(self, quiz_lunch_item):
           self.main.quiz_lunch_length = quiz_lunch_item.get_active_id()
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
            
    def values(self):
        self.test = (self.main.b_open,
                    self.main.header_title,
                    self.main.header_on_b,
                    self.main.quiz_morn,
                    self.main.quiz_aft,
                    self.main.quiz_start_time,
                    self.main.quiz_lunch_length,
                    )
                            
    def config_write(self,*args):
        config = configparser.SafeConfigParser()
        config['schedule'] = {}
        config['schedule']['auto_open'] = str(args[0])
        config['schedule']['header_title'] = str(args[1])
        config['schedule']['header_on'] = str(args[2])
        config['schedule']['Quizes_morning'] = str(args[3])
        config['schedule']['Quizes_After'] = str(args[4])
        config['schedule']['quiz_start'] = str(args[5])
        config['schedule']['lunch_length'] = str(args[6])
        with open(self.main.get_resource_path('settings.cfg'), 'w') as configfile:
            config.write(configfile)

                
    def button_settings(self,dialog,response):
            dialog.destroy()
    
class AddTeamDia(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Add Team", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 125)
        
        outer_box =Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing = 10) 
        self.vbox.add(outer_box)
        
        vbox_team = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box_team = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing =45)
        vbox_team.add(box_team)
        label = Gtk.Label('Team:')
        label.set_alignment(0, 0.5)
        self.entry_team = Gtk.Entry()
        self.entry_team.set_input_purpose(Gtk.InputPurpose.FREE_FORM)
        try:
            # Sets the length of the text box itself
            self.entry_team.set_max_width_chars(45) 
        except(AttributeError) as e:
            pass
        # sets how many characters your tex string can be.
        self.entry_team.set_max_length(25) 
        self.entry_team.set_tooltip_text('Hit the ENTER key to save the title')
        box_team.pack_start(label, False, False, 0)
        box_team.pack_start(self.entry_team, False, False, 0)
        #box = self.get_content_area()
        outer_box.add(vbox_team)

        vbox_abr = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box_abr = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing =20)
        vbox_abr.add(box_abr)
        label = Gtk.Label('Team abr:')
        label.set_alignment(0, 0.5)
        self.entry_abr = Gtk.Entry()
        self.entry_abr.set_input_purpose(Gtk.InputPurpose.FREE_FORM)
        try:
            # Sets the length of the text box itself
            self.entry_team.set_max_width_chars(45) 
        except(AttributeError) as e:
            pass
        # sets how many characters your tex string can be.
        self.entry_abr.set_max_length(5) 
        self.entry_abr.set_tooltip_text('Hit the ENTER key to save the title')
        box_abr.pack_start(label, False, False, 0)
        box_abr.pack_start(self.entry_abr, False, False, 0)
        #box = self.get_content_area()
        outer_box.add(vbox_abr)
        self.show_all()

class EditTeamDia(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Edit Team", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        with open('edit.txt', 'r') as edit_text:
           team = [line.rstrip('\n') for line in edit_text]
           
        self.set_default_size(150, 125)
        self.set_default_response(Gtk.ResponseType.CANCEL)
        outer_box =Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing = 10) 
        self.vbox.add(outer_box)
        
        vbox_team = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box_team = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing =45)
        vbox_team.add(box_team)
        label = Gtk.Label('Team:')
        label.set_alignment(0, 0.5)
        self.entry_team = Gtk.Entry()
        self.entry_team.set_input_purpose(Gtk.InputPurpose.FREE_FORM)
        self.entry_team.set_text(team[0])
        try:
            # Sets the length of the text box itself
            self.entry_team.set_max_width_chars(45) 
        except(AttributeError) as e:
            pass
        # sets how many characters your tex string can be.
        self.entry_team.set_max_length(25) 
        self.entry_team.set_tooltip_text('Hit the ENTER key to save the title')
        box_team.pack_start(label, False, False, 0)
        box_team.pack_start(self.entry_team, False, False, 0)
        #box = self.get_content_area()
        outer_box.add(vbox_team)

        vbox_abr = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box_abr = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing =20)
        vbox_abr.add(box_abr)
        label = Gtk.Label('Team abr:')
        label.set_alignment(0, 0.5)
        self.entry_abr = Gtk.Entry()
        self.entry_abr.set_input_purpose(Gtk.InputPurpose.FREE_FORM)
        self.entry_abr.set_text(team[1])
        try:
            # Sets the length of the text box itself
            self.entry_team.set_max_width_chars(45) 
        except(AttributeError) as e:
            pass
        # sets how many characters your tex string can be.
        self.entry_abr.set_max_length(5) 
        self.entry_abr.set_tooltip_text('Hit the ENTER key to save the title')
        box_abr.pack_start(label, False, False, 0)
        box_abr.pack_start(self.entry_abr, False, False, 0)
        #box = self.get_content_area()
        outer_box.add(vbox_abr)
        self.show_all()
        
class DelTeamDia(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Delete Team?", parent, 0,
            (Gtk.STOCK_NO, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_YES, Gtk.ResponseType.OK))
             
        self.set_default_size(100, 75)
        label = Gtk.Label('Are you sure you want to delete this team?')
        label.set_alignment(0, 0.5)
        self.vbox.add(label)
        self.show_all()
    
window = MainWindow()
window.connect('delete-event',Gtk.main_quit)
window.show_all()
Gtk.main()
