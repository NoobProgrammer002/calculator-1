from PyQt5 import QtWidgets
import MainWindow

import operator

READY = 1
INPUT = 0


class MyWindow(QtWidgets.QMainWindow, MainWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(self)

        for n in range(0, 10):
            getattr(self, "btn{}".format(n)).pressed.connect(
                lambda v=n: self.input_number(v)
            )

        self.btn_ac.pressed.connect(self.reset)
        self.btn_mr.pressed.connect(self.recall_number)
        self.btn_m.pressed.connect(self.memory_number)

        self.btn_pro.pressed.connect(self.percent)

        self.btn_equal.pressed.connect(self.equal)

        self.btn_div.pressed.connect(lambda: self.operation(operator.truediv, "/"))
        self.btn_sub.pressed.connect(lambda: self.operation(operator.sub, "-"))
        self.btn_mult.pressed.connect(lambda: self.operation(operator.mul, "*"))
        self.btn_sum.pressed.connect(lambda: self.operation(operator.add, "+"))

        self.memory = 0
        self.memory_status = ""
        self.show_memory()
        self.reset()

    def input_number(self, v):
        if self.state == READY:
            self.state = INPUT
            self.stak[-1] = v
            self.show_number()
        else:
            try:
                self.stak[-1] = self.stak[-1] * 10 + v
                self.show_number()
            except Exception:
                self.lcdNumber.display("Err")
                self.stak = [0]

    def memory_number(self):
        self.memory = self.lcdNumber.value()
        self.memory_status = "M"
        self.show_memory()

    def recall_number(self):
        self.state = INPUT
        self.stak[-1] = self.memory
        self.show_number()

    def reset(self):
        self.state = READY
        self.stak = [0]
        self.operant = None
        self.show_number()
        self.sign = ""
        self.show_operand()

    def percent(self):
        self.stak[-1] = self.stak[-1] / 100
        self.show_number()

    def operation(self, operant, sign):
        if not (self.operant and self.state == READY):
            if self.operant:
                self.equal()

            self.stak.append(0)
            self.state = READY

        self.operant = operant
        self.sign = sign
        self.show_operand()

    def equal(self):
        if self.operant:
            try:
                self.stak = [self.operant(*self.stak)]
                self.show_number()
            except Exception:
                self.lcdNumber.display("Err")
                self.stak = [0]
                self.sign = ""
                self.operant = None
                self.show_operand()
                # self.state = READY
            else:
                self.sign = ""
                self.show_operand()
                self.operant = None
                self.state = READY

    def show_number(self):
        self.lcdNumber.display(self.stak[-1])

    def show_operand(self):
        self.label_operant.setText(self.sign)

    def show_memory(self):
        self.label_memory.setText(self.memory_status)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
