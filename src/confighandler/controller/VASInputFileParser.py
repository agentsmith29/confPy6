
import ast
import logging
#import velox.controller.velox_config as velox_config

class Structure():

    def __init__(self, name: str, x_in: int, y_in: int, x_out: int, y_out: int, enabled: bool, repetitions: int):
        self.name = name
        self.x_in = x_in                # x coordinate of the input point
        self.y_in = y_in                # y coordinate of the input point
        self.x_out = x_out              # x coordinate of the output point
        self.y_out = y_out              # y coordinate of the output point
        self.enabled = bool(enabled)    # True if the structure is enabled
        self.repetitions = repetitions    # Number of repeated measurements of the structure
        
        self.is_reference(False)
        self.in_out_diff_x = self.x_in - self.x_out
        self.in_out_diff_y = self.y_in - self.y_out

        self.measurement_valid = False

    def __str__(self) -> str:
        return (f"{self.repetitions} x Structure ({self.name}, {self.enabled}): "
            f"IN ({self.x_in}, {self.y_in}), "
            f"OUT ({self.x_out} {self.y_out})")
    
    def __repr__(self) -> str:
        return (f"{self.repetitions} x Structure ({self.name}, {self.enabled}): "
            f"IN ({self.x_in}, {self.y_in}), "
            f"OUT ({self.x_out} {self.y_out})")
        
    def is_reference(self, is_reference: bool = False):
        if isinstance(is_reference, bool):
            self.is_reference = is_reference
        return  self.is_reference

