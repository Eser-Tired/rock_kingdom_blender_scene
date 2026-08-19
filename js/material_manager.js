/**
 * MaterialManager: Manages PBR materials, shadows, and emissive properties.
 * Adheres strictly to Three.js Specification 4 (MeshStandard/PhysicalMaterial, no MeshBasicMaterial).
 */
import * as THREE from '../vendor/three.module.js';

export class MaterialManager {
  constructor() {
    this.materials = new Map();
  }

  processModelMaterials(root) {
    root.traverse((child) => {
      if (child.isMesh) {
        // Enable shadow casting and receiving
        child.castShadow = true;
        child.receiveShadow = true;

        if (Array.isArray(child.material)) {
          child.material = child.material.map((mat) => this.upgradeMaterial(mat, child.name));
        } else if (child.material) {
          child.material = this.upgradeMaterial(child.material, child.name);
        }
      }
    });
  }

  upgradeMaterial(oldMat, meshName = '') {
    if (!oldMat) {
      return new THREE.MeshStandardMaterial({ color: 0xd0c0a8, roughness: 0.7, metalness: 0.05 });
    }

    // Strictly ensure MeshStandardMaterial / MeshPhysicalMaterial
    let newMat;
    if (oldMat.isMeshBasicMaterial || !oldMat.isMeshStandardMaterial) {
      newMat = new THREE.MeshStandardMaterial({
        color: oldMat.color ? oldMat.color.clone() : new THREE.Color(0xffffff),
        map: oldMat.map || null,
        roughness: oldMat.roughness !== undefined ? oldMat.roughness : 0.65,
        metalness: oldMat.metalness !== undefined ? oldMat.metalness : 0.05,
      });
    } else {
      newMat = oldMat;
    }

    const matName = (newMat.name || meshName).toLowerCase();

    // Specific PBR tuning for fantasy assets while preserving original vibrant baseColor
    if (matName.includes('gold') || matName.includes('crest') || matName.includes('ring') || matName.includes('crown')) {
      newMat.metalness = 0.85;
      newMat.roughness = 0.28;
    } else if (matName.includes('silver') || matName.includes('armor') || matName.includes('cuirass')) {
      newMat.metalness = 0.88;
      newMat.roughness = 0.22;
    } else if (matName.includes('lanternglow') || matName.includes('glow') || matName.includes('cube')) {
      newMat.emissive = newMat.color ? newMat.color.clone() : new THREE.Color(0xffaa22);
      newMat.emissiveIntensity = 2.8;
      newMat.roughness = 0.2;
    } else if (matName.includes('windowglow')) {
      newMat.emissive = new THREE.Color(0xff9918);
      newMat.emissiveIntensity = 2.2;
      newMat.roughness = 0.3;
    } else if (matName.includes('spriteglow')) {
      newMat.emissive = new THREE.Color(0x00e5ff);
      newMat.emissiveIntensity = 3.2;
      newMat.roughness = 0.15;
    } else if (matName.includes('stone') || matName.includes('pavement')) {
      newMat.roughness = 0.80;
      newMat.metalness = 0.02;
    } else if (matName.includes('roof')) {
      newMat.roughness = 0.60;
      newMat.metalness = 0.05;
    } else if (matName.includes('leaf') || matName.includes('foliage') || matName.includes('hedge')) {
      newMat.roughness = 0.75;
      newMat.metalness = 0.0;
    } else if (matName.includes('hair')) {
      newMat.roughness = 0.40;
      newMat.metalness = 0.05;
    } else if (matName.includes('skin')) {
      newMat.roughness = 0.58;
      newMat.metalness = 0.0;
    }

    newMat.needsUpdate = true;
    return newMat;
  }
}
