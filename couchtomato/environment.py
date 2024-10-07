from couchtomato.core.settings import Settings

class Env:

    ''' Environment variables '''
    _debug = False
    _settings = Settings()
    _options = None
    _args = None
    _quiet = False
    _deamonize = False

    ''' Data paths and directories '''
    _app_dir = ""
    _data_dir = ""
    _db_path = ""

    @staticmethod
    def doDebug():
        return Env._debug

    @staticmethod
    def get(attr):
        return getattr(Env, '_' + attr)

    @staticmethod
    def set(attr, value):
        return setattr(Env, '_' + attr, value)

    @staticmethod
    def setting(attr, section = 'global', value = None, default = ''):
        # Return setting
        if value == None:
            return Env.get('settings').get(attr, default = default, section = section)
            
        # Set setting
        s = Env.get('settings')
        s.set(section, attr, value)
        return s