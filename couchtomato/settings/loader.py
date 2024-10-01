from blinker import signal
from couchtomato.core.logger import CPLog
import glob
import os

log = CPLog(__name__)
class SettingsLoader:

    configs = {}

    def __init__(self, root = ''):

        self.settings_register = signal('settings.register')
        self.settings_save = signal('settings.save')

        self.paths = {
            'plugins' : ('couchtomato.core.plugins', os.path.join(root, 'couchtomato', 'core', 'plugins')),
            'providers' : ('couchtomato.core.providers', os.path.join(root, 'couchtomato', 'core', 'providers')),
        }
        for type, tuple in self.paths.items():
            self.addFromDir(tuple[0], tuple[1])

    def run(self):
        did_save = 0
        
        for module, plugin_name in self.configs.items():
            if plugin_name != '__pycache__':
                did_save += self.loadConfig(module, plugin_name, save = False)
            
            if did_save:
                self.settings_save.send()

    def addFromDir(self, module, dir):
        for file in glob.glob(os.path.join(dir, '*')):
            name = os.path.basename(file)
            if os.path.isdir(os.path.join(dir, name)):
                self.addConfig(module, name)

    def loadConfig(self, module, name, save = True):
        module_name = '%s.%s' % (module, name)
        print (module_name)
        try:
            m = getattr(self.loadModule(module_name), name)
            (section, options) = m.config
            self.settings_register.send(section, options = options, save = save)
            return True
        except (Exception, e):
            log.error("Failed loading config for %s: %s" % (name, e))
            return False

    def addConfig(self, module, name):
        self.configs[module] = name

    def loadModule(self, name):
        try:
            m = __import__(name)
            splitted = name.split('.')
            for sub in splitted[1:-1]:
                m = getattr(m, sub)
            return m
        except:
            raise