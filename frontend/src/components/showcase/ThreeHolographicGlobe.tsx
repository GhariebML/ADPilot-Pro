import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { Sparkles, Globe, Brain, Network, RotateCw } from 'lucide-react';

export type VisualMode = 'brain' | 'globe' | 'torus';

interface ThreeHolographicGlobeProps {
  className?: string;
}

export const ThreeHolographicGlobe: React.FC<ThreeHolographicGlobeProps> = ({
  className = "absolute inset-0 z-0 pointer-events-none"
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [activeMode, setActiveMode] = useState<VisualMode>('brain');
  const modeRef = useRef<VisualMode>('brain');
  modeRef.current = activeMode;

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const width = container.clientWidth || window.innerWidth;
    const height = container.clientHeight || window.innerHeight;

    // 1. Scene & Camera
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(55, width / height, 0.1, 1000);
    camera.position.z = 260;

    // 2. Renderer
    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    // 3. Particle System
    const particleCount = 420;
    const positions = new Float32Array(particleCount * 3);
    const targetPositions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);

    const colorPalette = [
      new THREE.Color(0x06b6d4), // Cyan
      new THREE.Color(0x8b5cf6), // Purple
      new THREE.Color(0x3b82f6), // Blue
      new THREE.Color(0x10b981), // Emerald
    ];

    // Compute shapes for each mode
    const computePositionsForMode = (mode: VisualMode, outArray: Float32Array) => {
      const radius = 105;
      for (let i = 0; i < particleCount; i++) {
        if (mode === 'brain') {
          // Dual-hemisphere brain cluster
          const u = Math.random();
          const v = Math.random();
          const theta = u * 2.0 * Math.PI;
          const phi = Math.acos(2.0 * v - 1.0);
          const hemisphere = i % 2 === 0 ? 1 : -1;
          const r = (Math.cbrt(Math.random()) * 0.7 + 0.3) * radius;

          const x = (r * Math.sin(phi) * Math.cos(theta)) * 0.85 + (hemisphere * 14);
          const y = (r * Math.sin(phi) * Math.sin(theta)) * 1.1;
          const z = r * Math.cos(phi) * 0.9;

          outArray[i * 3] = x;
          outArray[i * 3 + 1] = y;
          outArray[i * 3 + 2] = z;
        } else if (mode === 'globe') {
          // Global Marketing Dispatch Sphere with latitude rings
          const phi = Math.acos(-1 + (2 * i) / particleCount);
          const theta = Math.sqrt(particleCount * Math.PI) * phi;

          outArray[i * 3] = radius * Math.cos(theta) * Math.sin(phi);
          outArray[i * 3 + 1] = radius * Math.sin(theta) * Math.sin(phi);
          outArray[i * 3 + 2] = radius * Math.cos(phi);
        } else {
          // Quantum DAG Torus
          const u = (i / particleCount) * Math.PI * 2 * 3;
          const v = (i / particleCount) * Math.PI * 2;
          const R = 85;
          const r = 32;

          outArray[i * 3] = (R + r * Math.cos(v)) * Math.cos(u);
          outArray[i * 3 + 1] = (R + r * Math.cos(v)) * Math.sin(u);
          outArray[i * 3 + 2] = r * Math.sin(v);
        }
      }
    };

    // Initial position setup
    computePositionsForMode('brain', positions);
    computePositionsForMode('brain', targetPositions);

    for (let i = 0; i < particleCount; i++) {
      const color = colorPalette[i % colorPalette.length];
      colors[i * 3] = color.r;
      colors[i * 3 + 1] = color.g;
      colors[i * 3 + 2] = color.b;
    }

    const particleGeometry = new THREE.BufferGeometry();
    particleGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    particleGeometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    const particleMaterial = new THREE.PointsMaterial({
      size: 3.4,
      vertexColors: true,
      transparent: true,
      opacity: 0.88,
      blending: THREE.AdditiveBlending
    });

    const particles = new THREE.Points(particleGeometry, particleMaterial);
    scene.add(particles);

    // 4. Dynamic Synaptic Lines
    const maxConnections = particleCount * 5;
    const linePositions = new Float32Array(maxConnections * 6);
    const lineColors = new Float32Array(maxConnections * 6);

    const lineGeometry = new THREE.BufferGeometry();
    lineGeometry.setAttribute('position', new THREE.BufferAttribute(linePositions, 3));
    lineGeometry.setAttribute('color', new THREE.BufferAttribute(lineColors, 3));

    const lineMaterial = new THREE.LineBasicMaterial({
      vertexColors: true,
      transparent: true,
      opacity: 0.24,
      blending: THREE.AdditiveBlending
    });

    const lines = new THREE.LineSegments(lineGeometry, lineMaterial);
    scene.add(lines);

    // 5. Mouse Raycaster & Smooth Follow
    let mouseX = 0;
    let mouseY = 0;
    let targetRotX = 0;
    let targetRotY = 0;

    const handleMouseMove = (e: MouseEvent) => {
      const halfX = window.innerWidth / 2;
      const halfY = window.innerHeight / 2;
      mouseX = (e.clientX - halfX) * 0.0006;
      mouseY = (e.clientY - halfY) * 0.0006;
    };

    window.addEventListener('mousemove', handleMouseMove);

    // 6. Resize Handler
    const handleResize = () => {
      if (!container) return;
      const w = container.clientWidth;
      const h = container.clientHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };

    window.addEventListener('resize', handleResize);

    // 7. Animation Loop
    let animationFrameId: number;
    let currentModeState = modeRef.current;

    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);

      // Check if mode switched
      if (currentModeState !== modeRef.current) {
        currentModeState = modeRef.current;
        computePositionsForMode(currentModeState, targetPositions);
      }

      // Morph current positions toward targetPositions
      const pos = particleGeometry.attributes.position.array as Float32Array;
      for (let i = 0; i < particleCount * 3; i++) {
        pos[i] += (targetPositions[i] - pos[i]) * 0.045;
      }
      particleGeometry.attributes.position.needsUpdate = true;

      // Compute synaptic connecting lines
      let lineIndex = 0;
      let colorIndex = 0;
      const maxDistance = currentModeState === 'globe' ? 36 : 42;

      for (let i = 0; i < particleCount; i++) {
        for (let j = i + 1; j < particleCount; j++) {
          const dx = pos[i * 3] - pos[j * 3];
          const dy = pos[i * 3 + 1] - pos[j * 3 + 1];
          const dz = pos[i * 3 + 2] - pos[j * 3 + 2];
          const dist = Math.sqrt(dx * dx + dy * dy + dz * dz);

          if (dist < maxDistance) {
            const alpha = 1.0 - dist / maxDistance;

            linePositions[lineIndex++] = pos[i * 3];
            linePositions[lineIndex++] = pos[i * 3 + 1];
            linePositions[lineIndex++] = pos[i * 3 + 2];

            linePositions[lineIndex++] = pos[j * 3];
            linePositions[lineIndex++] = pos[j * 3 + 1];
            linePositions[lineIndex++] = pos[j * 3 + 2];

            lineColors[colorIndex++] = 0.02 * alpha;
            lineColors[colorIndex++] = 0.71 * alpha;
            lineColors[colorIndex++] = 0.83 * alpha;

            lineColors[colorIndex++] = 0.54 * alpha;
            lineColors[colorIndex++] = 0.36 * alpha;
            lineColors[colorIndex++] = 0.96 * alpha;
          }
        }
      }

      lineGeometry.setDrawRange(0, lineIndex / 3);
      lineGeometry.attributes.position.needsUpdate = true;
      lineGeometry.attributes.color.needsUpdate = true;

      // Camera rotation physics
      targetRotY += (mouseX - targetRotY) * 0.05;
      targetRotX += (mouseY - targetRotX) * 0.05;

      particles.rotation.y += 0.0022 + targetRotY * 0.1;
      particles.rotation.x += 0.0009 + targetRotX * 0.1;
      lines.rotation.y = particles.rotation.y;
      lines.rotation.x = particles.rotation.x;

      renderer.render(scene, camera);
    };

    animate();

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('resize', handleResize);
      cancelAnimationFrame(animationFrameId);
      if (container && renderer.domElement) {
        container.removeChild(renderer.domElement);
      }
      renderer.dispose();
      particleGeometry.dispose();
      lineGeometry.dispose();
      particleMaterial.dispose();
      lineMaterial.dispose();
    };
  }, []);

  return (
    <div className="relative w-full h-full">
      <div ref={containerRef} className={className} />

      {/* Interactive 3D Mode Switcher Overlay */}
      <div className="absolute top-6 right-6 z-20 pointer-events-auto flex items-center gap-1.5 p-1 rounded-xl bg-slate-950/85 border border-slate-800 backdrop-blur-xl shadow-xl">
        <button
          onClick={() => setActiveMode('brain')}
          className={`px-2.5 py-1.5 rounded-lg text-[10px] font-mono font-bold flex items-center gap-1.5 transition-all ${
            activeMode === 'brain'
              ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 shadow-sm'
              : 'text-slate-400 hover:text-white'
          }`}
        >
          <Brain className="w-3.5 h-3.5" />
          <span className="hidden sm:inline">Neural Brain</span>
        </button>

        <button
          onClick={() => setActiveMode('globe')}
          className={`px-2.5 py-1.5 rounded-lg text-[10px] font-mono font-bold flex items-center gap-1.5 transition-all ${
            activeMode === 'globe'
              ? 'bg-purple-500/20 text-purple-300 border border-purple-500/40 shadow-sm'
              : 'text-slate-400 hover:text-white'
          }`}
        >
          <Globe className="w-3.5 h-3.5" />
          <span className="hidden sm:inline">Ad Dispatch Globe</span>
        </button>

        <button
          onClick={() => setActiveMode('torus')}
          className={`px-2.5 py-1.5 rounded-lg text-[10px] font-mono font-bold flex items-center gap-1.5 transition-all ${
            activeMode === 'torus'
              ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 shadow-sm'
              : 'text-slate-400 hover:text-white'
          }`}
        >
          <Network className="w-3.5 h-3.5" />
          <span className="hidden sm:inline">Quantum DAG</span>
        </button>
      </div>
    </div>
  );
};

export default ThreeHolographicGlobe;
