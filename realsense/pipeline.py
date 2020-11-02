import pyrealsense2 as rs

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

pipeline.start(config)

try:
    while True:
        frames = pipeline.wait_for_frames()
        depth = frames.get_depth_frame()
        if not depth: 
            continue

        lines = []

        for y in range(48):
            line = [0]*64
            for x in range(640):
                dist = depth.get_distance(x, y*10)
                if 0 < dist and dist < 1:
                    line[int(x/10)] += 1
            lines.append(line)

        for y in range(48):
            output = ""

            for x in lines[y]:
                output += " .:!nhIBXWW"[int(x)]
            print(output)

        print("\n\n\n")

finally:
    pipeline.stop()