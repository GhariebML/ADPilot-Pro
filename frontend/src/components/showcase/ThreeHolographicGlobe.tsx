import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { Brain, Globe, Network, Sparkles } from 'lucide-react';

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
  const [internalMode, setInternalMode] = useState<VisualMode>('brain');
  const currentMode = externalMode || internalMode;
  const modeRef = useRef<VisualMode>(currentMode);
  modeRef.current = currentMode;

  const setMode = (m: VisualMode) => {
    setInternalMode(m);
    if (onModeChange) onModeChange(m);
  };

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

    // Root Group with smooth physics
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
      const texture = new THREE.CanvasTexture(canvas);
      return texture;
    };

    const particleTexture = createParticleTexture();

    // 4. Central Holographic Crystal Core (Octahedron + Wireframe Dodecahedron)
    const innerCrystalGeo = new THREE.OctahedronGeometry(28, 0);
    const innerCrystalMat = new THREE.MeshBasicMaterial({
      color: 0x8b5cf6, // Vibrant Purple
      wireframe: true,
      transparent: true,
      opacity: 0.45,
      blending: THREE.AdditiveBlending
    });
    const innerCrystal = new THREE.Mesh(innerCrystalGeo, innerCrystalMat);
    rootGroup.add(innerCrystal);

    const outerPolyGeo = new THREE.IcosahedronGeometry(46, 1);
    const outerPolyMat = new THREE.MeshBasicMaterial({
      color: 0x06b6d4, // Cyan
      wireframe: true,
      transparent: true,
      opacity: 0.25,
      blending: THREE.AdditiveBlending
    });
    const outerPoly = new THREE.Mesh(outerPolyGeo, outerPolyMat);
    rootGroup.add(outerPoly);

    // Glowing Inner Energy Sphere
    const auraGeo = new THREE.SphereGeometry(14, 32, 32);
    const auraMat = new THREE.MeshBasicMaterial({
      color: 0x38bdf8,
      transparent: true,
      opacity: 0.35,
      blending: THREE.AdditiveBlending
    });
    const auraMesh = new THREE.Mesh(auraGeo, auraMat);
    rootGroup.add(auraMesh);

    // 5. Silky Orbiting Energy Rings (Gyroscopic Gimbal)
    const createSmoothRing = (radius: number, tube: number, color: number, opacity: number) => {
      const geo = new THREE.TorusGeometry(radius, tube, 24, 160);
      const mat = new THREE.MeshBasicMaterial({
        color,
        transparent: true,
        opacity,
        blending: THREE.AdditiveBlending
      });
      return new THREE.Mesh(geo, mat);
    };

    const ring1 = createSmoothRing(72, 0.45, 0x06b6d4, 0.7);
    ring1.rotation.x = Math.PI / 3.2;
    rootGroup.add(ring1);

    const ring2 = createSmoothRing(88, 0.4, 0x8b5cf6, 0.6);
    ring2.rotation.y = Math.PI / 4;
    ring2.rotation.z = Math.PI / 5;
    rootGroup.add(ring2);

    const ring3 = createSmoothRing(102, 0.35, 0x10b981, 0.5);
    ring3.rotation.x = -Math.PI / 4;
    ring3.rotation.y = -Math.PI / 3;
    rootGroup.add(ring3);

    // 6. Smooth Undulating Cyber Wave Grid (Horizon Floor)
    const gridCols = 40;
    const gridRows = 30;
    const gridCount = gridCols * gridRows;
    const gridPositions = new Float32Array(gridCount * 3);

    let gIdx = 0;
    const gridWidth = 400;
    const gridDepth = 300;

    for (let i = 0; i < gridRows; i++) {
      for (let j = 0; j < gridCols; j++) {
        const u = (j / (gridCols - 1) - 0.5) * gridWidth;
        const v = (i / (gridRows - 1) - 0.5) * gridDepth;
        gridPositions[gIdx++] = u;
        gridPositions[gIdx++] = -65; // Y position floor
        gridPositions[gIdx++] = v + 40; // Z forward
      }
    }

    const gridGeo = new THREE.BufferGeometry();
    gridGeo.setAttribute('position', new THREE.BufferAttribute(gridPositions, 3));

    const gridMat = new THREE.PointsMaterial({
      size: 2.2,
      color: 0x0284c7,
      map: particleTexture,
      transparent: true,
      opacity: 0.35,
      blending: THREE.AdditiveBlending,
      depthWrite: false
    });

    const gridPoints = new THREE.Points(gridGeo, gridMat);
    scene.add(gridPoints);

    // 7. Particle Neural Mesh (360 Dynamic Nodes)
    const particleCount = 360;
    const positions = new Float32Array(particleCount * 3);
    const targetPositions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);

    const colorChoices = [
      new THREE.Color(0x38bdf8), // Cyan
      new THREE.Color(0xc084fc), // Purple
      new THREE.Color(0x34d399), // Emerald
      new THREE.Color(0x60a5fa), // Blue
    ];

    const computePositions = (mode: VisualMode, outArr: Float32Array) => {
      const radius = 95;
      for (let i = 0; i < particleCount; i++) {
        if (mode === 'brain') {
          // Dual Hemisphere Neural Cloud
          const u = Math.random();
          const v = Math.random();
          const theta = u * 2.0 * Math.PI;
          const phi = Math.acos(2.0 * v - 1.0);
          const hemisphere = i % 2 === 0 ? 1 : -1;
          const r = (Math.cbrt(Math.random()) * 0.65 + 0.35) * radius;

          outArr[i * 3] = (r * Math.sin(phi) * Math.cos(theta)) * 0.82 + (hemisphere * 12);
          outArr[i * 3 + 1] = (r * Math.sin(phi) * Math.sin(theta)) * 1.05;
          outArr[i * 3 + 2] = r * Math.cos(phi) * 0.9;
        } else if (mode === 'globe') {
          // Fibonacci Sphere Globe
          const phi = Math.acos(-1 + (2 * i) / particleCount);
          const theta = Math.sqrt(particleCount * Math.PI) * phi;

          outArr[i * 3] = radius * Math.cos(theta) * Math.sin(phi);
          outArr[i * 3 + 1] = radius * Math.sin(theta) * Math.sin(phi);
          outArr[i * 3 + 2] = radius * Math.cos(phi);
        } else {
          // Quantum Torus Rings
          const u = (i / particleCount) * Math.PI * 2 * 3;
          const v = (i / particleCount) * Math.PI * 2;
          const R = 75;
          const r = 26;

          outArr[i * 3] = (R + r * Math.cos(v)) * Math.cos(u);
          outArr[i * 3 + 1] = (R + r * Math.cos(v)) * Math.sin(u);
          outArr[i * 3 + 2] = r * Math.sin(v);
        }
      }
    };

    computePositions('brain', positions);
    computePositions('brain', targetPositions);

    for (let i = 0; i < particleCount; i++) {
      const col = colorChoices[i % colorChoices.length];
      colors[i * 3] = col.r;
      colors[i * 3 + 1] = col.g;
      colors[i * 3 + 2] = col.b;
    }

    const particleGeo = new THREE.BufferGeometry();
    particleGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    particleGeo.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    const particleMat = new THREE.PointsMaterial({
      size: 4.8,
      map: particleTexture,
      vertexColors: true,
      transparent: true,
      opacity: 0.95,
      blending: THREE.AdditiveBlending,
      depthWrite: false
    });

    const particles = new THREE.Points(particleGeo, particleMat);
    rootGroup.add(particles);

    // 8. Synaptic Connections
    const maxConn = particleCount * 4;
    const linePositions = new Float32Array(maxConn * 6);
    const lineColors = new Float32Array(maxConn * 6);

    const lineGeo = new THREE.BufferGeometry();
    lineGeo.setAttribute('position', new THREE.BufferAttribute(linePositions, 3));
    lineGeo.setAttribute('color', new THREE.BufferAttribute(lineColors, 3));

    const lineMat = new THREE.LineBasicMaterial({
      vertexColors: true,
      transparent: true,
      opacity: 0.3,
      blending: THREE.AdditiveBlending,
      depthWrite: false
    });

    const lines = new THREE.LineSegments(lineGeo, lineMat);
    rootGroup.add(lines);

    // 9. Silky Mouse Tracking
    let mouseX = 0;
    let mouseY = 0;
    let targetRotX = 0;
    let targetRotY = 0;

    const onMouseMove = (e: MouseEvent) => {
      const halfW = window.innerWidth / 2;
      const halfH = window.innerHeight / 2;
      mouseX = (e.clientX - halfW) * 0.0004;
      mouseY = (e.clientY - halfH) * 0.0004;
    };

    window.addEventListener('mousemove', onMouseMove);

    const onResize = () => {
      if (!container) return;
      const w = container.clientWidth;
      const h = container.clientHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };

    window.addEventListener('resize', onResize);

    // 10. Smooth Render Loop
    let animId: number;
    let prevMode = modeRef.current;
    const clock = new THREE.Clock();

    const animate = () => {
      animId = requestAnimationFrame(animate);
      const delta = clock.getDelta();
      const elapsed = clock.getElapsedTime();

      // Check mode transition
      if (prevMode !== modeRef.current) {
        prevMode = modeRef.current;
        computePositions(prevMode, targetPositions);
      }

      // Smooth Particle Morphing (Exponential Lerp)
      const pos = particleGeo.attributes.position.array as Float32Array;
      const morphSpeed = 4.5 * delta;
      for (let i = 0; i < particleCount * 3; i++) {
        pos[i] += (targetPositions[i] - pos[i]) * Math.min(morphSpeed, 0.2);
      }
      particleGeo.attributes.position.needsUpdate = true;

      // Update Floor Cyber Waves
      const gridPos = gridGeo.attributes.position.array as Float32Array;
      let waveIdx = 0;
      for (let i = 0; i < gridRows; i++) {
        for (let j = 0; j < gridCols; j++) {
          const u = gridPos[waveIdx];
          const v = gridPos[waveIdx + 2];
          gridPos[waveIdx + 1] = -65 + Math.sin(u * 0.03 + elapsed * 1.5) * Math.cos(v * 0.03 + elapsed * 1.2) * 5.0;
          waveIdx += 3;
        }
      }
      gridGeo.attributes.position.needsUpdate = true;

      // Synaptic Connection Calculations
      let lIdx = 0;
      let cIdx = 0;
      const maxDist = prevMode === 'globe' ? 32 : 38;

      for (let i = 0; i < particleCount; i += 2) {
        for (let j = i + 1; j < particleCount; j += 2) {
          const dx = pos[i * 3] - pos[j * 3];
          const dy = pos[i * 3 + 1] - pos[j * 3 + 1];
          const dz = pos[i * 3 + 2] - pos[j * 3 + 2];
          const dist = Math.sqrt(dx * dx + dy * dy + dz * dz);

          if (dist < maxDist) {
            const alpha = Math.pow(1.0 - dist / maxDist, 1.5);

            linePositions[lIdx++] = pos[i * 3];
            linePositions[lIdx++] = pos[i * 3 + 1];
            linePositions[lIdx++] = pos[i * 3 + 2];

            linePositions[lIdx++] = pos[j * 3];
            linePositions[lIdx++] = pos[j * 3 + 1];
            linePositions[lIdx++] = pos[j * 3 + 2];

            lineColors[cIdx++] = 0.02 * alpha;
            lineColors[cIdx++] = 0.74 * alpha;
            lineColors[cIdx++] = 0.95 * alpha;

            lineColors[cIdx++] = 0.65 * alpha;
            lineColors[cIdx++] = 0.35 * alpha;
            lineColors[cIdx++] = 0.98 * alpha;
          }
        }
      }

      lineGeo.setDrawRange(0, lIdx / 3);
      lineGeo.attributes.position.needsUpdate = true;
      lineGeo.attributes.color.needsUpdate = true;

      // Smooth Geometric Rotations
      innerCrystal.rotation.x = elapsed * 0.15;
      innerCrystal.rotation.y = elapsed * 0.22;

      outerPoly.rotation.x = -elapsed * 0.08;
      outerPoly.rotation.y = elapsed * 0.12;

      const pulse = 1.0 + Math.sin(elapsed * 2.0) * 0.1;
      auraMesh.scale.set(pulse, pulse, pulse);

      ring1.rotation.z = elapsed * 0.25;
      ring2.rotation.x = elapsed * -0.18;
      ring3.rotation.y = elapsed * 0.2;

      // Mouse Parallax Damping (Spring Smoothness)
      targetRotX += (mouseY * 1.5 - targetRotX) * 0.04;
      targetRotY += (mouseX * 1.5 - targetRotY) * 0.04;

      rootGroup.rotation.y = elapsed * 0.035 + targetRotY;
      rootGroup.rotation.x = Math.sin(elapsed * 0.03) * 0.04 + targetRotX;

      renderer.render(scene, camera);
    };

    animate();

    return () => {
      window.removeEventListener('mousemove', onMouseMove);
      window.removeEventListener('resize', onResize);
      cancelAnimationFrame(animId);
      if (container && renderer.domElement) {
        container.removeChild(renderer.domElement);
      }
      renderer.dispose();
      particleGeo.dispose();
      particleMat.dispose();
      lineGeo.dispose();
      lineMat.dispose();
      gridGeo.dispose();
      gridMat.dispose();
      innerCrystalGeo.dispose();
      innerCrystalMat.dispose();
      outerPolyGeo.dispose();
      outerPolyMat.dispose();
      auraGeo.dispose();
      auraMat.dispose();
      ring1.geometry.dispose();
      (ring1.material as THREE.Material).dispose();
      ring2.geometry.dispose();
      (ring2.material as THREE.Material).dispose();
      ring3.geometry.dispose();
      (ring3.material as THREE.Material).dispose();
      particleTexture.dispose();
    };
  }, []);

  return (
    <div ref={containerRef} className={className} />
  );
};

export default ThreeHolographicGlobe;
