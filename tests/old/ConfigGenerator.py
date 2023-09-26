import time
from pathlib import Path


class VeloxConfigOD():
    use_simulator = True
    wafer_version = "MaskARY1_final_2020_Feb_14"
    wafer_nr = "FSPM1W11G3"

    # Specify the output directory
    output_dir = Path("../../../..")
    output_dir = os.path.join(output_dir, 'measurement_' + str(time.strftime("%Y_%m_%d")), wafer_version, wafer_nr)

    # WORKING DORECTORIES
    # Specify the directoy of the script
    script_source_directory = os.getcwd()  # Path(".").resolve().parent
    # Create the output directory

    # INPUT FILES
    structure_file = 'list_of_structures.txt'
    structure_file_full = os.path.relpath(os.path.join(script_source_directory, structure_file))

    # OUTPUT FILES
    # Stores the measured values
    measurement_filename = "measurement_wafer_%s_%s.txt" % (wafer_nr, time.strftime("%Y%m%d-%H%M"))
    measurement_filename_full = os.path.relpath(os.path.join(output_dir, measurement_filename))

    # Stores the raw data of the digital oscilloscope
    ad2_raw_data = "ad2_out_%s_%s" % (wafer_nr, time.strftime("%Y%m%d-%H%M"))  # Omit file ending!
    ad2_raw_data_full = os.path.relpath(os.path.join(output_dir, 'analog_discovery_2_raw', ad2_raw_data))

    # Stores the logfiles
    log_file = "log_%s_%s.log" % (wafer_nr, time.strftime("%Y%m%d-%H%M"))
    log_file_full = os.path.relpath(os.path.join(output_dir, log_file))
    # logger.set_output_file(log_file_full)

    # Stores the bookmark file
    structure_bookmark_file = "bookmarks_%s.lyb" % (wafer_version)
    structure_bookmark_file_full = os.path.relpath(os.path.join(output_dir, 'bookmarks', structure_bookmark_file))

    # Stores the scope images
    scope_image_files = "scope_%s_" % (wafer_version)  # Omit file ending!
    scope_image_files_full = (os.path.join(output_dir, 'scope_shots', scope_image_files))
