from PyQt5.QtWidgets import QApplication
import sys
from pet import App
import pymysql
if __name__ == '__main__':

    # from RumiaPet_main.work_place.SmartDeskPet.RandomReminder import Sentiment_pet,Weather_pet
    # print(Sentiment_pet())
    # print(Weather_pet())

    app = QApplication(sys.argv)
    pet = App()
    sys.exit(app.exec_())
