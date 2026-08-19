/**
 * SceneSetup: Manages WebGLRenderer, PerspectiveCamera, Viewport Resize, and Fog.
 * Adheres strictly to Three.js Specifications 1, 2, and 4.
 */
import * as THREE from '../vendor/three.module.js';

export class SceneSetup {
  constructor(container) {
    this.container = container;
    this.width = container.clientWidth || window.innerWidth;
    this.height = container.clientHeight || window.innerHeight;

    // 1. WebGLRenderer with Antialiasing, SRGBColorSpace, ACESFilmicToneMapping
    this.renderer = new THREE.WebGLRenderer({
      canvas: document.getElementById('webgl-canvas'),
      antialias: true,
      powerPreference: 'high-performance',
      alpha: false,
    });
    this.renderer.setSize(this.width, this.height);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.outputColorSpace = THREE.SRGBColorSpace;
    this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 1.0;
    
    // Enable PCF Soft Shadows
    this.renderer.shadowMap.enabled = true;
    this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;

    // 2. PerspectiveCamera with reasonable near / far to prevent Z-fighting
    this.camera = new THREE.PerspectiveCamera(
      45,
      this.width / this.height,
      0.2,   // Safe near clipping plane (avoids Z-fighting)
      120.0  // Bounded far clipping plane
    );
    this.camera.position.set(9.6, 6.8, 19.0);

    // 3. Scene and Gentle Atmospheric Fog (0.0035 keeps foreground vivid)
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x060c18);
    this.fog = new THREE.FogExp2(0x060c18, 0.0035);
    this.scene.fog = this.fog;

    // 4. Responsive Viewport Resize Handling
    this.onWindowResize = this.onWindowResize.bind(this);
    window.addEventListener('resize', this.onWindowResize);
  }

  onWindowResize() {
    this.width = this.container.clientWidth || window.innerWidth;
    this.height = this.container.clientHeight || window.innerHeight;

    this.camera.aspect = this.width / this.height;
    this.camera.updateProjectionMatrix();

    this.renderer.setSize(this.width, this.height);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  }

  destroy() {
    window.removeEventListener('resize', this.onWindowResize);
  }
}
