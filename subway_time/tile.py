class Tile:
    def __init__(self, x, y, p):
        self.x = x
        self.y = y
        self.p = p  # Corresponding predictList[] object

    def __repr__(self):
        return "<Tile: x=%s y=%s>" % (self.x, self.y)

    def draw(self):
        x = self.x
        label = self.p.data[1] + ' '  # Route number or code
        draw.text((x, self.y + fontYoffset), label, font=font,
                  fill=routeColor)
        x += font.getsize(label)[0]
        label = self.p.data[3]  # Route direction/desc
        draw.text((x, self.y + fontYoffset), label, font=font,
                  fill=descColor)
        x = self.x
        if self.p.predictions == []:  # No predictions to display
            draw.text((x, self.y + fontYoffset + 8),
                      'No Predictions', font=font, fill=noTimesColor)
        else:
            isFirstShown = True
            count = 0
            for p in self.p.predictions:
                t = p - (currentTime - self.p.lastQueryTime)
                m = int(t / 60)
                if m <= minTime:
                    continue
                elif m <= shortTime:
                    fill = shortTimeColor
                elif m <= midTime:
                    fill = midTimeColor
                else:
                    fill = longTimeColor
                if isFirstShown:
                    isFirstShown = False
                else:
                    label = ', '
                    # The comma between times needs to
                    # be drawn in a goofball position
                    # so it's not cropped off bottom.
                    draw.text((x + 1,
                               self.y + fontYoffset + 8 - 2),
                              label, font=font, fill=minsColor)
                    x += font.getsize(label)[0]
                label = str(m)
                draw.text((x, self.y + fontYoffset + 8),
                          label, font=font, fill=fill)
                x += font.getsize(label)[0]
                count += 1
                if count >= maxPredictions:
                    break
            if count > 0:
                draw.text((x, self.y + fontYoffset + 8),
                          ' minutes', font=font, fill=minsColor)
