from pantheradesktop import pantheraClass
import pantheradesktop.tools as tools
import sys

class pantheraInteractiveConsole(pantheraClass):
    thread = None
    worker = None

    ## put here your console shortcuts
    recognizedChars = {
        'q': 'pa_exit'
    }

    def main(self):
        """
        Main function that registers base shortcuts and starts a thread
        :return:
        """

        self.recognizedChars['q'] = self.app.pa_exit
        self.thread, self.worker = tools.createThread(self.interactiveConsole)


    def interactiveConsole(self, thread=''):
        """
        Interactive console loop thread
        :param thread:
        :return:
        """

        while True:
            char = sys.stdin.read(1)

            if char and char in self.recognizedChars:
                self.recognizedChars[char]()
