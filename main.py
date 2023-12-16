import math 

# function for converting a ip to binary
def convertiptobin(ipadd):
    # return ipadd
    ipadd = str(ipadd)
    split_ip = ipadd.split('.')
    newip = []
    for x in split_ip:
        x=int(x)
        ipaddbin =format(x, '08b') #make it an 8bit format
    
        newip.append(ipaddbin)  
    ipAddBinary = ".".join(newip)
    return ipAddBinary

# function for converting a binary to decimal 
def convertbintoDecimal(binNum):
    decimal = 0
    for digit in binNum:
        decimal = (decimal <<1) | int (digit)
    return decimal

# function for converting binary ip addresses to decimal
def convertbinipAddToDecimal(binIpAdd):
    newip = []
    for x in binIpAdd:
        ipaddDec = str(convertbintoDecimal(x))
        newip.append(ipaddDec) 
        ipAddDecimal = ".".join(newip)
    return ipAddDecimal
    
# function for calculating IP Class
def checkIpClass(ipadd) :
    ipadd = str(ipadd)
    split_ip = ipadd.split('.')
    octet1st = int (split_ip[0])
   
    if(octet1st <= 127) :
        return "class A"
    elif(octet1st <= 191 ) :
        return "class B"
    elif(octet1st <= 223 ) :
        return "class C"
    elif(octet1st <= 239 ) :
        return "class D (Public Ip)"
    elif(octet1st <= 255 ) :
        return "class E (Public and Reserved Ip)"
    else:
        print("input a correct ip addresss")

# function for calculating Network octect and Host Octet based on IP Class      
def numberOfNetworkandHostClass(ipadd):  
    check = checkIpClass(ipadd)
    if(check == "class A"):
        return "11111111.00000000.00000000.0000000"
    elif(check == "class B"):
        return "11111111.11111111.00000000.0000000"
    elif(check == "class C"):
        return"11111111.11111111.11111111.00000000"

#function for calculating bit to be borrowed
def bitBorrowCalc(subnetNum):
    bitBorrow = math.log(subnetNum)/math.log(2 )
    # print(f" bit to borrow is {bitBorrow}")
    return bitBorrow

# function for calculating subnetMaskCalc
def subnetMaskCalc(ipadd, borrowedBit):
    borrowedBit = int(borrowedBit)
    check = checkIpClass(ipadd)
    if(check == "class A"):
        ipAddBin = numberOfNetworkandHostClass(ipadd)
        split_ip = ipAddBin.split('.')
        nextoct = split_ip[1]
        new = nextoct.replace('0','1',borrowedBit)
        split_ip[1] = new
        subnetmask = convertbinipAddToDecimal(split_ip)
        return subnetmask
    elif(check == "class B"):
        ipAddBin = numberOfNetworkandHostClass(ipadd)
        split_ip = ipAddBin.split('.')
        nextoct = split_ip[2]
        new = nextoct.replace('0','1',borrowedBit)
        split_ip[2] = new
        subnetmask = convertbinipAddToDecimal(split_ip)
        return subnetmask
    elif(check == "class C"):
        ipAddBin = numberOfNetworkandHostClass(ipadd)
        split_ip = ipAddBin.split('.')
        nextoct = split_ip[3]
        new = nextoct.replace('0','1',borrowedBit)
        split_ip[3] = new
        subnetmask = convertbinipAddToDecimal(split_ip)
        return subnetmask   
    
# slash value also known as CIDR Notation
def slashvalueCalc(ipadd, borrowedBit):
    borrowedBit = int(borrowedBit)
    checkHostNetwork = numberOfNetworkandHostClass(ipadd)
    numberofNetwork = checkHostNetwork.count('1') 
    slashValue = numberofNetwork + borrowedBit
    slashValueIp = ipadd + "/" + str(slashValue)
    return slashValueIp

# Function to calculate Network Id
def networkIdCalc(ipadd):
    ipadd = str(ipadd)
    split_ip = ipadd.split('.')
    lastoct = split_ip[3] = '0'
    netId = ".".join(str(x) for x in split_ip)
    return(netId) 

