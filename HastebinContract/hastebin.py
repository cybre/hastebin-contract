#!/usr/bin/python
import sys
from gi.repository import Gtk, Gdk, Notify
import urllib2

appName = "Hastebin"

msgOneFile = "Your file has been pasted."
msgMultipleFiles = "Your files have been pasted."
msgClipboard = "The link has been copied to your clipboard!"
msgClipboardMultiple = "The links have been copied to your clipboard!"
msgFailed = "Operation failed, try again later."

# Notification icons
iconInfo = "help-info"
iconError = "error"


class HastebinUploader:
    def __init__(self, args):

        files = []

        # Initialize the notification daemon
        Notify.init(appName)
        self.notification = Notify.Notification.new("", "", "")

        # Parse arguments
        if len(args) == 1:
            return
        else:
            for file in args:
                if file == args[0] or file == "":
                    continue
                files.append(file)

        self.paste(files)

    def notify(self, messageOne, messageTwo, icon, timeout=5000):
        try:
            self.notification.update(messageOne, messageTwo, icon)
            self.notification.set_timeout(timeout)
            self.notification.show()
        except:
            pass

    def paste(self, files):
        urls = []
        URL = "http://hastebin.com"

        for file in files:
            filecontents = open(file, 'r')
            try:
                data = "".join(filecontents.readlines()).strip()
            finally:
                filecontents.close()

            # Upload
            request = urllib2.Request(URL + "/documents", data)
            response = urllib2.urlopen(request)
            rdata = response.read()
            reval = eval(rdata)

            fileurl = "%s/%s" % (URL, reval['key'])
            urls.append(fileurl)

        # Copy to clipboard
        urllist = ", ".join(urls)
        print urllist
        self.setClipboard(urllist)
        if len(urls) > 1:
            self.notify(msgMultipleFiles, msgClipboardMultiple, iconInfo, 3000)
        else:
            self.notify(msgOneFile, msgClipboard, iconInfo, 3000)

    def setClipboard(self, urllist):
        display = Gdk.Display.get_default()
        selection = Gdk.Atom.intern("CLIPBOARD", False)
        clipboard = Gtk.Clipboard.get_for_display(display, selection)
        clipboard.set_text(urllist, -1)
        clipboard.store()

if __name__ == '__main__':
    uploader = HastebinUploader(sys.argv)
