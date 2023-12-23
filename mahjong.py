#!/usr/bin/env python3

import MenuWindow
import point
import Menu

import tkinter as tk
from tkinter import simpledialog, messagebox, font

class MahjongScoreboard:
    def __init__(self, root):
        self.root = root
        root.title("Mahjong Scoreboard")
        self.set_window_geometry()

        self.east_wind = '東'
        self.south_wind = '南'
        self.west_wind = '西'
        self.north_wind = '北'
        self.wind = [self.east_wind, self.south_wind, self.west_wind, self.north_wind]

        self.players = {f"{self.east_wind}": "", f"{self.south_wind}": "", f"{self.west_wind}": "", f"{self.north_wind}": ""}
        self.register_players()

        self.FIRST_DEALER = self.players[self.east_wind]
        self.round_wind = self.wind[0]
        self.honba = 0
        self.round = 1

        self.plyaer_font = font.Font(family="Arial", size=30, weight="bold")

        self.scores = {player: 25000 for player in self.players.values()}
        self.pot = 0
        self.score_labels = {}
        self.display_scores()

        tk.Button(root, text="立直", command=self.open_riichi_window).grid(row=0, column=3)
        tk.Button(root, text="和了", command=self.open_win_window).grid(row=1, column=3)
        tk.Button(root, text="流局", command=self.open_draw_window).grid(row=2, column=3)
        tk.Button(root, text="直接", command=self.open_adjust_score_window).grid(row=0, column=4)
        tk.Button(root, text=" 場", command=self.open_adjust_pot_window).grid(row=1, column=4)
        tk.Button(root, text="終了", command=root.quit).grid(row=2, column=4)
    
    def set_window_geometry(self):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        width = 900
        height = 200

        # ウィンドウを中央に配置するための x と y 座標を計算
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        root.geometry(f'{width}x{height}+{x}+{y}')

    def register_players(self):
        for direction in self.players:
            self.players[direction] = simpledialog.askstring("プレイヤー名入力", f"{direction}のプレイヤー名を入力してください:")

    def display_scores(self):
        names = [self.players["西"], self.players["南"], self.players["東"], self.players["北"]]
        rows = [0, 1, 2, 1]
        columns = [1, 2, 1, 0]
        for name, row, column in zip(names, rows, columns):
            if name in self.score_labels:
                self.score_labels[name].config(text=f"{name} ({self.parse_players_value(name)}): {self.scores[name]}点")
            else:
                self.score_labels[name] = tk.Label(self.root, font=self.plyaer_font, text=f"{name} ({self.parse_players_value(name)}): {self.scores[name]}点")
                self.score_labels[name].grid(row=row, column=column)

        if "pot" in self.score_labels:
            self.score_labels["pot"].config(text=f"場: {self.pot}点")
        else:
            self.score_labels["pot"] = tk.Label(self.root, text=f"場: {self.pot}点")
            self.score_labels["pot"].grid(row=1, column=1)
        
        tk.Label(self.root, font=self.plyaer_font, text=f"{self.round_wind}{self.round}局").grid(row=3, column=0)
        tk.Label(self.root, font=self.plyaer_font, text=f"{self.honba}本場").grid(row=4, column=0)

    def open_riichi_window(self):
        self.riichi_label = "立直した人"

        self.riichi_window = MenuWindow.MenuWindow(root=self.root, players=self.players)
        self.riichi_window.open_window(title="立直")

        self.riichi_menu = Menu.Menu(
            root=self.root,
            label=self.riichi_label,
            window=self.riichi_window.window,
            items=list(self.players.values())
        )
        self.riichi_menu.set_items_by_pulldown()

        tk.Button(self.riichi_window.window, text="立直", command=self.riichi).grid(row=1, column=1)

    def riichi(self):
        riichi_player = self.riichi_menu.item.get()
        if self.scores[riichi_player] >= 1000:
            self.scores[riichi_player] -= 1000
            self.pot += 1000
            self.display_scores()
        else:
            messagebox.showerror("エラー", f"{riichi_player}のプレイヤーは点数が不足しています。")

    def open_win_window(self):
        self.win_window = MenuWindow.MenuWindow(root=self.root, players=self.players)
        self.win_window.open_window(title="和了")

        self.winner_label="和了した人"
        self.loser_label="放銃した人"
        self.han_lablel="翻数"
        self.type_label="和了方法"

        self.winner_menu = Menu.Menu(
            root=self.root,
            label=self.winner_label,
            window=self.win_window.window,
            items=list(self.players.values()),
        )
        self.winner_menu.set_items_by_pulldown()

        self.loser_menu = Menu.Menu(
            root=self.root,
            label=self.loser_label,
            window=self.win_window.window,
            items=list(self.players.values()),
            row=1
        )
        self.loser_menu.set_items_by_pulldown()

        self.han_menu = Menu.Menu(
            root=self.root,
            label=self.han_lablel,
            window=self.win_window.window,
            items=list(range(1,14)),
            row=2
        )
        self.han_menu.set_items_by_pulldown()

        self.type_menu = Menu.Menu(
            root=self.root,
            label=self.type_label,
            window=self.win_window.window,
            items=["ロン", "ツモ"],
            row=3
        )
        self.type_menu.set_items_by_pulldown()

        tk.Button(self.win_window.window, text="和了", command=self.win).grid(row=4, column=1)

    def win(self):
        winner = self.winner_menu.item.get()
        loser  = self.loser_menu.item.get()
        winner_wind = self.parse_players_value(target_value=self.winner_menu.item.get())
        type = self.type_menu.item.get()
        han = int(self.han_menu.item.get())

        self.scores[winner] += self.pot
        self.pot = 0

        if type == "ロン":
            points = point.ron_point(han)

            if winner_wind == "東":
                self.scores[winner] += points[0]
                self.scores[loser] -= points[0]
            else:
                self.scores[winner] += points[1]
                self.scores[loser] -= points[1]
        else:
            points = point.tsumo_point(han)
            if winner_wind == "東":
                for key in self.players:
                    if key != winner_wind:
                        self.scores[self.players[key]] -= points[0]
                        self.scores[winner] += points[0]
            else:
                for key in self.players:
                    if key != winner_wind:
                        if key == "東":
                            self.scores[self.players[key]] -= points[0]
                            self.scores[winner] += points[0]
                        else:
                            self.scores[self.players[key]] -= points[1]
                            self.scores[winner] += points[1]

        if winner_wind != "東":
            self.change_wind()
        else:
            self.honba += 1
        self.display_scores()

    def open_draw_window(self):
        self.east_player_label = self.players["東"]
        self.south_player_label = self.players["南"]
        self.west_player_label = self.players["西"]
        self.north_player_label = self.players["北"]

        items=["聴牌", "不聴"]

        self.draw_window = MenuWindow.MenuWindow(root=self.root, players=self.players, weight=300)
        self.draw_window.open_window(title="流局")

        self.east_menu = Menu.Menu(
            root=self.root,
            label=self.east_player_label,
            window=self.draw_window.window,
            items=items
        )
        self.east_menu.set_checkbox_menu()

        self.south_menu = Menu.Menu(
            root=self.root,
            label=self.south_player_label,
            window=self.draw_window.window,
            items=items,
            row=1
        )
        self.south_menu.set_checkbox_menu()

        self.west_menu = Menu.Menu(
            root=self.root,
            label=self.west_player_label,
            window=self.draw_window.window,
            items=items,
            row=2
        )
        self.west_menu.set_checkbox_menu()

        self.north_menu = Menu.Menu(
            root=self.root,
            label=self.north_player_label,
            window=self.draw_window.window,
            items=items,
            row=3
        )
        self.north_menu.set_checkbox_menu()

        tk.Button(self.draw_window.window, text="流局", command=self.draw).grid(row=5, column=1)

    def draw(self):
        draw_status = {}

        draw_status[self.players['東']] = self.east_menu.get_checked_list()[0]
        draw_status[self.players['南']] = self.south_menu.get_checked_list()[0]
        draw_status[self.players['西']] = self.west_menu.get_checked_list()[0]
        draw_status[self.players['北']] = self.north_menu.get_checked_list()[0]

        tenpai_players = [key for key, value in draw_status.items() if value == "聴牌"]
        noten_players = [key for key, value in draw_status.items() if value == "不聴"]

        tenpai_point = point.ten_pai_point(len(tenpai_players))
        noten_point = point.no_ten_point(len(noten_players))

        for tenpai_player in tenpai_players:
            self.scores[tenpai_player] += tenpai_point

        for noten_player in noten_players:
            self.scores[noten_player] -= noten_point

        self.display_scores()

        if self.players["東"] in noten_players:
            self.change_wind()
        else:
            self.honba += 1

    def open_adjust_score_window(self):
        self.adjust_score_window = MenuWindow.MenuWindow(root=self.root, players=self.players)
        self.adjust_score_window.open_window(title="点数調整")

        self.from_label = "誰から"
        self.to_label = "誰に"
        self.point_label = "何点"

        self.from_menu = Menu.Menu(
            root=self.root,
            label=self.from_label,
            window=self.adjust_score_window.window,
            items=list(self.players.values())
        )
        self.from_menu.set_items_by_pulldown()

        self.to_menu = Menu.Menu(
            root=self.root,
            label=self.to_label,
            window=self.adjust_score_window.window,
            items=list(self.players.values()),
            row=1
        )
        self.to_menu.set_items_by_pulldown()

        self.point_menu = Menu.Menu(
            root=self.root,
            label=self.point_label,
            window=self.adjust_score_window.window,
            items=[],
            row=2
        )
        self.point_menu.set_point_menu()

        tk.Button(self.adjust_score_window.window, text="調整", command=self.adjust_score).grid(row=4, column=1)

    def adjust_score(self):
        from_player = self.from_menu.item.get()
        to_player = self.to_menu.item.get()
        point = int(self.point_menu.item.get())

        self.scores[from_player] -= point
        self.scores[to_player] += point

        self.display_scores()
    
    def open_adjust_pot_window(self):
        self.adjust_pot_window = MenuWindow.MenuWindow(root=self.root, players=self.players, weight=250)
        self.adjust_pot_window.open_window(title="場の調整")

        adjust_player_label = "プレーヤー"
        point_label= "点数"
        direction_label = "どちらに店が動くか"


        self.adjust_player_menu = Menu.Menu(
            root=self.root,
            label=adjust_player_label,
            window=self.adjust_pot_window.window,
            items=list(self.players.values())
        )
        self.adjust_player_menu.set_items_by_pulldown()

        self.pot_point_menu = Menu.Menu(
            root=self.root,
            label=point_label,
            window=self.adjust_pot_window.window,
            items=[],
            row=1
        )
        self.pot_point_menu.set_point_menu()

        self.move_direction_menu = Menu.Menu(
            root=self.root,
            label=direction_label,
            window=self.adjust_pot_window.window,
            items=["pot->player", "player->pot"],
            row=2
        )
        self.move_direction_menu.set_items_by_pulldown()

        tk.Button(self.adjust_pot_window.window, text="場の調整", command=self.adjust_pot).grid(row=4, column=1)

    def adjust_pot(self):
        adjust_player = self.adjust_player_menu.item.get()
        point = int(self.pot_point_menu.item.get())
        direction = self.move_direction_menu.item.get()

        if direction == self.move_direction_menu.items[0]:
            self.pot -= point
            self.scores[adjust_player] += point
        else:
            self.pot += point
            self.scores[adjust_player] -= point

        self.display_scores()

    def parse_players_value(self, target_value):
        for key, value in self.players.items():
            if value == target_value:
                return key
            
    def change_wind(self):
        temp_players = self.players.copy()
        self.players.update({"東" : temp_players.get("南")})
        self.players.update({"南" : temp_players.get("西")})
        self.players.update({"西" : temp_players.get("北")})
        self.players.update({"北" : temp_players.get("東")})

        self.honba = 0
        self.round += 1

        if self.round > 4:
            self.round = 1
            self.round_wind = self.wind[1]
            
        messagebox.showinfo("", "局が進みます．")

        self.display_scores()

if __name__ == "__main__":
    root = tk.Tk()
    app = MahjongScoreboard(root)
    root.mainloop()
