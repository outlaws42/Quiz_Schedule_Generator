#! /usr/bin/env python3
import pickle
import random
import xlsxwriter       
class Schedule(object):
    version = "1.0.1" # Current Version
    date_update="03/15/2016"
    
    def __init__(self):

        choice = None
        while choice != "0":
            print(
            """
            Quiz Meet Schedule Generator (V%s)
            0 - Quit
            1 - List Current Teams
            2 - Add Teams
            3 - Remove Teams
            4 - Generate Schedule
            5 - About
            """ %self.version
            )
            choice = input("Choice: ")

            # Exit
            if choice == "0":
                self.goodbye()

            # list teams
            elif choice == "1":
                self.open_file()
                self.list_teams()

            elif choice == "2":
                self.open_file()
                self.list_teams()
                self.add_team()
                self.save_file()
                self.list_teams()
                
            elif choice == "3":
                self.open_file()
                self.list_teams()
                self.remove_team()
                self.save_file()
                self.list_teams()

            elif choice == "4":
                self.open_file()
                self.team_info()
                self.quiz_list()
                self.excel_export()

            elif choice == "5":
                self.about_choice()

                
            else:
                print(
                """

                """
                )
                print("That isn't a correct choice")

    def about_choice(self):
        print(
          """
          
          """)
        print (
          """
          Quiz Meet Schedule Generator
          Version:%s  %s
          Copyright 2016 Troy Franks <outlaws42@gmail.com>
          This program is free software; you can redistribute it and/or modify
          it under the terms of the GNU General Public License as published by
          the Free Software Foundation; either version 2 of the License, or
          (at your option) any later version.

          This program is distributed in the hope that it will be useful,
          but WITHOUT ANY WARRANTY; without even the implied warranty of
          MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
          GNU General Public License for more details.

          You should have received a copy of the GNU General Public License
          along with this program; if not, write to the Free Software
          Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
          MA 02110-1301, USA.
          """ % (self.version,self.date_update)
          )
          
    def add_team(self):
        choice_add=input("Do you want to add a team? ")
        while choice_add.lower() == "yes" or choice_add.lower() =="y":
            print(choice_add)
            add_key = input("Team to add (Example: Columbia City 3): ")#Get a new team to add to the dictionary
            if add_key in self.teams_present.keys():#Makes sure the added team isn't already a team in the dictionary
                print(add_key, " is already one of the teams")
                print("Please Try Again!")
                add_key = input("Team to add (Example: Columbia City 3): ")#Get a new team to add to the dictionary
            add_value = input("Team abbreviation. (Example: CC3): ")#Get a new team abbreviation for the team
            if add_value in self.teams_present.values():
                print(add_value, " is already being used")
                print("Please Try Again!")
                add_value = input("Team abbreviation. (Example: CC3): ")#Get a new abbreviation to add to the dictionary
            self.teams_present.update({add_key: add_value})#Update dictionary with the new key and value
            choice_add=input("Do you want add another team? ")
    
    def remove_team(self):
        choice_rem=input("Do you want to remove a team? ")
        while choice_rem.lower() == "yes" or choice_rem.lower() =="y":
            del_team = input("Team to Remove (Example - Columbia City 3): ")
            if  del_team in self.teams_present.keys():
                del self.teams_present[del_team]
                print (
                 """
        
                """
                )
                for k in sorted(self.teams_present):
                    print(k, ':', self.teams_present[k])
            else:
                print (del_team, " isn't a current team")
            choice_rem=input("Do you want remove another team? ")
            
    def goodbye(self):
        print("Good-bye.")

    def list_teams(self):
        print(" ")
        print("LIST OF  TEAMS")
        for k in sorted(self.teams_present):#Sorts in alphebetical order and loops through the dictionary
            print(k, ':', self.teams_present[k])#At each loop we print the key(k) :  We print the  value(teams_present[k])
        print(#Printing space
        """
        """
        )

