import scratchconnect, time
from more_itertools import sliced

user = scratchconnect.ScratchConnect("firedestroyer1", "mypasswordnoyoudontgettoknow")

print("Connecting to project...")
project = user.connect_project(project_id=805918987)
variables = project.connect_cloud_variables()

print("connected")

while True:
    try:
        queued = variables.get_cloud_variable_value(variable_name="queued", limit=1)[0]

        if queued[0] == "2":
            time.sleep(0.1)

            toSend = variables.encode("This is a fallback text in case the file does not load.")

            with open('message.txt','r') as file:
                toSend=file.readline()


            toSend = list(sliced(toSend,250))
            
            print(f"Setting data")
            for packet in toSend:
                print("Attempting to set var data to "+str(packet))
                
                time.sleep(0.2)
                variables.set_cloud_variable(variable_name="data", value=packet)  # Set a Cloud Variable
                time.sleep(0.2)
                variables.set_cloud_variable(variable_name="queued", value='1')

                while True:
                    recieved = variables.get_cloud_variable_value(variable_name="queued", limit=1)[0]
                    print(recieved)
                    time.sleep(0.25)
                    if recieved == '3':
                        break

                time.sleep(0.2)
                variables.set_cloud_variable(variable_name="queued", value=0)
                
    except IndexError:
        pass
    time.sleep(0.25)
