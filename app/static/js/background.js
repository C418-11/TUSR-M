function createSpots() {
    const container = document.getElementById('spots-container');
    container.innerHTML = '';
    const colors = getComputedStyle(document.documentElement)
        .getPropertyValue('--spot-colors').split(', ');

    const vw = window.innerWidth;
    const vh = window.innerHeight;
    const screenArea = vw * vh;
    const baseAreaRatio = 0.6;
    const totalSpotArea = screenArea * baseAreaRatio;
    const baseSpots = Math.sqrt(screenArea) * 0.1;
    let spotsCount = baseSpots * (0.8 + Math.random() * 0.4);
    spotsCount = Math.max(12, Math.min(Math.round(spotsCount), 25));

    for (let i = 0; i < spotsCount; i++) {
        const spot = document.createElement('div');
        spot.className = 'spot';
        const avgArea = totalSpotArea / spotsCount;
        const area = avgArea * (0.7 + Math.random() * 0.6);
        const size = Math.sqrt(area / Math.PI) * 2;
        const sizeVw = (size / vw) * 100 * (0.9 + Math.random() * 0.2);
        spot.style.cssText = `
            width: ${sizeVw}vw;
            height: ${sizeVw}vw;
            left: ${Math.random() * 140 - 20}%;
            top: ${Math.random() * 140 - 20}%;
            background: ${colors[Math.floor(Math.random() * colors.length)]};
            animation-delay: ${Math.random() * -20}s;
        `;
        container.appendChild(spot);
    }
}

// 初始化背景
window.addEventListener('DOMContentLoaded', createSpots);
window.addEventListener('resize', () => {
    clearTimeout(window.resizeTimer);
    window.resizeTimer = setTimeout(createSpots, 200);
});