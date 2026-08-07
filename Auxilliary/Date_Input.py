from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import (
    QDialog,
    QLabel,
    QComboBox,
    QDateEdit,
    QDialogButtonBox,
    QGridLayout,
)


class DateRangeDialog(QDialog):

    @staticmethod
    def getDateRange(parent=None,
                     title="Select Date Range",
                     start=None,
                     end=None):

        dialog = DateRangeDialog(parent, start, end)
        dialog.setWindowTitle(title)

        accepted = dialog.exec_() == QDialog.Accepted

        return (
            dialog.startEdit.date(),
            dialog.endEdit.date(),
            accepted
        )

    def __init__(self, parent=None, start=None, end=None):
        super().__init__(parent)

        today = QDate.currentDate()

        if start is None:
            start = today.addDays(-7)

        if end is None or end > today:
            end = today

        # Ensure initial dates are valid
        if start >= end:
            start = end.addDays(-1)

        self.startEdit = QDateEdit(start)
        self.endEdit = QDateEdit(end)

        for edit in (self.startEdit, self.endEdit):
            edit.setCalendarPopup(True)
            edit.setDisplayFormat("yyyy-MM-dd")

        # No future dates
        self.startEdit.setMaximumDate(today)
        self.endEdit.setMaximumDate(today)

        # End date must be at least one day after start
        self.endEdit.setMinimumDate(start.addDays(1))

        # Start date must be at least one day before end
        self.startEdit.setMaximumDate(end.addDays(-1))

        self.startEdit.dateChanged.connect(self.validate)
        self.endEdit.dateChanged.connect(self.validate)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QGridLayout(self)

        layout.addWidget(QLabel("From"), 0, 0)
        layout.addWidget(self.startEdit, 0, 1)

        layout.addWidget(QLabel("To"), 1, 0)
        layout.addWidget(self.endEdit, 1, 1)

        layout.addWidget(buttons, 2, 0, 1, 2)


    def validate(self):
        start = self.startEdit.date()
        end = self.endEdit.date()
        today = QDate.currentDate()

        if start >= end:
            if self.sender() == self.startEdit:
                new_end = start.addDays(1)

                if new_end <= today:
                    self.endEdit.setDate(new_end)
                else:
                    self.startEdit.setDate(end.addDays(-1))

            else:
                self.startEdit.setDate(end.addDays(-1))

        # Update allowed ranges
        self.endEdit.setMinimumDate(
            self.startEdit.date().addDays(1)
        )

        self.endEdit.setMaximumDate(today)

        self.startEdit.setMaximumDate(
            self.endEdit.date().addDays(-1)
        )

class IntervalDialog(QDialog):

    @staticmethod
    def getInterval(parent=None,
                    title="Select Interval",
                    default="1m"):

        dialog = IntervalDialog(parent, default)
        dialog.setWindowTitle(title)

        accepted = dialog.exec_() == QDialog.Accepted

        return (
            dialog.intervalCombo.currentText(),
            accepted
        )

    def __init__(self, parent=None, default="1m"):
        super().__init__(parent)

        self.intervals = [
            "1m",
            "2m",
            "5m",
            "15m",
            "30m",
            "60m",
            "90m",
            "1h",
            "1d"
        ]

        self.intervalCombo = QComboBox()
        self.intervalCombo.addItems(self.intervals)

        if default in self.intervals:
            self.intervalCombo.setCurrentText(default)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QGridLayout(self)

        layout.addWidget(QLabel("Interval"), 0, 0)
        layout.addWidget(self.intervalCombo, 0, 1)

        layout.addWidget(buttons, 1, 0, 1, 2)
