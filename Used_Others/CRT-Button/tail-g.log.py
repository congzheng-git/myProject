# $language = "Python"
     
# $interface = "1.0"
     
import signal



def main():
	crt.Screen.Send('\x03')
	crt.Sleep(200) 


	crt.Screen.Send('cd  ../data/jelly_log/web/' + '\r')
	
	id = crt.Dialog.Prompt("输入要查的ID")
	crt.Screen.Send('tail -f g.log |grep ' + id + '\r')    
     
main()