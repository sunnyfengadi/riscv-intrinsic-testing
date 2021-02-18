def GenerateBitMap(): 
    with open('mask_bit_map.h', 'w') as f:
        for booltype in (32,16,8):
            #Lines = "uint32_t BOOL"+ str(booltype) +'_T_BITP[' + str(booltype) + '] = {' 
            for i in range(booltype): # BITP
                bitp = int(64-64/booltype*(i+1))
                Lines = str(bitp) + ','
                f.writelines(Lines)
        # for booltype in (32,16,8):
        #     f.writelines("/* mask bit map for bool"+str(booltype)+"_t */\n")
        #     for i in range(booltype): # BITP
        #         bitp = int(64-64/booltype*(i+1))
        #         Lines = '#define BOOL'+ str(booltype) +'_t_BITP'+ str(i) + '\t'+ str(bitp) +'\n'
        #         print(booltype, bitp, Lines)
        #         f.writelines(Lines)
        #     for i in range(booltype): # BITM
        #         bitp = int(64-64/booltype*(i+1))
        #         Lines = '#define BOOL'+ str(booltype) +'_t_BITM' + str(i) +'\t ( 0b01 << '+ 'BOOL' + str(booltype) + '_T_BITP'+ str(i) +' ) \n'
        #         print(booltype, bitp, Lines)
        #         f.writelines(Lines)
            f.writelines("\n")
    f.close()

def main():
    GenerateBitMap()
        
if __name__ == "__main__":  
    main() 