import os
import shutil

import customtkinter as ctk
import requests


class TeamInput(ctk.CTkFrame):
    def __init__(self, master, labelText="Team 1", name_callback=None, hero_callback=None, bwaa_callback=None,
                 score_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.name_callback = name_callback
        self.hero_callback = hero_callback
        self.bwaa_callback = bwaa_callback
        self.score_callback = score_callback

        self.label = ctk.CTkLabel(self, text=labelText, justify="center")
        self.label.pack(pady=(10, 5))

        self.team_name_label = ctk.CTkLabel(self, text="Team Name:", justify="center")
        self.team_name_label.pack()
        self.team_name_entry = ctk.CTkEntry(self, width=150, justify="center")
        self.team_name_entry.pack(pady=(0, 10))
        self.team_name_entry.bind("<KeyRelease>", self.on_name_change)
        self.team_name_entry.insert(0, labelText)

        bwaa_path = 'static/images/teams'
        bwaas = [os.path.splitext(f)[0] for f in os.listdir(bwaa_path) if os.path.isfile(os.path.join(bwaa_path, f))]
        bwaas.insert(0, bwaas.pop(bwaas.index("None")))

        self.team_bwaa_label = ctk.CTkLabel(self, text="Team Bwaa:", justify="center")
        self.team_bwaa_label.pack()
        self.team_bwaa_dropdown = ctk.CTkOptionMenu(self, values=bwaas, command=self.on_bwaa_change)
        self.team_bwaa_dropdown.set("None")
        self.team_bwaa_dropdown.pack(pady=(0, 10))

        # Score input
        self.score_label = ctk.CTkLabel(self, text="Score:", justify="center")
        self.score_label.pack()
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(padx=5, pady=(0, 10))

        self.decrement_button = ctk.CTkButton(self.frame, text="-", width=30, command=self.decrement)
        self.decrement_button.grid(row=0, column=0)

        self.entry = ctk.CTkEntry(self.frame, width=30, justify='center')
        self.entry.grid(row=0, column=1)
        self.entry.insert(0, "0")  # Default value

        self.increment_button = ctk.CTkButton(self.frame, text="+", width=30, command=self.increment)
        self.increment_button.grid(row=0, column=2)

        hero_path = 'static/images/bans'
        heroes = [os.path.splitext(f)[0] for f in os.listdir(hero_path) if os.path.isfile(os.path.join(hero_path, f))]
        heroes.insert(0, heroes.pop(heroes.index("None")))

        self.hero_banned_label = ctk.CTkLabel(self, text="Hero Banned:", justify="center")
        self.hero_banned_label.pack()
        self.hero_banned_dropdown = ctk.CTkOptionMenu(self, values=heroes, command=self.on_hero_change)
        self.hero_banned_dropdown.set("None")
        self.hero_banned_dropdown.pack(pady=(0, 10))

    def update_value(self, amount):
        current_value = int(self.entry.get())
        new_value = current_value + amount
        self.entry.delete(0, ctk.END)
        self.entry.insert(0, str(new_value))
        if self.score_callback:
            self.score_callback(new_value)

    def increment(self):
        self.update_value(1)

    def decrement(self):
        self.update_value(-1)

    def on_name_change(self, event):
        if self.name_callback:
            self.name_callback(self.team_name_entry.get())

    def on_hero_change(self, choice):
        if self.hero_callback:
            self.hero_callback(choice)

    def on_bwaa_change(self, choice):
        if self.bwaa_callback:
            self.bwaa_callback(choice)

    def update_imageOptions(self):
        main_dir = "bwaas/"
        child_dir = "static/images/teams/"

        # Synchronize files from the main directory to the child directory
        sync_main_to_child(main_dir, child_dir)

        bwaa_path = 'static/images/teams'
        bwaas = [os.path.splitext(f)[0] for f in os.listdir(bwaa_path) if os.path.isfile(os.path.join(bwaa_path, f))]
        bwaas.insert(0, bwaas.pop(bwaas.index("None")))
        self.team_bwaa_dropdown.configure(values=bwaas)
        self.team_bwaa_dropdown.update()

        hero_path = 'static/images/bans'
        heroes = [os.path.splitext(f)[0] for f in os.listdir(hero_path) if os.path.isfile(os.path.join(hero_path, f))]
        heroes.insert(0, heroes.pop(heroes.index("None")))
        self.hero_banned_dropdown.configure(values=heroes)
        self.hero_banned_dropdown.update()


class App(ctk.CTk):
    def __init__(self):
        self.url = "http://127.0.0.1:5000"
        super().__init__()
        self.geometry("800x400")
        self.title("Overwatch Overlay Helper")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1, 2), weight=1)

        self.team1Input = TeamInput(master=self, labelText="Team 1", score_callback=self.team1_score_updated,
                                    name_callback=self.team1_name_updated, hero_callback=self.team1_hero_updated,
                                    bwaa_callback=self.team1_bwaa_updated)
        self.team1Input.grid(row=0, column=0, padx=10, pady=10)

        self.swap_button_frame = ctk.CTkFrame(self)
        self.swap_button_frame.grid(row=0, column=1, padx=10, pady=10)
        self.swap_button = ctk.CTkButton(self.swap_button_frame, text="Swap Teams", command=self.swap_teams)
        self.swap_button.pack(pady=(0, 5))
        self.refresh_button = ctk.CTkButton(self.swap_button_frame, text="Refresh Images", command=self.refresh_images)
        self.refresh_button.pack()

        self.team2Input = TeamInput(master=self, labelText="Team 2", score_callback=self.team2_score_updated,
                                    name_callback=self.team2_name_updated, hero_callback=self.team2_hero_updated,
                                    bwaa_callback=self.team2_bwaa_updated)
        self.team2Input.grid(row=0, column=2, padx=10, pady=10)

    def team1_score_updated(self, score):
        data = {
            "teamNumber": 1,
            "teamScore": score
        }
        requests.post(self.url + "/api/updateScore", data)

    def team2_score_updated(self, score):
        data = {
            "teamNumber": 2,
            "teamScore": score
        }
        requests.post(self.url + "/api/updateScore", data)

    def team1_name_updated(self, name):
        data = {
            "teamNumber": 1,
            "teamName": name
        }
        requests.post(self.url + "/api/updateName", data)

    def team2_name_updated(self, name):
        data = {
            "teamNumber": 2,
            "teamName": name
        }
        requests.post(self.url + "/api/updateName", data)

    def team1_hero_updated(self, hero):
        data = {
            "teamNumber": 1,
            "teamBan": hero
        }
        requests.post(self.url + "/api/updateBanned", data)

    def team2_hero_updated(self, hero):
        data = {
            "teamNumber": 2,
            "teamBan": hero
        }
        requests.post(self.url + "/api/updateBanned", data)

    def team1_bwaa_updated(self, bwaa):
        data = {
            "teamNumber": 1,
            "teamBwaa": bwaa
        }
        requests.post(self.url + "/api/updateBwaa", data)

    def team2_bwaa_updated(self, bwaa):
        data = {
            "teamNumber": 2,
            "teamBwaa": bwaa
        }
        requests.post(self.url + "/api/updateBwaa", data)

    def refresh_images(self):
        self.team1Input.update_imageOptions()
        self.team2Input.update_imageOptions()

    def swap_teams(self):
        # Swap team names
        team1_name = self.team1Input.team_name_entry.get()
        team2_name = self.team2Input.team_name_entry.get()
        self.team1Input.team_name_entry.delete(0, ctk.END)
        self.team1Input.team_name_entry.insert(0, team2_name)
        self.team2Input.team_name_entry.delete(0, ctk.END)
        self.team2Input.team_name_entry.insert(0, team1_name)

        # Swap scores
        team1_score = self.team1Input.entry.get()
        team2_score = self.team2Input.entry.get()
        self.team1Input.entry.delete(0, ctk.END)
        self.team1Input.entry.insert(0, team2_score)
        self.team2Input.entry.delete(0, ctk.END)
        self.team2Input.entry.insert(0, team1_score)

        # Swap hero bans
        team1_hero = self.team1Input.hero_banned_dropdown.get()
        team2_hero = self.team2Input.hero_banned_dropdown.get()
        self.team1Input.hero_banned_dropdown.set(team2_hero)
        self.team2Input.hero_banned_dropdown.set(team1_hero)

        # Swap bwaa
        team1_bwaa = self.team1Input.team_bwaa_dropdown.get()
        team2_bwaa = self.team2Input.team_bwaa_dropdown.get()
        self.team1Input.team_bwaa_dropdown.set(team2_bwaa)
        self.team2Input.team_bwaa_dropdown.set(team1_bwaa)

        requests.get(self.url + "/api/swapTeams")


