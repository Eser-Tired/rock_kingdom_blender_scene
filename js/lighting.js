/**
 * LightingManager: Configures Ambient, Hemisphere, Key Moonlight, Fill Rim Light,
 * and dynamic warm Point Lights attached to lanterns and glowing elements.
 * Strictly adheres to Three.js Specification 3 (PCFSoftShadowMap, 2048 mapSize, bias, tight bounds).
 */
import * as THREE from '../vendor/three.module.js';

export class LightingManager {
  constructor(scene) {
    this.scene = scene;
    this.pointLights = [];
    this.setupLights();
  }

  setupLights() {
    // 1. Ambient & Hemisphere Light for rich night-time base tones
    this.ambientLight = new THREE.AmbientLight(0x22324c, 0.45);
    this.scene.add(this.ambientLight);

    this.hemiLight = new THREE.HemisphereLight(0x486c96, 0x1e1826, 0.4);
    this.hemiLight.position.set(0, 30, 0);
    this.scene.add(this.hemiLight);

    // 2. Key Directional Moonlight shining from front-top-right across the plaza
    this.moonLight = new THREE.DirectionalLight(0xbdd6ff, 1.85);
    this.moonLight.position.set(14, 22, 18);
    this.moonLight.target.position.set(-1.0, 2.5, -2.0);
    this.moonLight.castShadow = true;
    this.scene.add(this.moonLight.target);

    // Shadow Map Resolution: strictly >= 2048x2048
    this.moonLight.shadow.mapSize.width = 2048;
    this.moonLight.shadow.mapSize.height = 2048;

    // Shadow Camera Frustum: tightly wrapping the plaza scene
    this.moonLight.shadow.camera.near = 0.5;
    this.moonLight.shadow.camera.far = 65.0;
    const d = 24;
    this.moonLight.shadow.camera.left = -d;
    this.moonLight.shadow.camera.right = d;
    this.moonLight.shadow.camera.top = d;
    this.moonLight.shadow.camera.bottom = -d;

    // Shadow Bias: tiny negative bias (-0.0002) and normalBias to prevent shadow acne
    this.moonLight.shadow.bias = -0.0002;
    this.moonLight.shadow.normalBias = 0.02;

    this.scene.add(this.moonLight);

    // 3. Secondary Cool Fill / Rim Light from behind for depth
    this.rimLight = new THREE.DirectionalLight(0x3a5684, 0.75);
    this.rimLight.position.set(-14, 18, -16);
    this.scene.add(this.rimLight);

    // 4. Accurate Point Lights placed at landmark assets
    const lampConfigs = [
      // Street Lamps along Plaza
      { pos: [-14.0, 3.8, 8.5], color: 0xffaa33, intensity: 22, dist: 14 },
      { pos: [-14.0, 3.8, 0.0], color: 0xffaa33, intensity: 22, dist: 14 },
      { pos: [-14.0, 3.8, -7.5], color: 0xffaa33, intensity: 22, dist: 14 },
      { pos: [14.0, 3.8, 8.5], color: 0xffaa33, intensity: 22, dist: 14 },
      { pos: [14.0, 3.8, 0.0], color: 0xffaa33, intensity: 22, dist: 14 },
      { pos: [14.0, 3.8, -7.5], color: 0xffaa33, intensity: 22, dist: 14 },

      // Magic Cube on Gate Left Pedestal
      { pos: [-0.35, 3.35, -3.85], color: 0xffbb22, intensity: 35, dist: 16, isMagicCube: true },

      // Guildhall Porch & Display Window
      { pos: [-7.06, 3.5, -3.11], color: 0xff9922, intensity: 25, dist: 14 },
      { pos: [-11.5, 3.0, -2.5], color: 0xff8818, intensity: 20, dist: 12 },

      // Castle Gate Archway Warm Torch Glow
      { pos: [4.51, 4.27, -7.13], color: 0xff7718, intensity: 30, dist: 18 },

      // Hero Character Front Warm Key & Sprite Glow
      { pos: [-3.14, 2.5, 5.8], color: 0xffdfaa, intensity: 10, dist: 7 },
      { pos: [-2.5, 3.2, 4.0], color: 0x00e5ff, intensity: 16, dist: 5, isSprite: true },
    ];

    lampConfigs.forEach((spec) => {
      const pl = new THREE.PointLight(spec.color, spec.intensity, spec.dist, 2.0);
      pl.position.set(spec.pos[0], spec.pos[1], spec.pos[2]);
      pl.userData = {
        baseIntensity: spec.intensity,
        flickerSeed: Math.random() * 100,
        isMagicCube: spec.isMagicCube || false,
        isSprite: spec.isSprite || false
      };
      this.scene.add(pl);
      this.pointLights.push(pl);
    });
  }

  updateFlicker(elapsed) {
    this.pointLights.forEach((pl) => {
      if (pl.userData.isMagicCube) {
        // Smooth magical breathing glow
        const pulse = 0.85 + Math.sin(elapsed * 2.5) * 0.18;
        pl.intensity = pl.userData.baseIntensity * pulse;
      } else if (pl.userData.isSprite) {
        const pulse = 0.8 + Math.sin(elapsed * 4.0) * 0.2;
        pl.intensity = pl.userData.baseIntensity * pulse;
      } else {
        // Natural subtle lantern flicker
        const noise = Math.sin(elapsed * 6.0 + pl.userData.flickerSeed) * 0.06 +
                      Math.cos(elapsed * 13.0 + pl.userData.flickerSeed) * 0.04;
        pl.intensity = pl.userData.baseIntensity * (1.0 + noise);
      }
    });
  }

  setLightingMode(mode) {
    if (mode === 'night') {
      this.ambientLight.color.setHex(0x22324c);
      this.ambientLight.intensity = 0.45;
      this.moonLight.color.setHex(0xbdd6ff);
      this.moonLight.intensity = 1.85;
      this.rimLight.color.setHex(0x3a5684);
      this.rimLight.intensity = 0.75;
    } else if (mode === 'moonlight') {
      this.ambientLight.color.setHex(0x142036);
      this.ambientLight.intensity = 0.35;
      this.moonLight.color.setHex(0xd0e4ff);
      this.moonLight.intensity = 2.4;
      this.rimLight.color.setHex(0x5070a8);
      this.rimLight.intensity = 0.9;
    } else if (mode === 'golden') {
      this.ambientLight.color.setHex(0x3a2818);
      this.ambientLight.intensity = 0.55;
      this.moonLight.color.setHex(0xffaa44);
      this.moonLight.intensity = 2.0;
      this.rimLight.color.setHex(0x884422);
      this.rimLight.intensity = 0.6;
    }
  }
}
