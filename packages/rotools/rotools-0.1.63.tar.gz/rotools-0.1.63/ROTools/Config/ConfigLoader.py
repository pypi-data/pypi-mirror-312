from ROTools.Config.Config import Config
from ROTools.Helpers.DictObj import DictObj


def _config_constructor(loader, node):
    fields = loader.construct_mapping(node, deep=True)
    for item in fields.items():
        if isinstance(item[1], dict):
            fields[item[0]] = DictObj(item[1])
    return Config(**fields)


def build_config(file_name, skip_dump=False, prefix=None):
    config_loader = ConfigLoader(file_name, prefix=prefix)
    config = config_loader.build_config()

    if config.app.config_dump and not skip_dump:
        config.dump_config()

    return config


class ConfigLoader:
    def __init__(self, file_name, prefix):
        self.file_name = file_name
        self.prefix = prefix

    def build_config(self):
        import yaml
        yaml.add_constructor('!Config', _config_constructor)

        with open(self.file_name, 'r') as file:
            content = file.read()
        config = yaml.load(content, Loader=yaml.FullLoader)
        if self.prefix is not None:
            config.add_env_data(prefix=self.prefix)
        return config
