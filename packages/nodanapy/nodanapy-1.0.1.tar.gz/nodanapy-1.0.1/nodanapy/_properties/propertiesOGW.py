import numpy as np
import petpropy as pp

class PropertiesOil:
    def __init__(self, pressure, temperature, api, specific_gravity, bubble_pressure):
        self.pressure = pressure
        self.temperature = temperature
        self.api = api
        self.specific_gravity = specific_gravity
        self.bubble_pressure = bubble_pressure
        
        self.pressures = np.linspace(start=14.7, stop=self.pressure, num=25)
        
        
    def rs_oil(self, model='standing', P_separator=0, T_separator=0,):
        models = {
            'standing': pp.Rs.standing,
            'lasater': pp.Rs.lasater,
            'glaso': pp.Rs.glaso,
            'total': pp.Rs.total,
            'dokla': pp.Rs.dokla_osman,
            'petrosky': pp.Rs.petrosky_farshad,
        }
        
        models_c = {
            'vazquez': pp.Rs.vazquez, # CORRECTION
            'kartoatmodjo': pp.Rs.kartoatmodjo_schmidt, # CORRECTION
        }
        
        if model in models:
            rs = models[model](self.pressures, self.temperature, self.specific_gravity, self.api, Pb=self.bubble_pressure)
        elif model in models_c:
            rs = models_c[model](self.pressures, self.temperature, self.specific_gravity, self.api, Pb=self.bubble_pressure, P_sp=P_separator, T_sp=T_separator)
        
        return rs       
    
    def co_oil(self, model='vazquez', P_separator=0, T_separator=0,):
        rs = self.rs_oil()
        
        models = {
            'vazquez': pp.c_o.vazquez_beggs, # correction
            'kartoatmodjo': pp.c_o.kartoatmodjo_schmidt, # correction
        }
        
        if model in models:
            co = models[model](self.pressures, self.temperature, self.api, self.specific_gravity, rs, P_sp=P_separator, T_sp=T_separator)
        elif model == 'petrosky':
            co = pp.c_o.petrosky_farshad(self.pressures, self.temperature, self.api, self.specific_gravity, rs),
        elif model == 'maccain':
            co = pp.c_o.maccain_rollins_villena(self.pressures, self.temperature, self.api, self.specific_gravity, Rs=rs, Pb=self.bubble_pressure),

        return co
    
    def fvf_oil(self, model='standing', P_separator=0, T_separator=0,):
        rs = self.rs_oil()
        co = self.co_oil()[-1]
        
        models = {
            'standing': pp.Bo.standing,
            'glaso': pp.Bo.glaso,
            'total': pp.Bo.total,
            'almarhoun': pp.Bo.almarhoun,
            'dokla': pp.Bo.dokla_osman,
            'petrosky': pp.Bo.petrosky_farshad,
        }
        
        models_c = {
            'vazquez': pp.Bo.vazquez_beggs, # CORRECTION
            'kartoatmodjo': pp.Bo.kartoatmodjo_schmidt, # CORRECTION
        }
        
        if model in models:
            fvf_o = models[model](T=self.temperature, R_sb=rs, gamma_api=self.api, gamma_gas=self.specific_gravity, P=self.pressures, Pb=self.bubble_pressure, co=co)
        elif model in models_c:
            fvf_o = models_c[model](T=self.temperature, R_sb=rs, gamma_api=self.api, gamma_gas=self.specific_gravity, P=self.pressures, Pb=self.bubble_pressure, co=co, P_sp=P_separator, T_sp=T_separator)
        
        return fvf_o
    
    def rho_oil(self, model='vazquez',):
        rs = self.rs_oil()
        fvf_o = self.fvf_oil()
        
        models = {
            'vazquez': pp.rho_o.vazquez_beggs,
            'petrosky': pp.rho_o.petrosky_farshad,
        }
        
        if model in models:
            rho_o = models[model](self.pressures, self.temperature, self.bubble_pressure, fvf_o, rs, self.specific_gravity, self.api)
        elif model == 'standing':
            rho_o = pp.rho_o.standing(self.temperature, rs, self.specific_gravity, self.api)
        elif model == 'ahmed':
            rho_o = pp.rho_o.ahmed(self.pressures, self.bubble_pressure, fvf_o, rs, self.specific_gravity, self.api),
            
        return rho_o
    
    def mu_oil(self, mod_uod='Karto', mod_uob='Karto', mod_uo='Karto'):
        rs = self.rs_oil()
        mu = pp.mu_o.mu_oil(self.pressures, self.temperature, self.api, rs, Pb=self.bubble_pressure, model_uod=mod_uod, model_uob=mod_uob, model_uo=mod_uo)
        return mu
    
    def sigma_oil(self,):
        sigma = pp.sigma_o.baker_swedloff(self.pressures, self.temperature, self.api)
        return sigma
        
        
