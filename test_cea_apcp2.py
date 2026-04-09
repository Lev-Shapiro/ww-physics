from rocketcea.cea_obj import CEA_Obj, add_new_propellant

add_new_propellant("APCP_NO_AL", """
name NH4CLO4(I)       wt%=85.0
name R-45(HTPB FROM_RPL_DATA) C 7.3165 H 10.3360 O 0.1063    wt%=15.0
h,cal= 1200.0 t(k)=298.15 rho=0.9220
""")

add_new_propellant("APCP_15_AL", """
name NH4CLO4(I)       wt%=70.0
name R-45(HTPB FROM_RPL_DATA) C 7.3165 H 10.3360 O 0.1063    wt%=15.0
h,cal= 1200.0 t(k)=298.15 rho=0.9220
name Aluminum  AL 1       wt%=15.0
h,cal=0.0     t(k)=298.15
""")

add_new_propellant("APCP_20_AL", """
name NH4CLO4(I)       wt%=68.0
name R-45(HTPB FROM_RPL_DATA) C 7.3165 H 10.3360 O 0.1063    wt%=12.0
h,cal= 1200.0 t(k)=298.15 rho=0.9220
name Aluminum  AL 1       wt%=20.0
h,cal=0.0     t(k)=298.15
""")


cea1 = CEA_Obj(propName="APCP_NO_AL")
print("No Al Tcomb =", cea1.get_Tcomb(Pc=1000.0, MR=1.0) * 5.0/9.0)

cea2 = CEA_Obj(propName="APCP_15_AL")
print("15% Al Tcomb =", cea2.get_Tcomb(Pc=1000.0, MR=1.0) * 5.0/9.0)

cea3 = CEA_Obj(propName="APCP_20_AL")
print("20% Al Tcomb =", cea3.get_Tcomb(Pc=1000.0, MR=1.0) * 5.0/9.0)

