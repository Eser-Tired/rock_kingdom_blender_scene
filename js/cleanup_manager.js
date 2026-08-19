/**
 * CleanupManager: Recursively traverses the scene and disposes all geometries,
 * textures, materials, shadow maps, and clears WebGL caches.
 * Adheres strictly to Three.js Specification 7.
 */
import * as THREE from '../vendor/three.module.js';

export class CleanupManager {
  /**
   * Recursively dispose an object and its entire child hierarchy
   */
  static disposeObject(obj) {
    if (!obj) return;

    // Recursively process children first
    while (obj.children && obj.children.length > 0) {
      this.disposeObject(obj.children[0]);
      obj.remove(obj.children[0]);
    }

    // Dispose Geometry
    if (obj.geometry) {
      obj.geometry.dispose();
    }

    // Dispose Materials and associated Textures
    if (obj.material) {
      const materials = Array.isArray(obj.material) ? obj.material : [obj.material];
      materials.forEach((mat) => {
        if (!mat) return;
        // Dispose all active texture maps
        const textureKeys = [
          'map', 'normalMap', 'roughnessMap', 'metalnessMap',
          'emissiveMap', 'alphaMap', 'aoMap', 'displacementMap',
          'envMap', 'lightMap', 'bumpMap', 'clearcoatMap',
          'clearcoatRoughnessMap', 'transmissionMap', 'sheenColorMap'
        ];

        textureKeys.forEach((key) => {
          if (mat[key] && typeof mat[key].dispose === 'function') {
            mat[key].dispose();
          }
        });

        // Dispose the material itself
        if (typeof mat.dispose === 'function') {
          mat.dispose();
        }
      });
    }

    // Dispose Light Shadow Maps
    if (obj.isLight && obj.shadow && obj.shadow.map) {
      obj.shadow.map.dispose();
    }

    // Remove from parent if still attached
    if (obj.parent) {
      obj.parent.remove(obj);
    }
  }

  /**
   * Complete Scene & WebGL Context deallocation
   */
  static disposeScene(scene, renderer) {
    console.log('[CleanupManager] Starting complete memory cleanup and resource disposal...');

    let disposedCount = { geometries: 0, materials: 0, textures: 0, objects: 0 };

    if (scene) {
      scene.traverse((child) => {
        disposedCount.objects++;
        if (child.geometry) disposedCount.geometries++;
        if (child.material) {
          const mats = Array.isArray(child.material) ? child.material : [child.material];
          disposedCount.materials += mats.length;
        }
      });

      // Execute recursive disposal
      while (scene.children.length > 0) {
        this.disposeObject(scene.children[0]);
        scene.remove(scene.children[0]);
      }
      scene.clear();
    }

    if (renderer) {
      renderer.dispose();
      if (renderer.forceContextLoss) {
        renderer.forceContextLoss();
      }
    }

    console.log(
      '[CleanupManager] Memory disposal complete: ' + disposedCount.objects + ' objects, ' +
      disposedCount.geometries + ' geometries, ' + disposedCount.materials + ' materials purged.'
    );

    return disposedCount;
  }
}
