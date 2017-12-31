

from controller.actor.actor import Actor


class shortcuts:
    def enemies(self):
        return [a for a in Actor.find(active=True) if a is not self]


class Terminal(Actor):
    FORBIDDEN = ('exit()',)
    print("Following commands are available:")
    print("end         # ends the turn")
    print("quit        # quit game")
    print("distribute  # distributes available units to owned tiles")

    def do_turn(self, turn):
        super().do_turn(turn)
        print('New turn', turn)
        run = True
        while run:
            inp = input('>>> ')
            if inp == 'end':
                run = False
            elif inp == 'quit':
                run = False
                self.quit()
            elif inp == 'distribute':
                self.distribute_units()
            elif inp in self.FORBIDDEN:
                raise PermissionError(f"Command '{inp}' is not allowed")
            else:
                exec(inp)


Actor.TYPES['terminal'] = Terminal
