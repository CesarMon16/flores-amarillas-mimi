import tkinter as tk
import math
import random
import time

class FloresAmarillasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("💛 Flores Amarillas para mi Bella Conejita Mimi 🐰")
        
        # Dimensiones y configuración de ventana
        self.width = 900
        self.height = 750
        
        # Centrar ventana en pantalla
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = max(0, (screen_w - self.width) // 2)
        y = max(0, (screen_h - self.height) // 2)
        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")
        self.root.configure(bg="#0f0c1b")
        
        # Canvas principal
        self.canvas = tk.Canvas(
            self.root, 
            width=self.width, 
            height=self.height, 
            bg="#0f0c1b", 
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Estado
        self.state = "BUTTON"  # "BUTTON", "DRAWING", "COMPLETED"
        self.anim_step = 0
        self.particles = []
        self.floating_petals = []
        self.stars = []
        self.button_pulse = 0
        
        # Definición del ramo de flores (coordenadas relativas de las flores)
        # Cada flor: (x_offset, y_offset, radius, petal_count, flower_type, delay)
        self.flower_defs = [
            {"cx": 450, "cy": 330, "r": 34, "petals": 18, "petal_len": 65, "petal_w": 22, "start_frame": 120}, # Centro principal
            {"cx": 360, "cy": 290, "r": 28, "petals": 16, "petal_len": 55, "petal_w": 18, "start_frame": 170}, # Izquierda alta
            {"cx": 540, "cy": 295, "r": 28, "petals": 16, "petal_len": 55, "petal_w": 18, "start_frame": 210}, # Derecha alta
            {"cx": 310, "cy": 370, "r": 26, "petals": 15, "petal_len": 50, "petal_w": 17, "start_frame": 250}, # Izquierda baja
            {"cx": 590, "cy": 375, "r": 26, "petals": 15, "petal_len": 50, "petal_w": 17, "start_frame": 290}, # Derecha baja
            {"cx": 450, "cy": 235, "r": 30, "petals": 17, "petal_len": 58, "petal_w": 19, "start_frame": 330}, # Arriba centro
            {"cx": 400, "cy": 395, "r": 24, "petals": 14, "petal_len": 46, "petal_w": 15, "start_frame": 370}, # Frente centro izq
            {"cx": 500, "cy": 395, "r": 24, "petals": 14, "petal_len": 46, "petal_w": 15, "start_frame": 400}, # Frente centro der
        ]
        
        # Inicializar estrellas de fondo
        for _ in range(80):
            self.stars.append({
                "x": random.randint(10, self.width - 10),
                "y": random.randint(10, self.height - 10),
                "size": random.uniform(1, 2.8),
                "phase": random.uniform(0, math.pi * 2),
                "speed": random.uniform(0.03, 0.08)
            })

        # Inicializar pétalos flotantes
        for _ in range(25):
            self.floating_petals.append({
                "x": random.randint(0, self.width),
                "y": random.randint(-self.height, 0),
                "vx": random.uniform(-0.5, 0.5),
                "vy": random.uniform(1.2, 2.5),
                "rot": random.uniform(0, 360),
                "rot_speed": random.uniform(-2, 2),
                "size": random.uniform(8, 16),
                "color": random.choice(["#FFE066", "#FFD700", "#FFCC00", "#FFF38A"])
            })

        # Eventos
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.mouse_x = self.width // 2
        self.mouse_y = self.height // 2

        # Bucle de animación (60 FPS aprox -> 16 ms)
        self.update_loop()

    def on_mouse_move(self, event):
        self.mouse_x = event.x
        self.mouse_y = event.y

    def on_click(self, event):
        if self.state == "BUTTON":
            # Verificar si el clic fue en el botón rojo
            btn_x = self.width // 2
            btn_y = self.height // 2
            dist = math.hypot(event.x - btn_x, event.y - btn_y)
            if dist <= 85:
                # Disparar fuegos/partículas y comenzar animación
                self.spawn_explosion(btn_x, btn_y)
                self.state = "DRAWING"
                self.anim_step = 0
        else:
            # En cualquier otro estado, crear chispas de corazones al hacer clic
            for _ in range(12):
                angle = random.uniform(0, math.pi * 2)
                spd = random.uniform(2, 6)
                self.particles.append({
                    "x": event.x,
                    "y": event.y,
                    "vx": math.cos(angle) * spd,
                    "vy": math.sin(angle) * spd - 1,
                    "life": 1.0,
                    "decay": random.uniform(0.02, 0.04),
                    "color": random.choice(["#FFB6C1", "#FF69B4", "#FFD700", "#FFF0F5", "#FFC0CB"]),
                    "is_heart": random.choice([True, False])
                })

    def spawn_explosion(self, x, y):
        for _ in range(60):
            angle = random.uniform(0, math.pi * 2)
            spd = random.uniform(3, 9)
            self.particles.append({
                "x": x,
                "y": y,
                "vx": math.cos(angle) * spd,
                "vy": math.sin(angle) * spd - 2,
                "life": 1.0,
                "decay": random.uniform(0.015, 0.03),
                "color": random.choice(["#FF2A6D", "#FF6584", "#FFB86C", "#FFD700", "#FF7597", "#FFFFFF"]),
                "is_heart": random.choice([True, True, False])
            })

    def update_loop(self):
        self.canvas.delete("all")
        
        # 1. Dibujar fondo con resplandor y estrellas
        self.draw_background()
        
        # 2. Manejar estados principales
        if self.state == "BUTTON":
            self.draw_start_button()
        elif self.state in ["DRAWING", "COMPLETED"]:
            self.draw_bouquet()
            if self.state == "DRAWING":
                self.anim_step += 1
                if self.anim_step > 500:
                    self.state = "COMPLETED"
            
            # Dibujar texto romántico
            if self.anim_step >= 380:
                self.draw_romantic_text()
                
            # Dibujar conejita decorativa
            if self.anim_step >= 280:
                self.draw_cute_bunny()

        # 3. Dibujar y actualizar partículas
        self.update_and_draw_particles()

        # 4. Actualizar y dibujar pétalos flotantes
        if self.state in ["DRAWING", "COMPLETED"]:
            self.update_and_draw_floating_petals()

        # Programar siguiente frame
        self.root.after(16, self.update_loop)

    def draw_background(self):
        # Gradiente simulado suave con círculos de luz ambiental
        self.canvas.create_oval(
            self.width//2 - 400, self.height//2 - 350,
            self.width//2 + 400, self.height//2 + 450,
            fill="#1c142e", outline=""
        )
        self.canvas.create_oval(
            self.width//2 - 260, 200,
            self.width//2 + 260, 600,
            fill="#271c3d", outline=""
        )
        
        # Estrellas titilantes
        for s in self.stars:
            s["phase"] += s["speed"]
            brightness = (math.sin(s["phase"]) + 1) / 2
            size = s["size"] * (0.6 + 0.4 * brightness)
            if brightness > 0.3:
                color = "#FFF8E7" if brightness > 0.7 else "#B8A9C9"
                self.canvas.create_oval(
                    s["x"] - size, s["y"] - size,
                    s["x"] + size, s["y"] + size,
                    fill=color, outline=""
                )

    def draw_start_button(self):
        self.button_pulse += 0.05
        pulse = math.sin(self.button_pulse)
        cx = self.width // 2
        cy = self.height // 2
        
        # Aura de luz radiante
        glow_r = 85 + pulse * 10
        self.canvas.create_oval(
            cx - glow_r, cy - glow_r,
            cx + glow_r, cy + glow_r,
            fill="#521124", outline=""
        )
        
        # Botón rojo dinámico con efecto de profundidad
        btn_r = 72 + pulse * 4
        # Sombra
        self.canvas.create_oval(
            cx - btn_r, cy - btn_r + 6,
            cx + btn_r, cy + btn_r + 6,
            fill="#7a091b", outline=""
        )
        # Cuerpo principal del botón rojo escarlata
        self.canvas.create_oval(
            cx - btn_r, cy - btn_r,
            cx + btn_r, cy + btn_r,
            fill="#e61c3c", outline="#ff758c", width=3
        )
        # Brillo superior
        self.canvas.create_oval(
            cx - btn_r + 14, cy - btn_r + 10,
            cx + btn_r - 14, cy - btn_r + 34,
            fill="#ff6b81", outline=""
        )

        # Icono de corazón pulsante en el botón
        heart_scale = 1.0 + pulse * 0.08
        self.draw_heart_shape(cx, cy - 8, size=24 * heart_scale, color="#ffffff")
        
        # Texto dentro del botón
        self.canvas.create_text(
            cx, cy + 28,
            text="TÓCAME",
            font=("Helvetica", 14, "bold"),
            fill="#ffffff"
        )
        
        # Mensaje de invitación exterior
        self.canvas.create_text(
            cx, cy - 140,
            text="✨ Para mi niña hermosa ✨",
            font=("Georgia", 22, "italic"),
            fill="#ffb7d5"
        )
        self.canvas.create_text(
            cx, cy + 135,
            text="Toca el corazón para abrir tu sorpresa especial 💛",
            font=("Helvetica", 13),
            fill="#eedbf5"
        )

    def draw_heart_shape(self, cx, cy, size=20, color="#ff4081"):
        # Generar puntos paramétricos de corazón
        points = []
        for i in range(0, 360, 10):
            t = math.radians(i)
            # Ecuación paramétrica clásica del corazón
            x = 16 * (math.sin(t) ** 3)
            y = -(13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t))
            points.append(cx + (x * size / 16))
            points.append(cy + (y * size / 16))
        self.canvas.create_polygon(points, fill=color, outline="")

    def draw_bouquet(self):
        f = self.anim_step
        base_x = 450
        base_y = 660
        
        # 1. TALLOS (Frames 0 - 90)
        stem_progress = min(1.0, f / 90.0)
        if stem_progress > 0:
            for i, fl in enumerate(self.flower_defs):
                target_x = fl["cx"]
                target_y = fl["cy"]
                
                # Curva cuadrática para cada tallo
                ctrl_x = (base_x + target_x) / 2 + (target_x - base_x) * 0.3
                ctrl_y = (base_y + target_y) / 2 + 30
                
                steps = 25
                points = []
                max_step = int(steps * stem_progress)
                for s in range(max_step + 1):
                    t = s / steps
                    # Bezier cuadrático
                    px = (1-t)**2 * base_x + 2*(1-t)*t * ctrl_x + t**2 * target_x
                    py = (1-t)**2 * base_y + 2*(1-t)*t * ctrl_y + t**2 * target_y
                    points.extend([px, py])
                
                if len(points) >= 4:
                    self.canvas.create_line(points, fill="#2d6a4f", width=5, smooth=True, capstyle=tk.ROUND)
                    self.canvas.create_line(points, fill="#52b788", width=2, smooth=True, capstyle=tk.ROUND)

        # 2. HOJAS VERDES (Frames 40 - 130)
        if f > 40:
            leaf_prog = min(1.0, (f - 40) / 70.0)
            leaf_coords = [
                (360, 480, -35, 1.1),
                (540, 475, 35, 1.1),
                (320, 430, -50, 0.9),
                (580, 420, 50, 0.9),
                (400, 520, -20, 0.8),
                (500, 525, 20, 0.8),
                (450, 440, 5, 1.0)
            ]
            for lx, ly, angle_deg, scale in leaf_coords:
                self.draw_leaf(lx, ly, angle_deg, scale * leaf_prog)

        # 3. ENVOLTURA DE PAPEL KRAFT / RAMO ELEGANTE (Frames 70 - 160)
        if f > 70:
            wrap_prog = min(1.0, (f - 70) / 60.0)
            if wrap_prog > 0:
                self.draw_wrapping(base_x, base_y - 80, wrap_prog)

        # 4. FLORES AMARILLAS (Frames según cada definición)
        for fl in self.flower_defs:
            if f >= fl["start_frame"]:
                flower_prog = min(1.0, (f - fl["start_frame"]) / 55.0)
                # Efecto resorte elástico (bounce) al florecer
                eased = self.ease_out_back(flower_prog)
                self.draw_sunflower(
                    fl["cx"], fl["cy"], 
                    fl["r"] * eased, 
                    fl["petals"], 
                    fl["petal_len"] * eased, 
                    fl["petal_w"] * eased,
                    flower_prog
                )

        # 5. LAZO / MOÑO ROSA PASTEL Y DORADO (Frames 150 - 220)
        if f > 150:
            bow_prog = min(1.0, (f - 150) / 50.0)
            self.draw_ribbon_bow(base_x, 565, bow_prog)

    def ease_out_back(self, x):
        c1 = 1.70158
        c3 = c1 + 1
        return 1 + c3 * math.pow(x - 1, 3) + c1 * math.pow(x - 1, 2) if x < 1 else 1.0

    def draw_leaf(self, x, y, angle_deg, scale):
        if scale <= 0.05:
            return
        rad = math.radians(angle_deg)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        
        # Puntos de la hoja
        length = 60 * scale
        width = 24 * scale
        
        raw_pts = [
            (0, 0),
            (-width * 0.5, -length * 0.4),
            (0, -length),
            (width * 0.5, -length * 0.4)
        ]
        
        pts = []
        for px, py in raw_pts:
            rx = x + (px * cos_a - py * sin_a)
            ry = y + (px * sin_a + py * cos_a)
            pts.extend([rx, ry])
            
        self.canvas.create_polygon(pts, fill="#2d6a4f", outline="#1b4332", width=1, smooth=True)
        # Nervadura central
        tip_x = x + (0 * cos_a - (-length * 0.85) * sin_a)
        tip_y = y + (0 * sin_a + (-length * 0.85) * cos_a)
        self.canvas.create_line(x, y, tip_x, tip_y, fill="#74c69d", width=1.5)

    def draw_wrapping(self, cx, cy, prog):
        # Envoltura estilo papel bouquet vintage y cono estético
        w_top = 220 * prog
        w_bot = 40 * prog
        h = 190 * prog
        
        # Capa trasera de papel kraft
        pts_back = [
            cx - w_top * 1.05, cy - h * 0.4,
            cx, cy - h * 0.1,
            cx + w_top * 1.05, cy - h * 0.4,
            cx + w_bot, cy + h * 0.8,
            cx - w_bot, cy + h * 0.8
        ]
        self.canvas.create_polygon(pts_back, fill="#f2e2ce", outline="#d0bba2", width=2)
        
        # Capa frontal doblada
        pts_fold1 = [
            cx - w_top, cy - h * 0.35,
            cx + 20, cy + h * 0.75,
            cx - w_bot, cy + h * 0.8
        ]
        self.canvas.create_polygon(pts_fold1, fill="#e8d3ba", outline="#cbb194", width=1.5)
        
        pts_fold2 = [
            cx + w_top, cy - h * 0.35,
            cx - 20, cy + h * 0.75,
            cx + w_bot, cy + h * 0.8
        ]
        self.canvas.create_polygon(pts_fold2, fill="#f8ece0", outline="#cbb194", width=1.5)

    def draw_ribbon_bow(self, cx, cy, prog):
        size = 28 * prog
        # Nudo central
        self.canvas.create_oval(
            cx - size * 0.4, cy - size * 0.4,
            cx + size * 0.4, cy + size * 0.4,
            fill="#ff9ebb", outline="#ff7597", width=2
        )
        # Alas del lazo (izquierda y derecha)
        self.canvas.create_polygon([
            cx - size * 0.3, cy,
            cx - size * 1.6, cy - size * 0.8,
            cx - size * 1.8, cy + size * 0.6,
            cx - size * 0.3, cy
        ], fill="#ffb7d5", outline="#ff7597", width=1.5, smooth=True)
        
        self.canvas.create_polygon([
            cx + size * 0.3, cy,
            cx + size * 1.6, cy - size * 0.8,
            cx + size * 1.8, cy + size * 0.6,
            cx + size * 0.3, cy
        ], fill="#ffb7d5", outline="#ff7597", width=1.5, smooth=True)

        # Cintas colgantes
        self.canvas.create_line(
            cx - 5, cy + 5,
            cx - size * 0.9, cy + size * 1.8,
            fill="#ff9ebb", width=4, smooth=True
        )
        self.canvas.create_line(
            cx + 5, cy + 5,
            cx + size * 0.9, cy + size * 1.8,
            fill="#ff9ebb", width=4, smooth=True
        )

    def draw_sunflower(self, cx, cy, core_r, petals, petal_len, petal_w, prog):
        if prog <= 0.01:
            return
            
        # 1. Resplandor dorado tenue detrás de cada flor
        glow_rad = (core_r + petal_len) * 1.15
        self.canvas.create_oval(
            cx - glow_rad, cy - glow_rad,
            cx + glow_rad, cy + glow_rad,
            fill="#2c2016", outline=""
        )

        # 2. Capa trasera de pétalos (anaranjado dorado cálido)
        angle_step = (math.pi * 2) / petals
        half_step = angle_step / 2
        for i in range(petals):
            theta = i * angle_step + half_step
            self.draw_single_petal(cx, cy, theta, core_r * 0.8, petal_len * 0.95, petal_w * 0.9, "#FFA000", "#FF8F00")

        # 3. Capa delantera de pétalos (amarillo brillante vibrante)
        for i in range(petals):
            theta = i * angle_step
            self.draw_single_petal(cx, cy, theta, core_r * 0.85, petal_len, petal_w, "#FFD700", "#FFEB3B")

        # 4. Centro del girasol (disco con textura de espiral de semillas)
        if core_r > 3:
            # Sombra/Borde oscuro
            self.canvas.create_oval(
                cx - core_r - 2, cy - core_r - 2,
                cx + core_r + 2, cy + core_r + 2,
                fill="#3E2723", outline="#5D4037", width=2
            )
            # Centro cálido
            self.canvas.create_oval(
                cx - core_r, cy - core_r,
                cx + core_r, cy + core_r,
                fill="#4E342E", outline=""
            )
            
            # Anillo interior dorado de semillas
            inner_r = core_r * 0.65
            self.canvas.create_oval(
                cx - inner_r, cy - inner_r,
                cx + inner_r, cy + inner_r,
                fill="#3E2723", outline="#8D6E63", width=1
            )
            
            # Pequeñas semillas doradas/cafés
            seed_count = int(18 * prog)
            for s in range(seed_count):
                stheta = s * 2.39996  # Golden ratio angle
                srad = (core_r * 0.8) * math.sqrt(s / 18.0)
                sx = cx + math.cos(stheta) * srad
                sy = cy + math.sin(stheta) * srad
                self.canvas.create_oval(
                    sx - 1.5, sy - 1.5,
                    sx + 1.5, sy + 1.5,
                    fill="#FFB300", outline=""
                )

    def draw_single_petal(self, cx, cy, angle, start_dist, length, width, color1, color2):
        # Punta del pétalo
        tip_x = cx + math.cos(angle) * (start_dist + length)
        tip_y = cy + math.sin(angle) * (start_dist + length)
        
        # Base del pétalo
        base_x = cx + math.cos(angle) * start_dist
        base_y = cy + math.sin(angle) * start_dist
        
        # Puntos de control perpendiculares para hacer la forma ovalada suave
        perp_angle = angle + math.pi / 2
        mid_dist = start_dist + length * 0.5
        mid_x = cx + math.cos(angle) * mid_dist
        mid_y = cy + math.sin(angle) * mid_dist
        
        p1_x = mid_x + math.cos(perp_angle) * (width / 2)
        p1_y = mid_y + math.sin(perp_angle) * (width / 2)
        
        p2_x = mid_x - math.cos(perp_angle) * (width / 2)
        p2_y = mid_y - math.sin(perp_angle) * (width / 2)
        
        # Polígono de pétalo
        pts = [base_x, base_y, p1_x, p1_y, tip_x, tip_y, p2_x, p2_y]
        self.canvas.create_polygon(pts, fill=color1, outline=color2, width=1.2, smooth=True)

    def draw_cute_bunny(self):
        # Dibujo de una tierna conejita junto al ramo
        bx = 270
        by = 590
        
        # Cabeza
        self.canvas.create_oval(bx - 26, by - 26, bx + 26, by + 26, fill="#FFF5F7", outline="#FFB6C1", width=2)
        
        # Orejitas de conejito
        # Oreja izq
        self.canvas.create_oval(bx - 22, by - 65, bx - 6, by - 15, fill="#FFF5F7", outline="#FFB6C1", width=2)
        self.canvas.create_oval(bx - 19, by - 56, bx - 9, by - 22, fill="#FFB7D5", outline="")
        
        # Oreja der (ligeramente inclinada)
        self.canvas.create_oval(bx + 6, by - 65, bx + 22, by - 15, fill="#FFF5F7", outline="#FFB6C1", width=2)
        self.canvas.create_oval(bx + 9, by - 56, bx + 19, by - 22, fill="#FFB7D5", outline="")
        
        # Ojos felices (curvas cerradas tipo ^ ^)
        self.canvas.create_arc(bx - 16, by - 12, bx - 6, by + 2, start=0, extent=180, style=tk.ARC, width=2.5, outline="#4A2835")
        self.canvas.create_arc(bx + 6, by - 12, bx + 16, by + 2, start=0, extent=180, style=tk.ARC, width=2.5, outline="#4A2835")
        
        # Mejillas rosaditas
        self.canvas.create_oval(bx - 20, by + 2, bx - 10, by + 10, fill="#FF9EBB", outline="")
        self.canvas.create_oval(bx + 10, by + 2, bx + 20, by + 10, fill="#FF9EBB", outline="")
        
        # Naricita de corazón y boquita
        self.draw_heart_shape(bx, by + 3, size=5, color="#FF6584")
        self.canvas.create_arc(bx - 7, by + 5, bx, by + 13, start=180, extent=180, style=tk.ARC, width=1.5, outline="#4A2835")
        self.canvas.create_arc(bx, by + 5, bx + 7, by + 13, start=180, extent=180, style=tk.ARC, width=1.5, outline="#4A2835")
        
        # Manitas sosteniendo un corazoncito amarillo
        self.canvas.create_oval(bx - 20, by + 18, bx - 8, by + 30, fill="#FFF5F7", outline="#FFB6C1", width=1.5)
        self.canvas.create_oval(bx + 8, by + 18, bx + 20, by + 30, fill="#FFF5F7", outline="#FFB6C1", width=1.5)
        self.draw_heart_shape(bx, by + 25, size=14, color="#FFD700")

    def draw_romantic_text(self):
        f = self.anim_step
        text_prog = min(1.0, (f - 380) / 60.0)
        
        if text_prog <= 0:
            return
            
        cx = self.width // 2
        y_top = 80
        
        # Efecto de latido suave en el texto
        pulse = math.sin(time.time() * 3) * 0.05 + 1.0
        
        # 1. Resplandor / Sombra suave del texto en rosa pastel
        glow_color = "#631d3d"
        main_color = "#FFB7D5"  # Rosa Pastel Solicitado
        white_accent = "#FFF0F5"
        
        # Texto Principal solicitado:
        # "Feliz 21 de Septiembre, mi bella conejita mimi, te amo"
        
        # Línea 1: "✨ Feliz 21 de Septiembre ✨"
        self.canvas.create_text(
            cx + 2, y_top + 2,
            text="✨ Feliz 21 de Septiembre ✨",
            font=("Georgia", 24, "bold"),
            fill=glow_color
        )
        self.canvas.create_text(
            cx, y_top,
            text="✨ Feliz 21 de Septiembre ✨",
            font=("Georgia", 24, "bold"),
            fill="#FFD700"  # Toque dorado festivo
        )
        
        # Línea 2: "mi bella conejita mimi,"
        self.canvas.create_text(
            cx + 2, y_top + 46,
            text="Mi bella conejita Mimi,",
            font=("Segoe Script", 23, "bold"),
            fill=glow_color
        )
        self.canvas.create_text(
            cx, y_top + 44,
            text="Mi bella conejita Mimi,",
            font=("Segoe Script", 23, "bold"),
            fill=main_color  # Rosa pastel
        )

        # Línea 3: "Te Amo 💛🐰"
        self.canvas.create_text(
            cx + 2, y_top + 92,
            text="¡Te amo con todo mi corazón! 💛🐰",
            font=("Georgia", 22, "italic bold"),
            fill=glow_color
        )
        self.canvas.create_text(
            cx, y_top + 90,
            text="¡Te amo con todo mi corazón! 💛🐰",
            font=("Georgia", 22, "italic bold"),
            fill=white_accent
        )

        # Corazones flotantes alrededor del texto
        h_time = time.time() * 2
        self.draw_heart_shape(cx - 240 + math.sin(h_time) * 8, y_top + 40, size=16, color="#FFB7D5")
        self.draw_heart_shape(cx + 240 + math.cos(h_time) * 8, y_top + 40, size=16, color="#FFB7D5")
        self.draw_heart_shape(cx - 180, y_top + 90 + math.sin(h_time+1)*6, size=13, color="#FFD700")
        self.draw_heart_shape(cx + 180, y_top + 90 + math.cos(h_time+1)*6, size=13, color="#FFD700")

    def update_and_draw_particles(self):
        surviving = []
        for p in self.particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["life"] -= p["decay"]
            
            if p["life"] > 0:
                surviving.append(p)
                size = max(1.0, 10.0 * p["life"])
                if p.get("is_heart", False):
                    self.draw_heart_shape(p["x"], p["y"], size=size * 1.5, color=p["color"])
                else:
                    self.canvas.create_oval(
                        p["x"] - size/2, p["y"] - size/2,
                        p["x"] + size/2, p["y"] + size/2,
                        fill=p["color"], outline=""
                    )
        self.particles = surviving

    def update_and_draw_floating_petals(self):
        for pet in self.floating_petals:
            pet["y"] += pet["vy"]
            pet["x"] += pet["vx"] + math.sin(time.time() * 2 + pet["y"] * 0.01) * 0.8
            pet["rot"] += pet["rot_speed"]
            
            # Reciclar pétalo al salir de pantalla
            if pet["y"] > self.height + 20:
                pet["y"] = random.randint(-40, -10)
                pet["x"] = random.randint(0, self.width)
                
            # Dibujar pétalo individual suave
            px, py = pet["x"], pet["y"]
            sz = pet["size"]
            rad = math.radians(pet["rot"])
            
            # Dibujar elipse rotada como pétalo
            p1 = (px - sz * 0.5 * math.cos(rad), py - sz * 0.8 * math.sin(rad))
            p2 = (px + sz * 0.5 * math.cos(rad), py + sz * 0.8 * math.sin(rad))
            self.canvas.create_oval(
                p1[0], p1[1], p2[0] + sz, p2[1] + sz * 0.6,
                fill=pet["color"], outline="#F59E0B", width=0.5
            )

if __name__ == "__main__":
    root = tk.Tk()
    # Icono y configuración de DPI para nitidez en Windows
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass
        
    app = FloresAmarillasApp(root)
    root.mainloop()
