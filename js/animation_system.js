/**
 * AnimationSystem: Uses THREE.Clock with getDelta() to drive frame-rate independent
 * procedural animations, OrbitControls with damping, and camera transitions.
 * Adheres strictly to Three.js Specification 6.
 */
import * as THREE from '../vendor/three.module.js';
import { OrbitControls } from '../vendor/controls/OrbitControls.js';

export class AnimationSystem {
  constructor(scene, camera, renderer, lightingManager) {
    this.scene = scene;
    this.camera = camera;
    this.renderer = renderer;
    this.lightingManager = lightingManager;

    // 1. Frame-rate independent Clock
    this.clock = new THREE.Clock();
    this.isRunning = false;
    this.animationFrameId = null;

    // 2. OrbitControls with smooth damping
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.05;
    this.controls.maxPolarAngle = Math.PI / 2 - 0.02; // Restrict camera from dipping below ground
    this.controls.minDistance = 2.0;
    this.controls.maxDistance = 65.0;
    this.controls.target.set(0.0, 3.2, 0.0);

    // 3. Camera Transition System
    this.cameraTransition = {
      isTransitioning: false,
      startPos: new THREE.Vector3(),
      targetPos: new THREE.Vector3(),
      startLookAt: new THREE.Vector3(),
      targetLookAt: new THREE.Vector3(),
      progress: 0,
      duration: 1.2, // seconds
    };

    // 4. Animated Object References
    this.animatedElements = null;
    this.initialTransforms = new Map();

    // 5. FPS / Performance Counter
    this.fps = 60;
    this.framesThisSecond = 0;
    this.lastFpsUpdate = 0;
  }

  setAnimatedElements(elements) {
    this.animatedElements = elements;
    if (elements) {
      if (elements.magicCube) {
        elements.magicCube.forEach((cube) => {
          this.initialTransforms.set(cube, {
            pos: cube.position.clone(),
            rot: cube.rotation.clone(),
          });
        });
      }
      if (elements.sprite) {
        this.initialTransforms.set(elements.sprite, {
          pos: elements.sprite.position.clone(),
          rot: elements.sprite.rotation.clone(),
        });
      }
    }
  }

  start(onFrame) {
    if (this.isRunning) return;
    this.isRunning = true;
    this.clock.start();

    const loop = () => {
      if (!this.isRunning) return;
      this.animationFrameId = requestAnimationFrame(loop);

      // Extract delta time (seconds) for 60Hz / 120Hz / 144Hz consistency
      const delta = this.clock.getDelta();
      const elapsed = this.clock.getElapsedTime();

      // Measure FPS
      this.framesThisSecond++;
      if (elapsed - this.lastFpsUpdate >= 1.0) {
        this.fps = this.framesThisSecond;
        this.framesThisSecond = 0;
        this.lastFpsUpdate = elapsed;
      }

      // Update Procedural Scene Animations
      this.updateProceduralAnimations(delta, elapsed);

      // Update Lighting & Flicker
      if (this.lightingManager) {
        this.lightingManager.updateFlicker(elapsed);
      }

      // Update Camera Transition Lerp
      this.updateCameraTransition(delta);

      // Update OrbitControls with damping
      this.controls.update();

      // Render the frame
      this.renderer.render(this.scene, this.camera);

      if (onFrame) {
        onFrame({ fps: this.fps, delta, elapsed });
      }
    };

    loop();
  }

  updateProceduralAnimations(delta, elapsed) {
    if (!this.animatedElements) return;

    // 1. Floating Magic Cube: floating bob and rotational spin
    if (this.animatedElements.magicCube) {
      this.animatedElements.magicCube.forEach((cube, idx) => {
        const init = this.initialTransforms.get(cube);
        if (init) {
          const bob = Math.sin(elapsed * 2.2 + idx * 0.5) * 0.12;
          cube.position.y = init.pos.y + bob;
          cube.rotation.y += delta * 0.65;
          cube.rotation.x += delta * 0.35;
        }
      });
    }

    // 2. Fairy Sprite: gentle hovering
    if (this.animatedElements.sprite) {
      const init = this.initialTransforms.get(this.animatedElements.sprite);
      if (init) {
        const spriteBob = Math.sin(elapsed * 3.5) * 0.08;
        this.animatedElements.sprite.position.y = init.pos.y + spriteBob;
        this.animatedElements.sprite.rotation.y += delta * 1.2;
      }
    }

    // 3. Festival Bunting: subtle breeze sway
    if (this.animatedElements.bunting && this.animatedElements.bunting.length > 0) {
      this.animatedElements.bunting.forEach((flag, idx) => {
        flag.rotation.x = Math.sin(elapsed * 2.4 + idx * 0.3) * 0.06;
      });
    }

    // 4. Night Sky Motes: subtle floating
    if (this.animatedElements.motes && this.animatedElements.motes.length > 0) {
      this.animatedElements.motes.forEach((mote, idx) => {
        mote.position.y += Math.sin(elapsed * 1.5 + idx) * delta * 0.15;
      });
    }
  }

  transitionCameraTo(targetPosition, targetLookAt, duration = 1.2) {
    this.cameraTransition.startPos.copy(this.camera.position);
    this.cameraTransition.targetPos.copy(targetPosition);
    this.cameraTransition.startLookAt.copy(this.controls.target);
    this.cameraTransition.targetLookAt.copy(targetLookAt);
    this.cameraTransition.duration = duration;
    this.cameraTransition.progress = 0;
    this.cameraTransition.isTransitioning = true;
  }

  updateCameraTransition(delta) {
    if (!this.cameraTransition.isTransitioning) return;

    this.cameraTransition.progress += delta / this.cameraTransition.duration;
    const t = Math.min(this.cameraTransition.progress, 1.0);
    // Smooth ease-in-out curve
    const ease = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;

    this.camera.position.lerpVectors(
      this.cameraTransition.startPos,
      this.cameraTransition.targetPos,
      ease
    );

    this.controls.target.lerpVectors(
      this.cameraTransition.startLookAt,
      this.cameraTransition.targetLookAt,
      ease
    );

    if (t >= 1.0) {
      this.cameraTransition.isTransitioning = false;
    }
  }

  stop() {
    this.isRunning = false;
    if (this.animationFrameId !== null) {
      cancelAnimationFrame(this.animationFrameId);
      this.animationFrameId = null;
    }
  }

  destroy() {
    this.stop();
    if (this.controls) {
      this.controls.dispose();
    }
  }
}
