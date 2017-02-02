import math

import matplotlib.pyplot as plt

class AnnoteFinder(object):
    """callback for matplotlib to display an annotation when points are
    clicked on.  The point which is closest to the click and within
    xtol and ytol is identified.

    Register this function like this:

    scatter(xdata, ydata)
    af = AnnoteFinder(xdata, ydata, annotes)
    connect('button_press_event', af)
    """

    def __init__(self, xdata, ydata, annotes, ax=None, xtol=None, ytol=None):
        self.data = list(zip(xdata, ydata, annotes))
        if xtol is None:
            xtol = ((max(xdata) - min(xdata))/float(len(xdata)))
        if ytol is None:
            ytol = ((max(ydata) - min(ydata))/float(len(ydata)))
        self.xtol = xtol
        self.ytol = ytol
        if ax is None:
            self.ax = plt.gca()
        else:
            self.ax = ax
        self.drawnAnnotations = {}
        self.links = []

    def distance(self, x1, x2, y1, y2):
        """
        return the distance between two points
        """
        return(math.sqrt((x1 - x2)**2 + (y1 - y2)**2))

    def __call__(self, event):

        if event.inaxes:

            clickX = event.xdata
            clickY = event.ydata
            if (self.ax is None) or (self.ax is event.inaxes):
                annotes = []
                for x, y, a in self.data:
                    if ((clickX-self.xtol < x < clickX+self.xtol) and
                            (clickY-self.ytol < y < clickY+self.ytol)):
                        annotes.append(
                            (self.distance(x, clickX, y, clickY), x, y, a))
                if annotes:
                    breaklinecounter = 0
                    annotes.sort()
                    distance, x, y, _ = annotes[0]
                    annote = ""
                    for i in range(0, len(annotes)):
                        _, _, _, tmp = annotes[i]
                        tmp = tmp.split(",")
                        if(len(tmp) == 1):
                            a = tmp[0]
                            a = a.strip(" [']")
                            if(len(annote) == 0):
                                annote = a
                            else:
                                annote = annote + ", "+ a
                                breaklinecounter = breaklinecounter + 2
                            breaklinecounter = breaklinecounter + len(a)
                            if(breaklinecounter > 40):
                                annote = annote + "\n   "
                                breaklinecounter = 0
                        else:
                            for n in tmp:
                                a = n.strip(" [']")
                                if(len(annote) == 0):
                                    annote = a
                                else:
                                    annote = annote + ", "+ a
                                    breaklinecounter = breaklinecounter + 2
                                breaklinecounter = breaklinecounter + len(a)
                                if(breaklinecounter > 40):
                                    annote = annote + "\n "
                                    breaklinecounter = 0
                    self.drawAnnote(event.inaxes, x, y, annote)
                    for l in self.links:
                        l.drawSpecificAnnote(annote)

    def drawAnnote(self, ax, x, y, annote):
        """
        Draw the annotation on the plot
        """
        if (x, y) in self.drawnAnnotations:
            markers = self.drawnAnnotations[(x, y)]
            test = True
            for m in markers:
                m.set_visible(not m.get_visible())
                test = test and m.get_visible()
            if(test):
                print(annote)
            self.ax.figure.canvas.draw_idle()
        else:
            print(annote)
            t = ax.text(x, y, " - %s" % (annote),verticalalignment='top', bbox={'facecolor':"#FFD865", 'alpha':0.7, 'pad':5})
            m = ax.scatter([x], [y], marker='d', c='r', zorder=100)
            self.drawnAnnotations[(x, y)] = (t, m)
            self.ax.figure.canvas.draw_idle()

    def drawSpecificAnnote(self, annote):
        annotesToDraw = [(x, y, a) for x, y, a in self.data if a in annote]
        for x, y, a in annotesToDraw:
            self.drawAnnote(self.ax, x, y, a)
            
    def clearAnnote(self):
        for _, markers in self.drawnAnnotations.items():
            for m in markers:
                m.set_visible(False)
        self.drawnAnnotations = {}
