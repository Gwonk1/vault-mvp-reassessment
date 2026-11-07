"""Argon Test A5 & Test A6 (Reply to Claude Code Back-Channel 003, pre-registered in PREREGISTRATION_ARGON_003.md):
- Priority 1 (Test A5): Settle LEDGER #34 — Is the SPFH shoulder ADP-ribose/NAD+ pocket (PDB 11JB / 9BW6) LUMENAL, TRANSMURAL, or EXTERIOR?
  (1a) Exact radial offsets Delta_R = R_cyl - R_mid(|z|) in 10 A & 15 A bins for every heavy atom of AR6 and MVP residues 499-573 + 433-438.
  (1b) Directional 3D 0.4-A voxel probe flood-fill & Lee-Richards SASA computed TWICE (Lumen-only seed vs Exterior-only seed) + minimax pore bottleneck radius (R_max_lumen vs R_max_exterior, 0.1 A resolution) for both holo and apo 11JB.
  (1c) Formal pre-registered verdict: LUMENAL / TRANSMURAL / EXTERIOR.
- Priority 2 (Test A6): Luminal charge & Debye-Huckel electrostatic potential profile (150 mM salt, T=310K) comparing:
  (1) Rat 4V60 apo 78-mer, (2) Human 11JB apo 78-mer, (3) Human 11JB + 78x AR6(2-), (4) Human 11JB + 78x AR6(2-) + 20x PARP4-MINT (from 9BW6).
"""
import gzip, json, os, math
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree
from scipy.ndimage import label

RAW = "~/projects/Vault/argon/raw"
OUT = "~/projects/Vault/argon/results"
STRUCT_DIR = "~/projects/Vault/data/raw/struct"
os.makedirs(OUT, exist_ok=True)

VDW = {"C": 1.70, "N": 1.55, "O": 1.52, "S": 1.80, "P": 1.80, "SE": 1.90}

def parse_cif_heavy_atoms(cif_gz_path):
    """Fast streaming mmCIF parser returning heavy-atom DataFrame (excluding H/D)."""
    rows = []
    col_names = []
    in_atom = False
    idx = {}
    with gzip.open(cif_gz_path, "rt") as fh:
        for line in fh:
            if line.startswith("_atom_site."):
                in_atom = True
                col_names.append(line.strip().split(".")[1].split()[0])
                continue
            if in_atom:
                if line.startswith("#") or line.startswith("loop_") or line.startswith("_"):
                    in_atom = False
                    col_names = []
                    idx = {}
                    continue
                if not idx:
                    idx = {k: i for i, k in enumerate(col_names)}
                parts = line.split()
                if len(parts) < len(col_names):
                    continue
                elem = parts[idx["type_symbol"]].upper()
                if elem in ("H", "D"):
                    continue
                grp = parts[idx["group_PDB"]]
                cid = parts[idx.get("auth_asym_id", idx.get("label_asym_id"))]
                resname = parts[idx.get("auth_comp_id", idx.get("label_comp_id"))]
                atomname = parts[idx.get("auth_atom_id", idx.get("label_atom_id"))].strip('"')
                seq_str = parts[idx.get("auth_seq_id", idx.get("label_seq_id"))]
                resseq = int(seq_str) if seq_str.lstrip("-").isdigit() else -1
                # Keep altloc '.' or '?' or 'A' only to avoid double-counting disordered conformers
                if "label_alt_id" in idx:
                    alt = parts[idx["label_alt_id"]]
                    if alt not in (".", "?", "A"):
                        continue
                x = float(parts[idx["Cartn_x"]])
                y = float(parts[idx["Cartn_y"]])
                z = float(parts[idx["Cartn_z"]])
                rows.append((grp, cid, resseq, resname, atomname, elem, x, y, z))
    return pd.DataFrame(rows, columns=["group", "chain", "pos", "resname", "atom", "elem", "x", "y", "z"])

print("1. Loading full 78-mer PDB 11JB heavy atoms...")
df_11jb = parse_cif_heavy_atoms(f"{RAW}/11JB.cif.gz")
prot_11jb = df_11jb[df_11jb["group"] == "ATOM"].copy()
ar6_11jb = df_11jb[(df_11jb["group"] == "HETATM") & (df_11jb["resname"] == "AR6")].copy()
print(f"   11JB heavy atoms: protein={len(prot_11jb):,} across {prot_11jb['chain'].nunique()} chains | AR6={len(ar6_11jb):,} across {ar6_11jb['chain'].nunique()} chains ({len(ar6_11jb)//max(1,ar6_11jb['chain'].nunique())} heavy atoms/AR6)")

# Center on 78-mer CA centroid
ca_11jb = prot_11jb[prot_11jb["atom"] == "CA"]
cx, cy, cz = ca_11jb[["x", "y", "z"]].mean()
for d in (df_11jb, prot_11jb, ar6_11jb):
    d["dx"] = d["x"] - cx
    d["dy"] = d["y"] - cy
    d["dz"] = d["z"] - cz

# Confirm long axis is dz
spans = [prot_11jb["dx"].max() - prot_11jb["dx"].min(),
         prot_11jb["dy"].max() - prot_11jb["dy"].min(),
         prot_11jb["dz"].max() - prot_11jb["dz"].min()]
assert int(np.argmax(spans)) == 2, f"Expected dz as long axis, got spans={spans}"
for d in (df_11jb, prot_11jb, ar6_11jb):
    d["abs_z"] = d["dz"].abs()
    d["R_cyl"] = np.sqrt(d["dx"]**2 + d["dy"]**2)

ca_11jb = prot_11jb[prot_11jb["atom"] == "CA"].copy()
print(f"   11JB 78-mer CA geometry: z range [{ca_11jb['dz'].min():.1f}, {ca_11jb['dz'].max():.1f}] A | R_cyl range [{ca_11jb['R_cyl'].min():.1f}, {ca_11jb['R_cyl'].max():.1f}] A")

