from rocketcea.cea_obj import CEA_Obj, add_new_propellant
add_new_propellant("APCP_TEST", """
name NH4CLO4(I)       wt%=100.0
""")
cea = CEA_Obj(propName="APCP_TEST")
print(cea.get_full_cea_output(Pc=1000.0, short_output=1))
