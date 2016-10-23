#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import xlsxwriter
import generate_rand as rand


class ExportXlsx(object):
    def __init__(self):
        self.tms = rand.ScheduleGen()
        self.open_path_file()
        self.excel_export()
        

    def open_path_file(self):
        with open('path.txt', 'r') as path_text:
            self.path=path_text.read()

    def config_read(self):
        config = configparser.ConfigParser()
        config.read('settings.cfg')
        self.header_title = config.get('schedule', 'header_title')
        self.quiz_morn = config.get('schedule', 'quizes_morning')
        self.quiz_aft = config.get('schedule', 'quizes_after')

        

    def excel_export(self):  # Requires xlsxwriter module to work
            #file_ = input("Select a name for your schedule (No spaces):  ") or 'schedule'
            workbook = xlsxwriter.Workbook(self.path)
            worksheet = workbook.add_worksheet('Meet')
            worksheet.set_landscape()
            worksheet.set_page_view()
            worksheet.fit_to_pages(1, 1)
            #worksheet.set_print_scale(75)
            worksheet.center_horizontally()
            worksheet.set_paper(1)
            merge_format = workbook.add_format({'font_name': self.tms.font_head_fc,
                                                'font_size': self.tms.font_head_sz,
                                                'border': 1,
                                                'align': 'center',
                                                'valign': 'vcenter',
                                                })
            #merge_format.set_font_name(self.tms.font_head_fc)
            lunch_format = workbook.add_format({'font_name': self.tms.font_head_fc, 'align': 'center', 'valign': 'vcenter',})
            cell_format = workbook.add_format({'font_name': self.tms.font_abr_fc,
                                               'font_size': self.tms.font_abr_sz,
                                               'border': 1,
                                               'align': 'center',
                                               'valign':'vcenter',
                                               })

            title_format = workbook.add_format({'font_name': self.tms.font_title_fc,
                                                'font_size': self.tms.font_title_sz,
                                                'align': 'center',
                                                'valign':'vcenter'
                                                })
            date_format = workbook.add_format({'font_name': self.tms.font_head_fc,
                                                'font_size': self.tms.font_head_sz,
                                                'valign': 'vcenter'
                                                })
            
            merge_format.set_bg_color('#e5e5e5')
            worksheet.set_column('A:A', 17)
            worksheet.set_column('B:D', 6)  # teams column size
            worksheet.set_column('F:H', 6)  # teams column size
            worksheet.set_column('J:L', 6)  # teams column size
            worksheet.set_column('N:P', 6)  # teams column size
            worksheet.set_column('R:T', 6)  # teams column size
            worksheet.set_column('V:X', 6)  # teams column size
            worksheet.set_column('E:E', 1)  # space between rooms
            worksheet.set_column('I:I', 1)  # space between rooms
            worksheet.set_column('M:M', 1)  # space between rooms
            worksheet.set_column('Q:Q', 1)  # space between rooms
            worksheet.set_column('U:U', 1)  # space between rooms
            worksheet.write('A5', 'Time', merge_format)
            worksheet.merge_range('B5:D5', 'Room 1', merge_format)  # Merge cell range, writes the room name
            if self.tms.rooms >= 2:
                worksheet.merge_range('F5:H5', 'Room 2', merge_format)  # Merge cell range, writes the room name
                if self.tms.rooms >= 3:
                    worksheet.merge_range('J5:L5', 'Room 3', merge_format)  # Merge cell range, writes the room name
                    if self.tms.rooms >= 4:
                        worksheet.merge_range('N5:P5', 'Room 4',
                                              merge_format)  # Merge cell range, writes the room name(If there is a 4th room)
                        if self.tms.rooms >= 5:
                            worksheet.merge_range('R5:T5', 'Room 5',
                                                  merge_format)  # Merge cell range, writes the room name(If there is a 5th room

            else:
                pass
            #self.header_message = 'First Church of God'
            self.date_message = 'May 2 2016'
            if self.tms.header_on == True:
                worksheet.merge_range('A1:M1', self.tms.header_title,
                                    title_format)  # the header message
            #worksheet.merge_range('C2:M2', ' %s' % self.date_message, date_format)  # the header message

            # Morning quiz times and lunch
            start_in = '09:30'  # start time
            # separate hour from minute.  Create a hour and min list
            start_list_h = list(start_in)  # convert to list
            start_list_m = list(start_in)  # convert to list
            start_list_m[:-2] = []  # slice list for minutes
            start_list_h[2:] = []  # slice list for hour
            start_hour = "".join(start_list_h)  # join back to a string
            start_min = "".join(start_list_m)  # join back to a string
            hour = int(start_hour)
            if start_min == '30':
                hour = int(start_hour) + 1
                count = 1
                worksheet.write('A6', str(start_hour) + ':' + '30' + ' AM', cell_format)
                row = 7
            else:
                count = 0
                row = 5

            col = 0
            for h in range(hour, hour + 3):

                for m in range(0, 60, 20):
                    count = count + 1
                    if m < 10:
                        worksheet.write(row, col, str(h) + ':' + str(m) + '0 AM', cell_format)
                    else:
                        worksheet.write(row, col, str(h) + ':' + str(m) + ' AM', cell_format)
                    row += 2
                    if count == int(self.tms.quiz_morn):
                        row_lunch = (int(self.tms.quiz_morn) * 2) + 5
                        col_lunch = 0
                        if int(m) + 20 == 60:
                            lunchr = '00'
                            h = int(h) + 1
                            if h >= 12:
                                worksheet.write(row_lunch, col_lunch, str(h) + ':' + str(lunchr) + ' PM', cell_format)
                                col_lunch += 1
                                worksheet.write(row_lunch, col_lunch, ' LUNCH', lunch_format)
                            else:
                                worksheet.write(row_lunch, col_lunch, str(h) + ':' + str(lunchr) + ' AM', cell_format)
                                col_lunch += 1
                                worksheet.write(row_lunch, col_lunch, ' LUNCH', lunch_format)
                        else:
                            lunchr = int(m) + 20
                            worksheet.write(row_lunch, col_lunch, str(h) + ':' + str(lunchr) + ' AM', cell_format)
                            col_lunch += 1
                            worksheet.write(row_lunch, col_lunch, ' LUNCH', lunch_format)
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
            lunch_hour = "".join(lunch_list_h)  # join back to a string
            lunch_min = "".join(lunch_list_m)  # join back to a string
            after_start = int(lunch_hour) + 1

            if int(after_start) != 13:
                if int(after_start) >= 12:
                    count = 1
                    row = (int(self.tms.quiz_morn) * 2) + 7
                    worksheet.write(row, col, str(after_start) + ':' + str(lunch_min) + ' PM', cell_format)
                    row += 2
                    if int(lunch_min) == 20:
                        lunch_min = int(lunch_min) + 20
                        worksheet.write(row, col, str(after_start) + ':' + str(lunch_min) + ' PM', cell_format)
                        row += 2
                        count += 1
                else:
                    count = 0
                    row = (int(self.tms.quiz_morn) * 2) + 7
            else:
                count = 0
                row = (int(self.tms.quiz_morn) * 2) + 7

            for h in range(1, 5):

                for m in range(0, 60, 20):
                    count += 1
                    if m < 10:
                        worksheet.write(row, col, str(h) + ':' + str(m) + '0 PM', cell_format)
                    else:
                        worksheet.write(row, col, str(h) + ':' + str(m) + ' PM', cell_format)
                    row += 2

                    if count >= int(self.tms.quiz_after):
                        break
                if count >= int(self.tms.quiz_after):
                    break

            # Export breaks for  rooms
            if len(self.tms.teams) > self.tms.teams_capacity:  # conditon to see if we have any break teams
                if self.tms.rooms == 5:  # decide where the header for the break teams is going to go
                    if len(self.tms.teams) - self.tms.teams_capacity == 1:
                        worksheet.write('V5', 'Break', merge_format)
                    else:
                        worksheet.merge_range('V5:W5', 'Break', merge_format)

                elif self.tms.rooms == 4:  # decide where the header for the break teams is going to go
                    if len(self.tms.teams) - self.tms.teams_capacity == 1:
                        worksheet.write('R5', 'Break', merge_format)
                    else:
                        worksheet.merge_range('R5:S5', 'Break', merge_format)

                elif self.tms.rooms == 3:  # decide where the header for the break teams is going to go
                    if len(self.tms.teams) - self.tms.teams_capacity == 1:
                        worksheet.write('N5', 'Break', merge_format)
                    else:
                        worksheet.merge_range('N5:O5', 'Break', merge_format)

                elif self.tms.rooms == 2:  # decide where the header for the break teams is going to go
                    if len(self.tms.teams) - self.tms.teams_capacity == 1:
                        worksheet.write('J5', 'Break', merge_format)
                    else:
                        worksheet.merge_range('J5:K5', 'Break', merge_format)
                else:
                    if len(self.tms.teams) - self.tms.teams_capacity == 1:
                        worksheet.write('F5', 'Break', merge_format)
                    else:
                        worksheet.merge_range('F5:G5', 'Break', merge_format)

                # Populate the  break teams in the morning
                row = 5
                for i in range(self.tms.quiz_morn):
                    if self.tms.rooms == 5:
                        col = 21
                    elif self.tms.rooms == 4:
                        col = 17
                    elif self.tms.rooms == 3:
                        col = 13
                    elif self.tms.rooms == 2:
                        col = 9
                    else:
                        col = 5
                    for item in (self.tms.break_[i]):
                        worksheet.write(row, col, item, cell_format)
                        col += 1
                    row += 2

                # Populate the break teams in the afternoon
                row = (self.tms.quiz_morn * 2) + 7
                for i in range(self.tms.quiz_after, self.tms.quiz_after * 2):
                    if self.tms.rooms == 5:
                        col = 21
                    elif self.tms.rooms == 4:
                        col = 17
                    elif self.tms.rooms == 3:
                        col = 13
                    elif self.tms.rooms == 2:
                        col = 9
                    else:
                        col = 5
                    for item in (self.tms.break_[i]):
                        worksheet.write(row, col, item, cell_format)
                        col += 1
                    row += 2

            # Populates the  quiz matches for the morning
            colum = 1
            index_ = 0
            for n in range(self.tms.rooms):  # The rooms layer this many
                row = 5
                for i in range(self.tms.quiz_morn):  # the morning or # of quizzes layer
                    col = colum
                    for item in (self.tms.quiz_random[i][index_:index_ + 3]):
                        worksheet.write(row, col, item, cell_format)
                        col += 1
                    row += 2
                colum += 4
                index_ += 3

                # Populates the  quiz matches for the afternoon
            colum = 1
            index_ = 0
            for n in range(self.tms.rooms):  # The rooms layer this many
                row = (self.tms.quiz_morn * 2) + 7
                for i in range(self.tms.quiz_after, self.tms.quiz_after * 2):  # the afternoon or # of quizzes layer
                    col = colum
                    for item in (self.tms.quiz_random[i][index_:index_ + 3]):
                        worksheet.write(row, col, item, cell_format)
                        col += 1
                    row += 2
                colum += 4
                index_ += 3

            # Populate the ledgend with team name and team abreaviation

            row = (int(self.tms.quiz_day) * 2) + 7  
            col = 0  # starts the loop on column 0
            for key, value in sorted(self.tms.teams_present.items()):
                worksheet.write(row, col, key, merge_format)
                worksheet.write(row, col + 1, value, cell_format)
                row += 1
            workbook.close()

if __name__ == '__main__':
    app = ExportXlsx()
