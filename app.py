from controller import Controller
from model import Model
from view import View

class App:
    def __init__(self):
        self.model = Model()
        self.view = View(title='App')
        self.controller = Controller(model=self.model, view=self.view)
        self.view.set_controller(controller=self.controller)
        self.controller.init_defaults()

    def run(self):
        self.view.root.mainloop()

if __name__ == '__main__':
    app = App()
    app.run()