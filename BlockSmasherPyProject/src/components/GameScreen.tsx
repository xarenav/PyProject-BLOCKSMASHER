import { ArrowLeft, Pause, Play, RotateCcw } from 'lucide-react';
import { useEffect, useRef, useState } from 'react';
import { IconButton } from './IconButton';
import { GlassCard } from './GlassCard';
import { GameOverlay } from './GameOverlay';
import type { GameSettings } from './SettingsScreen';

interface GameScreenProps {
  onBack: () => void;
  levelId: number;
  settings: GameSettings;
  onLevelComplete: (levelId: number) => void;
}

interface Block {
  x: number;
  y: number;
  width: number;
  height: number;
  alive: boolean;
  color: string;
}

interface Ball {
  x: number;
  y: number;
  dx: number;
  dy: number;
  radius: number;
}

interface Paddle {
  x: number;
  y: number;
  width: number;
  height: number;
}

interface Particle {
  x: number;
  y: number;
  dx: number;
  dy: number;
  life: number;
  maxLife: number;
  size: number;
  color: string;
}

export function GameScreen({ onBack, levelId, settings, onLevelComplete }: GameScreenProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isPaused, setIsPaused] = useState(false);
  const [gameState, setGameState] = useState<'playing' | 'paused' | 'victory' | 'defeat'>('playing');
  const [score, setScore] = useState(0);
  const [lives, setLives] = useState(3);
  const [fps, setFps] = useState(60);
  
  const gameLoopRef = useRef<number>();
  const blocksRef = useRef<Block[]>([]);
  const ballRef = useRef<Ball | null>(null);
  const paddleRef = useRef<Paddle>({ x: 340, y: 560, width: 120, height: 15 });
  const particlesRef = useRef<Particle[]>([]);
  const keysRef = useRef<Set<string>>(new Set());
  const mouseXRef = useRef<number>(400);
  const lastFrameTimeRef = useRef<number>(0);
  const ballLaunchedRef = useRef(false);

  const CANVAS_WIDTH = 800;
  const CANVAS_HEIGHT = 600;

  // Seeded random number generator for consistent procedural generation
  const seededRandom = (seed: number) => {
    let state = seed;
    return () => {
      state = (state * 1664525 + 1013904223) % 4294967296;
      return state / 4294967296;
    };
  };

  // Generate blocks based on level
  const generateBlocksForLevel = (level: number): Block[] => {
    const blocks: Block[] = [];

    if (level === 1) {
      // Level 1: Classic grid
      const rows = 4;
      const cols = 6;
      const blockWidth = 60;
      const blockHeight = 25;
      const gapX = 5;
      const gapY = 5;
      const startX = 50;
      const startY = 50;

      for (let row = 0; row < rows; row++) {
        for (let col = 0; col < cols; col++) {
          blocks.push({
            x: startX + col * (blockWidth + gapX),
            y: startY + row * (blockHeight + gapY),
            width: blockWidth,
            height: blockHeight,
            alive: true,
            color: '#3b82f6',
          });
        }
      }
    } else if (level === 2) {
      // Level 2: 8 blocks in a circle
      const blockWidth = 70;
      const blockHeight = 25;
      const centerX = CANVAS_WIDTH / 2;
      const centerY = 200;
      const radius = 120;
      const numBlocks = 8;

      for (let i = 0; i < numBlocks; i++) {
        const angle = (i / numBlocks) * Math.PI * 2 - Math.PI / 2; // Start from top
        const x = centerX + Math.cos(angle) * radius - blockWidth / 2;
        const y = centerY + Math.sin(angle) * radius - blockHeight / 2;

        blocks.push({
          x,
          y,
          width: blockWidth,
          height: blockHeight,
          alive: true,
          color: '#7c3aed',
        });
      }
    } else if (level === 3) {
      // Level 3: Pyramid Power - Inverted pyramid formation
      const blockWidth = 55;
      const blockHeight = 22;
      const gapX = 8;
      const gapY = 8;
      const colors = ['#f97316', '#fb923c', '#fdba74', '#fed7aa']; // Orange gradient
      
      // Pyramid rows: 7, 6, 5, 4, 3, 2, 1
      const pyramidRows = [7, 6, 5, 4, 3, 2, 1];
      let startY = 50;
      
      pyramidRows.forEach((blocksInRow, rowIndex) => {
        const rowWidth = blocksInRow * blockWidth + (blocksInRow - 1) * gapX;
        const startX = (CANVAS_WIDTH - rowWidth) / 2;
        
        for (let i = 0; i < blocksInRow; i++) {
          blocks.push({
            x: startX + i * (blockWidth + gapX),
            y: startY,
            width: blockWidth,
            height: blockHeight,
            alive: true,
            color: colors[rowIndex % colors.length],
          });
        }
        startY += blockHeight + gapY;
      });
    } else if (level === 4) {
      // Level 4: Checkerboard - Alternating pattern
      const rows = 8;
      const cols = 8;
      const blockWidth = 55;
      const blockHeight = 22;
      const gapX = 4;
      const gapY = 4;
      const startX = (CANVAS_WIDTH - (cols * blockWidth + (cols - 1) * gapX)) / 2;
      const startY = 50;
      const color1 = '#06b6d4'; // Cyan
      const color2 = '#a855f7'; // Purple

      for (let row = 0; row < rows; row++) {
        for (let col = 0; col < cols; col++) {
          // Checkerboard pattern - only create blocks on alternating squares
          if ((row + col) % 2 === 0) {
            blocks.push({
              x: startX + col * (blockWidth + gapX),
              y: startY + row * (blockHeight + gapY),
              width: blockWidth,
              height: blockHeight,
              alive: true,
              color: row % 2 === 0 ? color1 : color2,
            });
          }
        }
      }
    } else if (level === 5) {
      // Level 5: The Fortress - Fortified layers forming a castle/fortress
      const blockWidth = 50;
      const blockHeight = 20;
      const gapX = 5;
      const gapY = 5;
      const colors = ['#dc2626', '#ef4444', '#f97316', '#fb923c']; // Red to orange gradient
      
      // Outer wall
      const outerWallBlocks = 12;
      const outerY = 50;
      const outerStartX = (CANVAS_WIDTH - (outerWallBlocks * blockWidth + (outerWallBlocks - 1) * gapX)) / 2;
      for (let i = 0; i < outerWallBlocks; i++) {
        blocks.push({
          x: outerStartX + i * (blockWidth + gapX),
          y: outerY,
          width: blockWidth,
          height: blockHeight,
          alive: true,
          color: colors[0],
        });
      }
      
      // Left tower (2 rows, 2 cols)
      for (let row = 0; row < 2; row++) {
        for (let col = 0; col < 2; col++) {
          blocks.push({
            x: outerStartX + col * (blockWidth + gapX),
            y: outerY + (row + 1) * (blockHeight + gapY),
            width: blockWidth,
            height: blockHeight,
            alive: true,
            color: colors[row + 1],
          });
        }
      }
      
      // Right tower (2 rows, 2 cols)
      for (let row = 0; row < 2; row++) {
        for (let col = 0; col < 2; col++) {
          blocks.push({
            x: outerStartX + (outerWallBlocks - 2 + col) * (blockWidth + gapX),
            y: outerY + (row + 1) * (blockHeight + gapY),
            width: blockWidth,
            height: blockHeight,
            alive: true,
            color: colors[row + 1],
          });
        }
      }
      
      // Inner wall - second layer
      const innerWallBlocks = 8;
      const innerY = outerY + (blockHeight + gapY) * 3;
      const innerStartX = (CANVAS_WIDTH - (innerWallBlocks * blockWidth + (innerWallBlocks - 1) * gapX)) / 2;
      for (let i = 0; i < innerWallBlocks; i++) {
        blocks.push({
          x: innerStartX + i * (blockWidth + gapX),
          y: innerY,
          width: blockWidth,
          height: blockHeight,
          alive: true,
          color: colors[1],
        });
      }
      
      // Core - central fortified area (3x2)
      const coreBlocks = 4;
      const coreY = innerY + (blockHeight + gapY);
      const coreStartX = (CANVAS_WIDTH - (coreBlocks * blockWidth + (coreBlocks - 1) * gapX)) / 2;
      for (let row = 0; row < 2; row++) {
        for (let col = 0; col < coreBlocks; col++) {
          blocks.push({
            x: coreStartX + col * (blockWidth + gapX),
            y: coreY + row * (blockHeight + gapY),
            width: blockWidth,
            height: blockHeight,
            alive: true,
            color: colors[3],
          });
        }
      }
    } else if (level === 6) {
      // Level 6: Explosive Chaos - Procedurally generated with seeded randomness
      const random = seededRandom(12345); // Fixed seed for consistent generation
      const colors = ['#f97316', '#06b6d4', '#a855f7', '#ec4899', '#eab308'];
      const margin = 50;
      const maxY = 420; // Keep away from paddle
      
      // Procedurally generate 10-12 clusters
      const numClusters = 10;
      const patterns = ['tight', 'scattered', 'line', 'arc'];
      
      for (let c = 0; c < numClusters; c++) {
        // Random cluster properties using seeded RNG
        const clusterX = margin + random() * (CANVAS_WIDTH - margin * 2 - 150);
        const clusterY = margin + random() * (maxY - margin - 100);
        const pattern = patterns[Math.floor(random() * patterns.length)];
        const blockCount = 5 + Math.floor(random() * 4); // 5-8 blocks per cluster
        const color = colors[Math.floor(random() * colors.length)];
        const blockWidth = 40 + random() * 15; // 40-55
        const blockHeight = 18 + random() * 8; // 18-26
        
        if (pattern === 'tight') {
          // Compact grid
          const rows = 2;
          const cols = Math.ceil(blockCount / rows);
          const gap = 4 + random() * 3;
          
          for (let i = 0; i < blockCount; i++) {
            const row = Math.floor(i / cols);
            const col = i % cols;
            const x = clusterX + col * (blockWidth + gap);
            const y = clusterY + row * (blockHeight + gap);
            
            if (x >= margin && x + blockWidth <= CANVAS_WIDTH - margin && 
                y >= margin && y + blockHeight <= maxY) {
              blocks.push({
                x, y,
                width: blockWidth,
                height: blockHeight,
                alive: true,
                color: color,
              });
            }
          }
        } else if (pattern === 'scattered') {
          // Scattered circle
          const radius = 25 + random() * 30;
          
          for (let i = 0; i < blockCount; i++) {
            const angle = (i / blockCount) * Math.PI * 2 + random() * 0.5;
            const r = radius * (0.7 + random() * 0.6);
            const x = clusterX + Math.cos(angle) * r;
            const y = clusterY + Math.sin(angle) * r;
            
            if (x >= margin && x + blockWidth <= CANVAS_WIDTH - margin && 
                y >= margin && y + blockHeight <= maxY) {
              blocks.push({
                x, y,
                width: blockWidth,
                height: blockHeight,
                alive: true,
                color: color,
              });
            }
          }
        } else if (pattern === 'line') {
          // Linear with variation
          const angle = random() * Math.PI / 4 - Math.PI / 8; // -22.5 to 22.5 degrees
          const spacing = blockWidth + 3 + random() * 5;
          
          for (let i = 0; i < blockCount; i++) {
            const x = clusterX + i * spacing * Math.cos(angle);
            const y = clusterY + i * spacing * Math.sin(angle) + Math.sin(i * 0.8) * 10;
            
            if (x >= margin && x + blockWidth <= CANVAS_WIDTH - margin && 
                y >= margin && y + blockHeight <= maxY) {
              blocks.push({
                x, y,
                width: blockWidth,
                height: blockHeight,
                alive: true,
                color: color,
              });
            }
          }
        } else if (pattern === 'arc') {
          // Arc/curve pattern
          const arcRadius = 40 + random() * 40;
          const startAngle = random() * Math.PI;
          const arcLength = Math.PI * 0.6 + random() * Math.PI * 0.4;
          
          for (let i = 0; i < blockCount; i++) {
            const t = i / (blockCount - 1 || 1);
            const angle = startAngle + t * arcLength;
            const x = clusterX + Math.cos(angle) * arcRadius;
            const y = clusterY + Math.sin(angle) * arcRadius;
            
            if (x >= margin && x + blockWidth <= CANVAS_WIDTH - margin && 
                y >= margin && y + blockHeight <= maxY) {
              blocks.push({
                x, y,
                width: blockWidth,
                height: blockHeight,
                alive: true,
                color: color,
              });
            }
          }
        }
      }
    } else if (level >= 100) {
      // Procedural levels (100+)
      const random = seededRandom(level); // Use level ID as seed
      const colors = ['#f97316', '#06b6d4', '#a855f7', '#ec4899', '#eab308'];
      const margin = 50;
      const maxY = 420;
      
      // Difficulty scaling based on level number
      const levelDifficulty = (level - 100) % 12; // 0-11 for first 12 levels, then repeats
      const numClusters = 6 + Math.floor(levelDifficulty / 2); // 6-11 clusters
      const patterns = ['tight', 'scattered', 'line', 'arc', 'spiral'];
      
      for (let c = 0; c < numClusters; c++) {
        // Generate cluster properties
        const clusterX = margin + random() * (CANVAS_WIDTH - margin * 2 - 150);
        const clusterY = margin + random() * (maxY - margin - 100);
        const pattern = patterns[Math.floor(random() * patterns.length)];
        const blockCount = 4 + Math.floor(random() * 6); // 4-9 blocks per cluster
        const color = colors[Math.floor(random() * colors.length)];
        const blockWidth = 35 + random() * 20; // 35-55
        const blockHeight = 18 + random() * 10; // 18-28
        
        if (pattern === 'tight') {
          // Compact grid
          const rows = 2;
          const cols = Math.ceil(blockCount / rows);
          const gap = 3 + random() * 4;
          
          for (let i = 0; i < blockCount; i++) {
            const row = Math.floor(i / cols);
            const col = i % cols;
            const x = clusterX + col * (blockWidth + gap);
            const y = clusterY + row * (blockHeight + gap);
            
            if (x >= margin && x + blockWidth <= CANVAS_WIDTH - margin && 
                y >= margin && y + blockHeight <= maxY) {
              blocks.push({ x, y, width: blockWidth, height: blockHeight, alive: true, color });
            }
          }
        } else if (pattern === 'scattered') {
          // Scattered circle
          const radius = 25 + random() * 35;
          
          for (let i = 0; i < blockCount; i++) {
            const angle = (i / blockCount) * Math.PI * 2 + random() * 0.6;
            const r = radius * (0.6 + random() * 0.7);
            const x = clusterX + Math.cos(angle) * r;
            const y = clusterY + Math.sin(angle) * r;
            
            if (x >= margin && x + blockWidth <= CANVAS_WIDTH - margin && 
                y >= margin && y + blockHeight <= maxY) {
              blocks.push({ x, y, width: blockWidth, height: blockHeight, alive: true, color });
            }
          }
        } else if (pattern === 'line') {
          // Linear with variation
          const angle = random() * Math.PI / 3 - Math.PI / 6; // -30 to 30 degrees
          const spacing = blockWidth + 2 + random() * 6;
          
          for (let i = 0; i < blockCount; i++) {
            const x = clusterX + i * spacing * Math.cos(angle);
            const y = clusterY + i * spacing * Math.sin(angle) + Math.sin(i * 0.9) * 12;
            
            if (x >= margin && x + blockWidth <= CANVAS_WIDTH - margin && 
                y >= margin && y + blockHeight <= maxY) {
              blocks.push({ x, y, width: blockWidth, height: blockHeight, alive: true, color });
            }
          }
        } else if (pattern === 'arc') {
          // Arc/curve pattern
          const arcRadius = 35 + random() * 50;
          const startAngle = random() * Math.PI;
          const arcLength = Math.PI * 0.5 + random() * Math.PI * 0.6;
          
          for (let i = 0; i < blockCount; i++) {
            const t = i / (blockCount - 1 || 1);
            const angle = startAngle + t * arcLength;
            const x = clusterX + Math.cos(angle) * arcRadius;
            const y = clusterY + Math.sin(angle) * arcRadius;
            
            if (x >= margin && x + blockWidth <= CANVAS_WIDTH - margin && 
                y >= margin && y + blockHeight <= maxY) {
              blocks.push({ x, y, width: blockWidth, height: blockHeight, alive: true, color });
            }
          }
        } else if (pattern === 'spiral') {
          // Spiral pattern
          const spiralTightness = 3 + random() * 4;
          
          for (let i = 0; i < blockCount; i++) {
            const angle = (i / blockCount) * Math.PI * 2 * 1.5;
            const radius = 10 + (i / blockCount) * spiralTightness * 15;
            const x = clusterX + Math.cos(angle) * radius;
            const y = clusterY + Math.sin(angle) * radius;
            
            if (x >= margin && x + blockWidth <= CANVAS_WIDTH - margin && 
                y >= margin && y + blockHeight <= maxY) {
              blocks.push({ x, y, width: blockWidth, height: blockHeight, alive: true, color });
            }
          }
        }
      }
    }

    return blocks;
  };

  // Initialize blocks for level
  useEffect(() => {
    blocksRef.current = generateBlocksForLevel(levelId);
  }, [levelId]);

  // Initialize ball on paddle
  useEffect(() => {
    ballRef.current = {
      x: paddleRef.current.x + paddleRef.current.width / 2,
      y: paddleRef.current.y - 10,
      dx: 0,
      dy: 0,
      radius: 8,
    };
    ballLaunchedRef.current = false;
  }, [levelId]);

  // Keyboard controls
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      keysRef.current.add(e.key);
      if (e.key === ' ' && !ballLaunchedRef.current && ballRef.current) {
        // Launch ball
        const angle = (Math.random() - 0.5) * Math.PI / 3; // -30 to +30 degrees
        const speed = 4;
        ballRef.current.dx = Math.sin(angle) * speed;
        ballRef.current.dy = -Math.cos(angle) * speed;
        ballLaunchedRef.current = true;
      }
    };

    const handleKeyUp = (e: KeyboardEvent) => {
      keysRef.current.delete(e.key);
    };

    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
    };
  }, []);

  // Mouse controls
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const handleMouseMove = (e: MouseEvent) => {
      const rect = canvas.getBoundingClientRect();
      mouseXRef.current = ((e.clientX - rect.left) / rect.width) * CANVAS_WIDTH;
    };

    const handleClick = () => {
      if (!ballLaunchedRef.current && ballRef.current) {
        const angle = (Math.random() - 0.5) * Math.PI / 3;
        const speed = 4;
        ballRef.current.dx = Math.sin(angle) * speed;
        ballRef.current.dy = -Math.cos(angle) * speed;
        ballLaunchedRef.current = true;
      }
    };

    canvas.addEventListener('mousemove', handleMouseMove);
    canvas.addEventListener('click', handleClick);

    return () => {
      canvas.removeEventListener('mousemove', handleMouseMove);
      canvas.removeEventListener('click', handleClick);
    };
  }, []);

  // Game loop
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationFrameId: number;
    let fpsCounter = 0;
    let fpsTime = performance.now();

    const createParticles = (x: number, y: number, count: number, color: string) => {
      if (!settings.particleEffects) return;
      
      for (let i = 0; i < count; i++) {
        particlesRef.current.push({
          x,
          y,
          dx: (Math.random() - 0.5) * 4,
          dy: (Math.random() - 0.5) * 4,
          life: 1,
          maxLife: 1,
          size: Math.random() * 3 + 2,
          color,
        });
      }
    };

    const gameLoop = (timestamp: number) => {
      if (gameState !== 'playing') {
        animationFrameId = requestAnimationFrame(gameLoop);
        return;
      }

      const deltaTime = timestamp - lastFrameTimeRef.current;
      lastFrameTimeRef.current = timestamp;

      // FPS counter
      fpsCounter++;
      if (timestamp - fpsTime >= 1000) {
        setFps(fpsCounter);
        fpsCounter = 0;
        fpsTime = timestamp;
      }

      // Clear canvas
      ctx.fillStyle = '#0a0e1a';
      ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

      // Draw gradient background
      const gradient = ctx.createLinearGradient(0, 0, 0, CANVAS_HEIGHT);
      gradient.addColorStop(0, 'rgba(10, 14, 26, 0.5)');
      gradient.addColorStop(1, 'rgba(10, 14, 26, 1)');
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

      // Update paddle
      const paddle = paddleRef.current;
      if (keysRef.current.has('ArrowLeft')) {
        paddle.x = Math.max(0, paddle.x - 8);
      }
      if (keysRef.current.has('ArrowRight')) {
        paddle.x = Math.min(CANVAS_WIDTH - paddle.width, paddle.x + 8);
      }
      // Mouse control
      paddle.x = Math.max(0, Math.min(CANVAS_WIDTH - paddle.width, mouseXRef.current - paddle.width / 2));

      // Draw paddle
      const paddleGradient = ctx.createLinearGradient(paddle.x, 0, paddle.x + paddle.width, 0);
      paddleGradient.addColorStop(0, '#00d9ff');
      paddleGradient.addColorStop(0.5, '#7c3aed');
      paddleGradient.addColorStop(1, '#ff00ff');
      ctx.fillStyle = paddleGradient;
      ctx.shadowColor = '#00d9ff';
      ctx.shadowBlur = 15;
      ctx.fillRect(paddle.x, paddle.y, paddle.width, paddle.height);
      ctx.shadowBlur = 0;

      // Update and draw ball
      const ball = ballRef.current;
      if (ball) {
        if (ballLaunchedRef.current) {
          ball.x += ball.dx;
          ball.y += ball.dy;

          // Wall collisions
          if (ball.x - ball.radius <= 0 || ball.x + ball.radius >= CANVAS_WIDTH) {
            ball.dx = -ball.dx;
            createParticles(ball.x, ball.y, 5, '#00d9ff');
          }
          if (ball.y - ball.radius <= 0) {
            ball.dy = -ball.dy;
            createParticles(ball.x, ball.y, 5, '#00d9ff');
          }

          // Paddle collision
          if (
            ball.y + ball.radius >= paddle.y &&
            ball.y - ball.radius <= paddle.y + paddle.height &&
            ball.x >= paddle.x &&
            ball.x <= paddle.x + paddle.width
          ) {
            ball.dy = -Math.abs(ball.dy);
            // Angle based on hit position
            const hitPos = (ball.x - paddle.x) / paddle.width; // 0 to 1
            const angle = (hitPos - 0.5) * Math.PI / 1.5; // -60 to +60 degrees
            const speed = Math.sqrt(ball.dx * ball.dx + ball.dy * ball.dy);
            ball.dx = Math.sin(angle) * speed;
            ball.dy = -Math.abs(Math.cos(angle) * speed);
            createParticles(ball.x, paddle.y, 8, '#7c3aed');
          }

          // Block collisions
          blocksRef.current.forEach((block) => {
            if (!block.alive) return;

            if (
              ball.x + ball.radius >= block.x &&
              ball.x - ball.radius <= block.x + block.width &&
              ball.y + ball.radius >= block.y &&
              ball.y - ball.radius <= block.y + block.height
            ) {
              block.alive = false;
              ball.dy = -ball.dy;
              setScore((s) => s + 10);
              createParticles(block.x + block.width / 2, block.y + block.height / 2, 15, block.color);
            }
          });

          // Ball out of bounds (bottom)
          if (ball.y - ball.radius > CANVAS_HEIGHT) {
            setLives((l) => {
              const newLives = l - 1;
              if (newLives <= 0) {
                setGameState('defeat');
              } else {
                // Reset ball
                ball.x = paddle.x + paddle.width / 2;
                ball.y = paddle.y - 10;
                ball.dx = 0;
                ball.dy = 0;
                ballLaunchedRef.current = false;
              }
              return newLives;
            });
          }
        } else {
          // Ball follows paddle before launch
          ball.x = paddle.x + paddle.width / 2;
          ball.y = paddle.y - 10;
        }

        // Draw ball with glow
        ctx.fillStyle = '#00d9ff';
        ctx.shadowColor = '#00d9ff';
        ctx.shadowBlur = 20;
        ctx.beginPath();
        ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
        ctx.fill();
        ctx.shadowBlur = 0;
      }

      // Draw blocks
      blocksRef.current.forEach((block) => {
        if (!block.alive) return;

        ctx.fillStyle = block.color;
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.3)';
        ctx.lineWidth = 2;
        ctx.fillRect(block.x, block.y, block.width, block.height);
        ctx.strokeRect(block.x, block.y, block.width, block.height);
      });

      // Update and draw particles
      particlesRef.current = particlesRef.current.filter((particle) => {
        particle.x += particle.dx;
        particle.y += particle.dy;
        particle.life -= 0.016;

        if (particle.life > 0) {
          ctx.fillStyle = particle.color;
          ctx.globalAlpha = particle.life / particle.maxLife;
          ctx.beginPath();
          ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
          ctx.fill();
          ctx.globalAlpha = 1;
          return true;
        }
        return false;
      });

      // Check victory
      if (blocksRef.current.every((block) => !block.alive)) {
        setGameState('victory');
        onLevelComplete(levelId);
      }

      animationFrameId = requestAnimationFrame(gameLoop);
    };

    animationFrameId = requestAnimationFrame(gameLoop);

    return () => {
      if (animationFrameId) {
        cancelAnimationFrame(animationFrameId);
      }
    };
  }, [gameState, settings.particleEffects]);

  const handleRestart = () => {
    setScore(0);
    setLives(3);
    setGameState('playing');
    ballLaunchedRef.current = false;
    particlesRef.current = [];
    
    // Reset blocks using level generator
    blocksRef.current = generateBlocksForLevel(levelId);

    // Reset ball
    ballRef.current = {
      x: paddleRef.current.x + paddleRef.current.width / 2,
      y: paddleRef.current.y - 10,
      dx: 0,
      dy: 0,
      radius: 8,
    };
  };

  const togglePause = () => {
    if (gameState === 'playing') {
      setGameState('paused');
    } else if (gameState === 'paused') {
      setGameState('playing');
    }
  };

  return (
    <div className="relative w-full min-h-screen p-8">
      {/* Background */}
      <div 
        className="absolute inset-0 -z-10"
        style={{
          background: `
            radial-gradient(circle at 20% 20%, rgba(64, 224, 208, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(255, 140, 0, 0.1) 0%, transparent 50%),
            var(--bg-dark)
          `,
        }}
      />

      <div className="max-w-5xl mx-auto">
        <GlassCard className="p-6">
          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-4">
              <IconButton size="md" onClick={onBack}>
                <ArrowLeft size={20} />
              </IconButton>
              <div>
                <h2 className="text-xl font-bold" style={{ color: 'var(--color-cyan)' }}>
                  {levelId >= 100 ? `Random Level #${levelId - 99}` : `Level ${levelId}`}
                </h2>
                <div className="flex gap-4 text-sm text-[var(--color-foreground)]/60 mt-1">
                  <span>Score: {score}</span>
                  <span>Lives: {lives}</span>
                  {settings.showFPS && <span>FPS: {fps}</span>}
                </div>
              </div>
            </div>
            <div className="flex gap-2">
              <IconButton size="md" onClick={togglePause}>
                {gameState === 'playing' ? <Pause size={16} /> : <Play size={16} />}
              </IconButton>
              <IconButton size="md" onClick={handleRestart}>
                <RotateCcw size={16} />
              </IconButton>
            </div>
          </div>

          {/* Game Canvas */}
          <div className="relative">
            <canvas
              ref={canvasRef}
              width={CANVAS_WIDTH}
              height={CANVAS_HEIGHT}
              className="w-full rounded-lg border-2"
              style={{
                borderColor: 'rgba(64, 224, 208, 0.3)',
                maxWidth: '100%',
                height: 'auto',
              }}
            />

            {/* Overlays */}
            {gameState === 'paused' && (
              <GameOverlay
                type="pause"
                score={score}
                onRestart={handleRestart}
                onMenu={onBack}
                onResume={togglePause}
              />
            )}
            {gameState === 'victory' && (
              <GameOverlay
                type="victory"
                score={score}
                onRestart={handleRestart}
                onMenu={onBack}
              />
            )}
            {gameState === 'defeat' && (
              <GameOverlay
                type="defeat"
                score={score}
                onRestart={handleRestart}
                onMenu={onBack}
              />
            )}
          </div>

          {/* Controls Info */}
          <p className="text-center text-sm text-[var(--color-foreground)]/60 mt-4">
            Move paddle: Mouse or Arrow Keys | Launch ball: Click or Space
          </p>
        </GlassCard>
      </div>
    </div>
  );
}
