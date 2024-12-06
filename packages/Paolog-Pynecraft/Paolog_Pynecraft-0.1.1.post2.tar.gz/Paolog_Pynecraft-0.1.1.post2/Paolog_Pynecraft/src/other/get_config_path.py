from appdata import AppDataPaths

def get_pynecraft_config_path():
    app_path = AppDataPaths(".pynecraft")
    app_path_data = app_path.app_data_path.replace("..", ".")
    
    return app_path_data