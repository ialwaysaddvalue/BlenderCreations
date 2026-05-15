"""
ROBLOX CHARACTER GENERATOR — Blender Python Script
===================================================
Character: Young girl, warm dark skin, dark hair bun,
           blue floral top, green shorts.
Target:    ~1.68m tall in Blender = 6 Roblox studs.

HOW TO RUN:
  1. Open Blender (any 3.x or 4.x version)
  2. Click the "Scripting" tab at the top
  3. Click "New" to create a script
  4. Paste this entire file
  5. Click "Run Script" (▶ button or Alt+P)

EXPORT (after script runs):
  File → Export → FBX (.fbx)
  Settings:
    Scale              → 0.01
    Apply Scalings     → FBX Units Scale
    Forward            → -Z Forward
    Up                 → Y Up
    Apply Modifiers    → ON  ✅
    Add Leaf Bones     → OFF ❌
    Path Mode          → Copy (embed textures)
"""

import bpy
import bmesh
from mathutils import Vector

# ─────────────────────────────────────────────
# 1. CLEAR SCENE
# ─────────────────────────────────────────────
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

for block in bpy.data.meshes:
    bpy.data.meshes.remove(block)
for block in bpy.data.materials:
    bpy.data.materials.remove(block)
for block in bpy.data.armatures:
    bpy.data.armatures.remove(block)
for block in bpy.data.cameras:
    bpy.data.cameras.remove(block)
for block in bpy.data.lights:
    bpy.data.lights.remove(block)

# ─────────────────────────────────────────────
# 2. MATERIALS
# ─────────────────────────────────────────────
def make_mat(name, hex_color, roughness=0.75):
    r = int(hex_color[0:2], 16) / 255
    g = int(hex_color[2:4], 16) / 255
    b = int(hex_color[4:6], 16) / 255
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = (r, g, b, 1.0)
    bsdf.inputs['Roughness'].default_value = roughness
    out = nodes.new('ShaderNodeOutputMaterial')
    links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat

M_SKIN   = make_mat("Skin",      "7A4030")   # warm dark brown
M_HAIR   = make_mat("Hair",      "1A0800")   # near-black
M_SHIRT  = make_mat("Shirt",     "5BB8D4")   # teal blue
M_SHORTS = make_mat("Shorts",    "6AAF3D")   # medium green
M_EYE    = make_mat("Eye",       "2C1505")   # dark brown eye
M_WHITE  = make_mat("EyeWhite",  "F2F0EE", roughness=0.4)
M_TOOTH  = make_mat("Teeth",     "FAF8F5", roughness=0.3)

def set_mat(obj, mat):
    obj.data.materials.clear()
    obj.data.materials.append(mat)

# ─────────────────────────────────────────────
# 3. PRIMITIVE HELPERS
# ─────────────────────────────────────────────
def add_sphere(name, radius, loc, seg=12, rings=8, mat=None):
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=seg, ring_count=rings, radius=radius, location=loc)
    obj = bpy.context.active_object
    obj.name = name
    if mat:
        set_mat(obj, mat)
    return obj

def add_cylinder(name, radius, depth, loc, rot=(0, 0, 0), verts=10, mat=None):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=verts, radius=radius, depth=depth,
        location=loc, rotation=rot)
    obj = bpy.context.active_object
    obj.name = name
    if mat:
        set_mat(obj, mat)
    return obj

