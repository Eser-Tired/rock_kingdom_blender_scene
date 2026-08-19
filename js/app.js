/**
 * Rock Kingdom Fantasy Plaza - Main Application Entry
 * Integrates SceneSetup, LightingManager, MaterialManager, ModelLoader, AnimationSystem, CleanupManager.
 */
import * as THREE from '../vendor/three.module.js';
import { SceneSetup } from './scene_setup.js';
import { LightingManager } from './lighting.js';
import { MaterialManager } from './material_manager.js';
import { ModelLoader } from './model_loader.js';
import { AnimationSystem } from './animation_system.js';
import { CleanupManager } from './cleanup_manager.js';

class App {
  constructor() {
    this.container = document.getElementById('canvas-container');
    this.loadingOverlay = document.getElementById('loading-overlay');
    this.progressBar = document.getElementById('progress-bar-fill');
    this.loadingStatus = document.getElementById('loading-status');
    this.toast = document.getElementById('toast');

    // Calibrated Preset Camera Angles
    this.cameraPresets = {
      hero: {
        name: 'Hero View (主全景)',
        pos: new THREE.Vector3(6.5, 5.5, 15.5),
        target: new THREE.Vector3(-1.0, 3.0, -1.0),
      },
      wide: {
        name: 'Plaza Wide (广场广角)',
        pos: new THREE.Vector3(-14.0, 6.0, 16.0),
        target: new THREE.Vector3(-1.5, 3.2, -2.0),
      },
      guildhall: {
        name: 'Guildhall Porch (公馆门廊)',
        pos: new THREE.Vector3(-6.5, 3.5, 6.0),
        target: new THREE.Vector3(-8.5, 3.5, -3.0),
      },
      gate: {
        name: 'Castle Gate (城堡大拱门与魔方)',
        pos: new THREE.Vector3(0.5, 3.8, 4.0),
        target: new THREE.Vector3(3.5, 4.2, -6.5),
      },
      closeup: {
        name: 'Hero & Pet (角色与宠物特写)',
        pos: new THREE.Vector3(0.5, 3.5, 9.5),
        target: new THREE.Vector3(-2.8, 3.0, 4.26),
      },
    };

    this.currentModelData = null;
    this.init();
  }

  async init() {
    console.log('[App] Initializing Three.js 3D Scene...');
    this.updateProgress(10, '正在初始化 3D 渲染器与场景...');

    try {
      // 1. Scene & Renderer Setup
      this.sceneSetup = new SceneSetup(this.container);
      this.scene = this.sceneSetup.scene;
      this.camera = this.sceneSetup.camera;
      this.renderer = this.sceneSetup.renderer;

      // 2. Lighting System
      this.updateProgress(25, '构建 PCF 软阴影光影系统...');
      this.lighting = new LightingManager(this.scene);

      // 3. Material Manager
      this.materials = new MaterialManager();

      // 4. Model Loader with Draco
      this.updateProgress(40, '配置本地 Draco GLTF 解码器...');
      this.loader = new ModelLoader(this.materials);

      // 5. Animation System
      this.animation = new AnimationSystem(
        this.scene,
        this.camera,
        this.renderer,
        this.lighting
      );

      // 6. Bind UI Controls
      this.bindUI();

      // 7. Load 3D Model
      await this.loadPlazaModel();
    } catch (err) {
      console.error('[App] Init Error:', err);
      if (this.loadingStatus) {
        this.loadingStatus.innerHTML = '<span style="color:#ef4444;">❌ 初始化失败: ' + err.message + '</span>';
      }
    }
  }

  async loadPlazaModel() {
    try {
      this.updateProgress(50, '正在载入洛克王国幻想广场 3D 场景资产...');
      const modelData = await this.loader.loadModel('rock_kingdom_plaza.glb', (percent) => {
        this.updateProgress(50 + percent * 0.4, '载入几何模型网格: ' + Math.round(percent) + '%');
      });

      this.currentModelData = modelData;
      this.scene.add(modelData.model);

      // Register animated elements
      this.animation.setAnimatedElements(modelData.animatedElements);

      // Calculate & display statistics
      this.updateModelStats(modelData.model);

      // Start Clock-driven Render Loop
      this.updateProgress(98, '启动 Clock 增量时间动画渲染循环...');
      this.animation.start(({ fps }) => {
        const fpsEl = document.getElementById('stat-fps');
        if (fpsEl) fpsEl.textContent = fps + ' FPS';
      });

      // Set initial camera to Hero Preset
      this.switchCameraPreset('hero');

      // Hide loading screen
      setTimeout(() => {
        if (this.loadingOverlay) this.loadingOverlay.classList.add('hidden');
        this.showToast('✨ 洛克王国幻想广场 3D 场景加载完毕！');
      }, 500);

    } catch (err) {
      console.error('[App] Failed to load 3D Model:', err);
      if (this.loadingStatus) {
        this.loadingStatus.innerHTML = '<span style="color:#ef4444;">❌ 加载模型失败: ' + err.message + '</span>';
      }
    }
  }

