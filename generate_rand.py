#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import sys, os
import pickle
import configparser

class ScheduleGen(object):
    def __init__(self):

        self.open_file()
        self.settings()
        self.team_info()
        self.quiz_list()

    def open_file(self):
        """
            read python dict back from the file. If it doesn't exist then it creates it.
        """
        if os.name == 'posix':
            with open(self.get_resource_path('teams.qs'), 'rb') as file_:
                self.teams_present = pickle.load(file_)
        elif os.name == 'nt':
            with open('teams.qs', 'rb') as file_:
                self.teams_present = pickle.load(file_)
          
    def team_info(self):
        self.teams = [x for x in self.teams_present.values()]  # Creates a list of teams from  the values of the dictionary teams_present
        self.rooms = int(len(self.teams) / 3)  # sees how many teams then divides it by 3 and returns a integer to figure the amount of rooms needed
        self.teams_capacity = self.rooms * 3  # takes the amount rooms we have and finds how many teams can quiz at once

    def quiz_breaks(self, quizzes, positions,
                    start=0):  # takes a combined list of possible break teams and groups them 1 or 2 sub list
        self.quizzes = quizzes
        self.positions = positions
        self.start = start
        while self.start <= len(self.quizzes) - self.positions:
            yield self.quizzes[self.start:self.start + self.positions]
            self.start += self.positions

    def random_list(self, list_):  # Randomizes the list
        self.list_ = list_
        for i in self.list_:
            rand = random.sample(self.list_, len(self.list_))
            return rand

    # Create lists  for teams
    def quiz_list(self):
        self.random_teams = self.random_list(
            self.teams)  # randomize list before creating quiz lists for the whole schedule
        self.quiz = []
        self.quiz_random = []
        for i in range(self.quiz_day + 5):
            i = self.random_teams[:]
            p = []
            self.quiz.append(i)
            self.quiz_random.append(p)

        if len(self.teams) > self.teams_capacity:
            breakr = self.quiz[self.quiz_day] + self.quiz[self.quiz_day] + self.quiz[self.quiz_day] + self.quiz[
                self.quiz_day] + self.quiz[self.quiz_day]  # create a long list to create the break list from
            if len(self.teams) - self.teams_capacity > 1:  # condition to see if we have 1 or 2 break teams
                self.break_ = list(
                    self.quiz_breaks(breakr, 2))  # Create the break list, with 2 quiz break teams in their sub list
            else:
                self.break_ = list(
                    self.quiz_breaks(breakr, 1))  # Create the break list, with 1 quiz break team in its sub list
            for i in range(self.quiz_day + 5):
                p = [x for x in self.quiz[i] if x not in self.break_[i]]  # Remove break teams from the quiz
                self.quiz_random[i] = self.random_list(p)  # randomize the lists.

        else:
            for i in range(self.quiz_day + 5):
                self.quiz_random[i] = self.random_list(self.quiz[i])  # randomize list if there  are no break teams


    def get_resource_path(self,rel_path):
        dir_of_py_file = os.path.dirname(__file__)
        rel_path_to_resource = os.path.join(dir_of_py_file, rel_path)
        abs_path_to_resource = os.path.abspath(rel_path_to_resource)
        return abs_path_to_resource

    def settings(self):
        config = configparser.SafeConfigParser()
        if os.name == 'posix':
            config.read(self.get_resource_path('settings.cfg'))
        elif os.name == 'nt':
            config.read('settings.cfg')
        self.header_title = config.get('schedule', 'header_title')
        self.header_on = config.getboolean('schedule', 'header_on')
        #self.header_on_b = config.get('schedule', 'header_on')
        self.quiz_morn = config.getint('schedule', 'quizes_morning')
        self.quiz_after = config.getint('schedule', 'quizes_after')
        self.font_title_fc =  config.get('schedule','title_font_face')
        self.font_title_sz =  config.get('schedule','title_font_size')
        self.font_head_fc =  config.get('schedule','head_font_face')
        self.font_head_sz =  config.get('schedule','head_font_size')
        self.font_abr_fc =  config.get('schedule','abr_font_face')
        self.font_abr_sz =  config.get('schedule','abr_font_size')
        self.date_update = "08/10/2016"
        self.quiz_day = self.quiz_morn + self.quiz_after


    def call_excel(self):
        self.excel = excel.ExportXlsx()
    
if __name__=='__main__':
    app = ScheduleGen()
