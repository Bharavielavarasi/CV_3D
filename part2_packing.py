import json,time,random
import open3d as o3d

MASTER_BOX=(100,100,100)
COLORS={"standard_box":(0.2,0.5,1),"flat_panel":(1,0.5,0),"long_beam":(1,0,0),
"large_crate":(0,0.8,0),"medium_cube":(0.7,0.2,0.8),"small_filler":(1,1,0),
"long_box":(0,1,1),"flat_box":(1,0.3,0.6)}

with open("data/Item List.json") as f: raw=json.load(f)

class Item:
    def __init__(self,d):
        self.id=d["id"]; self.length,self.width,self.height=d["dims"]; self.type=d["type"]
        self.volume=self.length*self.width*self.height
        self.x=self.y=self.z=None
    def __repr__(self):
        return f"Item {self.id} [{self.type}] {self.length}x{self.width}x{self.height} -> ({self.x},{self.y},{self.z})"

def collide(it,x,y,z,placed):
    for p in placed:
        if x<p.x+p.length and x+it.length>p.x and y<p.y+p.width and y+it.width>p.y and z<p.z+p.height and z+it.height>p.z:
            return True
    return False

def supported(it,x,y,z,placed):
    if z==0:return True
    for p in placed:
        if p.z+p.height==z:
            xo=max(0,min(x+it.length,p.x+p.length)-max(x,p.x))
            yo=max(0,min(y+it.width,p.y+p.width)-max(y,p.y))
            if xo>0 and yo>0:return True
    return False

def pack(items):
    items.sort(key=lambda i:i.volume,reverse=True)
    placed=[]; cand=[(0,0,0)]
    for it in items:
        cand=sorted(set(cand),key=lambda c:(c[2],c[1],c[0]))
        ok=False
        for x,y,z in cand:
            if x+it.length>100 or y+it.width>100 or z+it.height>100: continue
            if collide(it,x,y,z,placed): continue
            if not supported(it,x,y,z,placed): continue
            it.x,it.y,it.z=x,y,z
            placed.append(it)
            cand.extend([(x+it.length,y,z),(x,y+it.width,z),(x,y,z+it.height)])
            ok=True
            break
        if not ok: raise RuntimeError(f"Cannot place item {it.id}")
    return placed

def visualize(items):
    vis=o3d.visualization.Visualizer()
    vis.create_window("3D Packing",1200,800)
    frame=o3d.geometry.TriangleMesh.create_coordinate_frame(size=10)
    vis.add_geometry(frame)
    master=o3d.geometry.LineSet.create_from_axis_aligned_bounding_box(
        o3d.geometry.AxisAlignedBoundingBox((0,0,0),MASTER_BOX))
    vis.add_geometry(master)
    for it in items:
        b=o3d.geometry.TriangleMesh.create_box(width=it.length,height=it.width,depth=it.height)
        b.translate((it.x,it.y,it.z))
        b.compute_vertex_normals()
        b.paint_uniform_color(COLORS.get(it.type,(random.random(),random.random(),random.random())))
        vis.add_geometry(b)
        vis.poll_events(); vis.update_renderer(); time.sleep(0.3)
    vis.run(); vis.destroy_window()

items=[Item(d) for d in raw]
placed=pack(items)
print("="*60)
print("Packing Summary")
used=0
for p in placed:
    print(p); used+=p.volume
total=100*100*100
print(f"Total Volume: {total}")
print(f"Used Volume : {used}")
print(f"Free Volume : {total-used}")
print(f"Utilization : {used/total*100:.2f}%")
visualize(placed)