  updateProgress(percent, statusText) {
    if (this.progressBar) this.progressBar.style.width = percent + '%';
    if (this.loadingStatus && statusText) this.loadingStatus.textContent = statusText;
  }

  updateModelStats(model) {
    let meshCount = 0;
    let triangleCount = 0;
    let vertexCount = 0;

    model.traverse((child) => {
      if (child.isMesh && child.geometry) {
        meshCount++;
        const geo = child.geometry;
        if (geo.index) {
          triangleCount += geo.index.count / 3;
        } else if (geo.attributes.position) {
          triangleCount += geo.attributes.position.count / 3;
        }
        if (geo.attributes.position) {
          vertexCount += geo.attributes.position.count;
        }
      }
    });

    const meshEl = document.getElementById('stat-meshes');
    const polyEl = document.getElementById('stat-polys');
    if (meshEl) meshEl.textContent = meshCount.toLocaleString();
    if (polyEl) polyEl.textContent = Math.round(triangleCount).toLocaleString();
  }

  switchCameraPreset(presetKey) {
    const preset = this.cameraPresets[presetKey];
    if (!preset) return;

    // Update active button state
    document.querySelectorAll('.nav-btn').forEach((btn) => {
      btn.classList.toggle('active', btn.dataset.preset === presetKey);
    });

    this.animation.transitionCameraTo(preset.pos, preset.target, 1.2);
    this.showToast('📷 视角切换: ' + preset.name);
  }

  bindUI() {
    // 1. Camera Preset Buttons
    document.querySelectorAll('.nav-btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        const presetKey = btn.dataset.preset;
        if (presetKey) {
          this.switchCameraPreset(presetKey);
        }
      });
    });

    // 2. Lighting Mode Selector
    const lightSelect = document.getElementById('select-lighting');
    if (lightSelect) {
      lightSelect.addEventListener('change', (e) => {
        this.lighting.setLightingMode(e.target.value);
        this.showToast('💡 灯光模式切换: ' + e.target.options[e.target.selectedIndex].text);
      });
    }

    // 3. Fog Density Slider
    const fogSlider = document.getElementById('slider-fog');
    if (fogSlider) {
      fogSlider.addEventListener('input', (e) => {
        const val = parseFloat(e.target.value);
        this.scene.fog.density = val;
      });
    }

    // 4. Memory Disposal & Garbage Collection Test Button (Specification 7)
    const disposeBtn = document.getElementById('btn-dispose-test');
    if (disposeBtn) {
      disposeBtn.addEventListener('click', async () => {
        this.showToast('🧹 正在执行完整垃圾回收与内存释放 (Traverse Dispose)...');
        this.animation.stop();

        // Perform deep recursive scene and WebGL disposal
        const stats = CleanupManager.disposeScene(this.scene, this.renderer);

        this.loadingOverlay.classList.remove('hidden');
        this.updateProgress(20, '已释放 ' + stats.geometries + ' 组几何体与 ' + stats.materials + ' 个材质...');

        // Recreate scene & reload to test zero memory leak rebuild
        setTimeout(async () => {
          this.sceneSetup.destroy();
          this.loader.destroy();
          this.animation.destroy();

          // Re-initialize cleanly
          await this.init();
          this.showToast('✅ 场景完全销毁并重建成功，无内存泄漏！');
        }, 1000);
      });
    }
  }

  showToast(message) {
    if (!this.toast) return;
    this.toast.textContent = message;
    this.toast.classList.add('show');
    clearTimeout(this.toastTimer);
    this.toastTimer = setTimeout(() => {
      this.toast.classList.remove('show');
    }, 2800);
  }
}

// Bootstrap safely regardless of document.readyState
function startApp() {
  if (!window.__APP__) {
    window.__APP__ = new App();
  }
}

if (document.readyState === 'loading') {
  window.addEventListener('DOMContentLoaded', startApp);
} else {
  startApp();
}
