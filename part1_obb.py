import open3d as o3d
import os

files = [
    "data/CUBE.obj",
    "data/CYLINDER.obj",
    "data/TEAPOT.obj"
]

for file in files:

    print("=" * 60)
    print(f"Processing: {file}")

    mesh = o3d.io.read_triangle_mesh(file)

    if mesh.is_empty():
        print("Could not load mesh")
        continue

    mesh.compute_vertex_normals()

    obb = mesh.get_oriented_bounding_box()
    obb.color = (1, 0, 0)

    length, width, height = obb.extent
    volume = length * width * height

    print(f"Length : {length:.3f}")
    print(f"Width  : {width:.3f}")
    print(f"Height : {height:.3f}")
    print(f"Volume : {volume:.3f}")

    coordinate = o3d.geometry.TriangleMesh.create_coordinate_frame(size=20)

    vis = o3d.visualization.Visualizer()
    vis.create_window("OBB Visualization", width=1000, height=700)

    vis.add_geometry(mesh)
    vis.add_geometry(obb)

    vis.run()
    vis.destroy_window()