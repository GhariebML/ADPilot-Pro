import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { Brain, Globe, Network } from 'lucide-react';

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

    // Dimensions
    const width = container.clientWidth || window.innerWidth;
    const height = container.clientHeight || window.innerHeight;

    // 1. Scene & Camera
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 1000);
    camera.position.z = 190;

    // 2. Renderer
    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.2;
    container.appendChild(renderer.domElement);

    // Root Pivot for global smooth mouse rotation
    const rootPivot = new THREE.Group();
    scene.add(rootPivot);

    // 3. Central Holographic Geometric Core (Icosahedron / Geodesic Wireframe)
    const coreGeo = new THREE.IcosahedronGeometry(42, 2);
    const coreWireMat = new THREE.MeshBasicMaterial({
      color: 0x06b6d4, // Cyan
      wireframe: true,
      transparent: true,
      opacity: 0.35,
      blending: THREE.AdditiveBlending
    });
    const coreMesh = new THREE.Mesh(coreGeo, coreWireMat);
    rootPivot.add(coreMesh);

    // Inner Glowing Core (Solid Sphere with Fresnel-like glow)
    const innerCoreGeo = new THREE.SphereGeometry(18, 24, 24);
    const innerCoreMat = new THREE.MeshBasicMaterial({
      color: 0x8b5cf6, // Purple
      transparent: true,
      opacity: 0.45,
      blending: THREE.AdditiveBlending
    });
    const innerCoreMesh = new THREE.Mesh(innerCoreGeo, innerCoreMat);
    rootPivot.add(innerCoreMesh);

    // 4. Dual Orbiting Gyroscopic Rings
    const ring1Geo = new THREE.TorusGeometry(68, 0.6, 16, 100);
    const ring1Mat = new THREE.MeshBasicMaterial({
      color: 0x06b6d4,
      transparent: true,
      opacity: 0.65,
      blending: THREE.AdditiveBlending
    });
    const ring1 = new THREE.Mesh(ring1Geo, ring1Mat);
    ring1.rotation.x = Math.PI / 3;
    rootPivot.add(ring1);

    const ring2Geo = new THREE.TorusGeometry(82, 0.6, 16, 100);
    const ring2Mat = new THREE.MeshBasicMaterial({
      color: 0x8b5cf6,
      transparent: true,
      opacity: 0.55,
      blending: THREE.AdditiveBlending
    });
    const ring2 = new THREE.Mesh(ring2Geo, ring2Mat);
    ring2.rotation.y = Math.PI / 4;
    ring2.rotation.z = Math.PI / 6;
    rootPivot.add(ring2);

    const ring3Geo = new THREE.TorusGeometry(96, 0.4, 16, 100);
    const ring3Mat = new THREE.MeshBasicMaterial({
      color: 0x10b981,
      transparent: true,
      opacity: 0.45,
      blending: THREE.AdditiveBlending
    });
    const ring3 = new THREE.Mesh(ring3Geo, ring3Mat);
    ring3.rotation.x = -Math.PI / 5;
    ring3.rotation.y = -Math.PI / 3;
    rootPivot.add(ring3);

    // 5. Particle Neural Cloud (Nodes)
    const particleCount = 380;
    const positions = new Float32Array(particleCount * 3);
    const targetPositions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);

    const colorPalette = [
      new THREE.Color(0x06b6d4), // Cyan
      new THREE.Color(0x8b5cf6), // Purple
      new THREE.Color(0x3b82f6), // Blue
      new THREE.Color(0x10b981), // Emerald
    ];

    const computePositions = (mode: VisualMode, outArr: Float32Array) => {
      const radius = 95;
      for (let i = 0; i < particleCount; i++) {
        if (mode === 'brain') {
          // Dual hemisphere neural distribution
          const u = Math.random();
          const v = Math.random();
          const theta = u * 2.0 * Math.PI;
          const phi = Math.acos(2.0 * v - 1.0);
          const hemisphere = i % 2 === 0 ? 1 : -1;
          const r = (Math.cbrt(Math.random()) * 0.65 + 0.35) * radius;

          outArr[i * 3] = (r * Math.sin(phi) * Math.cos(theta)) * 0.85 + (hemisphere * 12);
          outArr[i * 3 + 1] = (r * Math.sin(phi) * Math.sin(theta)) * 1.05;
          outArr[i * 3 + 2] = r * Math.cos(phi) * 0.9;
        } else if (mode === 'globe') {
          // Fibonacci sphere distribution (Marketing Globe)
          const phi = Math.acos(-1 + (2 * i) / particleCount);
          const theta = Math.sqrt(particleCount * Math.PI) * phi;

          outArr[i * 3] = radius * Math.cos(theta) * Math.sin(phi);
          outArr[i * 3 + 1] = radius * Math.sin(theta) * Math.sin(phi);
          outArr[i * 3 + 2] = radius * Math.cos(phi);
        } else {
          // Quantum DAG Torus Cloud
          const u = (i / particleCount) * Math.PI * 2 * 3;
          const v = (i / particleCount) * Math.PI * 2;
          const R = 75;
          const r = 28;

          outArr[i * 3] = (R + r * Math.cos(v)) * Math.cos(u);
          outArr[i * 3 + 1] = (R + r * Math.cos(v)) * Math.sin(u);
          outArr[i * 3 + 2] = r * Math.sin(v);
        }
      }
    };

    computePositions('brain', positions);
    computePositions('brain', targetPositions);

    for (let i = 0; i < particleCount; i++) {
      const col = colorPalette[i % colorPalette.length];
      colors[i * 3] = col.r;
      colors[i * 3 + 1] = col.g;
      colors[i * 3 + 2] = col.b;
    }

    const particleGeo = new THREE.BufferGeometry();
    particleGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    particleGeo.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    const particleMat = new THREE.PointsMaterial({
      size: 3.2,
      vertexColors: true,
      transparent: true,
      opacity: 0.9,
      blending: THREE.AdditiveBlending
    });

    const particles = new THREE.Points(particleGeo, particleMat);
    rootPivot.add(particles);

    // 6. Synaptic Neural Connections
    const maxConn = particleCount * 4;
    const linePositions = new Float32Array(maxConn * 6);
    const lineColors = new Float32Array(maxConn * 6);

    const lineGeo = new THREE.BufferGeometry();
    lineGeo.setAttribute('position', new THREE.BufferAttribute(linePositions, 3));
    lineGeo.setAttribute('color', new THREE.BufferAttribute(lineColors, 3));

    const lineMat = new THREE.LineBasicMaterial({
      vertexColors: true,
      transparent: true,
      opacity: 0.25,
      blending: THREE.AdditiveBlending
    });

    const lines = new THREE.LineSegments(lineGeo, lineMat);
    rootPivot.add(lines);

    // 7. Mouse Tracking Physics
    let mouseX = 0;
    let mouseY = 0;
    let targetX = 0;
    let targetY = 0;

    const onMouseMove = (e: MouseEvent) => {
      const halfW = window.innerWidth / 2;
      const halfH = window.innerHeight / 2;
      mouseX = (e.clientX - halfW) * 0.0005;
      mouseY = (e.clientY - halfH) * 0.0005;
    };

    window.addEventListener('mousemove', onMouseMove);

    // 8. Resize Handler
    const onResize = () => {
      if (!container) return;
      const w = container.clientWidth;
      const h = container.clientHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };

    window.addEventListener('resize', onResize);

    // 9. Animation Loop
    let animId: number;
    let prevMode = modeRef.current;
    let clock = new THREE.Clock();

    const animate = () => {
      animId = requestAnimationFrame(animate);
      const elapsed = clock.getElapsedTime();

      // Check mode changes
      if (prevMode !== modeRef.current) {
        prevMode = modeRef.current;
        computePositions(prevMode, targetPositions);
      }

      // Morph particles to target
      const pos = particleGeo.attributes.position.array as Float32Array;
      for (let i = 0; i < particleCount * 3; i++) {
        pos[i] += (targetPositions[i] - pos[i]) * 0.04;
      }
      particleGeo.attributes.position.needsUpdate = true;

      // Update Synaptic Lines
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
            const alpha = (1.0 - dist / maxDist) * 0.7;

            linePositions[lIdx++] = pos[i * 3];
            linePositions[lIdx++] = pos[i * 3 + 1];
            linePositions[lIdx++] = pos[i * 3 + 2];

            linePositions[lIdx++] = pos[j * 3];
            linePositions[lIdx++] = pos[j * 3 + 1];
            linePositions[lIdx++] = pos[j * 3 + 2];

            lineColors[cIdx++] = 0.02 * alpha;
            lineColors[cIdx++] = 0.71 * alpha;
            lineColors[cIdx++] = 0.83 * alpha;

            lineColors[cIdx++] = 0.54 * alpha;
            lineColors[cIdx++] = 0.36 * alpha;
            lineColors[cIdx++] = 0.96 * alpha;
          }
        }
      }

      lineGeo.setDrawRange(0, lIdx / 3);
      lineGeo.attributes.position.needsUpdate = true;
      lineGeo.attributes.color.needsUpdate = true;

      // Rotate geometric elements
      coreMesh.rotation.x = elapsed * 0.12;
      coreMesh.rotation.y = elapsed * 0.18;

      innerCoreMesh.rotation.y = -elapsed * 0.25;
      const pulseScale = 1.0 + Math.sin(elapsed * 2.5) * 0.08;
      innerCoreMesh.scale.set(pulseScale, pulseScale, pulseScale);

      ring1.rotation.z = elapsed * 0.2;
      ring2.rotation.x = elapsed * -0.15;
      ring3.rotation.y = elapsed * 0.18;

      // Mouse orientation damping
      targetX += (mouseX - targetX) * 0.04;
      targetY += (mouseY - targetY) * 0.04;

      rootPivot.rotation.y = elapsed * 0.04 + targetX * 1.2;
      rootPivot.rotation.x = Math.sin(elapsed * 0.02) * 0.05 + targetY * 1.2;

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
      coreGeo.dispose();
      coreWireMat.dispose();
      innerCoreGeo.dispose();
      innerCoreMat.dispose();
      ring1Geo.dispose();
      ring1Mat.dispose();
      ring2Geo.dispose();
      ring2Mat.dispose();
      ring3Geo.dispose();
      ring3Mat.dispose();
    };
  }, []);

  return (
    <div ref={containerRef} className={className} />
  );
};

export default ThreeHolographicGlobe;
