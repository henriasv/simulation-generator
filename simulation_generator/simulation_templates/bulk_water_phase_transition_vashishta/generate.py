from pack_water import PackWater

def vashishta_only_water_coeffs(Z_h):
    pair_coeff_string=f"""#   .-.   .-.       .-.
#   : :.-.: :      .' `.
#   : :: :: : .--. `. .'.--. .--.
#   : `' `' ;' .; ; : :' '_.': ..'
#    `.,`.,' `.__,_;:_;`.__.':_;
# element1  element2  element3
#           H  eta  Zi  Zj  lambda1  D  lambda4
#           W  rc  B  gamma  r0  C  cos(theta)

O   O   O  1965.88  9  {-2*Z_h}  {-2*Z_h}  4.43  15.0383876  2.5
             10.0  5.5  0.0  0.0  0.0  0.0  0.0
# Provides H-H interactions
H   H   H  0.0  9  {Z_h} {Z_h} 4.43  0  2.5
             0.0  5.5  0.0  0.0  0.0  0.0  0.0
# Provides H-O-H and H-O interactions (2 body must be equal to H O O)
O   H   H  0.61437  9  {-2*Z_h}  {Z_h}  4.43  1.87988844607  1.51113
             0.0  5.5  52.9333  0.75  1.4  0.0  -0.138267391
# Provides O-H-O and H-O interactions (2 body must be equal to O H H)
H   O   O  0.61437  9  {Z_h}  {-2*Z_h}  4.43  1.87988844607  1.51113
             0.0  5.5  0.0  0.0  0.0  0.0  1.0
# These are all zero, not contributing, but must be here
H   O   H  0.0  0.0  0.0  0.0  0.0  0.0  0.0
             0.0  0.0  0.0  0.0  0.0  0.0  0.0
H   H   O  0.0  0.0  0.0  0.0  0.0  0.0  0.0
             0.0  0.0  0.0  0.0  0.0  0.0  0.0
O   H   O  0.0  0.0  0.0  0.0  0.0  0.0  0.0
             0.0  0.0  0.0  0.0  0.0  0.0  0.0
O   O   H  0.0  0.0  0.0  0.0  0.0  0.0  0.0
             0.0  0.0  0.0  0.0  0.0  0.0  0.0
"""
    return pair_coeff_string

def generate(nummol=400, Z_h=0.33983):
    packer = PackWater(nummol=nummol, density=0.998)
    packer(outfile="bulk_water.data", pbc=2.0)

    pair_coeff_string = vashishta_only_water_coeffs(Z_h=Z_h)
    
    with open("H2O.vashishta", "w") as ofile:
        ofile.write(pair_coeff_string)

if __name__=="__main__":
    generate()