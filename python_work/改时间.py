# $language = "Python"
     
# $interface = "1.0"
     
import signal



def timeAuthority():

	crt.Screen.Send('su' + '\r')
	crt.Sleep(400) 
	crt.Screen.Send('Microfun.001' + '\r')   
	crt.Screen.Send('date' + '\r')    


     
timeAuthority()