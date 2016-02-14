#!/usr/bin/python
from gi.repository import Gtk, Gdk, Notify
import sys
import urllib2


class HastebinUploader:
    def __init__ (self, args):

        files = []

        # Initialize the notification daemon
        Notify.init ("Hastebin")

        # Parse arguments
        if len (args) == 1:
            return
        else:
            for file in args:
                if file == args[0] or file == "":
                    continue
                files.append (file)

        self.paste_them_bad_boys (files)

    def notify (self, message_one, message_two, icon):
        try:
            notification = Notify.Notification.new (message_one, message_two, icon)
            notification.set_urgency (1)
            notification.show ()
            del notification
        except:
            pass

    def paste_them_bad_boys (self, files):
        urls = []
        URL  = "http://hastebin.com"

        for file in files:
            filecontents = open (file, 'r')
            try:
                data = "".join (filecontents.readlines ()).strip ()
            finally:
                filecontents.close ()

            # Upload
            request   = urllib2.Request (URL + "/documents", data)
            response  = urllib2.urlopen (request)
            read_data = response.read ()
            read_eval = eval (read_data)

            fileurl = "{}/{}".format (URL, read_eval['key'])
            urls.append (fileurl)

        # Copy to clipboard
        url_list = ", ".join (urls)
        print url_list
        self.set_clipboard (url_list)
        if len (urls) > 1:
            self.notify (
                "Your files have been pasted.", 
                "The links have been copied to your clipboard!", 
                "help-info"
            )
        else:
            self.notify (
                "Your file has been pasted.", 
                "The link has been copied to your clipboard!", 
                "help-info"
            )

    def set_clipboard (self, url_list):
        display   = Gdk.Display.get_default()
        selection = Gdk.Atom.intern ("CLIPBOARD", False)
        clipboard = Gtk.Clipboard.get_for_display (display, selection)
        clipboard.set_text (url_list, -1)
        clipboard.store ()

if __name__ == '__main__':
    uploader = HastebinUploader (sys.argv)
