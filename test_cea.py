from rocketcea.cea_obj import CEA_Obj, add_new_propellant

def run_test():
    al_pct = 15.0
    htpb_pct = 15.0
    ap_pct = 70.0
    
    print("Testing original way (all 'fuel'):")
    prop_name1 = "APCP_ALL_FUEL"
    add_new_propellant(prop_name1, f"""
fuel NH4CLO4(I)       wt%={ap_pct}
fuel R-45(HTPB FROM_RPL_DATA) C 7.3165 H 10.3360 O 0.1063    wt%={htpb_pct}
h,cal= 1200.0 t(k)=298.15 rho=0.9220
fuel Aluminum  AL 1       wt%={al_pct}
h,cal=0.0     t(k)=298.15
""")
    cea1 = CEA_Obj(propName=prop_name1)
    print("Tcomb =", cea1.get_Tcomb(Pc=1000.0, MR=1.0) * 5.0/9.0)

    print("\nTesting 'name' instead of 'fuel':")
    prop_name2 = "APCP_NAME"
    add_new_propellant(prop_name2, f"""
name NH4CLO4(I)       wt%={ap_pct}
name R-45(HTPB FROM_RPL_DATA) C 7.3165 H 10.3360 O 0.1063    wt%={htpb_pct}
h,cal= 1200.0 t(k)=298.15 rho=0.9220
name Aluminum  AL 1       wt%={al_pct}
h,cal=0.0     t(k)=298.15
""")
    cea2 = CEA_Obj(propName=prop_name2)
    # When propName is used, it acts like a monopropellant, so MR is ignored?
    print("Tcomb =", cea2.get_Tcomb(Pc=1000.0, MR=1.0) * 5.0/9.0)

    print("\nTesting 'oxid' and 'fuel' with true MR:")
    prop_name3 = "APCP_SEP"
    # Actually add_new_propellant creates a mono-propellant?
    # No, let's see. If we use oxid and fuel, we must use add_new_oxidizer and add_new_fuel?
    pass

run_test()
