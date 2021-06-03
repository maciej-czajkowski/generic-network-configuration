
# trzeba wymyśleć algorytm jak będzie juniper i to uprościć
class configurationTranslator:
  def __init__(self):
    pass
  def parseCisco2GenericJson(self, parsedConfig):
    self.cisco2Generic = ciscoGenericTranslator()
    result = {}
    for line in parsedConfig:
        for entry in line:
            if entry.startswith("interface"):
                for key in self.cisco2Generic.complexDictionary.get("interfaces").keys():
                    if entry.startswith(key):
                        resultKey = key + entry.replace(key, "")
                        result[resultKey] = {"test": "value"}
                        break
            for key in self.cisco2Generic.simpleDictionary.keys():
                if entry.startswith(key):
                    result[key] = entry.replace(key, "")
                    break
    return result


# --- list of generic keys, those names will be used for all translators cisco-generic, juniper-generic, generic-cisco etc.
GENERIC_HOSTNAME = "hostname"
GENERIC_ENABLE_PASSWORD = "enable password"

# --- list of complex keys, those names will be used for all translators cisco-generic, juniper-generic, generic-cisco etc.
GENERIC_FASTETHERNET_INTERFACE = "interface FastEthernet"


# --- translator cisco - generic
class ciscoGenericTranslator:
    # --- filed names in cisco config
    CISCO_HOSTNAME = "hostname"
    CISCO_ENABLE_PASSWORD = "enable password"

    # --- complex filed names in cisco config
    CISCO_FASTETHERNET_INTERFACE = "interface FastEthernet"

    def __init__(self):
        # --- we create a dictionary between cisco field name and generci field name used in json (here both are the same, they will probably differ in other config files)
        self.simpleDictionary = { self.CISCO_HOSTNAME        : GENERIC_HOSTNAME,
                                  self.CISCO_ENABLE_PASSWORD : GENERIC_ENABLE_PASSWORD}
        self.complexDictionary = { "interfaces" : {self.CISCO_FASTETHERNET_INTERFACE : GENERIC_FASTETHERNET_INTERFACE } }



