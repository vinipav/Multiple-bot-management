import streamlit as st
import os
from general_bot import ChatBot
from custom_bot import CustomizedBot

import json

class Botspace:
    def __init__(self):
        self.default_bots = {}
        self.user_bots = {}
        self.initialize_default_bots()
    
    def initialize_default_bots(self):
        self.default_bots["GeneralBot"] = ChatBot("GeneralBot", "gpt-3.5", "a helpful assistant.", 0.5)
        
       
    def add_general_bot(self, name, model, context_prompt, temperature):
        # Create and add a new bot to user_bots
        new_bot = ChatBot(name, model, context_prompt, temperature)
        self.user_bots[name] = new_bot

    
    def add_cust_bot(self, name, model, context_prompt, temperature):
        # Create and add a new bot to user_bots
        new_bot = CustomizedBot(name, model, context_prompt, temperature)
        self.user_bots[name] = new_bot

    def get_bot(self, name):
        # Retrieve a bot by name
        return self.user_bots.get(name) or self.default_bots.get(name)

    def get_all_bots(self):
        # Get all available bots
        return {**self.default_bots, **self.user_bots}.keys()

    def delete_bot(self, name):
        # Delete a user-added bot
        if name in self.user_bots:
            del self.user_bots[name]
            self.save_user_bots()

