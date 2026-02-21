class RobotEmil:
    def __init__(self, meno_suboru):
        self._robot = None
        self.post = []
        riadky = []
        mrow = []
        mcol = []
        self.objekty = {}
        self.prekazky = {}
        self.navstivene = set()
        with open(meno_suboru, "r", encoding="utf-8") as s:
            for r in s.readlines():
                riadky.append(list(r.split()))
        for i in range(len(riadky)):
            mrow.append(int(riadky[i][1]))
            mcol.append((int(riadky[i][2])))
        self.pole = [["." for _ in range(max(mcol) + 1)] for _ in range(max(mrow) + 1)]
        for i in riadky:
            ch, r, s = i
            if ch == "#":
                self.prekazky[(int(r), int(s))] = ch
            else:
                self.objekty[(int(r), int(s))] = ch
        print("prekazky: ", self.prekazky, "objekty: ", self.objekty)

    def daj_robot(self):
        if self._robot is not None:
            return self._robot
        return None

    def zmen_robot(self, pozicia):
        def inside(r, s):
            return 0 <= r < len(self.pole) and 0 <= s < len(self.pole[0])

        r, s = pozicia
        if inside(r, s) or (r, s) in self.objekty or (r, s) not in self.prekazky:
            self._robot = (r, s)
            self.navstivene.add((r, s))
            if (r, s) in self.objekty:
                self.post.append(self.objekty[(r, s)])
                # del self.objekty[(r, s)]

    robot = property(daj_robot, zmen_robot)

    def __repr__(self):
        pole = [row[:] for row in self.pole]
        for (r, s), ch in self.prekazky.items():
            pole[r][s] = ch
        for (r, s), ch in self.objekty.items():
            pole[r][s] = ch
        for (r, s) in self.navstivene:
            pole[r][s] = "+"

        if self._robot is not None:
            r, s = self._robot
            pole[r][s] = "@"
        return "\n".join("".join(row) for row in pole)

    def rob(self, prikazy):
        def inside(r, s):
            return 0 <= r < len(self.pole) and 0 <= s < len(self.pole[0])

        zozberane = set()
        vyk = 0
        dir = {"v": (0, 1), "j": (1, 0), "z": (0, -1), "s": (-1, 0)}

        for i in prikazy:  # z
            if i in dir:
                dr, dc = dir[i]
                if self._robot is not None:
                    r, s = self._robot
                    nr, ns = r + dr, s + dc
                    # print("nr,ns",nr,ns)

                    while inside(nr, ns) and (nr, ns) not in self.prekazky:
                        self.navstivene.add((nr, ns))
                        self.zmen_robot((nr, ns))
                        if (nr, ns) in self.objekty:
                            print("zozberane", zozberane)

                            # self.post.append(self.objekty[(nr,ns)])
                            zozberane.add(self.objekty[(nr, ns)])
                            print("zozberane", zozberane)
                            del self.objekty[(nr, ns)]
                        vyk += 1
                        nr, ns = nr + dr, ns + dc

        return (vyk, zozberane)

    @property
    def postupne(self):
        return self.post