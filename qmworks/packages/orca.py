# =======>  Standard and third party Python Libraries <======
from noodles import (Storable)
import pkg_resources as pkg
import plams

# ==================> Internal Modules  <=====================
from qmworks.settings import Settings
from qmworks.packages.packages import Package, Result
from qmworks.fileFunctions import json2Settings
# ========================= ADF ============================


class _PropertyGetter(Storable):
    def __init__(self, result, section):
        super(_PropertyGetter, self).__init__()
        self.result = result
        self.section = section

    def __getattr__(self, prop):
        pass

    def __getitem__(self, prop):
        pass


class ORCA(Package):
    """
    """
    def __init__(self):
        super(ORCA, self).__init__("orca")
        self.generic_dict_file = 'generic2ORCA.json'

    def prerun(self):
        pass

    def run_job(self, settings, mol, job_name="ORCAjob"):

        orca_settings = Settings()
        orca_settings.input = settings.specific.orca
        print(orca_settings)
        result = plams.ORCAJob(molecule=mol, settings=orca_settings, name=job_name).run()

        return ORCA_Result(orca_settings, mol, result)

    def postrun(self):
        pass

    def handle_special_keywords(self, settings, key, value, mol):
        pass


class ORCA_Result(Result):
    """Class providing access to PLAMS OrcaJob result results"""

    def __init__(self, settings, molecule, result):
        self.settings = settings
        self._molecule = molecule
        self.result = result
        properties = 'data/dictionaries/propertiesORCA.json'
        xs = pkg.resource_string("qmworks", properties)
        self.prop_dict = json2Settings(xs)

    def as_dict(self):
        return {
            "settings": self.settings,
            "molecule": self._molecule,
            "filename": self.result.path}

    @classmethod
    def from_dict(cls, settings, molecule, filename):
        pass

    def __getattr__(self, prop):
        """Returns a section of the results.

        Example:

        ..

            dipole = result.properties.dipole

        """
        r = self.result.awk_output(script = self.prop_dict[prop])
        try:
            result = [float(i) for i in r]
        except:
            result = r
        if len(result) == 1:
            result = result[0]
        return result

    @property
    def molecule(self):
        pass
    
orca = ORCA()
