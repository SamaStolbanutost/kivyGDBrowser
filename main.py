from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDFillRoundFlatButton
from kivy.lang import Builder
from kivy.core.window import Window
from requests import get
from os.path import basename
import json

#Window.size = (300, 500)

screen_helper = """
Screen:
    orientation: "vertical"

    MDToolbar:
        md_bg_color: 1, .8, .5, 1
        id: topbar
        title: "Level finder"
        pos_hint: {"top":1.0}


    MDBottomNavigation:
        MDBottomNavigationItem:
            name: "lvl_find"
            text: "Level finder"
            on_tab_release: current_finder = "lvl"

            MDTextField:
                id: userinput_lvl
                hint_text: "Enter Id of level"
                pos_hint: {"top":.85, "center_x":.5}
                size_hint_x: .8
                line_color_focus: 1, .8, .5, 1

            MDFillRoundFlatButton:
                text: "Search"
                pos_hint: {"center_x":.5, "center_y":.7}
                on_release: app.request_api("lvl")

            MDFillRoundFlatButton:
                text: "Download song"
                pos_hint: {"center_x":.5, "center_y":.6}
                on_release: app.request_api("sng_download_lvl")

            MDLabel:
                id: info_lvl
                text: " "
                halign: "center"
                pos_hint: {"center_x":.5, "center_y":.4}

        MDBottomNavigationItem:
            name: "plr_find"
            text: "Player fider"

            MDTextField:
                id: userinput_plr
                hint_text: "Enter Id or Username of player"
                pos_hint: {"top":.85, "center_x":.5}
                size_hint_x: .8
                line_color_focus: 1, .8, .5, 1

            MDFillRoundFlatButton:
                text: "Search"
                pos_hint: {"center_x":.5, "center_y":.7}
                on_release: app.request_api("plr")

            MDLabel:
                id: info_plr
                text: " "
                halign: "center"
                pos_hint: {"center_x":.5, "center_y":.4}

        MDBottomNavigationItem:
            name: "songs"
            text: "Song check"
            id: sng_tab

            MDTextField:
                id: userinput_sng
                hint_text: "Enter song ID"
                pos_hint: {"top":.85, "center_x":.5}
                size_hint_x: .8
                line_color_focus: 1, .8, .5, 1

            MDFillRoundFlatButton:
                text: "Check"
                pos_hint: {"center_x":.5, "center_y":.7}
                on_release: app.request_api("sng_check")

            MDFillRoundFlatButton:
                text: "Download"
                pos_hint: {"center_x":.5, "center_y":.6}
                on_release: app.request_api("sng_download")

            MDLabel:
                text: " "
                id: info_sng
                halign: "center"
                pos_hint: {"center_x":.5, "center_y":.4}
"""

# 70521879

# 1067091 1060826

class MainApp(MDApp):

    class ContentNavigationDrawer(BoxLayout):
        pass

    def build(self):
        screen = Builder.load_string(screen_helper)

        return screen

    def request_api(self, request):
        info_label = ""
        if request == "lvl":
            try:
                info = get("https://www.gdbrowser.com/api/level/" + self.root.ids.userinput_lvl.text).text
                info = json.loads(info)

                info_label += "Name: " + info["name"]
                info_label += "\nSong: " + info["songName"] + " by " + info["songAuthor"]
                info_label += "\nSong ID: " + str(info["songID"])
                info_label += "\nAuthor: " + info["author"]
                info_label += "\nDifficulty: " + info["difficulty"]
                if info["stars"] > 0:
                    info_label += " (" + str(info["stars"]) + " stars)"
                else:
                    info_label += " ( No stars )"

                    if info["featured"]:
                        if info["epic"]:
                            info_label += "\nEpic rate"
                        else:
                            info_label += "\nFeatured rate"
            except:
                info_label = "An error has occured"

            self.root.ids.info_lvl.text = info_label

        elif request == "plr":
            try:
                info = get("https://www.gdbrowser.com/api/profile/" + self.root.ids.userinput_plr.text).text
                info = json.loads(info)

                info_label += "Name: " + info["username"]
                info_label += "\nGlobal rank: " + str(info["rank"])
                info_label += "\nDemons: " + str(info["demons"])
                info_label += "\nAccount / Player IDs: " + str(info["playerID"]) + " / " + str(info["accountID"])
                info_label += "\nStars: " + str(info["stars"])
                info_label += "\nDiamonds: " + str(info["diamonds"])
                info_label += "\nOfficial coins: " + str(info["coins"])
                info_label += "\nUser coins: " + str(info["userCoins"])
                info_label += "\nCreator points: " + str(info["cp"])
                info_label += "\nModeration level: "
                if info["moderator"] == 0:
                    info_label += "Player"
                elif info["moderator"] == 1:
                    info_label += "Moderator"
                elif info["moderator"] == 2:
                    info_label += "Older moderator"

            except:
                info_label = "An error has occured"

            self.root.ids.info_plr.text = info_label
        elif request == "sng_check":
            try:
                info = get("https://www.gdbrowser.com/api/song/" + self.root.ids.userinput_sng.text).text
                if info:
                    info_label = "Song is allowed"
                else:
                    info_label = "Song is disallowed"
            except:
                info_label = "An error has occured"

            self.root.ids.info_sng.text = info_label

        elif request == "sng_download":
            try:
                song = get("https://www.newgrounds.com/audio/download/" + str(self.root.ids.userinput_sng.text))

                songname = song.headers["content-disposition"].replace("attachment; filename=", "")
                songname = songname[1:-1]

                with open("/storage/emulated/0/Music/" + songname, "wb") as file:
                   file.write(song.content)

                self.root.ids.info_sng.text = "Music saved! (check your Music folder)"

            except:
                self.root.ids.info_sng.text = "An error has occured"

        elif request == "sng_download_lvl":
            try:
                levelinfo = get("https://www.gdbrowser.com/api/level/" + self.root.ids.userinput_lvl.text).text
                levelinfo = json.loads(levelinfo)

                song = get("https://www.newgrounds.com/audio/download/" + str(levelinfo["songID"]))

                songname = song.headers["content-disposition"].replace("attachment; filename=", "")
                songname = songname[1:-1]

                with open("/storage/emulated/0/Music/" + songname, "wb") as file:
                    file.write(song.content)

                    self.root.ids.info_lvl.text = "Music saved! (check your Music folder)"

            except:
                self.root.ids.info_lvl.text = "An error has occured"

MainApp().run()