class PropertiesGas:
    def __init__(self, pressure, temperature, specific_gravity,):
        self.pressure = pressure
        self.temperature = temperature
        self.specific_gravity = specific_gravity
        
        self.pressures = np.linspace(start=14.7, stop=self.pressure, num=25)
        
    def prc_gas(self, y_co2=0, y_h2s=0, y_n2=0):
        pr = pp.pc_g.sutton(self.specific_gravity, yCO2=y_co2, yH2S=y_h2s, yN2=y_n2)
        return pr          
        
    def z_gas(self, model='dranchuk'):
        
        pc, tc = self.prc_gas()
        
        models = {
            'papay': pp.z_g.papay,
            'brill': pp.z_g.brill_beggs,
            'hall': pp.z_g.hall_yarborough,
            'gopal': pp.z_g.gopal,
            'dranchuk': pp.z_g.dranchuk_abou_kassem,
            'purvis': pp.z_g.dranchuk_purvis_robinson,
        }
    
        if model in models:
            z = models[model](self.pressures, self.temperature, pc, tc)
            
        return z
    
    def rho_gas(self,):
        
        z = self.z_gas()
        
        rho = pp.rho_g.rho_gas(self.pressures, self.temperature, self.specific_gravity, z)
        
        return rho
        
    def fvf_gas(self,):
        
        z = self.z_gas()
        
        bg = pp.Bg.B_g(self.pressures, self.temperature, z, units=True)
        
        return bg
    
    def mu_gas(self,):
        
        mg = 28.9645*self.specific_gravity
        z = self.z_gas()
        
        mu = pp.mu_g.lee_gonzalez_eakin(self.pressures, self.temperature, mg, z)
        
        return mu
        
    def co_gas(self, model='brill',):
        
        pc, tc = self.prc_gas()
        z = self.z_gas()
        
        models = {
            'papay': pp.c_g.papay,
            'brill': pp.c_g.brill_beggs,
            #'gopal': pp.c_g.gopal,
        }
        
        if model in models:
            co = models[model](self.pressures, self.temperature, pc, tc, z)
            
        return np.abs(co)
    
    def exp_gas(self,):
        bg = self.fvf_gas()
        eg = pp.Bg.E_g(Bg=bg)
        return eg
        
class PropertiesWater:
    def __init__(self, pressure, temperature, salinity):
        self.pressure = pressure
        self.temperature = temperature
        self.salinity = salinity
        
        self.pressures = np.linspace(start=14.7, stop=self.pressure, num=25)
        
    def fvf_water(self, model='mccain'):
        
        if model == 'mccoy':
            bw = pp.Bw.mccoy(self.pressures, self.temperature, S=self.salinity)
        elif model == 'mccain':
            bw = pp.Bw.mccain(self.pressures, self.temperature)
        
        return bw
    
    def rho_water(self, model='mccain'):
        bw = self.fvf_water()
        
        if model == 'normal':
            rho = pp.rho_w.rho_water_equation(bw, S=self.salinity)
        elif model == 'mccain':
            rho = pp.rho_w.mccain(bw, S=self.salinity)
            
        return rho
    
    def rs_water(self, model='mccoy'):
        
        models = {
            'culberson': pp.Rsw.culberson_macketta,
            'mccoy': pp.Rsw.mccoy,
        }
        
        if model in models:
            rs = models[model](self.pressures, self.temperature, S=self.salinity)
            
        return rs
    
    def mu_water(self, model='mccain'):
        
        models = {
            'matthews': pp.mu_w.matthews_russel,
            'mccain': pp.mu_w.mccain,
        }
        
        if model in models:
            mu = models[model](self.pressures, self.temperature, S=self.salinity)
        
        return mu
    
    def co_water(self, model='brill'):
        rs = self.rs_water()
        
        if model == 'dodson':
            co = pp.c_w.dodson_standing(self.pressures, self.temperature, rs, S=self.salinity)
        elif model == 'osif':
            co = pp.c_w.osif(self.pressures, self.temperature, S=self.salinity)
        elif model == 'brill':
            co = pp.c_w.brill_beggs(self.pressures, self.temperature)
            
        return co
    
    def sigma_water(self,):
        sigma = pp.sigma_w.jennings_newman(self.pressures, self.temperature)
            
        return sigma
        
if __name__ == "__main__":
    

    # ps = np.linspace(14.7, 10000, 25)
    # t = 150+460
    # sg = 0.65
    # api = 35
    # pb = 1500
    # rs = pp.Rs.standing(ps, t, sg, api, Pb=pb)
    # bo = pp.Bo.standing(t, rs, api, sg, P=ps, Pb=pb, co=1.5e-6)
    # rho = pp.rho_o.standing(t, rs, sg, api)
    # print(rs, bo, rho)
    
    #co = PropertiesOil(3000, 550, 35, 0.65, 1500).sigma_oil()
    #print(co)
    
    z = PropertiesGas(7000, 650, 0.65).z_gas(model='gopal')
    print(z)
    