
routes = ["/muse/eeg", "/muse/eeg/quantization","/muse/elements/alpha_relative",
          "/muse/elements/beta_relative","/muse/elements/delta_relative",
          "/muse/elements/gamma_relative","/muse/elements/theta_relative",
          "/muse/elements/horseshoe","/muse/elements/is_good","/muse/elements/raw_fft0",
          "/muse/elements/raw_fft1","/muse/elements/raw_fft2","/muse/elements/raw_fft3",
          "/muse/elements/low_freqs_absolute","/muse/elements/alpha_absolute",
          "/muse/elements/beta_absolute","/muse/elements/delta_absolute",
          "/muse/elements/gamma_absolute","/muse/elements/theta_absolute",
          "/muse/elements/alpha_session_score","/muse/elements/beta_session_score",
          "/muse/elements/delta_session_score","/muse/elements/gamma_session_score",
          "/muse/elements/theta_session_score","/muse/acc","/muse/drlref",
          "/muse/batt","/muse/elements/blink","/muse/elements/jaw_clench","/muse/elements/touching_forehead"]

class printModule:

    def __init__(self):
        pass

    def mapAllForPrint(self,dispatcher,function=print):
        dispatcher.mapSameFunctionToPaths(function, routes)

    def configure(self, dispatcher):
        self.mapAllForPrint(dispatcher)


class printModuleTest:

    def __init__(self):
        pass

    def printLOL(self,unused_addr,*args):
        for x in range(1, len(args)):
            print(args[x])

    def mapAllForPrint(self,dispatcher,function=printLOL):
        dispatcher.mapSameFunctionToPaths(function,routes)

    def configure(self, dispatcher):
        self.mapAllForPrint(dispatcher)

    #TODO: Fer funcio que canvii 0 a 1 i k es guardi al fitxer de sessio com a event