class VASInputFileParser():

    

    def __init__(self) -> None:
        self.logger = logging.getLogger("ParseInputFile")
        self.grouped_structures = {}

        self.list_of_structures = {}
        self.list_of_bookmarks = {}
        self.num_of_structs = 0
        self.num_of_runs = 0

       

    def convert(self, key, value):
        value = ast.literal_eval(f"{value}")
        return key, value
    
    def parse_line(self, line):
        line = line.strip()
        # check if line is empty
        line_split = line.split('=')
        if len(line_split) == 2:
            key = line_split[0].strip().replace(' ', '')
            value = line_split[1].strip().replace(' ', '')
        else:
            raise Exception(f"More than 2 parameters extracted. Expected 2 in line {line}")       
    
        return key, value
    
    def as_bookmark(self, key, value):
        self.list_of_bookmarks[key] = value

    def as_single_struct(self, key, value):
        # convert to structure
        if "enabled" not in value:
            value['enabled'] = True

        if "repetitions" not in value:
            value['repetitions'] = 1

        structure = Structure(
            key,
            int(value['x_in']), int(value['y_in']), 
            int(value['x_out']), int(value['y_out']), 
            int(value['enabled']), 
            int(value['repetitions']))

        self.list_of_structures[key] = structure
        self.num_of_runs += structure.repetitions
        return [(key, structure)]
        
    
    def as_sequential_structs(self, key, value):
        cur_list_of_structures = []
        num = value['num'] 
        spacing = 0

        for idx in range(num):
            if idx > 0:
                spacing = value['spacing'] 
                
            value['y_in'] = value['y_in'] + spacing
            value['y_out'] = value['y_out'] + spacing
            key_seq = f"{key}_{idx+1}"
            structs = self.as_single_struct(key_seq, value)[0]
            cur_list_of_structures.append((structs[0], structs[1]))

        return cur_list_of_structures


    def read_file(self, input_file):
        current_group = None
        cur_list_of_structures = {}
        structs = []
        #list_of_structures = {}
        self.logger.info(f"Reading input file: {input_file}")
        with open(input_file, 'r') as f:
            for idx, line in enumerate(f):
                # check if line is empty
                if line.startswith('#') or len(line.strip().replace(' ', '')) == 0:
                    continue
                
                key, value = self.parse_line(line)
                if key == "group":
                    if len(cur_list_of_structures) > 0:
                        self.grouped_structures[current_group] = cur_list_of_structures
                        cur_list_of_structures = {}
                        structs = []
                    current_group = value
                    continue
                else:
                    key, value = self.convert(key, value)    
                    
                #list_of_structures[key] = value
                if "bookmark" in key: 
                    self.as_bookmark(key, value)
                elif ("num" in value) and ("spacing" in value):
                    structs = self.as_sequential_structs(key, value)
                else:
                    structs = self.as_single_struct(key, value)
                
                # convert to dictionary
                for struct in structs:
                    cur_list_of_structures[struct[0]] = struct[1]
        
        if len(cur_list_of_structures) > 0:
            self.grouped_structures[current_group] = cur_list_of_structures
            cur_list_of_structures = {}

        self.num_of_structs = len( 
            [
            key for key in self.list_of_structures if self.list_of_structures[key].enabled == True
            ] 
        ) 
        return self.grouped_structures, self.list_of_bookmarks

    # @staticmethod
    # def read_input(vaut_config: velox_config.VAutomatorConfig):
    #     filename_rel = vaut_config.automator_config.structure_file.rel
    #     filename = vaut_config.automator_config.structure_file.abs
    #     ParseInputFile.logger.info("Reading input file: %s" % filename_rel)
       

    #     number_of_structures = 0

    #     list_of_structure_groups = []
    #     list_of_bookmarks = []
    #     list_of_structs_sub = []

    #     with open(filename, 'r') as f:
            
    #         for idx, line in enumerate(f):
    #             line = line.strip()

    #             if line.strip().startswith('#') or line.strip().replace(' ', '') == '':
    #                 continue # skip comment lines
    #             else:
    #                 line_split = line.split('=')
    #                 if len(line_split) == 2:
    #                     varname = line_split[0].strip().replace(' ', '')
    #                     varcontent = line_split[1].strip().replace(' ', '')
    #                 else:
    #                     raise Exception("Error in line %d: %s" % (idx, line))
                    
    #                 if cmd != line.replace(' ', ''):
    #                         raise ValueError(
    #                             "Error parsing command, could not correctly seperate the string."
    #                             "\nPlease check your input line %d:\nin >>  '%s'\nout << '%s'" 
    #                             % (idx, line.replace(' ', ''), cmd))
                            
    #                 # Parse the lines
    #                 if "bookmark" in line:
    #                     cmd = ("%s=%s" % (varname, varcontent)).strip()
    #                     # Check if command is the same
    #                     if cmd != line.replace(' ', ''):
    #                         raise ValueError(
    #                             "Error parsing command, could not correctly seperate the string."
    #                             "\nPlease check your input line %d:\nin >>  '%s'\nout << '%s'" 
    #                             % (idx, line.replace(' ', ''), cmd))
    #                     else:
    #                         setattr(ParseInputFile, varname, {})
    #                         # Exec ( assign the value to the attribute)
    #                         exec("%s.%s" % ("ParseInputFile", cmd) )
    #                         # retrieve the value als correct type
    #                         var_content = getattr(ParseInputFile, varname)
    #                         # Add this structure to the list
    #                         list_of_bookmarks.append({varname:var_content} )
    #                         #-uc-# print("Bookmark %s" % list_of_bookmarks[-1])
    #                 # Only if we have the keyword "spacing" and "num" in line, then proceed
    #                 elif ("num" in line) and ("spacing" in line):
                      
    #                     cmd = ("%s=%s" % (varname, varcontent)).strip()
    #                     # Check if command is the same
    #                     if cmd != line.replace(' ', ''):
    #                         raise ValueError(
    #                             "Error parsing command, could not correctly seperate the string."
    #                             "\nPlease check your input line %d:\nin >>  '%s'\nout << '%s'" 
    #                             % (idx, line.replace(' ', ''), cmd))
    #                     else:
    #                         # Set the attribute for later accessing
    #                         setattr(ParseInputFile, varname, {})
    #                         # Exec ( assign the value to the attribute)
    #                         exec("%s.%s" % ("ParseInputFile", cmd) )
    #                         # retrieve the value als correct type
    #                         var_content = getattr(ParseInputFile, varname)
    #                         try:
    #                             if var_content['num'] <= 0:
    #                                 raise ValueError("'num': Number of structur list can not be zero or below. Error in line %d: %s" % (idx, line))
    #                         except:
    #                             raise ValueError("'num' keyword not found in dictionry. Error in line %d: %s" % (idx, line))
                            
    #                         try:
    #                             if var_content['spacing'] == 0:
    #                                 raise ValueError("'spacing': Spacing can not be zero. Error in line %d: %s" % (idx, line))
    #                         except:
    #                             raise ValueError("'spacing' keyword not found in dictionry. Error in line %d: %s" % (idx, line))

                               
                            
    #                         for idx in range(0, var_content['num']):
    #                             try:
    #                                 num_start = var_content['start'] + 1
    #                             except:
    #                                 num_start = 1
                                    
    #                             y_in_temp = var_content['y_in'] + idx * var_content['spacing']
    #                             y_out_temp = var_content['y_out'] + idx * var_content['spacing']
    #                             x_in_temp = var_content['x_in']
    #                             x_out_temp = var_content['x_out']
    #                             if 'rep' not in var_content:
    #                                 var_content['rep'] = 1
                                
    #                             var_content_tmp ={
    #                                 'x_in':         x_in_temp,
    #                                 'y_in':         y_in_temp,       # Convert y-axis to negative values
    #                                 'x_out':        x_out_temp,
    #                                 'y_out':        y_out_temp,      # Convert y-axis to negative values
    #                                 'in_out_diff_x' :x_in_temp - x_out_temp,
    #                                 'in_out_diff_y' :y_in_temp - y_out_temp,
    #                                 'enabled':       True,
    #                                 'rep':    var_content['rep']
    #                                 }
    #                             list_of_structs_sub.append( {varname+"_"+str(idx+num_start):var_content_tmp} )    
    #                         number_of_structures += var_content['num']                        
    #                 elif "group" in line:
    #                         groupname = line_split[1].strip().replace(' ', '')
                            
    #                         if list_of_structs_sub == []:
    #                             #-uc-# print ("Init group %s" % groupname)
    #                             list_of_structs_sub = []
    #                         else:
                                
    #                             if list_of_structs_sub != []:
    #                                 #-uc-# print ("Adding data %s to list" % (list_of_structs_sub))
    #                                 list_of_structure_groups.append(list_of_structs_sub)
    #                             #-uc-# print ("New group %s, reset group" % groupname)
    #                             list_of_structs_sub = []
    #                 else:                            
    #                     cmd = ("%s=%s" % (varname, varcontent)).strip()
    #                     # Check if command is the same
    #                     if cmd != line.replace(' ', ''):
    #                         raise ValueError(
    #                             "Error parsing command, could not correctly seperate the string."
    #                             "\nPlease check your input line %d:\nin >>  '%s'\nout << '%s'" 
    #                             % (idx, line.replace(' ', ''), cmd))
    #                     else:
    #                         # Set the attribute for later accessing
    #                         setattr(ParseInputFile, varname, {})
    #                         # Exec ( assign the value to the attribute)
    #                         exec("%s.%s" % ("ParseInputFile", cmd) )
    #                         # retrieve the value als correct type
    #                         var_content = getattr(ParseInputFile, varname)
    #                         if 'rep' not in var_content:
    #                             var_content['rep'] = 1
    #                         # Add this structure to the list
    #                         try: 
    #                             var_content_tmp ={
    #                                     'x_in':             var_content['x_in'],
    #                                     'y_in':             var_content['y_in'],
    #                                     'x_out':            var_content['x_out'],
    #                                     'y_out':            var_content['y_out'],
    #                                     'in_out_diff_x' :   var_content['x_in'] - var_content['x_out'],
    #                                     'in_out_diff_y' :   var_content['y_in'] - var_content['y_out'],
    #                                     'enabled':          True,
    #                                     'rep':              var_content['rep']
    #                             }
    #                         except:
    #                             raise ValueError("Error in line %d: %s" % (idx, line))
    #                         list_of_structs_sub.append( {varname:var_content_tmp} )
    #                         number_of_structures += 1
        

    #         # Append the last group
    #         if list_of_structs_sub != []:
    #             #-uc-# print ("Adding last data %s to list" % (list_of_structs_sub))
    #             list_of_structure_groups.append(list_of_structs_sub)
    #         #-uc-# print ("Last group %s" % groupname)
    #         list_of_structs_sub = []
        
    #     #print(len(list_of_structure_groups))
    #     # for gr in list_of_structure_groups:
    #     #     print("Group: %s\n\n" % gr)
    #     ParseInputFile.logger.info("Total number of structures to process %s" % number_of_structures)
    #     return list_of_structure_groups, list_of_bookmarks, number_of_structures

    def write_bookmarks(
        self, cell_name="MaskARY1_final_2020_Feb_14", 
        bookmark_file="bookmarks.lyb"
    ):
        print(f"Writing bookmarks to file {bookmark_file}") 
        
        with open(bookmark_file, 'w+') as f:
            f.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<bookmarks>\n")
            for bookmark in self.list_of_bookmarks:
                print(f"{bookmark}: {bookmarks[bookmark]}")
                for key in bookmark:
                    bookmar_string =  (
                          "<bookmark>\n"
                        + " <name>" + str(bookmark) + "</name>\n"
                        + " <x-left>" + str(bookmarks[bookmark]['x_left']) + "</x-left>\n"
                        + " <x-right>" + str(bookmarks[bookmark]['x_right']) + "</x-right>\n"
                        + " <y-bottom>" + str(bookmarks[bookmark]['y_bottom']) + "</y-bottom>\n"
                        + " <y-top>" + str(bookmarks[bookmark]['y_top']) + "</y-top>\n"
                        + " <min-hier>0</min-hier>\n"
                        + " <max-hier>9</max-hier>\n"
                        + " <cellpaths>\n"
                        + "  <cellpath>\n"
                        + "   <cellname>" + str(cell_name) + "</cellname>\n"
                        + "  </cellpath>\n"
                        + " </cellpaths>\n"
                        + "</bookmark>" 
                    )

                f.write(bookmar_string + "\n")
            f.write("</bookmarks>")


# pi = ParseInputFile()
# grouped_structures, bookmarks = pi.read_file(input_file="./list_of_structures.vas")


# for groups in grouped_structures:
#     print(f"Group *{groups}*")
#     for structs in grouped_structures[groups]:
#         print(f"  -> {grouped_structures[groups][structs]}")

# #for bookmark in bookmarks:
# #    print(f"{bookmark}: {bookmarks[bookmark]}")

# print(pi.num_of_runs)