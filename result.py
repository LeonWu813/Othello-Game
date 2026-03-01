class Result:
    """Result of a Othello game"""

    def __init__(self, black_point, white_point):
        self.black_point = black_point
        self.white_point = white_point
        if black_point > white_point:
            self.result = "BLACK WIN"
            self.scores = str(black_point) + " : " + str(white_point)
        elif black_point < white_point:
            self.result = "WHITE WIN"
            self.scores = str(white_point) + " : " + str(black_point)
        else:
            self.result = "TIE"
            self.scores = str(black_point) + " : " + str(white_point)

    def write_result_to_txt(self, name):
        scores = {}
        try:
            with open("scores.txt", "r") as file:
                for line in file:
                    parts = line.split(" ")
                    scores[parts[0]] = parts
        except OSError:
            print("Unable to open scores.txt")

        if name in scores:
            scores[name][1] = str(int(scores[name][1]) + 1)
        else:
            scores[name] = [name, "1", "\n"]

        with open("scores.txt", "w") as file:
            for result in scores.values():
                file.write(" ".join(result))

        file.close()
