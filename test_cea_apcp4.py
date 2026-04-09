from rocketcea.cea_obj import CEA_Obj, add_new_propellant
add_new_propellant("APCP_NO_AL", """
name NH4CLO4(I)       wt%=85.0
name R-45(HTPB FROM_RPL_DATA) C 7.3165 H 10.3360 O 0.1063    wt%=15.0
h,cal= 1200.0 t(k)=298.15 rho=0.9220
""")
cea = CEA_Obj(propName="APCP_NO_AL")
print(cea.get_full_cea_output(Pc=1000.0, MR=1.0, short_output=1))
