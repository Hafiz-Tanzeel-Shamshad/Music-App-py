import tkinter as tk
from tkinter import filedialog, ttk
import pygame
import os

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("600x400")

        # Initialize Pygame mixer
        pygame.mixer.init()

        # Create variables
        self.music_file = None
        self.paused = False
        self.volume = tk.DoubleVar()

        # Create control frame
        self.control_frame = tk.Frame(self.root, pady=20)
        self.control_frame.pack()

        # Create volume frame
        self.volume_frame = tk.Frame(self.root, pady=10)
        self.volume_frame.pack()

        # Create song info frame
        self.info_frame = tk.Frame(self.root, pady=10)
        self.info_frame.pack()

        # Create playlist frame
        self.playlist_frame = tk.Frame(self.root, pady=10)
        self.playlist_frame.pack()

        # Create progress frame
        self.progress_frame = tk.Frame(self.root, pady=10)
        self.progress_frame.pack()

        # Create buttons
        self.load_button = tk.Button(self.control_frame, text="Load", command=self.load_music, padx=10, pady=5)
        self.load_button.grid(row=0, column=0, padx=10)

        self.play_button = tk.Button(self.control_frame, text="Play", command=self.play_music, padx=10, pady=5)
        self.play_button.grid(row=0, column=1, padx=10)

        self.pause_button = tk.Button(self.control_frame, text="Pause", command=self.pause_music, padx=10, pady=5)
        self.pause_button.grid(row=0, column=2, padx=10)

        self.stop_button = tk.Button(self.control_frame, text="Stop", command=self.stop_music, padx=10, pady=5)
        self.stop_button.grid(row=0, column=3, padx=10)

        # Volume slider
        self.volume_label = tk.Label(self.volume_frame, text="Volume", padx=10)
        self.volume_label.pack(side=tk.LEFT)

        self.volume_slider = ttk.Scale(self.volume_frame, from_=0, to=1, orient=tk.HORIZONTAL, variable=self.volume, command=self.set_volume)
        self.volume_slider.pack(fill=tk.X, padx=10, pady=5)
        self.volume_slider.set(0.5)  # Set initial volume to 50%

        # Song information labels
        self.song_label = tk.Label(self.info_frame, text="Song: ", padx=10)
        self.song_label.grid(row=0, column=0, sticky="w")

        self.artist_label = tk.Label(self.info_frame, text="Artist: ", padx=10)
        self.artist_label.grid(row=1, column=0, sticky="w")

        # Playlist
        self.playlist_label = tk.Label(self.playlist_frame, text="Playlist:")
        self.playlist_label.pack()

        self.playlist = tk.Listbox(self.playlist_frame, selectmode=tk.SINGLE, height=10, width=70)
        self.playlist.pack(pady=5)

        # Progress bar
        self.progress_bar = ttk.Progressbar(self.progress_frame, orient=tk.HORIZONTAL, mode='determinate')
        self.progress_bar.pack(fill=tk.X, padx=10, pady=5)

        # Populate playlist with example songs
        self.populate_playlist()

        # Update song info initially
        self.update_song_info()

        # Update progress bar
        self.update_progress_bar()

        # Update progress bar every second
        self.root.after(1000, self.update_progress_bar)

    def load_music(self):
        self.music_file = filedialog.askopenfilename(filetypes=(("Audio Files", "*.mp3;*.wav"),))
        if self.music_file:
            self.playlist.insert(tk.END, os.path.basename(self.music_file))
            pygame.mixer.music.load(self.music_file)
            self.update_song_info()
            self.root.title(f"Music Player - {os.path.basename(self.music_file)}")

    def play_music(self):
        if self.music_file:
            if self.paused:
                pygame.mixer.music.unpause()
                self.paused = False
            else:
                pygame.mixer.music.play()
                self.paused = False

    def pause_music(self):
        if pygame.mixer.music.get_busy() and not self.paused:
            pygame.mixer.music.pause()
            self.paused = True

    def stop_music(self):
        pygame.mixer.music.stop()

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume))

    def populate_playlist(self):
        # Example function to populate playlist with some sample songs
        self.playlist.insert(tk.END, "Song 1")
        self.playlist.insert(tk.END, "Song 2")
        self.playlist.insert(tk.END, "Song 3")

    def update_song_info(self):
        # Update song information labels
        if self.music_file:
            file_name = os.path.basename(self.music_file)
            self.song_label.config(text=f"Song: {file_name}")

            # Example: Extract artist name from file name
            artist_name = "Unknown Artist"
            if "-" in file_name:
                artist_name = file_name.split("-")[0].strip()
            self.artist_label.config(text=f"Artist: {artist_name}")

    def update_progress_bar(self):
        # Update progress bar based on music playback
        if self.music_file:
            # Length of the music in seconds
            music_length = pygame.mixer.Sound(self.music_file).get_length()

            # Current position of playback
            current_time = pygame.mixer.music.get_pos() / 1000  # in seconds

            # Calculate percentage progress
            progress = (current_time / music_length) * 100

            # Update progress bar
            self.progress_bar['value'] = progress

            # Update every second
            self.root.after(1000, self.update_progress_bar)

# Main function to start the application
if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()