# read python dict back from the file. If it doesn't exist then it creates it.
    def open_file(self):
        try:
            pkl_file = open('quiz_meet.pkl', 'rb')
            self.teams_present = pickle.load(pkl_file)
            pkl_file.close()
        except FileNotFoundError:
            pkl_file = open('quiz_meet.pkl', 'wb')
            self.teams_present = {
            "Columbia City 1": "CC1",
            "Columbia City 2": "CC2",
            "College 1st 1": "CF1",
            "College 1st 2":"CF2",
            "Sugar Grove 1":"SG1",
            "Sugar Grove 2":"SG2",
            "Oak Grove 1": "OG1",
            "Oak Grove 2": "OG2",
            "Syracuse 1": "SY1",
            "Syracuse 2": "SY2"
            }
            pickle.dump(self.teams_present, pkl_file)
            pkl_file.close()
            
    def save_file(self):
        output = open('quiz_meet.pkl', 'wb')
        pickle.dump(self.teams_present, output)
        output.close()
        
    def team_info(self):
        self.teams = [x for x in self.teams_present.values()] # Creates a list of teams from  the values of the dictionary teams_present
        self.rooms = int(len(self.teams) / 3) # sees how many teams then divides it by 3 and returns a integer to figure the amount of rooms needed
        self.teams_capacity = self.rooms * 3  # takes the amount rooms we have and finds how many teams can quiz at once
        
    def quiz_breaks(self,quizzes, positions, start=0): # takes a combined list of possible break teams and groups them 1 or 2 sub list
        self.quizzes = quizzes
        self.positions = positions
        self.start = start
        while self.start <= len(self.quizzes) - self.positions:
            yield self.quizzes[self.start:self.start+self.positions]
            self.start += self.positions
                             
    def random_list(self,list_): # Randomizes the list 
        self.list_ = list_
        for i in self.list_:
            rand = random.sample(self.list_,len(self.list_))
            return rand
            
    # Create lists  for teams       
    def quiz_list(self): 
        self.quiz =[]
        self.quiz_random = []
        for i in range(13):
            i = self.teams[:]
            p = []
            self.quiz.append(i)
            self.quiz_random.append(p)
    
        if len(self.teams) > self.teams_capacity:
            breakr = self.quiz[12] + self.quiz[12] + self.quiz[12] # create a long list to create the break list from
            if len(self.teams) - self.teams_capacity > 1: # condition to see if we have 1 or 2 break teams
                self.break_= list(self.quiz_breaks(breakr, 2)) # Create the break list, with 2 quiz break teams in their sub list
            else:
                self.break_= list(self.quiz_breaks(breakr, 1)) # Create the break list, with 1 quiz break team in its sub list
            for i in range(12):
                p = [x for x in self.quiz[i] if x not in self.break_[i]] # Remove break teams from the quiz
                self.quiz_random[i] = self.random_list(p) # randomize the lists.
               
        else:
            for i in range(12):
                self.quiz_random[i] = self.random_list(self.quiz[i]) # randomize list if there  are no break teams
                
    def excel_export(self): # Requires xlsxwriter module to work
        file_= input("Select a name for your schedule (No spaces):  ")
        workbook = xlsxwriter.Workbook(file_ + '.xlsx')
        worksheet = workbook.add_worksheet('Meet')
        worksheet.set_paper(1)
        bold = workbook.add_format({'bold': 1, 'align': 'center'})
        merge_format = workbook.add_format({'bold': 5,'border': 1,'align': 'center','valign': 'vcenter',})
        cell_format = workbook.add_format({'border': 1,'align': 'center','valign': 'vcenter',})
        format1 = workbook.add_format({'border': 5})
        #merge_format.set_bg_color('#e5e5e5')
        worksheet.set_column('A:A', 17)
        worksheet.set_column('E:E', 1) # space between rooms
        worksheet.set_column('I:I', 1)# space between rooms
        worksheet.set_column('M:M', 1)# space between rooms
        worksheet.set_column('Q:Q', 1)# space between rooms
        worksheet.write('A3', 'Time', merge_format)
        worksheet.merge_range('B3:D3', 'Room 1', merge_format)#Merge cell range, writes the room name
        worksheet.merge_range('F3:H3', 'Room 2', merge_format)#Merge cell range, writes the room name
        worksheet.merge_range('J3:L3', 'Room 3', merge_format)#Merge cell range, writes the room name
        if self.rooms == 4:
            worksheet.merge_range('N3:P3', 'Room 4', merge_format)#Merge cell range, writes the room name(If there is a 4th room)
        worksheet.write('A4', '09:30 AM', merge_format)#Times List  in what cell
        worksheet.write('A6', '10:00 AM', merge_format)
        worksheet.write('A8', '10:20 AM', merge_format)
        worksheet.write('A10', '10:40 AM', merge_format)
        worksheet.write('A12', '11:00 AM', merge_format)
        worksheet.write('A14', '11:20 AM', merge_format)
        worksheet.write('A16', '11:40 AM', merge_format)
        worksheet.write('A18', '12:40 PM', merge_format)
        worksheet.write('A20', '01:00 PM', merge_format)
        worksheet.write('A22', '01:20 PM', merge_format)
        worksheet.write('A24', '01:40 PM', merge_format)
        worksheet.write('A26', '02:00 PM', merge_format)
        worksheet.write('A28', '02:20 PM', merge_format)
        worksheet.write('B16', 'LUNCH', bold)

        # Export breaks for  rooms
        if len(self.teams) > self.teams_capacity: # conditon to see if we have any break teams
            if self.rooms == 4: # decide where the header for the break teams is going to go
                if len(self.teams) - self.teams_capacity == 1:
                    worksheet.write('R3', 'Break', merge_format)
                else:
                    worksheet.merge_range('R3:S3', 'Break', merge_format)
            else:
                if len(self.teams) - self.teams_capacity == 1:
                    worksheet.write('N3', 'Break', merge_format)
                else:
                    worksheet.merge_range('N3:O3', 'Break', merge_format)

            # Populate the  break teams in the morning
            row = 3
            for i in range(6):
                if self.rooms == 4:
                    col = 17
                else:
                    col = 13
                for item in (self.break_[i]):
                    worksheet.write(row, col,     item, cell_format)
                    col += 1
                row += 2

            # Populate the break teams in the afternoon
            row = 17
            for i in range(6,12):
                if self.rooms == 4:
                    col = 17
                else:
                    col = 13
                for item in (self.break_[i]):
                    worksheet.write(row, col,     item, cell_format)
                    col += 1
                row += 2

        # Populates the  quiz matches for the morning
        colum = 1
        index_ = 0
        for n in range(self.rooms): # The rooms layer this many
            row = 3
            for i in range(6): # the morning or 6 quizzes layer
                col = colum
                for item in (self.quiz_random[i][index_:index_ + 3]):
                    worksheet.write(row, col,     item, cell_format)
                    col += 1
                row += 2
            colum += 4
            index_ += 3       
            
        # Populates the  quiz matches for the afternoon
        colum = 1
        index_ = 0
        for n in range(self.rooms): # The rooms layer this many
            row = 17
            for i in range(6,12): # the afternoon or 6 quizzes layer
                col = colum
                for item in (self.quiz_random[i][index_:index_ + 3]):
                    worksheet.write(row, col,     item, cell_format)
                    col += 1
                row += 2
            colum += 4
            index_ += 3
            
        # Populate the ledger with team name and team abreaviation
        row = 30 # starts the loop on row 30
        col = 0 # starts the loop on column 0
        for key, value in sorted(self.teams_present.items()):
            worksheet.write(row, col,     key, merge_format)
            worksheet.write(row, col + 1, value, cell_format)
            row += 1
        workbook.close()       
              
        print("There will be a spreadsheet named %s.xlsx in your home folder " %file_ )
    
if __name__=='__main__':
    app = Schedule()









        
    
