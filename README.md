# 洛克王国幻想广场 3D 场景与 WebGL 交互系统 (Rock Kingdom Fantasy Plaza 3D)

基于多视角实机参考图，通过 Blender 程序化建模精修还原并构建的高性能 Three.js 3D Web 交互场景项目。

## 场景特色与多视角精修还原

- **卡通 PBR 渲染风格**：低噪声节点材质、暖色建筑与灯火、冷蓝月光夜空、红瓦与米白石材、秋季植被。
- **完整场景元素精修**：
  - **城堡大拱门与阶梯**：包含主拱门、皇家盾徽、红金垂旗、阶梯红地毯、阶梯花台立柱与**悬浮旋转发光魔方水晶灯**、银甲守卫骑士。
  - **公馆与花市门廊**：3 柱式门廊、门廊悬吊陶盆花篮、向日葵花坛、蓝色绣球花摊位、圆塔拱门与水晶风向标、店员 NPC。
  - **前景主广场**：中央星形徽记与环形铺装、卷涡纹铁艺路灯、叠层陶罐花柱雕塑、节日三角彩旗挂绳、秋季金橙树林与高耸柏树。
  - **中心角色与伙伴**：Q 版主角（分层渐变发束、红蝴蝶结、王冠宝石、皮带扣饰与羽毛裙）、陪伴宠物与浮空发光精灵水母。

## Three.js Web 3D 场景工程规范落地

本项目 Web 3D 代码严格按照 7 大生产级规范编写：

1. **渲染器与相机基础配置**：开启 `antialias: true`，设置 `outputColorSpace = SRGBColorSpace`，启用 `ACESFilmicToneMapping`；相机 near (0.2) 与 far (120.0) 严密约束，杜绝 Z-fighting。
2. **响应式视口自适应**：监听 `resize` 事件，动态更新相机 `aspect` 与投影矩阵，同步重置 `renderer.setSize` 与 `renderer.setPixelRatio(Math.min(devicePixelRatio, 2))`。
3. **光影与阴影系统**：环境光 + 半球光 + PCFSoftShadowMap 软阴影平行月光；阴影贴图分辨率 `2048x2048`，阴影相机紧凑包裹，微小偏置 `bias: -0.0002` 防止条纹。
4. **材质与雾效**：严禁 `MeshBasicMaterial`，全量使用 `MeshStandardMaterial` / `MeshPhysicalMaterial`；配置微弱指数雾 `FogExp2` 增强夜空深邃感。
5. **模型加载与对齐**：启用 `DRACOLoader` 解压加载 GLB 模型；通过 `Box3` 计算几何中心归零，对齐 `min.y` 保证底部与地面完全贴合。
6. **动画平滑度**：采用 `THREE.Clock` 与 `getDelta()` 驱动浮空魔方、小精灵、彩旗微风摆动，确保在 60Hz/120Hz/144Hz 屏幕上恒速物理运行；`OrbitControls` 开启 `enableDamping = true` 并在每帧调用 `controls.update()`。
7. **垃圾回收与内存释放**：提供完整的 `CleanupManager.disposeScene()` 递归遍历释放 Geometry、Material、Texture 与 WebGL 缓存，支持无内存泄漏的热重载。

## 目录结构

- `rock_kingdom_fantasy_plaza.blend` - 核心 Blender 3D 场景源文件
- `rock_kingdom_plaza.glb` - 导出的 Draco 压缩 GLB 模型文件
- `index.html` - Three.js Web 3D 交互主页面
- `style.css` - 幻想风格 HUD 与响应式控制面板样式
- `js/` - 模块化 Three.js 核心代码：
  - `js/app.js` - 应用总控制器与 UI 交互绑定
  - `js/scene_setup.js` - 渲染器、相机、Resize 监听与 FogExp2 雾效
  - `js/lighting.js` - PCFSoftShadowMap 软阴影光照与点光源呼吸
  - `js/material_manager.js` - PBR 材质与高光/发光配置
  - `js/model_loader.js` - Draco GLTF 加载与 Box3 贴地对齐
  - `js/animation_system.js` - Clock 恒速动画与相机平滑平移
  - `js/cleanup_manager.js` - 深度遍历内存释放与 WebGL 垃圾回收
- `scripts/` - Blender 场景自动化生成与渲染脚本
- `renders/` - 渲染输出效果图（全景主视角、广场广角、角色特写）
- `references/` - 原始参考截图
- `tests/` - 场景契约测试与产物验证脚本

## 渲染预览

| 全景主视角 (`final_hero.png`) | 广场广角 (`plaza_wide.png`) | 角色特写 (`character_closeup.png`) |
| :---: | :---: | :---: |
| ![Final Hero](renders/final_hero.png) | ![Plaza Wide](renders/plaza_wide.png) | ![Character Closeup](renders/character_closeup.png) |

