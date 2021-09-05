#!/usr/bin/env python
# APP Framework 1.0

import csv
import os
import sys
import shutil
from pprint import pprint

class App:
    def __init__(self):
        self.title_line = sys.argv[0]
        self.counter = 1
        self.workingDir = None
        
    def printCounter(self, data=None):
        print("[%04d] Porcessing: %s" % (self.counter, str(data)))
        self.counter += 1
    
    def initCounter(self, value=1):
        self.counter = value
        
    def run(self):
        self.usage()
        self.process()
        
    def usage(self):
        print("*" * 80)
        print("*", " " * 76, "*")
        print(" " * ((80-12-len(self.title_line))//2), 
            self.title_line,  
            " " * ((80-12-len(self.title_line))//2))
        print("*", " " * 76, "*")
        print("*" * 80)
        
    def input(self, notification, default=None):
        var = input(notification)
        
        if len(var) == 0:
            return default
        else:
            return var
            
    def readCsvToDict(self, filename, encoding="GBK"):
        data = list()
        with open(filename, 'r+', encoding=encoding) as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data
        
    def writeCsvFromDict(self, filename, data, fieldnames=None, encoding="GBK", newline=''):
        if fieldnames is None:
            fieldnames = data[0].keys()

        with open(filename, 'w+', encoding=encoding, newline=newline) as f:
            writer = csv.DictWriter(f,
                fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
            
    def addSuffixToFilename(self, filename, suffix):
        filename, ext = os.path.splitext(filename)
        return filename + suffix + ext
        
    def getWorkingDir(self):
        return self.workingDir
    
    def setWorkingDir(self, wd):
        self.workingDir = wd
        return self.workingDir
        
    def setWorkingDirFromFilename(self, filename):
        return self.setWorkingDir(os.path.dirname(filename))
        
    def process(self):
        pass
        

class MyApp(App): 
    def process(self):
        src_image_path = 'images'
        dst_image_path = 'newimages'
        nofound_property_name = 'nofound'
        input_filename = self.input(
            "请将待处理的文件拖动到此窗口，然后按回车键。", 
            default="./test/product_data_cscart.csv")
        self.setWorkingDirFromFilename(input_filename)
        # pprint(self.workingDir)
        output_filename = self.addSuffixToFilename(input_filename, '_new')
        
        data = self.readCsvToDict(input_filename)
        #pprint(data)
        
        for line in data:
            # add notfound
            line[nofound_property_name] = None
            image_property = line['images']
            dst_image_property = image_property.replace(src_image_path, dst_image_path)
            image_filename = os.path.join(self.getWorkingDir(), image_property)
            dst_image_filename = image_filename.replace(src_image_path, dst_image_path)
            #pprint(image_filename)
            if os.path.exists(image_filename):
                line['images'] = dst_image_property #update data file images property
                #pprint(data['images'])
                os.makedirs(os.path.dirname(dst_image_filename), exist_ok=True)
                shutil.copy(image_filename, dst_image_filename) # copy image to newimages folder
                self.printCounter("[WorkdingDir: %s]%s -> %s" % (self.workingDir, image_property, dst_image_property))
            else:
                line[nofound_property_name] = 1
                self.printCounter("%s not found!" % (image_filename))
                
        fieldnames = list(data[0].keys())
        #pprint(fieldnames)
        self.writeCsvFromDict(output_filename, data, fieldnames=fieldnames)
        
        
if __name__ == "__main__":
    app = MyApp()
    app.run()