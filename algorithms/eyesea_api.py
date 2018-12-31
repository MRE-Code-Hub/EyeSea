# eysesea_api.py
# Algorithm API for EyeSea application.
# 
'''
Copyright 2018 Battelle Memorial Institute. All rights reserved.
'''

import argparse
import os
import json
import datetime
#import annotator as a


# parse command line arguments based on json file definitions
def get_args(jfile):
    parser = argparse.ArgumentParser()
    parser.add_argument("vidfile", help="video file to process")
    parser.add_argument("outfile", help="output file for results")

    
    # TODO: support type= type from json file
    if os.path.isfile(jfile):
        with open(jfile, 'r') as f:
            jsondata = json.load(f)
    else:
        eye_env = os.environ
        for i in eye_env['PATH'].split(os.pathsep):
            if os.path.isfile(i + os.sep + jfile):
                with open(i + os.sep + jfile, 'r') as f:
                    jsondata = json.load(f)
    
    for jarg in jsondata["parameters"]:
        parser.add_argument( jarg["arg"], 
            help=jarg["help"],
            default=jarg["default"],
            type=int if jarg["type"] == "int" else (float if jarg["type"] == "float" else str))

    parser.add_argument('--verbose', '-v', action='store_true')

    return parser.parse_args()

class BBox():
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

class Frame():
    def __init__(self, index, img, detections=list() ):
        self.frameindex = index #the frame index of image filename
        self.detections = detections #a list of bounding boxes
        self.img = img #a numpy array containing the pixel data
        
class Annotations():
    def __init__(self, videosource, user, frames=list(), last_edit=str(datetime.datetime.now())):
        self.source = videosource #the video this frame comes from
        self.user = user #last user to edit this file
        self.last_edit = last_edit
        self.frames = frames
        
            
#This writes the annotations to a custom json file.
# annotations: an annotation object containing all of the bounding data
# out: a writable object, such as an open file handle
def annotations_to_json(annotations, output):
    output.write("{") # annotations
    output.write(" \"source\": \"" + annotations.source + "\",\n")
    output.write(" \"user\": \"" + annotations.user + "\",\n")
    output.write(" \"last_edit\": \"" + annotations.last_edit + "\",\n")
    output.write(" \"frames\": [\n") # frames
    
    frames = annotations.frames
    for i in range(len(frames)):
        output.write(" {\n") # frame
        output.write("  \"frameindex\": " + str(frames[i].frameindex) + ",\n")
        output.write("  \"detections\": [\n") # detections
        
        
        #for detection in frame.detections:
        detections = frames[i].detections
        for j in range(len(detections)):
            output.write("  {\n") # detection
            output.write("   \"x1\": " + str(detections[j].x1) + ",\n")
            output.write("   \"y1\": " + str(detections[j].y1) + ",\n")
            output.write("   \"x2\": " + str(detections[j].x2) + ",\n")
            output.write("   \"y2\": " + str(detections[j].y2) + "\n")
            output.write("  }")
            if (j < len(detections) -1 ):
                output.write(",\n") # /detection
            else:
                output.write("\n")
        output.write("  ]\n") # /detections
        output.write(" }")
        if (i < len(frames)-1):
            output.write(",\n")
        else:
            output.write("\n") # /frame
    output.write(" ]\n") # /frames
    
    output.write("}\n") # /annotations
        
        
def json_to_annotations(f):
    jsondata = json.load(f)
    
    frames = list()
    for jsonframe in jsondata["frames"]:
        detections = list()
        for jsondetection in jsonframe["detections"]:
            detections.append( BBox(jsondetection["x1"], jsondetection["y1"], jsondetection["x2"], jsondetection["y2"]) )
        frames.append(Frame(jsonframe["frameindex"], None, detections ) )
    
    annotations = Annotations(jsondata["source"], jsondata["user"], frames, jsondata["last_edit"])
    
    return annotations

# save_results() translates from common object
# detection file formats into eyesea json format
def save_results(results, outfile):
    with open(outfile,'w') as f:
        #json.dump(results,f)
        annotations_to_json(results, f)

# TODO:  add structure/class for eyesea json format

if __name__ == "__main__":
    print("testing eysea_api")
    # TODO:  add tests
    args = get_args('algorithm.json.example')
