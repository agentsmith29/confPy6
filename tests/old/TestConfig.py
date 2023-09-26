from ConfigHandler.controller.VAutomatorConfig import VAutomatorConfig

if __name__ == "__main__":
    # create a velox config
    velox_config = VAutomatorConfig()
    # dump it
    velox_config.store_config('test.yaml')
    # velox_config = VAutomatorConfig.load_config('./configs/init_config.yaml')

    # print(velox_config)
    # config = VAutomatorConfig.load_config("./../configs/init_config.yaml")
    # config.convert_all_folders()
    # config.create_folder_structure()

    # print(config.output_directory)

    # print(config.automator_config.log_file.rel)
    # print(config.automator_config.structure_file.rel)
    # print(config.automator_config.measurement_output.rel)
    # print(config.automator_config.measurement_mat_file.rel)
    # print(config.automator_config.bookmark_file.rel)
    # print(config.automator_config.scope_image_file.rel)

    # print(config.ad2_device_config.sample_rate)
    # print(config.ad2_device_config.total_samples)
    # print(config.ad2_device_config.sample_time)
    # print(config.ad2_device_config.ad2_raw_out_file.rel)

    # print(config.sacher_laser_config.wavelength_range)
    # print(config.sacher_laser_config.velocity)
    # print(config.sacher_laser_config.acceleration)
    # print(config.sacher_laser_config.start_file.rel)

    # config.store_config("./../configs/init_config_altered.yaml")
