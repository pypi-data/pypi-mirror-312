import io
import json
import pandas as pd
import numpy as np
from importlib.resources import files

class Settings(dict):
    
    def __init__(self):
        super().__init__()
        for json_file in files('openSIMS.Methods.json').iterdir():
            json_string = json_file.read_text()
            method_name = json_file.stem
            method = json.loads(json_string)
            if method['type'] == 'geochron':
                self[method_name] = geochron_setting(method_name,method)
            elif method['type'] == 'geochron_PbPb':
                self[method_name] = PbPb_setting(method_name,method)
            elif method['type'] == 'stable':
                self[method_name] = stable_setting(method_name,method)
            else:
                raise ValueError('Invalid method type')

    def get_ions(self,method,instrument):
        if instrument == 'SHRIMP': 
            return self[method]['ions'] + ['bkg']
        else:
            return self[method]['ions']

    def ions2channels(self,ions,**kwargs):
        channels = dict()
        for ion, channel in kwargs.items():
            if ion in ions:
                channels[ion] = channel
            else:
                channels[ion] = None
        return channels

class setting(dict):
    
    def __init__(self,method_name,pars):
        super().__init__(pars)
        self.name = method_name
        f = files('openSIMS.Methods.csv').joinpath(method_name + '.csv')
        csv_string = f.read_text()
        csv_stringio = io.StringIO(csv_string)
        self['refmats'] = pd.read_csv(csv_stringio,index_col=0)

class geochron_setting(setting):

    def __init__(self,method_name,pars):
        super().__init__(method_name,pars)

    def get_DP(self,refmat):
        L = self['lambda']
        t = self['refmats']['t'][refmat]
        return np.exp(L*t) - 1

    def get_DP_1Ma(self):
        L = self['lambda']
        return np.exp(L) - 1

    def get_y0(self,refmat):
        return self['refmats'].iloc[:,2][refmat]

    def get_labels(self):
        ions = self['ions']
        return {'P':ions[0],'D':ions[2],'d':ions[3]}

class stable_setting(setting):

    def __init__(self,method_name,pars):
        super().__init__(method_name,pars)

    def get_num_den(self):
        num = self['deltaref']['num']
        den = self['deltaref']['den']
        return num, den

    def get_labels(self):
        num, den = self.get_num_den()
        return [f"{n}/{d}" for n, d in zip(num, den)]

class PbPb_setting(setting):

    def __init__(self,method_name,pars):
        super().__init__(method_name,pars)

    def get_Pb76(self,refmat):
        L5, L8  = self['lambda']
        t = self['refmats']['t'][refmat]
        U58 = 1/self['U238U235']
        return U58*(np.exp(L5*t)-1)/(np.exp(L8*t)-1)

    def get_Pb74_0(self,refmat):
        return self['refmats']['Pb74_0'][refmat]