def sync_main_to_child(main_dir, child_dir):
    """
    Synchronize files from the main directory to the child directory.
    """
    # Ensure both directories exist
    os.makedirs(main_dir, exist_ok=True)
    os.makedirs(child_dir, exist_ok=True)

    # Function to copy files from source to destination
    def copy_files(src, dest):
        for filename in os.listdir(src):
            src_path = os.path.join(src, filename)
            dest_path = os.path.join(dest, filename)

            # Only copy files (skip directories)
            if os.path.isfile(src_path):
                if not os.path.exists(dest_path) or not file_contents_match(src_path, dest_path):
                    shutil.copy2(src_path, dest_path)
                    print(f"Copied {src_path} to {dest_path}")

        # Remove files in the child directory that are not in the main directory
        for filename in os.listdir(dest):
            if filename == "None.png":
                continue
            dest_path = os.path.join(dest, filename)
            src_path = os.path.join(src, filename)
            if not os.path.exists(src_path):
                os.remove(dest_path)
                print(f"Removed {dest_path}")

    # Check if two files have the same contents
    def file_contents_match(file1, file2):
        with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
            return f1.read() == f2.read()

    # Synchronize files from main to child
    copy_files(main_dir, child_dir)


if __name__ == "__main__":
    app = App()
    app.mainloop()
