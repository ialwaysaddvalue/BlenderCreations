--[[
  IDLE ANIMATION — Daughter Roblox Character
  ============================================
  Smooth breathing, head tilt, arm sway, and hair bounce.

  HOW TO SET UP IN ROBLOX STUDIO:
  ─────────────────────────────────────────────────────────
  1. Import your FBX character (Home → Import 3D)
  2. In the Explorer panel, find the character Model
  3. Make sure it has:
       • HumanoidRootPart  (a Part — set as PrimaryPart)
       • Humanoid          (add one if missing)
       • Motor6D joints    (Roblox creates these from your FBX rig)
  4. In StarterPlayer → StarterCharacterScripts,
     create a new LocalScript and paste this entire file.
  5. Hit Play — the idle animation runs automatically.

  JOINT NAMES (must match your imported FBX bone names):
  ─────────────────────────────────────────────────────────
  Spine, Chest, Neck, Head,
  Shoulder_L, Shoulder_R,
  UpperArm_L, UpperArm_R
  (These match the bone names from daughter_roblox_character.py)
--]]

-- ── Services ──────────────────────────────────────────────────────────────
local TweenService = game:GetService("TweenService")
local RunService   = game:GetService("RunService")

-- ── Wait for character to fully load ──────────────────────────────────────
local character = script.Parent
local humanoid  = character:WaitForChild("Humanoid", 15)
if not humanoid then
    warn("[IdleAnim] Humanoid not found — animation skipped.")
    return
end

-- Disable Roblox's built-in animate script so it doesn't fight ours
local defaultAnimate = character:FindFirstChild("Animate")
if defaultAnimate then
    defaultAnimate.Enabled = false
end

-- ── Animation Timing ──────────────────────────────────────────────────────
local BREATH_HALF = 2.6   -- seconds for one breath phase (in or out)
local SWAY_HALF   = 3.2   -- seconds for one arm sway phase
local NOD_HALF    = 4.0   -- seconds for one head tilt phase
local BOUNCE_HALF = 1.3   -- seconds for hair bun bounce

-- Easing functions
local breathEase = TweenInfo.new(BREATH_HALF, Enum.EasingStyle.Sine, Enum.EasingDirection.InOut)
local swayEase   = TweenInfo.new(SWAY_HALF,   Enum.EasingStyle.Sine, Enum.EasingDirection.InOut)
local nodEase    = TweenInfo.new(NOD_HALF,     Enum.EasingStyle.Sine, Enum.EasingDirection.InOut)
local bounceEase = TweenInfo.new(BOUNCE_HALF,  Enum.EasingStyle.Sine, Enum.EasingDirection.InOut)

-- ── Find Motor6D Joints ────────────────────────────────────────────────────
-- Motor6D joints are created automatically when Roblox imports your FBX rig.
-- Each one lives inside the child Part (not the parent).

local function findMotor(name)
    -- Search all descendants for a Motor6D with this name
    for _, obj in ipairs(character:GetDescendants()) do
        if obj:IsA("Motor6D") and obj.Name == name then
            return obj
        end
    end
    warn("[IdleAnim] Motor6D not found: " .. name)
    return nil
end

local J = {
    Spine      = findMotor("Spine"),
    Chest      = findMotor("Chest"),
    Neck       = findMotor("Neck"),
    Head       = findMotor("Head"),
    Shoulder_L = findMotor("Shoulder_L"),
    Shoulder_R = findMotor("Shoulder_R"),
    UpperArm_L = findMotor("UpperArm_L"),
    UpperArm_R = findMotor("UpperArm_R"),
}

-- Save each joint's original C0 so we offset from it, not from zero
local base = {}
for name, motor in pairs(J) do
    if motor then
        base[name] = motor.C0
    end
end

-- ── Tween Helper ──────────────────────────────────────────────────────────
-- Tweens a Motor6D's C0 by adding a CFrame offset to its base position,
-- waits for completion, then tweens back to base.  Loops forever.

local function pingpong(motor, baseCF, offsetA, offsetB, tweenInfo)
    if not motor then return end
    task.spawn(function()
        while true do
            -- Phase A: base → offset
            local tweenA = TweenService:Create(motor, tweenInfo, {
                C0 = baseCF * offsetA
            })
            tweenA:Play()
            tweenA.Completed:Wait()

            -- Phase B: offset → base (or opposite offset for swing)
            local tweenB = TweenService:Create(motor, tweenInfo, {
                C0 = baseCF * offsetB
            })
            tweenB:Play()
            tweenB.Completed:Wait()
        end
    end)
