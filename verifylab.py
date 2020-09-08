import sys
import fileinput
import os
import json
import sys

def run_az_command(cmd, return_json=True, echo=True):

    try:
        if echo:
            print ("Running command: " + cmd)
        o = os.popen(cmd).read()
        if return_json:
            return json.loads(o)

    except Exception as error:
        print("Error running az command:")
        print(str(error))
        sys.exit(1)        

def az_login(usr, pss):
    print ("Logging in to Azure...")
    cmd = "az login -u " + usr + " -p '" + pss + "'"
    run_az_command(cmd,False,False)

# load the user logins
lines = list(fileinput.input(files=["logins.tsv"]))

# build dictionary of expected resources
expectedResources = {}
expectedResourceCount = 0
rlines = list(fileinput.input(files=["expected_resources.tsv"]))
for rl in rlines:
    expResourceParts = rl.split()
    expectedResources[expResourceParts[0]] = int(expResourceParts[1])
    expectedResourceCount += int(expResourceParts[1])

# save users in a dict to check for dupes
users = {}

# parse username file
count = 0
for line in lines:
    parts = line.split()
    usr = parts[0]
    pss = parts[1]
    count += 1
    print (f"User {count}: {usr}")

    # check for duplicate user
    if usr in users:
        print(f"Duplicate user {usr} found!!!")
        sys.exit(1) 
    else:
        users[usr] = 1

    # log into azure    
    az_login(usr, pss)

    # get the list of resources in the account
    cmd = "az resource list"
    resources = run_az_command(cmd)
    resourceCount = len(resources)
    print (f"{resourceCount} resources found.")

    # verify resource counts
    if resourceCount != expectedResourceCount:
        print (f"Wrong number of resources found. Expected: {expectedResourceCount} Found: {resourceCount}")
        sys.exit(1) 

    # verify count of each of the resource types 
    resourceType = {}
    for resource in resources:
        typ = resource["type"]
        resourceType.setdefault(typ, 0)
        resourceType[typ] += 1
    
    for rt in resourceType:
        if resourceType[rt] != expectedResources[rt]:
            print(f"Account missing resources. User: {usr} Resource Type: {rt} Expecting: {expectedResources[rt]} Found: {resourceType[rt]}")
            sys.exit(1) 

    print("Resource list correct.")

    # Logout
    cmd = "az logout"
    run_az_command(cmd,False)    