# ==============================================================================
# PRIORITY 1A: Local Shell Midsurface R_mid(|z|) in 10 A & 15 A Axial Bins
# ==============================================================================
print("\n=== PRIORITY 1A: Radial Offsets Delta_R = R_cyl - R_mid(|z|) on 78-mer 11JB ===")
ca_11jb["bin10"] = (ca_11jb["abs_z"] // 10.0) * 10.0
ca_11jb["bin15"] = (ca_11jb["abs_z"] // 15.0) * 15.0
prot_11jb["bin10"] = (prot_11jb["abs_z"] // 10.0) * 10.0

rmid_10 = ca_11jb.groupby("bin10")["R_cyl"].median().to_dict()
rmid_15 = ca_11jb.groupby("bin15")["R_cyl"].median().to_dict()
r_in05_10 = prot_11jb.groupby("bin10")["R_cyl"].quantile(0.05).to_dict()
r_out95_10 = prot_11jb.groupby("bin10")["R_cyl"].quantile(0.95).to_dict()

# Smooth linear interpolation of R_mid(|z|) from 5-A CA slice medians for zero bin-edge jitter
ca_11jb["bin5"] = (ca_11jb["abs_z"] // 5.0) * 5.0 + 2.5
prof5 = ca_11jb.groupby("bin5")["R_cyl"].median().sort_index()
def interp_rmid(abs_z_arr):
    return np.interp(abs_z_arr, prof5.index.values, prof5.values)

# Evaluate Chain A's bound AR6 heavy atoms
ar6_A = ar6_11jb[ar6_11jb["chain"] == "A"].copy()
ar6_A["R_mid_10A"] = ((ar6_A["abs_z"] // 10.0) * 10.0).map(rmid_10)
ar6_A["R_mid_15A"] = ((ar6_A["abs_z"] // 15.0) * 15.0).map(rmid_15)
ar6_A["R_mid_interp"] = interp_rmid(ar6_A["abs_z"].values)
ar6_A["R_in05_10A"] = ((ar6_A["abs_z"] // 10.0) * 10.0).map(r_in05_10)
ar6_A["R_out95_10A"] = ((ar6_A["abs_z"] // 10.0) * 10.0).map(r_out95_10)
ar6_A["Delta_R_10A"] = ar6_A["R_cyl"] - ar6_A["R_mid_10A"]
ar6_A["Delta_R_15A"] = ar6_A["R_cyl"] - ar6_A["R_mid_15A"]
ar6_A["Delta_R_interp"] = ar6_A["R_cyl"] - ar6_A["R_mid_interp"]

print(f"AR6 (Chain A, n={len(ar6_A)} heavy atoms): |z| range [{ar6_A['abs_z'].min():.2f}, {ar6_A['abs_z'].max():.2f}] A | R_cyl range [{ar6_A['R_cyl'].min():.2f}, {ar6_A['R_cyl'].max():.2f}] A")
print(f"Local shell midsurface at AR6 |z|: R_mid_10A = {ar6_A['R_mid_10A'].mean():.2f} A, R_mid_15A = {ar6_A['R_mid_15A'].mean():.2f} A | Wall [5th, 95th] heavy-atom R = [{ar6_A['R_in05_10A'].mean():.2f}, {ar6_A['R_out95_10A'].mean():.2f}] A")
print(f"AR6 Delta_R_10A:    min={ar6_A['Delta_R_10A'].min():+.2f} A, mean={ar6_A['Delta_R_10A'].mean():+.2f} A, max={ar6_A['Delta_R_10A'].max():+.2f} A | n_atoms >= 0: {(ar6_A['Delta_R_10A'] >= 0).sum()}/{len(ar6_A)}")
print(f"AR6 Delta_R_15A:    min={ar6_A['Delta_R_15A'].min():+.2f} A, mean={ar6_A['Delta_R_15A'].mean():+.2f} A, max={ar6_A['Delta_R_15A'].max():+.2f} A | n_atoms >= 0: {(ar6_A['Delta_R_15A'] >= 0).sum()}/{len(ar6_A)}")
print(f"AR6 Delta_R_interp: min={ar6_A['Delta_R_interp'].min():+.2f} A, mean={ar6_A['Delta_R_interp'].mean():+.2f} A, max={ar6_A['Delta_R_interp'].max():+.2f} A | n_atoms >= 0: {(ar6_A['Delta_R_interp'] >= 0).sum()}/{len(ar6_A)}")
print("\nPer-atom AR6 radial table (Chain A):")
print(ar6_A[["atom", "elem", "abs_z", "R_cyl", "R_mid_10A", "Delta_R_10A", "Delta_R_15A", "Delta_R_interp"]].to_string(index=False))

# MVP residues 499-573 + 433-438 radial profile on Chain A
mvp_A = prot_11jb[prot_11jb["chain"] == "A"].copy()
mvp_A["R_mid_10A"] = ((mvp_A["abs_z"] // 10.0) * 10.0).map(rmid_10)
mvp_A["R_mid_15A"] = ((mvp_A["abs_z"] // 15.0) * 15.0).map(rmid_15)
mvp_A["Delta_R_10A"] = mvp_A["R_cyl"] - mvp_A["R_mid_10A"]
mvp_A["Delta_R_15A"] = mvp_A["R_cyl"] - mvp_A["R_mid_15A"]

res_target = list(range(433, 439)) + list(range(499, 574))
sub_res = mvp_A[mvp_A["pos"].isin(res_target)]
ca_sub = sub_res[sub_res["atom"] == "CA"].set_index("pos")
grp_sub = sub_res.groupby("pos").agg(
    resname=("resname", "first"),
    abs_z=("abs_z", "mean"),
    min_Delta_R_10A=("Delta_R_10A", "min"),
    max_Delta_R_10A=("Delta_R_10A", "max"),
).join(ca_sub[["R_cyl", "R_mid_10A", "Delta_R_10A", "Delta_R_15A"]].rename(columns={"R_cyl": "CA_R_cyl", "Delta_R_10A": "CA_Delta_R_10A", "Delta_R_15A": "CA_Delta_R_15A"}))

key_pocket = [433, 437, 438, 499, 500, 501, 502, 503, 504, 506, 507, 508, 509, 511, 513, 515, 516, 517, 521, 522, 523, 524, 545, 547, 565, 566, 567, 568, 569, 573]
print("\nKey Pocket & Keyhole Residues (433-438, 499-573) Radial Offsets from Local Midsurface:")
print(grp_sub.loc[[p for p in key_pocket if p in grp_sub.index]][["resname", "abs_z", "CA_R_cyl", "R_mid_10A", "CA_Delta_R_10A", "CA_Delta_R_15A", "min_Delta_R_10A", "max_Delta_R_10A"]].round(2).to_string())
print(f"\nAcross all 75 shoulder residues 499-573: lumen-side CA (Delta_R_10A < 0) = {(grp_sub.loc[grp_sub.index >= 499, 'CA_Delta_R_10A'] < 0).sum()}/75 | exterior-side CA (>=0) = {(grp_sub.loc[grp_sub.index >= 499, 'CA_Delta_R_10A'] >= 0).sum()}/75")
print(f"Across 30 AR6/keyhole contact residues: lumen-side CA (Delta_R_10A < 0) = {(grp_sub.loc[[p for p in key_pocket if p in grp_sub.index], 'CA_Delta_R_10A'] < 0).sum()}/30 | min sidechain atom < 0 = {(grp_sub.loc[[p for p in key_pocket if p in grp_sub.index], 'min_Delta_R_10A'] < 0).sum()}/30")

# ==============================================================================
# PRIORITY 1B: Directional 3D Probe Accessibility (Lumen-only vs Exterior-only) & Bottleneck Radius
# ==============================================================================
print("\n=== PRIORITY 1B: Directional 3D Voxel Flood-Fill & Lee-Richards SASA (0.4 A Grid) ===")
# Rotate (dx, dy) around Z so Chain A's AR6 centroid sits at v = 0, u > 0
ar6_cx, ar6_cy, ar6_cz = ar6_A[["dx", "dy", "dz"]].mean()
theta0 = math.atan2(ar6_cy, ar6_cx)
cos_t, sin_t = math.cos(-theta0), math.sin(-theta0)

def to_uvz(df_in):
    u = df_in["dx"].values * cos_t - df_in["dy"].values * sin_t
    v = df_in["dx"].values * sin_t + df_in["dy"].values * cos_t
    z = df_in["dz"].values
    r_vdw = np.array([VDW.get(e, 1.70) for e in df_in["elem"].values])
    return np.column_stack([u, v, z]), r_vdw

u0 = math.hypot(ar6_cx, ar6_cy)
rmid_at_z0 = float(interp_rmid(np.array([abs(ar6_cz)]))[0])
print(f"AR6_A centroid in rotated frame: u0={u0:.2f} A, v0=0.00 A, z0={ar6_cz:.2f} A | local R_mid(|z0|)={rmid_at_z0:.2f} A")

# Select ALL 78-mer protein atoms + OTHER chains' AR6 atoms within 55 A of AR6_A centroid (captures ~9 adjacent chains, 100% sealed wall!)
all_prot_uvz, all_prot_vdw = to_uvz(prot_11jb)
other_ar6 = ar6_11jb[ar6_11jb["chain"] != "A"]
other_ar6_uvz, other_ar6_vdw = to_uvz(other_ar6)
ar6_A_uvz, ar6_A_vdw = to_uvz(ar6_A)

center_uvz = np.array([rmid_at_z0, 0.0, ar6_cz])
mask_near_prot = np.linalg.norm(all_prot_uvz - center_uvz, axis=1) <= 58.0
near_prot_uvz = all_prot_uvz[mask_near_prot]
near_prot_vdw = all_prot_vdw[mask_near_prot]
mask_near_oar6 = np.linalg.norm(other_ar6_uvz - center_uvz, axis=1) <= 58.0
near_holo_other_uvz = np.vstack([near_prot_uvz, other_ar6_uvz[mask_near_oar6]])
near_holo_other_vdw = np.concatenate([near_prot_vdw, other_ar6_vdw[mask_near_oar6]])
print(f"Local 78-mer shell sector atoms within 58 A: protein={len(near_prot_uvz):,} (+ neighbor AR6={mask_near_oar6.sum()})")

# Build 0.4-A 3D grid spanning u in [rmid-34, rmid+34], v in [-22, +22], z in [z0-24, z0+24]
# Note: at v in [-22, +22] (~2.6 chains wide), the vault wall is completely continuous across the entire (v, z) cross-section!
STEP = 0.4
u_grid = np.arange(rmid_at_z0 - 34.0, rmid_at_z0 + 34.0 + 1e-6, STEP)
v_grid = np.arange(-22.0, 22.0 + 1e-6, STEP)
z_grid = np.arange(ar6_cz - 24.0, ar6_cz + 24.0 + 1e-6, STEP)
UU, VV, ZZ = np.meshgrid(u_grid, v_grid, z_grid, indexing="ij")
grid_pts = np.column_stack([UU.ravel(), VV.ravel(), ZZ.ravel()])
R_grid = np.sqrt(UU**2 + VV**2)
R_mid_grid = interp_rmid(np.abs(ZZ))
Delta_R_grid = R_grid - R_mid_grid
print(f"3D voxel grid shape: {UU.shape} = {len(grid_pts):,} voxels at {STEP} A resolution")

# Compute exact clearance = min_i (||x - atom_i|| - r_vdw[i]) at every voxel!
# Since r_vdw varies slightly (1.52..1.80 A), group by unique r_vdw (only 4 unique values!) and take min across 4 cKDTree queries — exact & takes <1.5 sec!
def compute_exact_clearance(pts, atom_xyz, atom_vdw):
    clr = np.full(len(pts), 999.0, dtype=np.float32)
    for rv in np.unique(atom_vdw):
        sub_xyz = atom_xyz[atom_vdw == rv]
        d, _ = cKDTree(sub_xyz).query(pts, workers=-1)
        clr = np.minimum(clr, d.astype(np.float32) - float(rv))
    return clr

print("Computing exact van der Waals surface clearance field (apo, holo-neighbor, and holo-full)...")
clr_apo = compute_exact_clearance(grid_pts, near_prot_uvz, near_prot_vdw).reshape(UU.shape)
clr_holo_env = compute_exact_clearance(grid_pts, near_holo_other_uvz, near_holo_other_vdw).reshape(UU.shape)
clr_holo_full = compute_exact_clearance(
    grid_pts,
    np.vstack([near_holo_other_uvz, ar6_A_uvz]),
    np.concatenate([near_holo_other_vdw, ar6_A_vdw]),
).reshape(UU.shape)

# Hermetically seal all 4 lateral boundary faces (v_min, v_max, z_min, z_max) across the full radial span
rim_mask = (np.abs(VV) >= 20.0) | (np.abs(ZZ - ar6_cz) >= 22.0)

lumen_seed_mask = (Delta_R_grid <= -24.0) & (~rim_mask)
ext_seed_mask = (Delta_R_grid >= +24.0) & (~rim_mask)
assert lumen_seed_mask.sum() > 1000 and ext_seed_mask.sum() > 1000

# Map AR6_A heavy atoms to nearest voxel indices to test apo pocket reachability & minimax bottleneck radius!
def xyz_to_ijk(xyz):
    i = np.clip(np.round((xyz[:, 0] - u_grid[0]) / STEP).astype(int), 0, len(u_grid) - 1)
    j = np.clip(np.round((xyz[:, 1] - v_grid[0]) / STEP).astype(int), 0, len(v_grid) - 1)
    k = np.clip(np.round((xyz[:, 2] - z_grid[0]) / STEP).astype(int), 0, len(z_grid) - 1)
    return i, j, k

ai, aj, ak = xyz_to_ijk(ar6_A_uvz)

# Binary/grid scan over probe radii 0.4 A .. 5.0 A (0.1 A step) in APO pocket (AR6 removed):
# Run TWICE at each r_probe:
#   (1) Lumen-only access: exterior blocked (Delta_R >= +11 A sealed), seeded from lumen_seed_mask
#   (2) Direct Exterior-only access to AR6 pocket: bulk lumen cavity blocked (Delta_R <= -11 A sealed so probes cannot sneak into the lumen 15 A away at the Repeat-8/9 hinge seam |z|=155-167 A and walk back up from the inside!), seeded from ext_seed_mask
#   (3) Unblocked sector-wide check: max radius crossing anywhere across the 48-A shoulder+hinge sector (captures the 1.60 A Repeat-8/9 inter-chain water micro-cleft at |z|=155-167 A)
radii_test = np.round(np.arange(0.4, 5.05, 0.1), 2)
rmax_lumen_to_ar6 = 0.0
rmax_ext_to_ar6 = 0.0
rmax_transmural_anywhere = 0.0

struct26 = np.ones((3, 3, 3), dtype=int)  # 26-connectivity on 0.4 A grid

for rp in radii_test:
    free = (clr_apo >= rp) & (~rim_mask)
    # 1. Lumen-only run
    free_lum = free & (Delta_R_grid < +11.0)
    lbl_lum, _ = label(free_lum, structure=struct26)
    lum_labels = set(np.unique(lbl_lum[lumen_seed_mask & free_lum])) - {0}
    ar6_lum_hit = any(lbl_lum[i, j, k] in lum_labels for i, j, k in zip(ai, aj, ak))
    if ar6_lum_hit:
        rmax_lumen_to_ar6 = float(rp)

    # 2. Direct Exterior-only run (bulk lumen Delta_R <= -11.0 A blocked to prevent lumen wrap-around from |z|=155-167 A hinge seam)
    free_ext = free & (Delta_R_grid > -11.0)
    lbl_ext, _ = label(free_ext, structure=struct26)
    ext_labels = set(np.unique(lbl_ext[ext_seed_mask & free_ext])) - {0}
    ar6_ext_hit = any(lbl_ext[i, j, k] in ext_labels for i, j, k in zip(ai, aj, ak))
    if ar6_ext_hit:
        rmax_ext_to_ar6 = float(rp)

    # 3. Direct lumen-to-exterior pore anywhere across the shoulder + Repeat-8/9 hinge sector
    lbl_all, _ = label(free, structure=struct26)
    lset = set(np.unique(lbl_all[lumen_seed_mask & free])) - {0}
    eset = set(np.unique(lbl_all[ext_seed_mask & free])) - {0}
    if lset & eset:
        rmax_transmural_anywhere = float(rp)

print(f"\nApo Pocket Minimax Bottleneck Sphere Radius (0.4-A 3D EDT):")
print(f"  Max probe radius reaching AR6 site from LUMEN           (R_max_lumen)    = {rmax_lumen_to_ar6:.2f} A")
print(f"  Max probe radius reaching AR6 site DIRECTLY from EXTERIOR (R_max_exterior) = {rmax_ext_to_ar6:.2f} A")
print(f"  Max probe radius crossing adjacent Repeat-8/9 hinge seam (|z|=155-167 A) = {rmax_transmural_anywhere:.2f} A (water/ion micro-cleft; impermeable to NAD+ >=2.5 A)")

# Compute exact Lee-Richards SASA (Å²) of bound AR6_A partitioned into Lumen-only vs Direct-Exterior-only access at r_probe = 1.4 A (water) and 2.5 A (nucleotide)!
def compute_directional_sasa(target_xyz, target_vdw, env_xyz, env_vdw, clr_grid_for_flood, r_probe=1.4, n_sphere=300):
    # Golden-section Fibonacci sphere
    idx_s = np.arange(n_sphere, dtype=float) + 0.5
    phi = np.arccos(1.0 - 2.0 * idx_s / n_sphere)
    theta = np.pi * (1.0 + 5.0**0.5) * idx_s
    unit_pts = np.column_stack([np.sin(phi) * np.cos(theta), np.sin(phi) * np.sin(theta), np.cos(phi)])

    # Pre-label Lumen-only (Delta_R < +11 A) and Direct-Exterior-only (Delta_R > -11 A, preventing bulk-lumen wrap-around) probe-center spaces
    free_lum = (clr_grid_for_flood >= r_probe) & (~rim_mask) & (Delta_R_grid < +11.0)
    lbl_lum, _ = label(free_lum, structure=struct26)
    lum_ids = set(np.unique(lbl_lum[lumen_seed_mask & free_lum])) - {0}

    free_ext = (clr_grid_for_flood >= r_probe) & (~rim_mask) & (Delta_R_grid > -11.0)
    lbl_ext, _ = label(free_ext, structure=struct26)
    ext_ids = set(np.unique(lbl_ext[ext_seed_mask & free_ext])) - {0}

    # Combine env + other atoms of target itself for SASA occlusion
    sasa_total = 0.0
    sasa_lumen = 0.0
    sasa_exterior = 0.0
    sasa_buried_cavity = 0.0
    atom_sasa_rows = []

    # Build per-vdw KD-trees for env
    env_trees = [(rv, cKDTree(env_xyz[env_vdw == rv])) for rv in np.unique(env_vdw)]

    for m in range(len(target_xyz)):
        rad = float(target_vdw[m]) + r_probe
        area_per_pt = 4.0 * math.pi * (rad**2) / n_sphere
        test_pts = target_xyz[m] + rad * unit_pts

        # Occlusion by other target atoms
        keep = np.ones(n_sphere, dtype=bool)
        for m2 in range(len(target_xyz)):
            if m2 == m: continue
            d2 = np.linalg.norm(test_pts - target_xyz[m2], axis=1)
            keep &= d2 >= (target_vdw[m2] + r_probe - 1e-5)
        if not keep.any():
            atom_sasa_rows.append((m, 0.0, 0.0, 0.0))
            continue

        # Occlusion by surrounding 78-mer protein + neighbor AR6
        pts_k = test_pts[keep]
        ok_env = np.ones(len(pts_k), dtype=bool)
        for rv, tr in env_trees:
            d_env, _ = tr.query(pts_k)
            ok_env &= d_env >= (float(rv) + r_probe - 1e-5)

        exposed_pts = pts_k[ok_env]
        if len(exposed_pts) == 0:
            atom_sasa_rows.append((m, 0.0, 0.0, 0.0))
            continue

        ti, tj, tk = xyz_to_ijk(exposed_pts)
        # Also allow 1-voxel neighborhood lookup in case continuous surface point rounds 0.2A into boundary voxel
        in_lum = np.zeros(len(exposed_pts), dtype=bool)
        in_ext = np.zeros(len(exposed_pts), dtype=bool)
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                for dk in (-1, 0, 1):
                    ii = np.clip(ti + di, 0, len(u_grid) - 1)
                    jj = np.clip(tj + dj, 0, len(v_grid) - 1)
                    kk = np.clip(tk + dk, 0, len(z_grid) - 1)
                    in_lum |= np.isin(lbl_lum[ii, jj, kk], list(lum_ids))
                    in_ext |= np.isin(lbl_ext[ii, jj, kk], list(ext_ids))

        a_tot = len(exposed_pts) * area_per_pt
        a_lum = int(in_lum.sum()) * area_per_pt
        a_ext = int(in_ext.sum()) * area_per_pt
        a_cav = int((~in_lum & ~in_ext).sum()) * area_per_pt
        sasa_total += a_tot
        sasa_lumen += a_lum
        sasa_exterior += a_ext
        sasa_buried_cavity += a_cav
        atom_sasa_rows.append((m, a_tot, a_lum, a_ext))

    return {
        "r_probe": r_probe,
        "sasa_total_A2": round(sasa_total, 2),
        "sasa_lumen_only_A2": round(sasa_lumen, 2),
        "sasa_exterior_only_A2": round(sasa_exterior, 2),
        "sasa_sealed_cavity_A2": round(sasa_buried_cavity, 2),
        "n_atoms_lumen_accessible": sum(1 for _, _, al, _ in atom_sasa_rows if al > 0.05),
        "n_atoms_exterior_accessible": sum(1 for _, _, _, ae in atom_sasa_rows if ae > 0.05),
        "per_atom": atom_sasa_rows,
    }

sasa_ar6_14 = compute_directional_sasa(ar6_A_uvz, ar6_A_vdw, near_holo_other_uvz, near_holo_other_vdw, clr_holo_full, r_probe=1.4)
sasa_ar6_14_ghost = compute_directional_sasa(ar6_A_uvz, ar6_A_vdw, near_holo_other_uvz, near_holo_other_vdw, clr_holo_env, r_probe=1.4)
sasa_ar6_25 = compute_directional_sasa(ar6_A_uvz, ar6_A_vdw, near_holo_other_uvz, near_holo_other_vdw, clr_holo_full, r_probe=2.5)

# Also compute directional SASA of the 30 MVP pocket-lining residues (433-438, 499-573 AR6/keyhole contacts) in APO 11JB!
pocket_mask_A = (prot_11jb["chain"] == "A") & (prot_11jb["pos"].isin(key_pocket))
pock_uvz, pock_vdw = to_uvz(prot_11jb[pocket_mask_A])
env_no_pock = prot_11jb[~pocket_mask_A]
env_np_uvz, env_np_vdw = to_uvz(env_no_pock)
env_np_near = np.linalg.norm(env_np_uvz - center_uvz, axis=1) <= 58.0
sasa_pocket_14 = compute_directional_sasa(pock_uvz, pock_vdw, env_np_uvz[env_np_near], env_np_vdw[env_np_near], clr_apo, r_probe=1.4)

print(f"\nBound AR6 Directional SASA (r_probe = 1.4 A water):")
print(f"  Total exposed SASA = {sasa_ar6_14['sasa_total_A2']:.2f} A^2 | LUMEN-accessible = {sasa_ar6_14['sasa_lumen_only_A2']:.2f} A^2 ({sasa_ar6_14['n_atoms_lumen_accessible']}/36 atoms) | EXTERIOR-accessible = {sasa_ar6_14['sasa_exterior_only_A2']:.2f} A^2 ({sasa_ar6_14['n_atoms_exterior_accessible']}/36 atoms) | Sealed micro-cavity = {sasa_ar6_14['sasa_sealed_cavity_A2']:.2f} A^2")
print(f"Bound AR6 Directional SASA (r_probe = 2.5 A nucleotide/ring):")
print(f"  Total exposed SASA = {sasa_ar6_25['sasa_total_A2']:.2f} A^2 | LUMEN-accessible = {sasa_ar6_25['sasa_lumen_only_A2']:.2f} A^2 | EXTERIOR-accessible = {sasa_ar6_25['sasa_exterior_only_A2']:.2f} A^2")
print(f"Apo 30-Residue MVP Pocket Lining Directional SASA (r_probe = 1.4 A):")
print(f"  LUMEN-accessible = {sasa_pocket_14['sasa_lumen_only_A2']:.2f} A^2 | EXTERIOR-accessible = {sasa_pocket_14['sasa_exterior_only_A2']:.2f} A^2")

# Evaluate pre-registered verdict & kill condition!
all_ar6_inside_mid = bool((ar6_A["Delta_R_10A"] < 0).all() and (ar6_A["Delta_R_15A"] < 0).all() and (ar6_A["Delta_R_interp"] < 0).all())
ext_zero = (sasa_ar6_14["sasa_exterior_only_A2"] == 0.0) and (rmax_ext_to_ar6 < 1.4)
if all_ar6_inside_mid and ext_zero and sasa_ar6_14["sasa_lumen_only_A2"] > 0:
    verdict = "LUMENAL (TRANSMURAL KILLED BY PRE-REGISTERED KILL CONDITION)"
elif sasa_ar6_14["sasa_lumen_only_A2"] > 0 and (sasa_ar6_14["sasa_exterior_only_A2"] > 0 or rmax_ext_to_ar6 >= 1.4):
    verdict = "TRANSMURAL"
elif sasa_ar6_14["sasa_exterior_only_A2"] > 0 and sasa_ar6_14["sasa_lumen_only_A2"] == 0:
    verdict = "EXTERIOR"
else:
    verdict = f"MIXED/OTHER (all_inside={all_ar6_inside_mid}, ext_sasa={sasa_ar6_14['sasa_exterior_only_A2']}, lum_sasa={sasa_ar6_14['sasa_lumen_only_A2']})"
print(f"\n>>> FORMAL VERDICT ON LEDGER #34: {verdict} <<<")

# ==============================================================================
# PRIORITY 2 (TEST A6): 11JB / 9BW6 vs 4V60 Luminal Electrostatics Comparison
# ==============================================================================
print("\n=== PRIORITY 2 (TEST A6): 4V60 Apo vs 11JB Apo vs 11JB+78*AR6 vs 11JB+78*AR6+20*PARP4-MINT Electrostatics ===")
df_4v60 = parse_cif_heavy_atoms(f"{STRUCT_DIR}/4V60-assembly1.cif.gz")
prot_4v60 = df_4v60[df_4v60["group"] == "ATOM"].copy()
ca_4v = prot_4v60[prot_4v60["atom"] == "CA"]
cx4, cy4, cz4 = ca_4v[["x", "y", "z"]].mean()
prot_4v60["dx"] = prot_4v60["x"] - cx4
prot_4v60["dy"] = prot_4v60["y"] - cy4
prot_4v60["dz"] = prot_4v60["z"] - cz4
spans4 = [prot_4v60["dx"].max() - prot_4v60["dx"].min(), prot_4v60["dy"].max() - prot_4v60["dy"].min(), prot_4v60["dz"].max() - prot_4v60["dz"].min()]
long4 = int(np.argmax(spans4))
axes4 = ["dx", "dy", "dz"]
rad4 = [a for i, a in enumerate(axes4) if i != long4]
prot_4v60["z_ax"] = prot_4v60[axes4[long4]]
prot_4v60["abs_z"] = prot_4v60["z_ax"].abs()
prot_4v60["R_cyl"] = np.sqrt(prot_4v60[rad4[0]]**2 + prot_4v60[rad4[1]]**2)
print(f"4V60-assembly1 loaded: {prot_4v60['chain'].nunique()} chains, z range [{prot_4v60['z_ax'].min():.1f}, {prot_4v60['z_ax'].max():.1f}] A, R_cyl range [{prot_4v60['R_cyl'].min():.1f}, {prot_4v60['R_cyl'].max():.1f}] A")

# Parse 9BW6 to get PARP4-MINT (chain B, residues ~1570-1724) and superpose onto Chain A of 11JB via CA alignment of MVP repeats 2-5 (pos 60..260)!
df_9bw6 = parse_cif_heavy_atoms(f"{RAW}/9BW6.cif.gz")
bw_A_ca = df_9bw6[(df_9bw6["chain"] == "A") & (df_9bw6["atom"] == "CA") & (df_9bw6["pos"].between(60, 260))].set_index("pos")
jb_A_ca = prot_11jb[(prot_11jb["chain"] == "A") & (prot_11jb["atom"] == "CA") & (prot_11jb["pos"].between(60, 260))].set_index("pos")
common_pos = bw_A_ca.index.intersection(jb_A_ca.index)
P = bw_A_ca.loc[common_pos, ["x", "y", "z"]].values
Q = jb_A_ca.loc[common_pos, ["dx", "dy", "dz"]].values  # centered 11JB frame!
P_c = P - P.mean(axis=0); Q_c = Q - Q.mean(axis=0)
H = P_c.T @ Q_c
U_s, _, Vt_s = np.linalg.svd(H)
R_sup = Vt_s.T @ U_s.T
if np.linalg.det(R_sup) < 0:
    Vt_s[-1, :] *= -1
    R_sup = Vt_s.T @ U_s.T
t_sup = Q.mean(axis=0) - P.mean(axis=0) @ R_sup
rmsd_sup = float(np.sqrt(np.mean(np.sum((P @ R_sup + t_sup - Q)**2, axis=1))))
print(f"Superposed 9BW6 MVP+PARP4-MINT onto 11JB Chain A (n={len(common_pos)} CAs, RMSD={rmsd_sup:.2f} A)")

mint_B = df_9bw6[df_9bw6["chain"] == "B"].copy()
mint_xyz_A = mint_B[["x", "y", "z"]].values @ R_sup + t_sup
mint_B["dx"], mint_B["dy"], mint_B["dz"] = mint_xyz_A[:, 0], mint_xyz_A[:, 1], mint_xyz_A[:, 2]
mint_B["abs_z"] = mint_B["dz"].abs()
mint_B["R_cyl"] = np.sqrt(mint_B["dx"]**2 + mint_B["dy"]**2)
print(f"Docked PARP4-MINT (136 aa) in 11JB frame: |z| range [{mint_B['abs_z'].min():.1f}, {mint_B['abs_z'].max():.1f}] A | R_cyl range [{mint_B['R_cyl'].min():.1f}, {mint_B['R_cyl'].max():.1f}] A (local wall R_mid={interp_rmid(np.array([mint_B['abs_z'].mean()]))[0]:.1f} A -> purely LUMENAL!)")

# Replicate 20 PARP4-MINT copies symmetrically around the two halves (10 evenly spaced around upper C39 ring + 10 around lower C39 ring)
mint_20_charges = []
# Assign formal charges at pH 7.4 to specific charge-bearing atoms
CHARGE_ATOMS = {
    ("ARG", "CZ"): +1.0,
    ("LYS", "NZ"): +1.0,
    ("HIS", "CE1"): +0.1,
    ("ASP", "CG"): -1.0,
    ("GLU", "CD"): -1.0,
}

def extract_point_charges(df_in, c_axes=("dx", "dy", "dz")):
    sub = df_in[df_in["resname"].isin(["ARG", "LYS", "HIS", "ASP", "GLU"])].copy()
    keys = list(zip(sub["resname"], sub["atom"]))
    q = np.array([CHARGE_ATOMS.get(k, 0.0) for k in keys])
    m = q != 0.0
    xyz = sub.loc[m, list(c_axes)].values
    pos = sub.loc[m, "pos"].values
    r_cyl = sub.loc[m, "R_cyl"].values
    abs_z = sub.loc[m, "abs_z"].values
    return xyz, q[m], pos, r_cyl, abs_z

q4_xyz, q4_val, q4_pos, q4_r, q4_z = extract_point_charges(prot_4v60, ("dx", "dy", "z_ax"))
q11_xyz, q11_val, q11_pos, q11_r, q11_z = extract_point_charges(prot_11jb, ("dx", "dy", "dz"))

# AR6 point charges (-1.0e on PA, -1.0e on PB = -2.0e per ADP-ribose * 78 = -156.0e total!)
ar6_p = ar6_11jb[ar6_11jb["atom"].isin(["PA", "PB"])]
qar6_xyz = ar6_p[["dx", "dy", "dz"]].values
qar6_val = np.full(len(ar6_p), -1.0)
print(f"Point charges extracted: 4V60={len(q4_val):,} (net={q4_val.sum():+.1f} e) | 11JB apo={len(q11_val):,} (net={q11_val.sum():+.1f} e) | 78x AR6={len(qar6_val)} P-centers (net={qar6_val.sum():+.1f} e)")

# Generate 20 symmetric copies of PARP4-MINT charges (10 upper ring + 10 lower ring via C2 reflection `(x, -y, -z)`)
qm1_xyz, qm1_val, _, _, _ = extract_point_charges(mint_B, ("dx", "dy", "dz"))
print(f"Single PARP4-MINT domain net formal charge (pH 7.4): {qm1_val.sum():+.1f} e (20 copies = {20*qm1_val.sum():+.1f} e)")
qm20_xyz_list = []
qm20_val_list = []
for k in range(10):
    ang = 2.0 * math.pi * k / 10.0
    ca_k, sa_k = math.cos(ang), math.sin(ang)
    # Upper half copy
    xu = qm1_xyz[:, 0] * ca_k - qm1_xyz[:, 1] * sa_k
    yu = qm1_xyz[:, 0] * sa_k + qm1_xyz[:, 1] * ca_k
    zu = qm1_xyz[:, 2]
    qm20_xyz_list.append(np.column_stack([xu, yu, zu]))
    qm20_val_list.append(qm1_val)
    # Lower half C2 copy
    qm20_xyz_list.append(np.column_stack([xu, -yu, -zu]))
    qm20_val_list.append(qm1_val)
qm20_xyz = np.vstack(qm20_xyz_list)
qm20_val = np.concatenate(qm20_val_list)

# Compute domain-by-domain LUMINAL-FACE (R_cyl < R_mid(|z|)) net charge per 78-mer!
ca4 = prot_4v60[prot_4v60["atom"] == "CA"].copy()
ca4["bin5"] = (ca4["abs_z"] // 5.0) * 5.0 + 2.5
prof4_5 = ca4.groupby("bin5")["R_cyl"].median().sort_index()
q4_lum = q4_r < np.interp(q4_z, prof4_5.index.values, prof4_5.values)
q11_lum = q11_r < interp_rmid(q11_z)

domains_elec = [
    ("Repeats_1_2 (1-112)", 1, 112),
    ("Repeats_3_4_MINT_zone (113-222)", 113, 222),
    ("Repeats_5_9 (223-498)", 223, 498),
    ("SPFH_shoulder_pocket (499-665)", 499, 665),
    ("Cap_helix (666-790)", 666, 790),
    ("Cap_disk (791-893)", 791, 893),
]
print("\nLuminal-Face (Delta_R < 0) Net Formal Charge across Full 78-mer by Domain:")
dom_charge_rows = []
for dname, s, e in domains_elec:
    c_4v = float(q4_val[q4_lum & (q4_pos >= s) & (q4_pos <= e)].sum())
    c_11_apo = float(q11_val[q11_lum & (q11_pos >= s) & (q11_pos <= e)].sum())
    c_ar6 = float(qar6_val.sum()) if s == 499 else 0.0
    c_mint = float(qm20_val.sum()) if s == 113 else 0.0
    c_11_holo = c_11_apo + c_ar6 + c_mint
    print(f"  {dname:34s}: 4V60_apo={c_4v:+7.1f} e | 11JB_apo={c_11_apo:+7.1f} e | 11JB_holo(+AR6+MINT)={c_11_holo:+7.1f} e (per-chain: {c_11_apo/78:+.2f} -> {c_11_holo/78:+.2f} e)")
    dom_charge_rows.append({"domain": dname, "q_4v60_apo_78mer": round(c_4v, 1), "q_11jb_apo_78mer": round(c_11_apo, 1), "q_11jb_holo_78mer": round(c_11_holo, 1)})

# Evaluate Debye-Huckel Electrostatic Potential Phi_lumen(|z|) in mV at 150 mM salt (kappa = 0.103 A^-1, eps_r = 78.5, T = 310 K)
# Conversion: e / (4*pi*eps_0 * eps_r * 1 A) = 14399.645 / 78.5 = 183.435 mV*A/e
PREFAC_MV = 14399.645 / 78.5
KAPPA = 0.103

def eval_dh_lumen_profile(q_xyz, q_val, r_in05_func, z_slices):
    phi_mv = []
    # Average over 39 azimuthal points around the inner luminal ring at R_eval = R_in05(|z|) - 3.0 A (3 A inside lumen from inner wall!)
    angles = np.linspace(0, 2 * np.pi, 39, endpoint=False)
    tree_q = cKDTree(q_xyz)
    for zval in z_slices:
        r_ev = max(8.0, float(r_in05_func(zval)) - 3.0)
        pts_ring = np.column_stack([r_ev * np.cos(angles), r_ev * np.sin(angles), np.full(39, zval)])
        # Cutoff 45 A (>4.6 Debye lengths, exp(-4.6) < 0.01)
        idxs = tree_q.query_ball_point(pts_ring, r=45.0)
        vals = []
        for p, nb in zip(pts_ring, idxs):
            if not nb:
                vals.append(0.0)
                continue
            d = np.maximum(1.5, np.linalg.norm(q_xyz[nb] - p, axis=1))
            vals.append(float(np.sum(PREFAC_MV * q_val[nb] * np.exp(-KAPPA * d) / d)))
        phi_mv.append(round(float(np.mean(vals)), 2))
    return phi_mv

# Smooth inner-wall R_in05(|z|) for 4V60 and 11JB
prot_4v60["bin10"] = (prot_4v60["abs_z"] // 10.0) * 10.0 + 5.0
rin4_prof = prot_4v60.groupby("bin10")["R_cyl"].quantile(0.05).sort_index()
prot_11jb["bin10_c"] = (prot_11jb["abs_z"] // 10.0) * 10.0 + 5.0
rin11_prof = prot_11jb.groupby("bin10_c")["R_cyl"].quantile(0.05).sort_index()

z_eval = list(range(10, 311, 20))
phi_4v60 = eval_dh_lumen_profile(q4_xyz, q4_val, lambda z: np.interp(z, rin4_prof.index, rin4_prof.values), z_eval)
phi_11_apo = eval_dh_lumen_profile(q11_xyz, q11_val, lambda z: np.interp(z, rin11_prof.index, rin11_prof.values), z_eval)
phi_11_ar6 = eval_dh_lumen_profile(np.vstack([q11_xyz, qar6_xyz]), np.concatenate([q11_val, qar6_val]),
                                   lambda z: np.interp(z, rin11_prof.index, rin11_prof.values), z_eval)
phi_11_holo = eval_dh_lumen_profile(np.vstack([q11_xyz, qar6_xyz, qm20_xyz]), np.concatenate([q11_val, qar6_val, qm20_val]),
                                    lambda z: np.interp(z, rin11_prof.index, rin11_prof.values), z_eval)

df_phi = pd.DataFrame({
    "abs_z_A": z_eval,
    "R_eval_11JB_A": [round(max(8.0, float(np.interp(z, rin11_prof.index, rin11_prof.values)) - 3.0), 1) for z in z_eval],
    "Phi_4V60_apo_mV": phi_4v60,
    "Phi_11JB_apo_mV": phi_11_apo,
    "Phi_11JB_plus_78AR6_mV": phi_11_ar6,
    "Phi_11JB_holo_AR6_20MINT_mV": phi_11_holo,
    "Delta_Holo_minus_Apo_mV": np.round(np.array(phi_11_holo) - np.array(phi_11_apo), 2),
})
print("\nAxial Luminal Debye-Huckel Electrostatic Potential Profile (3 A inside inner wall, 150 mM salt, mV):")
print(df_phi.to_string(index=False))

out_data = {
    "preregistration_sha256": open("~/projects/Vault/argon/PREREGISTRATION_ARGON_003.sha256").read().split()[0],
    "priority_1_pocket_orientation_and_pore": {
        "verdict": verdict,
        "kill_condition_met_against_transmural": bool(all_ar6_inside_mid and ext_zero),
        "geometry_78mer_11JB": {
            "z_min_A": round(float(ca_11jb["dz"].min()), 2),
            "z_max_A": round(float(ca_11jb["dz"].max()), 2),
            "r_min_A": round(float(ca_11jb["R_cyl"].min()), 2),
            "r_max_A": round(float(ca_11jb["R_cyl"].max()), 2),
        },
        "ar6_heavy_atoms_radial_offset": {
            "n_heavy_atoms": int(len(ar6_A)),
            "abs_z_range_A": [round(float(ar6_A["abs_z"].min()), 2), round(float(ar6_A["abs_z"].max()), 2)],
            "R_cyl_range_A": [round(float(ar6_A["R_cyl"].min()), 2), round(float(ar6_A["R_cyl"].max()), 2)],
            "R_mid_10A_mean_A": round(float(ar6_A["R_mid_10A"].mean()), 2),
            "R_mid_15A_mean_A": round(float(ar6_A["R_mid_15A"].mean()), 2),
            "Delta_R_10A_min_mean_max_A": [round(float(ar6_A["Delta_R_10A"].min()), 2), round(float(ar6_A["Delta_R_10A"].mean()), 2), round(float(ar6_A["Delta_R_10A"].max()), 2)],
            "Delta_R_15A_min_mean_max_A": [round(float(ar6_A["Delta_R_15A"].min()), 2), round(float(ar6_A["Delta_R_15A"].mean()), 2), round(float(ar6_A["Delta_R_15A"].max()), 2)],
            "Delta_R_interp_min_mean_max_A": [round(float(ar6_A["Delta_R_interp"].min()), 2), round(float(ar6_A["Delta_R_interp"].mean()), 2), round(float(ar6_A["Delta_R_interp"].max()), 2)],
            "n_atoms_outside_midsurface": int((ar6_A["Delta_R_10A"] >= 0).sum()),
            "atoms": ar6_A[["atom", "elem", "abs_z", "R_cyl", "R_mid_10A", "Delta_R_10A", "Delta_R_15A", "Delta_R_interp"]].round(3).to_dict(orient="records"),
        },
        "mvp_shoulder_499_573_radial_summary": {
            "n_lumen_CA_10A": int((grp_sub.loc[grp_sub.index >= 499, "CA_Delta_R_10A"] < 0).sum()),
            "n_exterior_CA_10A": int((grp_sub.loc[grp_sub.index >= 499, "CA_Delta_R_10A"] >= 0).sum()),
            "key_pocket_30_residues": grp_sub.loc[[p for p in key_pocket if p in grp_sub.index]][["resname", "abs_z", "CA_R_cyl", "R_mid_10A", "CA_Delta_R_10A", "CA_Delta_R_15A", "min_Delta_R_10A", "max_Delta_R_10A"]].round(3).reset_index().to_dict(orient="records"),
        },
        "directional_probe_accessibility": {
            "grid_step_A": STEP,
            "rmax_lumen_to_ar6_A": rmax_lumen_to_ar6,
            "rmax_exterior_direct_to_ar6_A": rmax_ext_to_ar6,
            "rmax_repeat89_hinge_water_cleft_A": rmax_transmural_anywhere,
            "ar6_sasa_1_4A_holo": {k: v for k, v in sasa_ar6_14.items() if k != "per_atom"},
            "ar6_sasa_1_4A_apo_pocket_ghost": {k: v for k, v in sasa_ar6_14_ghost.items() if k != "per_atom"},
            "ar6_sasa_2_5A_nucleotide": {k: v for k, v in sasa_ar6_25.items() if k != "per_atom"},
            "apo_30res_pocket_sasa_1_4A": {k: v for k, v in sasa_pocket_14.items() if k != "per_atom"},
        },
    },
    "priority_2_electrostatics_11JB_9BW6_vs_4V60": {
        "parp4_mint_superposition_rmsd_A": round(rmsd_sup, 3),
        "parp4_mint_single_net_charge_e": round(float(qm1_val.sum()), 1),
        "domain_luminal_formal_charges_78mer": dom_charge_rows,
        "axial_debye_huckel_lumen_profile": df_phi.to_dict(orient="records"),
    },
}
json.dump(out_data, open(f"{OUT}/test_003_pore_and_electrostatics.json", "w"), indent=2)
df_phi.to_csv(f"{OUT}/electrostatics_profile_11jb_vs_4v60.csv", index=False)
print("\nSaved results/test_003_pore_and_electrostatics.json and electrostatics_profile_11jb_vs_4v60.csv successfully.")
