import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';

export type VisualMode = 'brain' | 'globe' | 'torus';

interface ThreeHolographicGlobeProps {
  className?: string;
  activeMode?: VisualMode;
  onModeChange?: (mode: VisualMode) => void;
}

export const ThreeHolographicGlobe: React.FC<ThreeHolographicGlobeProps> = ({
  className = "absolute inset-0 w-full h-full pointer-events-none z-0",
  activeMode: externalMode,
  onModeChange,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  
  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const width = container.clientWidth || window.innerWidth;
    const height = container.clientHeight || window.innerHeight;

    // 1. Scene & Camera
    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x030712, 0.0035);

    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1200);
    camera.position.set(0, 10, 220);

    // 2. Renderer
    const renderer = new THREE.WebGLRenderer({
      alpha: true,
      antialias: true,
      powerPreference: 'high-performance'
    });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.35;
    container.appendChild(renderer.domElement);

    // Root Group for Mouse Parallax
    const rootGroup = new THREE.Group();
    scene.add(rootGroup);

    // 3. Helper: Generate Soft Circular Glow Texture
    const createParticleTexture = () => {
      const canvas = document.createElement('canvas');
      canvas.width = 64;
      canvas.height = 64;
      const ctx = canvas.getContext('2d');
      if (ctx) {
        const gradient = ctx.createRadialGradient(32, 32, 0, 32, 32, 32);
        gradient.addColorStop(0, 'rgba(255, 255, 255, 1)');
        gradient.addColorStop(0.2, 'rgba(56, 189, 248, 0.9)');
        gradient.addColorStop(0.5, 'rgba(168, 85, 247, 0.4)');
        gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, 64, 64);
      }
      return new THREE.CanvasTexture(canvas);
    };

    const particleTexture = createParticleTexture();

    // 4. Professional Falling Cosmic Point Cloud
    const particleCount = 4000;
    const positions = new Float32Array(particleCount * 3);
    const velocities = new Float32Array(particleCount);
    const colors = new Float32Array(particleCount * 3);

    const colorPalette = [
      new THREE.Color(0xffffff), // White
      new THREE.Color(0x38bdf8), // Sky Blue
      new THREE.Color(0xc084fc), // Soft Purple
      new THREE.Color(0x818cf8), // Indigo
      new THREE.Color(0x2dd4bf), // Teal
    ];

    for (let i = 0; i < particleCount; i++) {
      positions[i * 3] = (Math.random() - 0.5) * 600; // x spread
      positions[i * 3 + 1] = Math.random() * 600 - 200; // y spread (from -200 to 400)
      positions[i * 3 + 2] = (Math.random() - 0.5) * 400 - 100; // z spread (mostly behind and around)

      // Varied falling velocities (slow and elegant)
      velocities[i] = Math.random() * 10.0 + 2.0; // speed between 2 and 12 units/sec

      const col = colorPalette[Math.floor(Math.random() * colorPalette.length)];
      
      // Make them slightly dimmer randomly for depth
      const intensity = Math.random() * 0.6 + 0.4;
      colors[i * 3] = col.r * intensity;
      colors[i * 3 + 1] = col.g * intensity;
      colors[i * 3 + 2] = col.b * intensity;
    }

    const pointsGeo = new THREE.BufferGeometry();
    pointsGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    pointsGeo.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    const pointsMat = new THREE.PointsMaterial({
      size: 3.2,
      map: particleTexture,
      vertexColors: true,
      transparent: true,
      opacity: 0.9,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
      sizeAttenuation: true
    });

    const starfield = new THREE.Points(pointsGeo, pointsMat);
    rootGroup.add(starfield);

    // 5. Mouse & Scroll Parallax setup
    let mouseX = 0;
    let mouseY = 0;
    let targetRotX = 0;
    let targetRotY = 0;
    let targetScrollY = 0;
    let currentScrollY = 0;

    const onMouseMove = (e: MouseEvent) => {
      const halfW = window.innerWidth / 2;
      const halfH = window.innerHeight / 2;
      mouseX = (e.clientX - halfW) * 0.0003;
      mouseY = (e.clientY - halfH) * 0.0003;
    };

    const onScroll = () => {
      targetScrollY = window.scrollY * 0.08; // multiplier for parallax strength
    };

    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('scroll', onScroll, { passive: true });

    const onResize = () => {
      if (!container) return;
      const w = container.clientWidth;
      const h = container.clientHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };

    window.addEventListener('resize', onResize);

    // 6. Render Loop with Delta Time
    let animId: number;
    const clock = new THREE.Clock();

    const animate = () => {
      animId = requestAnimationFrame(animate);
      const delta = clock.getDelta();

      // Update falling particles
      const pos = pointsGeo.attributes.position.array as Float32Array;
      for (let i = 0; i < particleCount; i++) {
        pos[i * 3 + 1] -= velocities[i] * delta;

        // Reset if too low
        if (pos[i * 3 + 1] < -250) {
          pos[i * 3 + 1] = 350 + Math.random() * 100;
          pos[i * 3] = (Math.random() - 0.5) * 600;
          pos[i * 3 + 2] = (Math.random() - 0.5) * 400 - 100;
        }
      }
      pointsGeo.attributes.position.needsUpdate = true;

      // Mouse & Scroll Parallax Damping
      targetRotX += (mouseY * 1.5 - targetRotX) * 0.03;
      targetRotY += (mouseX * 1.5 - targetRotY) * 0.03;
      currentScrollY += (targetScrollY - currentScrollY) * 0.05;

      rootGroup.rotation.y = targetRotY;
      rootGroup.rotation.x = targetRotX;
      camera.position.y = 10 - currentScrollY; // Move camera down as you scroll down, making stars go up

      // Slight global drift
      rootGroup.rotation.y += clock.getElapsedTime() * 0.005;

      renderer.render(scene, camera);
    };

    animate();

    return () => {
      window.removeEventListener('mousemove', onMouseMove);
      window.removeEventListener('scroll', onScroll);
      window.removeEventListener('resize', onResize);
      cancelAnimationFrame(animId);
      if (container && renderer.domElement) {
        container.removeChild(renderer.domElement);
      }
      renderer.dispose();
      pointsGeo.dispose();
      pointsMat.dispose();
      particleTexture.dispose();
    };
  }, []);

  return (
    <div ref={containerRef} className={className} />
  );
};

export default ThreeHolographicGlobe;
