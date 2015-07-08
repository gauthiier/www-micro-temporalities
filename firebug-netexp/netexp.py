from selenium import webdriver
import sys, json, urllib2, time, os

firefox_ext = "/firefox_ext/"
firebug_ext = "firebug-1.12.8.xpi"
firestarter_ext = "fireStarter-0.1a6.xpi"
netexport_ext = "netExport-0.9b7.xpi"

def config():

	global firefox_ext;
	config = webdriver.firefox.firefox_profile.FirefoxProfile();

	firefox_ext = os.getcwd() + firefox_ext;
	config.add_extension(firefox_ext + firebug_ext);
	config.add_extension(firefox_ext + firestarter_ext);	
	config.add_extension(firefox_ext + netexport_ext);

	config.set_preference("app.update.enabled", False);
	config.native_events_enabled = True
	#config.set_preference("webdriver.log.file", "log_webdriver.txt");

	ext_firebug = "extensions.firebug.";

	config.set_preference(ext_firebug + "currentVersion", "1.12.8");
	config.set_preference(ext_firebug + "allPagesActivation", "on");
	config.set_preference(ext_firebug + "defaultPanelName", "net");
	config.set_preference(ext_firebug + "net.enableSites", True);
	config.set_preference(ext_firebug + "addonBarOpened", True);
	config.set_preference(ext_firebug + "consoles.enableSite", True);
	config.set_preference(ext_firebug + "console.enableSites", True);
	config.set_preference(ext_firebug + "script.enableSites", True);
	config.set_preference(ext_firebug + "net.enableSites", True);
	config.set_preference(ext_firebug + "onByDefault", True);
	config.set_preference(ext_firebug + "DBG_STARTER", True);

	config.set_preference(ext_firebug + "netexport.alwaysEnableAutoExport", True);
	config.set_preference(ext_firebug + "netexport.autoExportToFile", True);
	config.set_preference(ext_firebug + "netexport.saveFiles", True);
	config.set_preference(ext_firebug + "netexport.showPreview", False);
	config.set_preference(ext_firebug + "netexport.defaultLogDir", os.getcwd());
	config.set_preference(ext_firebug + "netexport.pageLoadedTimeout", 20000);
	config.set_preference(ext_firebug + "netexport.timeout", 25000);

	return config;


if __name__ == '__main__':

	conf = config();
	driver = webdriver.Firefox(conf);

	time.sleep(7);

	driver.get("http://www.nytimes.com");

	time.sleep(20);

	driver.close();