# Function to calculate wildcard
def wildcardCalc(ipadd, bitBorrow):
    ipadd = str(ipadd)
    subnetmask = subnetMaskCalc(ipadd, bitBorrow) #calculate subnet mask
    subnetmaskBin = convertiptobin(subnetmask)  #convert to binary
    split_ip = subnetmaskBin.split('.')
    inverseOct = []
    # loop through the given ip octect
    for x in split_ip:
        firstarr =[]  #array to store each index of the octect after inversing
        # lopping through each octect to inverse the value
        for i in x:
            str(i)
            if(i=="1"):
                new = i[0].replace('1','0')
                firstarr.append(new)
            else:
                new = i[0].replace('0','1')
                firstarr.append(new)
        newOct = "".join(str(i) for i in firstarr)  # using join to concatenate each value stored in firstarr
        inverseOct.append(newOct)  # store each octet after inversing
    wildcardBinary = ".".join(str(k) for k in inverseOct)
    wildcardDecimal = convertbinipAddToDecimal(inverseOct)
    return(wildcardDecimal) 

#   calculate available host ip address
def hostIpCalc(ipadd, bitBorrow):
    subnet = subnetMaskCalc(ipadd, bitBorrow)
    split_ip = subnet.split('.')
    checkClass = checkIpClass(ipadd)
    if(checkClass =="class A"):
        nextOct = int(split_ip[1])
    elif(checkClass =="class B"):
        nextOct = int(split_ip[2])
    elif(checkClass =="class C"):
        nextOct = int(split_ip[3])
    availableIp = nextOct - 2  # minus 2 reserved ips (networkIds) 
    return availableIp

# Calculate the broadcast address 
def broadcastIdCalc(ipadd, bitBorrow):
    hostip = hostIpCalc(ipadd, bitBorrow)
    broadcastId = int(hostip) + 1 #plus 1 to enter the last resverd Id
    
    split_ip = ipadd.split('.')
    checkClass = checkIpClass(ipadd)
    if(checkClass =="class A"):
        nextOct = split_ip[1] = broadcastId
    elif(checkClass =="class B"):
        nextOct = split_ip[2] = broadcastId
    elif(checkClass =="class C"):
        nextOct = split_ip[3] = broadcastId
    broadcastIpAdd = ".".join(str(k) for k in split_ip) ; #using join to convert back to ip address
    return broadcastIpAdd

# ________________________________________________________________________________________________
# MAIN FUNCTION 192.168.40.0
# ________________________________________________________________________________________________
def subnetCalc():
    # print("subnet calculator on the way")
    ip_add = str(input("Enter IP address: ")) 
    hostNum = int(input("Enter the number of host (Subnets): ")) 
    split_ip = ip_add.split('.')
    if len(split_ip) != 4:
        print("You have entered incorrect IP address please enter valid IP address")
            
    else:
        # check the class of the ip address
        ipClass = checkIpClass(ip_add)
        #check octet for network and host
        hostnetwork = numberOfNetworkandHostClass(ip_add)
        # calculate number of bit to borrow
        bitBorrow = bitBorrowCalc(hostNum)
        #convert ip to binary format
        ip_binary = convertiptobin(ip_add)
        # calculate slashvalue
        slashvalue = slashvalueCalc(ip_add, bitBorrow)
        # calculate subnetMask
        subnetmask = subnetMaskCalc(ip_add, bitBorrow)
        # calculate subnetMask Binary
        subnetmaskBin = convertiptobin(subnetmask)
        # calculate network Id
        networkId = networkIdCalc(ip_add)
        # calculate wildcard
        wildcard = wildcardCalc(ip_add, bitBorrow)
        # calculate the number of host
        hostIp = hostIpCalc(ip_add, bitBorrow)
        # calculate the broadcast Id 
        broadcastId = broadcastIdCalc(ip_add, bitBorrow)
        
        # checher to be deleted later
        print(f"""
                You Entered:  {ip_add}
                Your Network Id is {networkId}
                Your Ip Binary is: {ip_binary}
                Your Ip Class is: {ipClass}
                The Ip Class Binar is: {hostnetwork}
                The Number of bit to borrow is: {bitBorrow}
                The Slash Value is: {slashvalue}
                The subnetmask is: {subnetmask}
                The wildcard is: {wildcard}
                The Number of available Host IP addresses is {hostIp}
                The Broadcast Id is: {broadcastId}
                
              """)
        
if __name__ == '__main__':
    print("Select operation.")
    print("1. Subnet Calculator")
    print("2. Exit")
    
    while True:
        # take input from the user
        choice = input("Enter choice(1/2): ")
        if choice in ('1', '2'): 
            if choice=='1':
                subnetCalc()
            elif choice=='2':
                break
        else:   
            print("Invalid Input")