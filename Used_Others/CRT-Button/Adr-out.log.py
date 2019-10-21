# $language = "Python"
     
# $interface = "1.0"
     
import signal



def main():
	crt.Screen.Send('\x03')
	crt.Sleep(200) 


	crt.Screen.Send('cd' + '\r')
	crt.Screen.Send('cd service/jelly_adr_9091/logs' + '\r') 
	
	id = crt.Dialog.Prompt("输入要查的ID")
	crt.Screen.Send('tail -f out.log |grep ' + id + '\r')    
     
main()