def add_cube(name, loc, sx, sy, sz, mat=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (sx, sy, sz)
    bpy.ops.object.transform_apply(scale=True)
    if mat:
        set_mat(obj, mat)
    return obj

parts = []   # all mesh objects — will be parented to armature

def track(obj):
    parts.append(obj)
    return obj

# ─────────────────────────────────────────────
# 4. BODY
#    Total height ≈ 1.68 m  (6 Roblox studs)
#    Head top  ~1.70 m
#    Foot sole ~0.05 m
# ─────────────────────────────────────────────

# HEAD (slightly taller than wide — child proportions)
head = add_sphere("Head", 0.135, (0, 0, 1.555), seg=14, rings=10, mat=M_SKIN)
head.scale = (1.0, 0.88, 1.02)
bpy.ops.object.transform_apply(scale=True)
track(head)

# NECK
track(add_cylinder("Neck", 0.046, 0.10, (0, 0, 1.395), verts=8, mat=M_SKIN))

# TORSO
track(add_cube("Torso", (0, 0, 1.095), 0.185, 0.115, 0.225, M_SKIN))

# UPPER ARMS (angled outward slightly)
track(add_cylinder("UpperArm_L", 0.042, 0.215,
      (-0.232, 0, 1.205), rot=(0,  0.32, 0), verts=8, mat=M_SKIN))
track(add_cylinder("UpperArm_R", 0.042, 0.215,
      ( 0.232, 0, 1.205), rot=(0, -0.32, 0), verts=8, mat=M_SKIN))

# LOWER ARMS
track(add_cylinder("LowerArm_L", 0.036, 0.195,
      (-0.308, 0, 0.985), verts=8, mat=M_SKIN))
track(add_cylinder("LowerArm_R", 0.036, 0.195,
      ( 0.308, 0, 0.985), verts=8, mat=M_SKIN))

# HANDS
hl = add_sphere("Hand_L", 0.043, (-0.308, 0, 0.858), seg=8, rings=6, mat=M_SKIN)
hl.scale = (1.0, 0.70, 0.78)
bpy.ops.object.transform_apply(scale=True)
track(hl)

hr = add_sphere("Hand_R", 0.043, ( 0.308, 0, 0.858), seg=8, rings=6, mat=M_SKIN)
hr.scale = (1.0, 0.70, 0.78)
bpy.ops.object.transform_apply(scale=True)
track(hr)

# UPPER LEGS
track(add_cylinder("UpperLeg_L", 0.056, 0.285,
      (-0.088, 0, 0.728), verts=10, mat=M_SKIN))
track(add_cylinder("UpperLeg_R", 0.056, 0.285,
      ( 0.088, 0, 0.728), verts=10, mat=M_SKIN))

# LOWER LEGS
track(add_cylinder("LowerLeg_L", 0.044, 0.260,
      (-0.088, 0, 0.428), verts=10, mat=M_SKIN))
track(add_cylinder("LowerLeg_R", 0.044, 0.260,
      ( 0.088, 0, 0.428), verts=10, mat=M_SKIN))

# FEET
track(add_cube("Foot_L", (-0.088,  0.032, 0.072), 0.058, 0.095, 0.040, M_SKIN))
track(add_cube("Foot_R", ( 0.088,  0.032, 0.072), 0.058, 0.095, 0.040, M_SKIN))

# ─────────────────────────────────────────────
# 5. FACE FEATURES
# ─────────────────────────────────────────────

# Eye whites (flattened sphere facing forward)
for side, x in (("L", -0.052), ("R", 0.052)):
    ew = add_sphere(f"EyeWhite_{side}", 0.022, (x, -0.118, 1.555), seg=8, rings=6, mat=M_WHITE)
    ew.scale = (1.0, 0.48, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    track(ew)

# Pupils
for side, x in (("L", -0.052), ("R", 0.052)):
    track(add_sphere(f"Pupil_{side}", 0.013, (x, -0.133, 1.555),
          seg=6, rings=4, mat=M_EYE))

# Nose (tiny bump)
track(add_sphere("Nose", 0.018, (0, -0.130, 1.490), seg=6, rings=4, mat=M_SKIN))

# Smile (two small sphere bumps at mouth corners)
for side, x in (("L", -0.030), ("R", 0.030)):
    sm = add_sphere(f"SmileCorner_{side}", 0.010,
                    (x, -0.130, 1.450), seg=6, rings=4, mat=M_SKIN)
    track(sm)

# ─────────────────────────────────────────────
# 6. HAIR
# ─────────────────────────────────────────────

# Main hair cap — sphere with lower half removed
hair_cap = add_sphere("Hair_Cap", 0.147, (0, 0, 1.585), seg=14, rings=10, mat=M_HAIR)
hair_cap.scale = (1.03, 1.01, 0.82)
bpy.ops.object.transform_apply(scale=True)

bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(hair_cap.data)
to_del = [v for v in bm.verts if v.co.z < -0.035]
bmesh.ops.delete(bm, geom=to_del, context='VERTS')
bmesh.update_edit_mesh(hair_cap.data)
bpy.ops.object.mode_set(mode='OBJECT')
track(hair_cap)

# Top puff / bun
bun = add_sphere("Hair_Bun", 0.068, (0, 0.068, 1.715), seg=10, rings=8, mat=M_HAIR)
bun.scale = (1.0, 0.88, 1.0)
bpy.ops.object.transform_apply(scale=True)
track(bun)

# Hair tie band
track(add_cylinder("Hair_Band", 0.074, 0.018,
      (0, 0.052, 1.678), rot=(1.12, 0, 0), verts=16, mat=M_HAIR))

# Short hair strand framing face (left side)
track(add_cylinder("HairStrand_L", 0.012, 0.085,
      (-0.115, -0.058, 1.490), rot=(0.4, -0.2, 0.1), verts=6, mat=M_HAIR))

# ─────────────────────────────────────────────
# 7. CLOTHING
# ─────────────────────────────────────────────

# SHIRT — body
track(add_cube("Shirt_Body", (0, 0, 1.095), 0.200, 0.130, 0.232, M_SHIRT))

# SHIRT — short sleeves (sits over UpperArm)
track(add_cylinder("Sleeve_L", 0.049, 0.120,
      (-0.236, 0, 1.258), rot=(0,  0.32, 0), verts=8, mat=M_SHIRT))
track(add_cylinder("Sleeve_R", 0.049, 0.120,
      ( 0.236, 0, 1.258), rot=(0, -0.32, 0), verts=8, mat=M_SHIRT))

# Collar ring
track(add_cylinder("Collar", 0.054, 0.022,
      (0, -0.088, 1.342), rot=(1.5708, 0, 0), verts=14, mat=M_SHIRT))

# SHORTS — waistband block
track(add_cube("Shorts_Body", (0, 0, 0.874), 0.198, 0.132, 0.098, M_SHORTS))

# SHORTS — leg tubes
track(add_cylinder("ShortsLeg_L", 0.061, 0.105,
      (-0.088, 0, 0.766), verts=10, mat=M_SHORTS))
track(add_cylinder("ShortsLeg_R", 0.061, 0.105,
      ( 0.088, 0, 0.766), verts=10, mat=M_SHORTS))

# ─────────────────────────────────────────────
# 8. ARMATURE / RIG
# ─────────────────────────────────────────────
bpy.ops.object.armature_add(enter_editmode=True, location=(0, 0, 0))
arm_obj = bpy.context.active_object
arm_obj.name = "Rig"
arm_obj.data.name = "Rig"

eb = arm_obj.data.edit_bones
for b in list(eb):
    eb.remove(b)

def bone(name, head, tail, parent=None, connect=False):
    b = eb.new(name)
    b.head = Vector(head)
    b.tail = Vector(tail)
    if parent:
        b.parent = eb[parent]
        b.use_connect = connect
    return b

# Spine chain
bone("Root",        (0, 0, 0),         (0, 0, 0.08))
bone("Hips",        (0, 0, 0.874),     (0, 0, 0.975),    "Root")
bone("Spine",       (0, 0, 0.975),     (0, 0, 1.115),    "Hips",       True)
bone("Chest",       (0, 0, 1.115),     (0, 0, 1.282),    "Spine",      True)
bone("Neck",        (0, 0, 1.282),     (0, 0, 1.410),    "Chest",      True)
bone("Head",        (0, 0, 1.410),     (0, 0, 1.695),    "Neck",       True)

# Left arm chain
bone("Shoulder_L",  (-0.118, 0, 1.282), (-0.198, 0, 1.262), "Chest")
bone("UpperArm_L",  (-0.198, 0, 1.262), (-0.292, 0, 1.098), "Shoulder_L")
bone("LowerArm_L",  (-0.292, 0, 1.098), (-0.308, 0, 0.888), "UpperArm_L", True)
bone("Hand_L",      (-0.308, 0, 0.888), (-0.308, 0, 0.810), "LowerArm_L", True)

# Right arm chain
bone("Shoulder_R",  (0.118, 0, 1.282),  (0.198, 0, 1.262),  "Chest")
bone("UpperArm_R",  (0.198, 0, 1.262),  (0.292, 0, 1.098),  "Shoulder_R")
bone("LowerArm_R",  (0.292, 0, 1.098),  (0.308, 0, 0.888),  "UpperArm_R", True)
bone("Hand_R",      (0.308, 0, 0.888),  (0.308, 0, 0.810),  "LowerArm_R", True)

# Left leg chain
bone("UpperLeg_L",  (-0.088, 0, 0.874), (-0.088, 0, 0.590), "Hips")
bone("LowerLeg_L",  (-0.088, 0, 0.590), (-0.088, 0, 0.295), "UpperLeg_L", True)
bone("Foot_L",      (-0.088, 0, 0.295), (-0.088, 0.082, 0.075), "LowerLeg_L", True)

# Right leg chain
bone("UpperLeg_R",  (0.088, 0, 0.874),  (0.088, 0, 0.590),  "Hips")
bone("LowerLeg_R",  (0.088, 0, 0.590),  (0.088, 0, 0.295),  "UpperLeg_R", True)
bone("Foot_R",      (0.088, 0, 0.295),  (0.088, 0.082, 0.075), "LowerLeg_R", True)

bpy.ops.object.mode_set(mode='OBJECT')

# ─────────────────────────────────────────────
# 9. PARENT MESHES → ARMATURE (Auto Weights)
# ─────────────────────────────────────────────
bpy.ops.object.select_all(action='DESELECT')
for p in parts:
    p.select_set(True)
arm_obj.select_set(True)
bpy.context.view_layer.objects.active = arm_obj
bpy.ops.object.parent_set(type='ARMATURE_AUTO')
bpy.ops.object.select_all(action='DESELECT')

# ─────────────────────────────────────────────
# 10. SCENE — CAMERA & LIGHT
# ─────────────────────────────────────────────
bpy.ops.object.light_add(type='SUN', location=(2.5, -2.5, 4.0))
sun = bpy.context.active_object
sun.name = "Sun"
sun.data.energy = 3.5

bpy.ops.object.light_add(type='AREA', location=(-1.5, -2.0, 1.2))
fill = bpy.context.active_object
fill.name = "FillLight"
fill.data.energy = 80

bpy.ops.object.camera_add(
    location=(0, -4.0, 0.9),
    rotation=(1.5708, 0, 0))
cam = bpy.context.active_object
cam.name = "Camera"
bpy.context.scene.camera = cam

# ─────────────────────────────────────────────
# 11. DONE
# ─────────────────────────────────────────────
print("")
print("=" * 52)
print("  ✅  CHARACTER BUILT SUCCESSFULLY!")
print("=" * 52)
print(f"  Mesh parts created : {len(parts)}")
print(f"  Armature bones     : {len(arm_obj.data.bones)}")
print("")
print("  NEXT STEPS:")
print("  1. Check the viewport — character is centred at origin")
print("  2. Adjust any mesh positions in Object Mode if needed")
print("  3. File → Export → FBX (.fbx)")
print("     • Scale            : 0.01")
print("     • Apply Scalings   : FBX Units Scale")
print("     • Forward          : -Z Forward")
print("     • Up               : Y Up")
print("     • Apply Modifiers  : ON")
print("     • Add Leaf Bones   : OFF")
print("  4. Import FBX into Roblox Studio (Home → Import 3D)")
print("=" * 52)
