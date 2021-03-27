import gennetconf as cfg

# cisco -> cisco tree
cisco_config_tree = cfg.CiscoConfigParser("input/ciscoexample.txt").parse()
# print(RenderTree(cisco_config_tree, style=AsciiStyle()).by_attr())

# cisco_tree -> generic
generic_cfg = cfg.Cisco2GenericTranslator(cisco_config_tree).get_json(4)
# print(generic_cfg)

# generic -> juniper_tree
juniper_config_tree = cfg.Generic2JuniperTranslator(generic_cfg).get_root()
# print(RenderTree(juniper_config_tree, style=AsciiStyle()).by_attr())

# juniper_tree -> juniper
juniper_config = cfg.JuniperConfigGenerator(juniper_config_tree)
juniper_config.write_to_file("gen/generatedJuniper.cfg")

