#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import math
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.pagesizes import landscape
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
    import reportlab.rl_settings
except(ImportError) as e:
    logging.info('reportlab imports  ' + str(e))
    
# External imports
try:
    import generate_rand as rand
except(ImportError) as e:
    logging.info('generate rand from pdf_export  ' + str(e))

class ExportPdf(object):
    def __init__(self):
        self.tms = rand.ScheduleGen()
        self.open_path_file()
        self.times()
        self.room_breakdown()
        self.breaks()
        self.legend()
        self.generate_cert()
        
    def open_path_file(self):
        with open('path.txt', 'r') as path_text:
            self.path=path_text.read()
                
    def legend(self):
        # Populate the ledgend with team name and team abreaviation
        # Seperate team name and team abr into 2 lists
        self.legend_break_amount = 12
        legend_name = [[key] for key, value in sorted(self.tms.teams_present.items())]
        legend_abr = [[value] for key, value in sorted(self.tms.teams_present.items())]

        if len(self.tms.teams) >= self.legend_break_amount:
            # Divide legend in two for space
            self.legend_name = legend_name[:math.ceil(len(legend_name)/2)]
            self.legend_name2 = legend_name[math.ceil(len(legend_name)/2):]
            self.legend_abr = legend_abr[:math.ceil(len(legend_abr)/2)]
            self.legend_abr2 = legend_abr[math.ceil(len(legend_abr)/2):]
        else:
            self.legend_name = legend_name
            self.legend_abr = legend_abr
            
    def room_breakdown(self):
        if self.tms.rooms ==1:
            rooms = ['Room 1']
        elif self.tms.rooms ==2:
            rooms = ['Room 1',' ',' ', 'Room 2']
        elif self.tms.rooms ==3:
            rooms = ['Room 1',' ',' ', 'Room 2','','', 'Room 3']
        elif self.tms.rooms ==4:
            rooms = ['Room 1',' ',' ', 'Room 2','','', 'Room 3', ' ', ' ', 'Room 4']
        elif self.tms.rooms ==5:
            rooms = ['Room 1',' ',' ', 'Room 2','','', 'Room 3', ' ', ' ', 'Room 4', ' ', ' ', 'Room 5']
        self.set_quiz_list(rooms)

    def set_quiz_list(self,rooms):
        lunch =['Lunch']
        morn_quiz = []
        for i in range(self.tms.quiz_morn ):
                morn_quiz.append(self.tms.quiz_random[i])
        self.morn_quiz = [rooms] + morn_quiz + [lunch]
        self.after_quiz = []
        for i in range(self.tms.quiz_morn, self.tms.quiz_day):
                self.after_quiz.append(self.tms.quiz_random[i])

    def breaks(self):
        if len(self.tms.teams) > self.tms.teams_capacity:
            lunch =['Lunch']
            b_title = ['Break']
            break_teams_m = []
            self.break_after = []
            for i in range(self.tms.quiz_morn):
                break_teams_m.append(self.tms.break_[i])
            self.break_morn = [b_title] + break_teams_m + [lunch]
            for i in range(self.tms.quiz_morn, self.tms.quiz_day):
                self.break_after.append(self.tms.break_[i])
        else:
            pass
            
    def times(self):
        time_morn = ['Time']
        time_after = []
        # Morning quiz times and lunch
        start_in = self.tms.quiz_start_time  # start time
        # separate hour from minute.  Create a hour and min list
        start_list_h = list(start_in)  # convert to list
        start_list_m = list(start_in)  # convert to list
        start_list_m[:-2] = []  # slice list for minutes
        start_list_h[2:] = []  # slice list for hour
        start_hour = ''.join(start_list_h)  # join back to a string
        start_min = ''.join(start_list_m)  # join back to a string
        hour = int(start_hour)
        if start_min == '00':
            hour = int(start_hour) + 1
            count = 3
            time = str(start_hour) + ':' + '00' + ' AM'
            time_morn.append(time)
            time = str(start_hour) + ':' + '20' + ' AM'
            time_morn.append(time)
            time = str(start_hour) + ':' + '40' + ' AM'
            time_morn.append(time)

        elif start_min == '20':
            hour = int(start_hour) + 1
            count = 2
            time = str(start_hour) + ':' + '20' + ' AM'
            time_morn.append(time)
            time = str(start_hour) + ':' + '40' + ' AM'
            time_morn.append(time)
        elif start_min == '30':
            hour = int(start_hour) + 1
            count = 1
            time = str(start_hour) + ':' + '30' + ' AM'
            time_morn.append(time)

        elif start_min == '40':
            hour = int(start_hour) + 1
            count = 1
            time = str(start_hour) + ':' + '40' + ' AM'
            time_morn.append(time)

        for h in range(hour, hour + 3):

            for m in range(0, 60, 20):
                count = count + 1
                if m < 10:
                    time = str(h) + ':' + str(m) + '0 AM'
                    time_morn.append(time)
                else:
                    time = str(h) + ':' + str(m) + ' AM'
                    time_morn.append(time)
                if count == int(self.tms.quiz_morn):
                    if int(m) + 20 == 60:
                        lunchr = '00'
                        h = int(h) + 1
                        if h >= 12:
                            time = str(h) + ':' + str(lunchr) + ' PM'
                            time_morn.append(time)
            
                        else:
                            time = str(h) + ':' + str(lunchr) + ' AM'
                            time_morn.append(time)
                    else:
                        lunchr = int(m) + 20
                        time = str(h) + ':' + str(lunchr) + ' AM'
                        time_morn.append(time)
                    break
            if count == int(self.tms.quiz_morn):
                break
        # Afternoon quiz times
        # separate hour from minute. Create a hour and min list
        lunch_in = str(h) + ':' + str(lunchr)
        lunch_list_h = list(lunch_in)  # convert to list
        lunch_list_m = list(lunch_in)  # convert to list

        lunch_list_m[:-2] = []  # slice list for minutes
        lunch_list_h[2:] = []  # slice list for hour
        lunch_hour = ''.join(lunch_list_h)  # join back to a string
        lunch_min = ''.join(lunch_list_m)  # join back to a string
        lunch_length = self.tms.quiz_lunch_length
        if lunch_length > 40: 
            after_start = int(lunch_hour) + 1
        else:
            lunch_min = int(lunch_min) + int(lunch_length)
            if lunch_min >= 60:
                lunch_min = int(lunch_min) - 60
                after_start = int(lunch_hour) + 1
            else:
                after_start = int(lunch_hour)
                
        if int(after_start) != 13:
            if int(after_start) >= 12:
                if int(lunch_min) == 00:
                    count = 0
                    for i in range(0,60,20):
                        min_start = int(lunch_min)
                        min_start += i
                        count += 1
                        if i == 0:
                            time = str(after_start) + ':' + str(min_start) +  '0 PM'
                            time_after.append(time)
                        else:
                            time = str(after_start) + ':' + str(min_start) +  ' PM'
                            time_after.append(time)
                else:
                    count = 1
                    time = str(after_start) + ':' + str(lunch_min) +  ' PM'
                    time_after.append(time)
                if int(lunch_min) == 20:
                    lunch_min = int(lunch_min) + 20
                    time = str(after_start) + ':' + str(lunch_min) + ' PM'
                    time_after.append(time)
                    count += 1

        else:
            count = 0
        for h in range(1, 5):

            for m in range(0, 60, 20):
                count += 1
                if m < 10:
                    time = '0' + str(h) + ':' + str(m) + '0 PM'
                    time_after.append(time)
                else:
                    time = '0' + str(h) + ':' + str(m) + ' PM'
                    time_after.append(time)

                if count >= int(self.tms.quiz_after):
                    break
            if count >= int(self.tms.quiz_after):
                break
        self.morn_times = list(self.tms.group_list_items(time_morn, 1))
        self.after_times = list(self.tms.group_list_items(time_after, 1))

    def generate_cert(self):
        cell_width_time = 0.75
        cell_width = 0.5
        row_height = 0.25
        row_morn = self.tms.quiz_morn + 2
        row_after = self.tms.quiz_after
        line_width = 2
        path = self.path
        margin_size = .5
        doc = SimpleDocTemplate(path, pagesize=landscape(letter),topMargin = margin_size*inch,
                              bottomMargin = margin_size*inch, leftMargin = margin_size*inch, rightMargin = margin_size*inch)
        title_text = self.tms.header_title
        title_list = [[title_text]]
        # container for the 'Flowable' objects
        elements = []
        if self.tms.header_on == True:
            title=Table(title_list,1*[cell_width_time*inch], 1*[row_height*inch])
            title.setStyle(TableStyle([('ALIGN',(1,1),(-1,-1),'LEFT'),
                    ('ALIGN',(0,0),(-1,-1),'CENTER'),
                    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                    ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                    ('FONTSIZE',(0,0),(-1,-1),18),
                    ('TOPPADDING', (0,0), (-1,-1), .25*inch),
                    ('BOTTOMPADDING', (0,0), (-1,-1), .75*inch),
                    
                        ]))            
            elements.append(title)
        morn_time=Table(self.morn_times,1*[cell_width_time*inch], row_morn*[row_height*inch])
        morn_time.setStyle(TableStyle([('ALIGN',(1,1),(-1,-1),'LEFT'),
                    ('BOX',(0,0),(-1,-1),line_width,colors.black),
                    ('ALIGN',(0,0),(-1,-1),'CENTER'),
                    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                    ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                    ('BACKGROUND',(0,0),(-1,0),colors.lightgrey),

                        ]))
        col_quiz = len(self.tms.quiz_random[0])
        morn_team=Table(self.morn_quiz,col_quiz*[cell_width*inch], row_morn*[row_height*inch])
        if self.tms.rooms ==1:
            morn_team.setStyle(TableStyle([('ALIGN',(1,1),(-2,-2),'LEFT'),
                        ('BOX',(0,0),(2,-1),line_width,colors.black),
                        ('SPAN',(0,0),(2,0)),
                        ('SPAN',(0,-1),(2,-1)), 
                        ('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                        ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                        ('BACKGROUND',(0,0),(-1,0),colors.lightgrey),
                        

                        ]))

        elif self.tms.rooms ==2:
            morn_team.setStyle(TableStyle([('ALIGN',(1,1),(-2,-2),'LEFT'),
                        ('BOX',(0,0),(2,-1),line_width,colors.black),
                        ('BOX',(3,0),(5,-1),line_width,colors.black),
                        ('SPAN',(0,0),(2,0)),
                        ('SPAN',(3,0),(5,0)), 
                        ('SPAN',(0,-1),(5,-1)), 
                        ('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                        ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                        ('BACKGROUND',(0,0),(-1,0),colors.lightgrey),

                        ]))

        elif self.tms.rooms ==3:
            morn_team.setStyle(TableStyle([('ALIGN',(1,1),(-2,-2),'LEFT'),
                        ('BOX',(0,0),(2,-1),line_width,colors.black),
                        ('BOX',(3,0),(5,-1),line_width,colors.black),
                        ('BOX',(6,0),(8,-1),line_width,colors.black),
                        ('SPAN',(0,0),(2,0)),
                        ('SPAN',(3,0),(5,0)),
                        ('SPAN',(6,0),(8,0)), 
                        ('SPAN',(0,-1),(8,-1)), 
                        ('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                        ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                        ('BACKGROUND',(0,0),(-1,0),colors.lightgrey),
                        ]))
                        
        elif self.tms.rooms ==4:
            morn_team.setStyle(TableStyle([('ALIGN',(1,1),(-2,-2),'LEFT'),
                        ('BOX',(0,0),(2,-1),line_width,colors.black),
                        ('BOX',(3,0),(5,-1),line_width,colors.black),
                        ('BOX',(6,0),(8,-1),line_width,colors.black),
                        ('BOX',(9,0),(11,-1),line_width,colors.black),
                        ('SPAN',(0,0),(2,0)),
                        ('SPAN',(3,0),(5,0)),
                        ('SPAN',(6,0),(8,0)),
                        ('SPAN',(9,0),(11,0)),
                        ('SPAN',(0,-1),(11,-1)), 
                        ('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                        ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                        ('BACKGROUND',(0,0),(-1,0),colors.lightgrey),
                        ]))
                        
        elif self.tms.rooms ==5:
            morn_team.setStyle(TableStyle([('ALIGN',(1,1),(-2,-2),'LEFT'),
                        ('BOX',(0,0),(2,-1),line_width,colors.black),
                        ('BOX',(3,0),(5,-1),line_width,colors.black),
                        ('BOX',(6,0),(8,-1),line_width,colors.black),
                        ('BOX',(9,0),(11,-1),line_width,colors.black),
                        ('BOX',(12,0),(14,-1),line_width,colors.black),
                        ('SPAN',(0,0),(2,0)),
                        ('SPAN',(3,0),(5,0)),
                        ('SPAN',(6,0),(8,0)),
                        ('SPAN',(9,0),(11,0)),
                        ('SPAN',(12,0),(14,0)),
                        ('SPAN',(0,-1),(14,-1)), 
                        ('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                        ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                        ('BACKGROUND',(0,0),(-1,0),colors.lightgrey),
                        ]))
                        
                       
        if len(self.tms.teams) > self.tms.teams_capacity:
            col_break = len(self.tms.teams) - self.tms.teams_capacity
            morn_break=Table(self.break_morn,col_break*[cell_width*inch], row_morn*[row_height*inch])
            if col_break == 2:
                morn_break.setStyle(TableStyle([('ALIGN',(1,1),(-2,-2),'LEFT'),
                        ('BOX',(0,0),(-1,-1),line_width,colors.black),
                        ('SPAN',(0,0),(1,0)),
                        ('SPAN',(0,-1),(1,-1)),
                        ('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                        ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                        ('BACKGROUND',(0,0),(0,0),colors.lightgrey),

                        ]))
            else:
                morn_break.setStyle(TableStyle([('ALIGN',(1,1),(-2,-2),'LEFT'),
                        ('BOX',(0,0),(-1,-1),line_width,colors.black),
                        ('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                        ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                        ('BACKGROUND',(0,0),(0,0),colors.lightgrey),

                        ]))
        if self.tms.quiz_morn == 3:
            t1_h = 1.25 * inch
        elif self.tms.quiz_morn == 4:
            t1_h = 1.5 * inch        
        elif self.tms.quiz_morn == 5:
            t1_h = 1.75 * inch
        elif self.tms.quiz_morn == 6:
            t1_h = 2 * inch
        elif self.tms.quiz_morn == 7:
            t1_h = 2.25 * inch  
            
        if len(self.tms.teams) > self.tms.teams_capacity:
            morn_quiz = [[morn_time, morn_team, morn_break]]
            #adjust the length of tables
            t1_w = .75 * inch
            if self.tms.rooms == 1:
                t2_w = 1.5 * inch
                t3_w = 1.5 * inch
            elif self.tms.rooms == 2:
                t2_w = 3 * inch
                t3_w = 1.5 * inch
            elif self.tms.rooms == 3:
                t2_w = 4.5 * inch
                t3_w = 1.5 * inch
            elif self.tms.rooms == 4:
                t2_w = 6 * inch
                t3_w = 1.5 * inch
            elif self.tms.rooms == 5:
                t2_w = 7.5 * inch
                t3_w = 1.5 * inch
            
        else:
            morn_quiz = [[morn_time, morn_team]]
            #adjust the length of tables
            t1_w = .75 * inch
            if self.tms.rooms == 1:
                t2_w = 1.5 * inch
            elif self.tms.rooms == 2:
                t2_w = 3 * inch
            elif self.tms.rooms == 3:
                t2_w = 4.5 * inch
            elif self.tms.rooms == 4:
                t2_w = 6 * inch
            elif self.tms.rooms == 5:
                t2_w = 7.5 * inch
        if len(self.tms.teams) > self.tms.teams_capacity:    
            shell_table = Table(morn_quiz, rowHeights = [t1_h],colWidths=[t1_w, t2_w,t3_w])
        else:
            shell_table = Table(morn_quiz, rowHeights = [t1_h], colWidths=[t1_w, t2_w])
    
        shell_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
        elements.append(shell_table)

        # Afternoon quizzes ******************************************************************************
        after_time=Table(self.after_times,1*[cell_width_time*inch], row_after*[row_height*inch])
        after_time.setStyle(TableStyle([('ALIGN',(1,1),(-1,-1),'LEFT'),
                    ('BOX',(0,0),(-1,-1),line_width,colors.black),
                    ('ALIGN',(0,0),(-1,-1),'CENTER'),
                    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                    ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),

                        ]))
        col_quiz = len(self.tms.quiz_random[0])
        after_team=Table(self.after_quiz,col_quiz*[cell_width*inch], row_after*[row_height*inch])
        if self.tms.rooms ==1:
            after_team.setStyle(TableStyle([('ALIGN',(1,1),(-2,-2),'LEFT'),
                        ('BOX',(0,0),(2,-1),line_width,colors.black),
                        ('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                        ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),

                        ]))

        elif self.tms.rooms ==2:
            after_team.setStyle(TableStyle([('ALIGN',(1,1),(-2,-2),'LEFT'),
                        ('BOX',(0,0),(2,-1),line_width,colors.black),
                        ('BOX',(3,0),(5,-1),line_width,colors.black), 
                        ('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                        ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),

                        ]))

        elif self.tms.rooms ==3:
            after_team.setStyle(TableStyle([('ALIGN',(1,1),(-2,-2),'LEFT'),
                        ('BOX',(0,0),(2,-1),line_width,colors.black),
                        ('BOX',(3,0),(5,-1),line_width,colors.black),
                        ('BOX',(6,0),(8,-1),line_width,colors.black),
                        ('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                        ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),

                        ]))
                        
        elif self.tms.rooms ==4:
            after_team.setStyle(TableStyle([('ALIGN',(1,1),(-2,-2),'LEFT'),
                        ('BOX',(0,0),(2,-1),line_width,colors.black),
                        ('BOX',(3,0),(5,-1),line_width,colors.black),
                        ('BOX',(6,0),(8,-1),line_width,colors.black),
                        ('BOX',(9,0),(11,-1),line_width,colors.black), 
                        ('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                        ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                        ]))
                        
        elif self.tms.rooms ==5:
            after_team.setStyle(TableStyle([('ALIGN',(1,1),(-2,-2),'LEFT'),
                        ('BOX',(0,0),(2,-1),line_width,colors.black),
                        ('BOX',(3,0),(5,-1),line_width,colors.black),
                        ('BOX',(6,0),(8,-1),line_width,colors.black),
                        ('BOX',(9,0),(11,-1),line_width,colors.black),
                        ('BOX',(12,0),(14,-1),line_width,colors.black), 
                        ('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                        ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                        ]))
                        
        if len(self.tms.teams) > self.tms.teams_capacity:
            col_break = len(self.tms.teams) - self.tms.teams_capacity
            after_break=Table(self.break_after,col_break*[cell_width*inch], row_after*[row_height*inch])
            after_break.setStyle(TableStyle([('ALIGN',(1,1),(-2,-2),'LEFT'),
                        ('BOX',(0,0),(-1,-1),line_width,colors.black),
                        ('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                        ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),

                        ]))

        if self.tms.quiz_after == 4:
            t1_h = 1.25 * inch        
        elif self.tms.quiz_after == 5:
            t1_h = 1.5 * inch
        elif self.tms.quiz_after == 6:
            t1_h = 1.75 * inch
        elif self.tms.quiz_after == 7:
            t1_h = 2.0 * inch  
                      
        if len(self.tms.teams) > self.tms.teams_capacity:
            after_quiz = [[after_time, after_team, after_break]]
            #adjust the length of tables
            t1_w = .75 * inch
            if self.tms.rooms == 1:
                t2_w = 1.5 * inch
                t3_w = 1.5 * inch
            elif self.tms.rooms == 2:
                t2_w = 3 * inch
                t3_w = 1.5 * inch
            elif self.tms.rooms == 3:
                t2_w = 4.5 * inch
                t3_w = 1.5 * inch
            elif self.tms.rooms == 4:
                t2_w = 6 * inch
                t3_w = 1.5 * inch
            elif self.tms.rooms == 5:
                t2_w = 7.5 * inch
                t3_w = 1.5 * inch
            
        else:
            after_quiz = [[after_time, after_team]]
            #adjust the length of tables
            t1_w = .75 * inch
            if self.tms.rooms == 1:
                t2_w = 1.5 * inch
            elif self.tms.rooms == 2:
                t2_w = 3 * inch
            elif self.tms.rooms == 3:
                t2_w = 4.5 * inch
            elif self.tms.rooms == 4:
                t2_w = 6 * inch
            elif self.tms.rooms == 5:
                t2_w = 7.5 * inch
        if len(self.tms.teams) > self.tms.teams_capacity:
            shell_table2 = Table(after_quiz, rowHeights = [t1_h],colWidths=[t1_w, t2_w,t3_w])
        else:
            shell_table2 = Table(after_quiz, rowHeights = [t1_h],colWidths=[t1_w, t2_w])
        shell_table2.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
        elements.append(shell_table2)
        
        leg_row_height = 0.2
        row_after = len(self.legend_name)
        t4=Table(self.legend_name,1*[1.5*inch], row_after*[leg_row_height*inch])
        t4.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'LEFT'),
                    ('BOX',(0,0),(-1,-1),line_width,colors.black),
                    ('ALIGN',(0,0),(-1,-1),'CENTER'),
                    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                    ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                    ('BACKGROUND',(0,0),(0,-1),colors.lightgrey),
                    ]))
                    
        
        t5=Table(self.legend_abr,1*[.75*inch], row_after*[0.2*inch])
        t5.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'LEFT'),
                    ('BOX',(0,0),(-1,-1),line_width,colors.black),
                    ('ALIGN',(0,0),(-1,-1),'CENTER'),
                    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                    ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                    ]))
                    

        if len(self.tms.teams) >= self.legend_break_amount:

            leg_row_height = 0.2
            row_after = len(self.legend_name2)
            t6=Table(self.legend_name2,1*[1.5*inch], row_after*[leg_row_height*inch])
            t6.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'LEFT'),
                    ('BOX',(0,0),(-1,-1),line_width,colors.black),
                    ('ALIGN',(0,0),(-1,-1),'CENTER'),
                    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                    ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                    ('BACKGROUND',(0,0),(0,-1),colors.lightgrey),
                    ]))
                    
        
            t7=Table(self.legend_abr2,1*[.75*inch], row_after*[0.2*inch])
            t7.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'LEFT'),
                    ('BOX',(0,0),(-1,-1),line_width,colors.black),
                    ('ALIGN',(0,0),(-1,-1),'CENTER'),
                    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                    ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                    ]))
                      
        if len(self.tms.teams) < self.legend_break_amount:
            leg = [[t4, t5]]
            t6_w = 1.5 * inch
            t7_w = 1.5 * inch
            shell_table3 = Table(leg,colWidths=[t6_w, t7_w])
        else:
            leg = [[t4, t5, t6, t7]]
            t4_w = 1.5 * inch
            t5_w = .750 * inch
            t6_w = 1.5 * inch
            t7_w = 1.0 * inch
            shell_table3 = Table(leg,colWidths=[t4_w, t5_w, t6_w, t7_w])

        shell_table3.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
        elements.append(shell_table3)
        doc.build(elements)

if __name__ == '__main__':
    app = ExportPdf()
    