end

-- ── Launch All Idle Animations ─────────────────────────────────────────────

-- 1. BREATHING — Spine rises and falls gently
pingpong(
    J.Spine,
    base.Spine or CFrame.new(),
    CFrame.new(0, 0.008, 0) * CFrame.Angles(math.rad( 1.2), 0, 0),  -- inhale
    CFrame.new(0,-0.004, 0) * CFrame.Angles(math.rad(-0.6), 0, 0),  -- exhale
    breathEase
)

-- 2. CHEST — slight expansion with breath
pingpong(
    J.Chest,
    base.Chest or CFrame.new(),
    CFrame.Angles(math.rad( 0.8), 0, 0),
    CFrame.Angles(math.rad(-0.4), 0, 0),
    breathEase
)

-- 3. HEAD NOD — very gentle downward tilt, side to side
pingpong(
    J.Head,
    base.Head or CFrame.new(),
    CFrame.Angles(math.rad( 2.5), math.rad( 1.5), math.rad( 0.8)),
    CFrame.Angles(math.rad(-1.0), math.rad(-1.5), math.rad(-0.8)),
    nodEase
)

-- 4. NECK — supports head movement
pingpong(
    J.Neck,
    base.Neck or CFrame.new(),
    CFrame.Angles(math.rad( 1.0), math.rad( 0.5), 0),
    CFrame.Angles(math.rad(-0.5), math.rad(-0.5), 0),
    nodEase
)

-- 5. LEFT ARM SWAY — relaxed hang with slight forward/back
pingpong(
    J.Shoulder_L,
    base.Shoulder_L or CFrame.new(),
    CFrame.Angles(math.rad( 2.5), 0, math.rad( 1.5)),
    CFrame.Angles(math.rad(-1.5), 0, math.rad(-0.8)),
    swayEase
)

-- 6. RIGHT ARM SWAY — opposite phase for natural feel
task.delay(SWAY_HALF, function()   -- offset start by half cycle
    pingpong(
        J.Shoulder_R,
        base.Shoulder_R or CFrame.new(),
        CFrame.Angles(math.rad( 2.5), 0, math.rad(-1.5)),
        CFrame.Angles(math.rad(-1.5), 0, math.rad( 0.8)),
        swayEase
    )
end)

-- 7. UPPER ARMS — slight dangle rotation
pingpong(
    J.UpperArm_L,
    base.UpperArm_L or CFrame.new(),
    CFrame.Angles(math.rad( 1.2), 0, 0),
    CFrame.Angles(math.rad(-0.6), 0, 0),
    swayEase
)
task.delay(SWAY_HALF, function()
    pingpong(
        J.UpperArm_R,
        base.UpperArm_R or CFrame.new(),
        CFrame.Angles(math.rad( 1.2), 0, 0),
        CFrame.Angles(math.rad(-0.6), 0, 0),
        swayEase
    )
end)

-- ── Hair Bun Bounce (MeshPart position, not Motor6D) ──────────────────────
-- The hair bun is a MeshPart — we tween its position offset relative to root.
-- Only runs if Hair_Bun exists as a direct mesh (non-rigged attachment).

local hairBun = character:FindFirstChild("Hair_Bun")
if hairBun and hairBun:IsA("MeshPart") then
    local bunBase = hairBun.Position
    task.spawn(function()
        while true do
            local up = TweenService:Create(hairBun, bounceEase, {
                Position = bunBase + Vector3.new(0, 0.012, 0)
            })
            up:Play(); up.Completed:Wait()

            local down = TweenService:Create(hairBun, bounceEase, {
                Position = bunBase
            })
            down:Play(); down.Completed:Wait()
        end
    end)
end

-- ── Footstep Breathing (root slight vertical bob) ─────────────────────────
local rootPart = character:FindFirstChild("HumanoidRootPart")
if rootPart then
    local rootBase = rootPart.CFrame
    task.spawn(function()
        while humanoid.Health > 0 do
            local rise = TweenService:Create(rootPart, breathEase, {
                CFrame = rootBase * CFrame.new(0, 0.018, 0)
            })
            rise:Play(); rise.Completed:Wait()

            local fall = TweenService:Create(rootPart, breathEase, {
                CFrame = rootBase
            })
            fall:Play(); fall.Completed:Wait()
        end
    end)
end

-- ── Stop cleanly when character dies ──────────────────────────────────────
humanoid.Died:Connect(function()
    -- Tweens stop naturally when the character is removed from workspace
end)

print("[IdleAnim] Idle animation started for: " .. character.Name)
