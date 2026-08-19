/**
 * ModelLoader: Loads GLTF/GLB with DRACOLoader, centers geometry via Box3,
 * and aligns bottom min.y to the ground plane.
 * Adheres strictly to Three.js Specification 5.
 */
import * as THREE from '../vendor/three.module.js';
import { GLTFLoader } from '../vendor/loaders/GLTFLoader.js';
import { DRACOLoader } from '../vendor/loaders/DRACOLoader.js';

export class ModelLoader {
  constructor(materialManager) {
    this.materialManager = materialManager;
    this.loader = new GLTFLoader();

    // Configure DRACOLoader with local vendor decoder path
    this.dracoLoader = new DRACOLoader();
    this.dracoLoader.setDecoderPath('./vendor/draco/');
    this.dracoLoader.setDecoderConfig({ type: 'js' });
    this.loader.setDRACOLoader(this.dracoLoader);
  }

  loadModel(url, onProgress) {
    return new Promise((resolve, reject) => {
      this.loader.load(
        url,
        (gltf) => {
          const model = gltf.scene;

          // 1. Remove raw 40,000-lumen glTF lights imported from Blender
          const lightsToRemove = [];
          model.traverse((child) => {
            if (child.isLight) {
              lightsToRemove.push(child);
            }
          });
          lightsToRemove.forEach((light) => {
            if (light.parent) light.parent.remove(light);
            if (light.dispose) light.dispose();
          });

          // 2. Process and upgrade all materials to standard PBR
          this.materialManager.processModelMaterials(model);

          // 2. Compute exact World Bounding Box via Box3
          const box = new THREE.Box3().setFromObject(model);
          const size = box.getSize(new THREE.Vector3());
          const center = box.getCenter(new THREE.Vector3());

          // 3. Center horizontally (X and Z to origin)
          model.position.x = -center.x;
          model.position.z = -center.z;

          // 4. Align bottom edge (min.y) perfectly onto ground plane (y = 0)
          model.position.y = -box.min.y;

          // Collect dynamic objects for procedural animations
          const animatedElements = {
            magicCube: null,
            sprite: null,
            bunting: [],
            motes: [],
          };

          model.traverse((child) => {
            const name = child.name || '';
            if (name.includes('MagicCube') || name.includes('floating_lantern')) {
              if (name.includes('Outer') || name.includes('Core')) {
                animatedElements.magicCube = animatedElements.magicCube || [];
                animatedElements.magicCube.push(child);
              }
            } else if (name.includes('Sprite') || name.includes('RK_Light_Sprite')) {
              animatedElements.sprite = child;
            } else if (name.includes('Bunting')) {
              animatedElements.bunting.push(child);
            } else if (name.includes('SkyMote')) {
              animatedElements.motes.push(child);
            }
          });

          resolve({
            model,
            box,
            size,
            center,
            animatedElements,
            gltf,
          });
        },
        (xhr) => {
          if (xhr.lengthComputable && onProgress) {
            const percent = (xhr.loaded / xhr.total) * 100;
            onProgress(percent);
          }
        },
        (error) => {
          console.error('Error loading 3D model:', error);
          reject(error);
        }
      );
    });
  }

  destroy() {
    if (this.dracoLoader) {
      this.dracoLoader.dispose();
    }
  }
}
