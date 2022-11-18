from FileReader.classes import BasicFileReaderMeta
from Automator.classes import VJudge
from FileReader.classes import JsonFileReader
import os

config_file_path = os.getcwd() + '/' + 'config.json'
data = JsonFileReader().read(config_file_path)
VJudge(data).automate()
