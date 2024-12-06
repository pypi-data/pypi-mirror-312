"""
The main user facing ml-kem tool file.
"""

from quantumcrypto.utils.parameters import P512, P768, P1024
from quantumcrypto.utils.functions import ml_kem_gey_gen, ml_kem_encaps, ml_kem_decaps


class MLKEM:
    """
    ML_KEM
    """

    def __init__(self, parameter_set="1024") -> None:

        if parameter_set == "512":
            self.pm_set = P512
        elif parameter_set == "768":
            self.pm_set = P768
        else:
            self.pm_set = P1024

    def generate_keys(self):
        """
        Creates the keys
        """
        ek, dk = ml_kem_gey_gen(self.pm_set.k, self.pm_set.n1)
        return ek, dk

    def encaps(self, ek: bytes):
        """
        Creates the shared secret key and cipher
        """
        key, cipher = ml_kem_encaps(ek, self.pm_set)
        return key, cipher

    def decaps(self, dk: bytes, cipher: bytes):
        """
        Creates the shared secret key out of cipher
        """
        key = ml_kem_decaps(dk, cipher, self.pm_set)
        return key
