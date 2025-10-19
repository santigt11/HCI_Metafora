/**
 * Animaciones del Bus del Aprendizaje en Python
 * Solo animaciones CSS y transiciones de UI
 */

// Animar éxito (respuesta correcta)
function animateSuccess() {
    const container = document.getElementById('exerciseContainer');
    if (!container) return;
    
    container.classList.add('feedback-success');
    setTimeout(() => container.classList.remove('feedback-success'), 600);
    
    playSuccessSound();
}

// Animar error (respuesta incorrecta)
function animateError() {
    const container = document.getElementById('exerciseContainer');
    if (!container) return;
    
    container.classList.add('feedback-error');
    setTimeout(() => container.classList.remove('feedback-error'), 400);
    
    playErrorSound();
}

// Sonidos simples con Web Audio API (sin archivos externos)
function playSuccessSound() {
    try {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        oscillator.frequency.value = 800;
        oscillator.type = 'sine';
        
        gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1);
        
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.1);
    } catch (e) {
        // Si no funciona audio, simplemente continuar
    }
}

function playErrorSound() {
    try {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        oscillator.frequency.value = 300;
        oscillator.type = 'sine';
        
        gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.15);
        
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.15);
    } catch (e) {
        // Si no funciona audio, simplemente continuar
    }
}

// Scroll suave a elemento
function smoothScroll(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

// Fade in/out genérico
function fadeElement(element, fadeIn = true, duration = 300) {
    if (!element) return;
    
    element.style.transition = `opacity ${duration}ms ease-in-out`;
    element.style.opacity = fadeIn ? '1' : '0';
}

// Pulse animation para mensajes
function pulseElement(element) {
    if (!element) return;
    
    element.classList.add('pulse');
    setTimeout(() => element.classList.remove('pulse'), 600);
}
