import tkinter as tk
from tkinter import ttk
import time

class HanoiBitwiseVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualiseur Bitwise - Tour de Hanoï")
        self.root.geometry("1100x700")
        self.root.configure(bg="#1a1d21")

        self.n = 3
        self.rods = [[], [], []]
        self.disk_positions = {}
        self.current_move = 0
        self.total_moves = 0
        self.auto_playing = False
        self.animation_speed = 0.5  # secondes

        self.setup_ui()
        self.reset_game()

    def setup_ui(self):
        # Style sombre
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", foreground="white", background="#1a1d21", font=("Arial", 11))
        style.configure("TButton", foreground="white", background="#2a2e35", font=("Arial", 10, "bold"))
        style.configure("TFrame", background="#1a1d21")
        style.configure("TEntry", fieldbackground="#2a2e35", foreground="white")

        # --- Panneau de Visualisation (Gauche) ---
        viz_frame = ttk.Frame(self.root, padding=10)
        viz_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Label(viz_frame, text="Bitwise Tower of Hanoï Visualizer", font=("Arial", 16, "bold"), foreground="#00cccc").pack(pady=10)

        # Zone de dessin (Canvas) pour les tours et disques
        self.canvas = tk.Canvas(viz_frame, width=700, height=450, bg="white", highlightthickness=0)
        self.canvas.pack(pady=10)
        self.draw_base_rods()

        # Compteur de coups
        self.move_label = ttk.Label(viz_frame, text="COUP: 0 / 0 (n=3)", font=("Arial", 22, "bold"), foreground="white")
        self.move_label.pack(pady=20)

        # Timeline
        timeline_frame = ttk.Frame(viz_frame)
        timeline_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.timeline_slider = ttk.Scale(timeline_frame, from_=0, to=7, orient=tk.HORIZONTAL, command=self.on_timeline_scroll)
        self.timeline_slider.pack(fill=tk.X)
        self.time_labels_frame = ttk.Frame(timeline_frame)
        self.time_labels_frame.pack(fill=tk.X)

        # --- Panneau de Contrôles & Analyse (Droite) ---
        ctrl_frame = ttk.Frame(self.root, padding=15, relief="solid", borderwidth=1)
        ctrl_frame.pack(side=tk.RIGHT, fill=tk.Y)
        ttk.Label(ctrl_frame, text="Contrôles & Analyse", font=("Arial", 14, "bold"), foreground="white").pack(pady=10)

        # 1. Configuration
        ttk.Label(ctrl_frame, text="1. Configuration", foreground="#00aaaa", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(15, 5))
        ttk.Label(ctrl_frame, text="NOMBRE DE DISQUES (n)").pack(anchor=tk.W)
        self.n_slider = ttk.Scale(ctrl_frame, from_=1, to=7, orient=tk.HORIZONTAL, command=self.on_n_change)
        self.n_slider.set(3)
        self.n_slider.pack(fill=tk.X, pady=(0, 10))

        # 2. Navigation
        ttk.Label(ctrl_frame, text="2. Navigation", foreground="#00aaaa", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(15, 5))
        nav_buttons = ttk.Frame(ctrl_frame)
        nav_buttons.pack(pady=5)
        self.btn_play = ttk.Button(nav_buttons, text="▶/⏸", width=5, command=self.toggle_autoplay)
        self.btn_play.pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_buttons, text="⏪", width=5, command=self.prev_move).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_buttons, text="⏩", width=5, command=self.next_move).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_buttons, text="🔄", width=5, command=self.reset_game).pack(side=tk.LEFT, padx=2)

        ttk.Label(ctrl_frame, text="VITESSE DE L'ANIMATION").pack(anchor=tk.W, pady=(10, 0))
        self.speed_slider = ttk.Scale(ctrl_frame, from_=0.1, to=2.0, orient=tk.HORIZONTAL, command=self.on_speed_change)
        self.speed_slider.set(0.5)
        self.speed_slider.pack(fill=tk.X)

        # 3. Algorithme Bitwise
        ttk.Label(ctrl_frame, text="3. Algorithme Bitwise", foreground="#00aaaa", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(20, 5))
        
        self.ana_disk = ttk.Label(ctrl_frame, text="Niveau (disk): -", foreground="white", wraplength=350, justify=tk.LEFT)
        self.ana_disk.pack(anchor=tk.W, pady=2)
        
        self.ana_dir = ttk.Label(ctrl_frame, text="Direction: -", foreground="white", wraplength=350, justify=tk.LEFT)
        self.ana_dir.pack(anchor=tk.W, pady=2)

        self.ana_move = ttk.Label(ctrl_frame, text="Mouvement: -", foreground="white", wraplength=350, justify=tk.LEFT)
        self.ana_move.pack(anchor=tk.W, pady=2)

        # 4. Historique
        ttk.Label(ctrl_frame, text="Historique des États", foreground="#00aaaa", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(20, 5))
        self.history_text = tk.Text(ctrl_frame, height=8, width=40, bg="#101215", fg="#a0a0a0", font=("Consolas", 10), state=tk.DISABLED)
        self.history_text.pack(pady=5)

    # --- Logique Visuelle ---
    def draw_base_rods(self):
        self.canvas.delete("rod")
        rw, rh = 12, 350
        y_base = 400
        for i in range(3):
            x = 150 + i * 200
            self.canvas.create_rectangle(x-rw/2, y_base-rh, x+rw/2, y_base, fill="#c0c0c0", outline="#a0a0a0", tags="rod")
            ttk.Label(self.root, text=f"ROD {i}", background="white", foreground="black", font=("Arial", 10, "bold")).place(x=x+100, y=465, anchor=tk.CENTER)

    def draw_disks(self):
        self.canvas.delete("disk")
        colors = ["#ffd700", "#32cd32", "#4169e1", "#ff4500", "#9370db", "#8b4513", "#ff1493"]
        y_base = 400
        disk_height = 30
        
        for r_idx in range(3):
            x_rod = 150 + r_idx * 200
            for d_idx, disk_size in enumerate(self.rods[r_idx]):
                dw = 40 + disk_size * 25
                x1 = x_rod - dw/2
                y1 = y_base - (d_idx + 1) * disk_height
                x2 = x_rod + dw/2
                y2 = y_base - d_idx * disk_height
                
                color = colors[(disk_size-1) % len(colors)]
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#202020", width=2, tags="disk")
                # Optionnel: numéro du disque
                self.canvas.create_text(x_rod, (y1+y2)/2, text=str(disk_size), fill="white", font=("Arial", 10, "bold"), tags="disk")

    # --- Logique Hanoï Bitwise ---
    def reset_game(self):
        self.auto_playing = False
        self.n = int(self.n_slider.get())
        self.total_moves = (1 << self.n) - 1
        self.rods = [list(range(self.n, 0, -1)), [], []]
        self.disk_positions = {disk: 0 for disk in range(1, self.n + 1)}
        self.current_move = 0
        
        self.timeline_slider.configure(to=self.total_moves)
        self.timeline_slider.set(0)
        self.update_ui_state()
        self.update_analysis("-", "-", "-")
        self.update_history("", clear=True)

    def perform_move(self, move_num):
        """Exécute la logique BITWISE pour un coup donné."""
        # 1. Identifier le disque (LSB de move_num)
        disk = (move_num & -move_num).bit_length()
        source = self.disk_positions[disk]

        # 2. Direction
        if (self.n - disk) % 2 == 0:
            direction = 1  # Horaire
            dir_text = f"Disk {disk} is ({self.n}-{disk}) % 2 == 0 (PAIRE) -> DIRECTION HORAIRE"
        else:
            direction = 2  # Anti-horaire
            dir_text = f"Disk {disk} is ({self.n}-{disk}) % 2 == 1 (IMPAIRE) -> DIRECTION ANTI-HORAIRE"

        target = (source + direction) % 3

        # 3. Déplacement
        self.rods[source].pop()
        self.rods[target].append(disk)
        self.disk_positions[disk] = target

        # Mise à jour analyse
        disk_analysis = f"Niveau (disk): disk = (move & -move).bit_length()\nMove {move_num} ({bin(move_num)[2:].zfill(self.n)}₂). Highlight Disk {disk}"
        mv_text = f"Déplacer Disque {disk} de ROD {source} à ROD {target}"
        self.update_analysis(disk_analysis, dir_text, mv_text)

        # Mise à jour historique
        state_str = f"{self.rods[0]} {self.rods[1]} {self.rods[2]}"
        self.update_history(state_str)

    def next_move(self):
        if self.current_move < self.total_moves:
            self.current_move += 1
            self.perform_move(self.current_move)
            self.update_ui_state()
        else:
            self.auto_playing = False

    def prev_move(self):
        # Pour revenir en arrière simplement dans cette démo, on reset et rejoue
        if self.current_move > 0:
            target_move = self.current_move - 1
            self.reset_game()
            for _ in range(target_move):
                self.next_move()

    def update_ui_state(self):
        self.draw_disks()
        self.move_label.configure(text=f"COUP: {self.current_move} / {self.total_moves} (n={self.n})")
        self.timeline_slider.set(self.current_move)

    def update_analysis(self, disk_raw, dir_raw, mv_raw):
        self.ana_disk.configure(text=disk_raw)
        self.ana_dir.configure(text=dir_raw)
        self.ana_move.configure(text=mv_raw)

    def update_history(self, state_str, clear=False):
        self.history_text.configure(state=tk.NORMAL)
        if clear:
            self.history_text.delete('1.0', tk.END)
            # État initial
            self.history_text.insert(tk.END, f"{list(range(self.n, 0, -1))} [] []\n")
        else:
            self.history_text.insert(tk.END, state_str + "\n")
            self.history_text.see(tk.END) # Scroll automatique
        self.history_text.configure(state=tk.DISABLED)

    # --- Handlers d'événements ---
    def on_n_change(self, val):
        if not self.auto_playing:
            self.reset_game()

    def on_speed_change(self, val):
        self.animation_speed = float(val)

    def on_timeline_scroll(self, val):
        if not self.auto_playing:
            target_move = int(float(val))
            if target_move != self.current_move:
                if target_move > self.current_move:
                    # Avancer
                    for _ in range(target_move - self.current_move):
                        self.next_move()
                else:
                    # Reculer (reset + replay)
                    self.reset_game()
                    for _ in range(target_move):
                        self.next_move()

    def toggle_autoplay(self):
        self.auto_playing = not self.auto_playing
        if self.auto_playing:
            self.play_loop()

    def play_loop(self):
        if self.auto_playing and self.current_move < self.total_moves:
            self.next_move()
            # Planifie le prochain coup
            self.root.after(int(self.animation_speed * 1000), self.play_loop)
        else:
            self.auto_playing = False

if __name__ == "__main__":
    root = tk.Tk()
    app = HanoiBitwiseVisualizer(root)
    root.mainloop()