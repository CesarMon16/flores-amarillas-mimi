// Flores Amarillas para Mimi - Core Animation & Audio Logic

document.addEventListener('DOMContentLoaded', () => {
  // ELEMENTOS DEL DOM
  const introScreen = document.getElementById('intro-screen');
  const flowerScreen = document.getElementById('flower-screen');
  const startBtn = document.getElementById('start-btn');
  const bgCanvas = document.getElementById('bg-canvas');
  const flowerCanvas = document.getElementById('flower-canvas');
  const letterToggleBtn = document.getElementById('letter-toggle-btn');
  const closeLetterBtn = document.getElementById('close-letter-btn');
  const letterModal = document.getElementById('letter-modal');
  const musicToggleBtn = document.getElementById('music-toggle-btn');
  const musicText = document.getElementById('music-text');
  const bunnyCompanion = document.getElementById('bunny-companion');

  const bgCtx = bgCanvas.getContext('2d');
  const flCtx = flowerCanvas.getContext('2d');

  // REDIMENSIONADO DE CANVAS
  function resizeCanvas() {
    bgCanvas.width = window.innerWidth;
    bgCanvas.height = window.innerHeight;
  }
  window.addEventListener('resize', resizeCanvas);
  resizeCanvas();

  // 1. SISTEMA DE PARTÍCULAS DE FONDO Y PÉTALOS FLOTANTES
  const stars = [];
  const floatingPetals = [];
  const clickHearts = [];

  // Crear estrellas
  for (let i = 0; i < 90; i++) {
    stars.push({
      x: Math.random() * window.innerWidth,
      y: Math.random() * window.innerHeight,
      radius: Math.random() * 1.6 + 0.5,
      alpha: Math.random(),
      speed: Math.random() * 0.02 + 0.01
    });
  }

  // Crear pétalos
  for (let i = 0; i < 30; i++) {
    floatingPetals.push({
      x: Math.random() * window.innerWidth,
      y: Math.random() * window.innerHeight,
      size: Math.random() * 12 + 8,
      speedX: (Math.random() - 0.5) * 1.2,
      speedY: Math.random() * 1.5 + 1.0,
      rot: Math.random() * 360,
      rotSpeed: (Math.random() - 0.5) * 2.5,
      color: ['#FFD700', '#FFE066', '#FFCC00', '#FFF38A', '#FFB7D5'][Math.floor(Math.random() * 5)]
    });
  }

  function renderBackground() {
    bgCtx.clearRect(0, 0, bgCanvas.width, bgCanvas.height);

    // Dibujar estrellas titilantes
    for (let s of stars) {
      s.alpha += s.speed;
      let opacity = (Math.sin(s.alpha) + 1) / 2;
      bgCtx.fillStyle = `rgba(255, 248, 231, ${opacity * 0.8})`;
      bgCtx.beginPath();
      bgCtx.arc(s.x, s.y, s.radius, 0, Math.PI * 2);
      bgCtx.fill();
    }

    // Dibujar pétalos cayendo suavemente
    for (let p of floatingPetals) {
      p.y += p.speedY;
      p.x += p.speedX + Math.sin(p.y * 0.01) * 0.5;
      p.rot += p.rotSpeed;

      if (p.y > bgCanvas.height + 20) {
        p.y = -20;
        p.x = Math.random() * bgCanvas.width;
      }

      bgCtx.save();
      bgCtx.translate(p.x, p.y);
      bgCtx.rotate((p.rot * Math.PI) / 180);
      bgCtx.fillStyle = p.color;
      bgCtx.beginPath();
      bgCtx.ellipse(0, 0, p.size * 0.5, p.size, 0, 0, Math.PI * 2);
      bgCtx.fill();
      bgCtx.restore();
    }

    // Dibujar corazones al hacer clic
    for (let i = clickHearts.length - 1; i >= 0; i--) {
      let h = clickHearts[i];
      h.x += h.vx;
      h.y += h.vy;
      h.life -= h.decay;
      if (h.life <= 0) {
        clickHearts.splice(i, 1);
        continue;
      }

      bgCtx.save();
      bgCtx.translate(h.x, h.y);
      bgCtx.scale(h.size * h.life, h.size * h.life);
      bgCtx.fillStyle = h.color;
      bgCtx.beginPath();
      // Dibujar forma de corazón
      bgCtx.moveTo(0, 0);
      bgCtx.bezierCurveTo(-5, -7, -12, 0, 0, 10);
      bgCtx.bezierCurveTo(12, 0, 5, -7, 0, 0);
      bgCtx.fill();
      bgCtx.restore();
    }

    requestAnimationFrame(renderBackground);
  }
  renderBackground();

  // Efecto de corazones interactivos al tocar cualquier lugar
  window.addEventListener('pointerdown', (e) => {
    for (let i = 0; i < 8; i++) {
      let angle = Math.random() * Math.PI * 2;
      let spd = Math.random() * 4 + 2;
      clickHearts.push({
        x: e.clientX,
        y: e.clientY,
        vx: Math.cos(angle) * spd,
        vy: Math.sin(angle) * spd - 1,
        life: 1.0,
        decay: Math.random() * 0.02 + 0.015,
        size: Math.random() * 0.8 + 0.6,
        color: ['#FF69B4', '#FFB7D5', '#FFD700', '#FF1493', '#FFF0F5'][Math.floor(Math.random() * 5)]
      });
    }
  });

  // 2. GENERADOR DE MÚSICA ROMÁNTICA SINTETIZADA (Web Audio API)
  let audioCtx = null;
  let isMusicPlaying = false;
  let melodyInterval = null;

  function initAudio() {
    if (!audioCtx) {
      audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
    if (audioCtx.state === 'suspended') {
      audioCtx.resume();
    }
  }

  function playTone(freq, time, duration, type = 'sine', gainVal = 0.12) {
    if (!audioCtx) return;
    const osc = audioCtx.createOscillator();
    const gainNode = audioCtx.createGain();

    osc.type = type;
    osc.frequency.setValueAtTime(freq, time);

    gainNode.gain.setValueAtTime(0.001, time);
    gainNode.gain.exponentialRampToValueAtTime(gainVal, time + 0.05);
    gainNode.gain.exponentialRampToValueAtTime(0.0001, time + duration);

    osc.connect(gainNode);
    gainNode.connect(audioCtx.destination);

    osc.start(time);
    osc.stop(time + duration);
  }

  // Melodía romántica en escala pentatónica cálida (C4, D4, E4, G4, A4, C5, D5, E5)
  const notes = [
    261.63, 293.66, 329.63, 392.00, 440.00, 523.25, 587.33, 659.25,
    523.25, 440.00, 392.00, 329.63, 440.00, 523.25, 659.25, 783.99
  ];

  function startRomanticMelody() {
    initAudio();
    isMusicPlaying = true;
    musicText.textContent = 'Música: Sonando 💖';

    let step = 0;
    melodyInterval = setInterval(() => {
      if (!isMusicPlaying) return;
      const now = audioCtx.currentTime;
      const baseFreq = notes[step % notes.length];
      
      // Tono de piano/arpa suave
      playTone(baseFreq, now, 1.2, 'sine', 0.15);
      // Armónico sutil
      playTone(baseFreq * 2, now + 0.08, 0.8, 'triangle', 0.05);
      
      // Acorde suave de fondo cada 4 notas
      if (step % 4 === 0) {
        playTone(baseFreq * 0.5, now, 2.0, 'sine', 0.1);
      }

      step++;
    }, 450);
  }

  function stopRomanticMelody() {
    isMusicPlaying = false;
    clearInterval(melodyInterval);
    musicText.textContent = 'Música: Pausada 🎵';
  }

  musicToggleBtn.addEventListener('click', () => {
    if (isMusicPlaying) {
      stopRomanticMelody();
    } else {
      startRomanticMelody();
    }
  });

  // 3. RENDERIZADO VECTORIAL DEL RAMO DE FLORES AMARILLAS
  let bouquetAnimFrame = 0;
  const flowerDefinitions = [
    { cx: 400, cy: 300, r: 38, petals: 20, petalLen: 75, petalW: 24, startF: 90 }, // Centro principal
    { cx: 300, cy: 260, r: 32, petals: 18, petalLen: 62, petalW: 20, startF: 140 }, // Izq arriba
    { cx: 500, cy: 265, r: 32, petals: 18, petalLen: 62, petalW: 20, startF: 180 }, // Der arriba
    { cx: 240, cy: 340, r: 28, petals: 16, petalLen: 54, petalW: 18, startF: 220 }, // Izq baja
    { cx: 560, cy: 345, r: 28, petals: 16, petalLen: 54, petalW: 18, startF: 260 }, // Der baja
    { cx: 400, cy: 190, r: 32, petals: 18, petalLen: 65, petalW: 20, startF: 300 }, // Arriba centro
    { cx: 340, cy: 370, r: 28, petals: 15, petalLen: 50, petalW: 16, startF: 340 }, // Frente izq
    { cx: 460, cy: 370, r: 28, petals: 15, petalLen: 50, petalW: 16, startF: 370 }, // Frente der
  ];

  function easeOutBack(x) {
    const c1 = 1.70158;
    const c3 = c1 + 1;
    return x >= 1 ? 1 : 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2);
  }

  function drawBouquetFrame() {
    flCtx.clearRect(0, 0, flowerCanvas.width, flowerCanvas.height);
    const f = bouquetAnimFrame;
    const baseX = 400;
    const baseY = 650;

    // 1. DIBUJAR TALLOS VERDES
    const stemProg = Math.min(1.0, f / 80.0);
    if (stemProg > 0) {
      for (let fl of flowerDefinitions) {
        const ctrlX = (baseX + fl.cx) / 2 + (fl.cx - baseX) * 0.25;
        const ctrlY = (baseY + fl.cy) / 2 + 30;

        flCtx.beginPath();
        flCtx.moveTo(baseX, baseY);
        
        // Interpolar curva cuadrática
        const steps = 30;
        const currentSteps = Math.floor(steps * stemProg);
        for (let i = 0; i <= currentSteps; i++) {
          let t = i / steps;
          let px = (1 - t) * (1 - t) * baseX + 2 * (1 - t) * t * ctrlX + t * t * fl.cx;
          let py = (1 - t) * (1 - t) * baseY + 2 * (1 - t) * t * ctrlY + t * t * fl.cy;
          if (i === 0) flCtx.moveTo(px, py);
          else flCtx.lineTo(px, py);
        }
        flCtx.strokeStyle = '#2D6A4F';
        flCtx.lineWidth = 6;
        flCtx.lineCap = 'round';
        flCtx.stroke();

        flCtx.strokeStyle = '#52B788';
        flCtx.lineWidth = 2.5;
        flCtx.stroke();
      }
    }

    // 2. HOJAS VERDES
    if (f > 30) {
      const leafProg = Math.min(1.0, (f - 30) / 60.0);
      const leaves = [
        { x: 310, y: 460, angle: -40, scale: 1.1 },
        { x: 490, y: 450, angle: 40, scale: 1.1 },
        { x: 270, y: 400, angle: -60, scale: 0.9 },
        { x: 530, y: 390, angle: 60, scale: 0.9 },
        { x: 360, y: 500, angle: -20, scale: 0.8 },
        { x: 440, y: 500, angle: 20, scale: 0.8 },
      ];
      for (let l of leaves) {
        drawLeaf(flCtx, l.x, l.y, l.angle, l.scale * leafProg);
      }
    }

    // 3. ENVOLTURA ELEGANTE DEL RAMO
    if (f > 60) {
      const wrapProg = Math.min(1.0, (f - 60) / 50.0);
      drawWrappingPaper(flCtx, baseX, baseY - 90, wrapProg);
    }

    // 4. FLORES AMARILLAS (GIRASOLES FLORECIENDO)
    for (let fl of flowerDefinitions) {
      if (f >= fl.startF) {
        const rawProg = Math.min(1.0, (f - fl.startF) / 50.0);
        const prog = easeOutBack(rawProg);
        drawSunflower(flCtx, fl.cx, fl.cy, fl.r * prog, fl.petals, fl.petalLen * prog, fl.petalW * prog, rawProg);
      }
    }

    // 5. MOÑO Y LISTÓN ROSA
    if (f > 130) {
      const bowProg = Math.min(1.0, (f - 130) / 40.0);
      drawBow(flCtx, baseX, 550, bowProg);
    }

    if (bouquetAnimFrame < 460) {
      bouquetAnimFrame++;
      requestAnimationFrame(drawBouquetFrame);
    }
  }

  function drawLeaf(ctx, x, y, angleDeg, scale) {
    if (scale <= 0.01) return;
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate((angleDeg * Math.PI) / 180);
    ctx.scale(scale, scale);

    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.quadraticCurveTo(-18, -25, 0, -60);
    ctx.quadraticCurveTo(18, -25, 0, 0);
    ctx.fillStyle = '#2D6A4F';
    ctx.fill();
    ctx.strokeStyle = '#1B4332';
    ctx.lineWidth = 1.5;
    ctx.stroke();

    // Nervadura
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(0, -55);
    ctx.strokeStyle = '#74C69D';
    ctx.lineWidth = 1.5;
    ctx.stroke();

    ctx.restore();
  }

  function drawWrappingPaper(ctx, cx, cy, prog) {
    const wTop = 240 * prog;
    const wBot = 45 * prog;
    const h = 210 * prog;

    ctx.save();
    // Capa base de papel Kraft
    ctx.beginPath();
    ctx.moveTo(cx - wTop, cy - h * 0.4);
    ctx.lineTo(cx, cy - h * 0.1);
    ctx.lineTo(cx + wTop, cy - h * 0.4);
    ctx.lineTo(cx + wBot, cy + h * 0.7);
    ctx.lineTo(cx - wBot, cy + h * 0.7);
    ctx.closePath();
    ctx.fillStyle = '#F4E7D7';
    ctx.shadowColor = 'rgba(0,0,0,0.4)';
    ctx.shadowBlur = 15;
    ctx.fill();

    // Pliegue izquierdo
    ctx.beginPath();
    ctx.moveTo(cx - wTop * 0.95, cy - h * 0.35);
    ctx.lineTo(cx + 25, cy + h * 0.65);
    ctx.lineTo(cx - wBot, cy + h * 0.7);
    ctx.closePath();
    ctx.fillStyle = '#EBD5BD';
    ctx.fill();

    // Pliegue derecho
    ctx.beginPath();
    ctx.moveTo(cx + wTop * 0.95, cy - h * 0.35);
    ctx.lineTo(cx - 25, cy + h * 0.65);
    ctx.lineTo(cx + wBot, cy + h * 0.7);
    ctx.closePath();
    ctx.fillStyle = '#FAF0E6';
    ctx.fill();

    ctx.restore();
  }

  function drawBow(ctx, cx, cy, prog) {
    const sz = 32 * prog;
    ctx.save();
    ctx.translate(cx, cy);

    // Cintas colgantes
    ctx.beginPath();
    ctx.moveTo(-6, 5);
    ctx.quadraticCurveTo(-25, sz * 0.8, -sz * 0.9, sz * 1.8);
    ctx.strokeStyle = '#FF9EBB';
    ctx.lineWidth = 5;
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(6, 5);
    ctx.quadraticCurveTo(25, sz * 0.8, sz * 0.9, sz * 1.8);
    ctx.strokeStyle = '#FF9EBB';
    ctx.lineWidth = 5;
    ctx.stroke();

    // Lazos
    ctx.fillStyle = '#FFB7D5';
    ctx.strokeStyle = '#FF7597';
    ctx.lineWidth = 2;

    // Ala izquierda
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.bezierCurveTo(-sz * 1.5, -sz * 0.9, -sz * 1.8, sz * 0.7, 0, 0);
    ctx.fill();
    ctx.stroke();

    // Ala derecha
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.bezierCurveTo(sz * 1.5, -sz * 0.9, sz * 1.8, sz * 0.7, 0, 0);
    ctx.fill();
    ctx.stroke();

    // Nudo central
    ctx.beginPath();
    ctx.arc(0, 0, sz * 0.35, 0, Math.PI * 2);
    ctx.fillStyle = '#FF9EBB';
    ctx.fill();
    ctx.stroke();

    ctx.restore();
  }

  function drawSunflower(ctx, cx, cy, coreR, petals, petalLen, petalW, rawProg) {
    if (coreR <= 0.5) return;

    ctx.save();

    // Resplandor dorado suave
    const glow = ctx.createRadialGradient(cx, cy, coreR, cx, cy, coreR + petalLen * 1.2);
    glow.addColorStop(0, 'rgba(255, 215, 0, 0.4)');
    glow.addColorStop(1, 'rgba(255, 215, 0, 0)');
    ctx.fillStyle = glow;
    ctx.beginPath();
    ctx.arc(cx, cy, coreR + petalLen * 1.2, 0, Math.PI * 2);
    ctx.fill();

    // Capa de pétalos trasera (tono ámbar/naranja dorado)
    const angleStep = (Math.PI * 2) / petals;
    for (let i = 0; i < petals; i++) {
      let angle = i * angleStep + angleStep / 2;
      drawSinglePetal(ctx, cx, cy, angle, coreR * 0.8, petalLen * 0.92, petalW * 0.85, '#FFA000', '#FF8F00');
    }

    // Capa de pétalos delantera (amarillo radiante)
    for (let i = 0; i < petals; i++) {
      let angle = i * angleStep;
      drawSinglePetal(ctx, cx, cy, angle, coreR * 0.85, petalLen, petalW, '#FFD700', '#FFF176');
    }

    // Centro del girasol
    ctx.beginPath();
    ctx.arc(cx, cy, coreR + 2, 0, Math.PI * 2);
    ctx.fillStyle = '#3E2723';
    ctx.fill();

    const coreGrad = ctx.createRadialGradient(cx - 3, cy - 3, coreR * 0.1, cx, cy, coreR);
    coreGrad.addColorStop(0, '#5D4037');
    coreGrad.addColorStop(0.8, '#4E342E');
    coreGrad.addColorStop(1, '#2E1C14');
    ctx.fillStyle = coreGrad;
    ctx.beginPath();
    ctx.arc(cx, cy, coreR, 0, Math.PI * 2);
    ctx.fill();

    // Semillas en espiral doradas
    const seedCount = Math.floor(22 * rawProg);
    for (let s = 0; s < seedCount; s++) {
      const stheta = s * 2.39996;
      const srad = (coreR * 0.78) * Math.sqrt(s / 22);
      const sx = cx + Math.cos(stheta) * srad;
      const sy = cy + Math.sin(stheta) * srad;

      ctx.fillStyle = '#FFB300';
      ctx.beginPath();
      ctx.arc(sx, sy, 1.6, 0, Math.PI * 2);
      ctx.fill();
    }

    ctx.restore();
  }

  function drawSinglePetal(ctx, cx, cy, angle, startDist, len, width, fillCol, strokeCol) {
    ctx.save();
    ctx.translate(cx, cy);
    ctx.rotate(angle);

    ctx.beginPath();
    ctx.moveTo(startDist, 0);
    ctx.quadraticCurveTo(startDist + len * 0.5, width * 0.55, startDist + len, 0);
    ctx.quadraticCurveTo(startDist + len * 0.5, -width * 0.55, startDist, 0);

    ctx.fillStyle = fillCol;
    ctx.fill();
    ctx.strokeStyle = strokeCol;
    ctx.lineWidth = 1.2;
    ctx.stroke();

    ctx.restore();
  }

  // 4. TRANSICIÓN AL PRESIONAR EL BOTÓN ROJO
  startBtn.addEventListener('click', (e) => {
    // Iniciar melodía romántica
    startRomanticMelody();

    // Generar explosión de corazones y chispas
    const rect = startBtn.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;

    for (let i = 0; i < 40; i++) {
      let angle = Math.random() * Math.PI * 2;
      let spd = Math.random() * 8 + 3;
      clickHearts.push({
        x: centerX,
        y: centerY,
        vx: Math.cos(angle) * spd,
        vy: Math.sin(angle) * spd - 3,
        life: 1.0,
        decay: Math.random() * 0.02 + 0.015,
        size: Math.random() * 1.2 + 0.8,
        color: ['#FF2A6D', '#FFB7D5', '#FFD700', '#FFFFFF', '#FF6584'][Math.floor(Math.random() * 5)]
      });
    }

    // Transición suave
    introScreen.style.opacity = '0';
    introScreen.style.transition = 'opacity 0.6s ease';

    setTimeout(() => {
      introScreen.classList.remove('active');
      flowerScreen.classList.add('active');
      drawBouquetFrame();
    }, 600);
  });

  // 5. INTERACCIÓN CON LA CARTITA Y CONEJITA
  letterToggleBtn.addEventListener('click', () => {
    letterModal.classList.add('active');
  });

  closeLetterBtn.addEventListener('click', () => {
    letterModal.classList.remove('active');
  });

  letterModal.querySelector('.modal-backdrop').addEventListener('click', () => {
    letterModal.classList.remove('active');
  });

  bunnyCompanion.addEventListener('click', () => {
    const bubble = bunnyCompanion.querySelector('.bunny-bubble');
    const phrases = [
      '¡Te amo con todo mi corazón! 💛',
      '¡Eres la conejita más hermosa! 🐰💖',
      '¡Feliz 21 de Septiembre, Mimi! ✨',
      '¡Gracias por hacerme tan feliz! 🌸'
    ];
    bubble.textContent = phrases[Math.floor(Math.random() * phrases.length)];
  });
});
