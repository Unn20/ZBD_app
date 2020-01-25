from tkintertable import TableCanvas, Formula
from tkinter import *


class CustomTable(TableCanvas):
    def __init(self, parent=None, model=None):
        TableCanvas.__init__(read_only=False,
                             cellwidth=60, cellbackgr='#e3f698',
                             thefont=('Arial', 12), rowheight=20, rowheaderwidth=30,
                             rowselectedcolor='yellow', editable=True)
        return

    def handle_left_click(self, event):
        """Respond to a single press"""
        # which row and column is the click inside?
        self.clearSelected()
        self.allrows = False
        rowclicked = self.get_row_clicked(event)
        colclicked = self.get_col_clicked(event)
        self.focus_set()
        if self.mode == 'formula':
            self.handleFormulaClick(rowclicked, colclicked)
            return
        if hasattr(self, 'cellentry'):
            self.cellentry.destroy()
        # ensure popup menus are removed if present
        if hasattr(self, 'rightmenu'):
            self.rightmenu.destroy()
        if hasattr(self.tablecolheader, 'rightmenu'):
            self.tablecolheader.rightmenu.destroy()

        self.startrow = rowclicked
        self.endrow = rowclicked
        self.startcol = colclicked
        self.endcol = colclicked
        # reset multiple selection list
        self.multiplerowlist = []
        self.multiplerowlist.append(rowclicked)
        if rowclicked is None or colclicked is None:
            return
        if self.read_only is True:
            return
        if 0 <= rowclicked < self.rows and 0 <= colclicked < self.cols:
            self.setSelectedRow(rowclicked)
            self.setSelectedCol(colclicked)
            self.drawSelectedRect(self.currentrow, self.currentcol)
            self.drawSelectedRow()
            self.tablerowheader.drawSelectedRows(rowclicked)
            coltype = self.model.getColumnType(colclicked)
            if coltype == 'text' or coltype == 'number':
                self.drawCellEntry(rowclicked, colclicked)
        return

    def handle_right_click(self, event):
        if self.read_only == True:
            return
        self.delete('tooltip')
        self.tablerowheader.clearSelected()
        if hasattr(self, 'rightmenu'):
            self.rightmenu.destroy()
        rowclicked = self.get_row_clicked(event)
        colclicked = self.get_col_clicked(event)
        if colclicked == None:
            self.rightmenu = self.popupMenu(event, outside=1)
            return

        if (rowclicked in self.multiplerowlist or self.allrows == True) and colclicked in self.multiplecollist:
            self.rightmenu = self.popupMenu(event, rows=self.multiplerowlist, cols=self.multiplecollist)
        else:
            if 0 <= rowclicked < self.rows and 0 <= colclicked < self.cols:
                self.clearSelected()
                self.allrows = False
                self.setSelectedRow(rowclicked)
                self.setSelectedCol(colclicked)
                self.drawSelectedRect(self.currentrow, self.currentcol)
                self.drawSelectedRow()
            if self.isInsideTable(event.x, event.y) == 1:
                self.rightmenu = self.popupMenu(event, rows=self.multiplerowlist, cols=self.multiplecollist)
            else:
                self.rightmenu = self.popupMenu(event, outside=1)
        return

    def drawCellEntry(self, row, col, text=None):
        """When the user single/double clicks on a text/number cell, bring up entry window"""

        if self.read_only == True:
            return
        # absrow = self.get_AbsoluteRow(row)
        h = self.rowheight
        model = self.getModel()
        cellvalue = self.model.getCellRecord(row, col)
        if Formula.isFormula(cellvalue):
            return
        else:
            text = self.model.getValueAt(row, col)
        x1, y1, x2, y2 = self.getCellCoords(row, col)
        w = x2 - x1
        # Draw an entry window
        txtvar = StringVar()
        txtvar.set(text)

        def callback(e):
            value = txtvar.get()
            if value == '=':
                # do a dialog that gets the formula into a text area
                # then they can click on the cells they want
                # when done the user presses ok and its entered into the cell
                self.cellentry.destroy()
                # its all done here..
                self.formula_Dialog(row, col)
                return

            coltype = self.model.getColumnType(col)
            if coltype == 'number':
                sta = self.checkDataEntry(e)
                if sta == 1:
                    model.setValueAt(value, row, col)
            elif coltype == 'text':
                model.setValueAt(value, row, col)

            color = self.model.getColorAt(row, col, 'fg')
            self.drawText(row, col, value, color, align=self.align)
            if e.keysym == 'Return':
                self.delete('entry')
                # self.drawRect(row, col)
                # self.gotonextCell(e)
            return

        self.cellentry = Entry(self.parentframe, width=20,
                               textvariable=txtvar,
                               # bg=self.entrybackgr,
                               # relief=FLAT,
                               takefocus=1,
                               font=self.thefont)
        self.cellentry.icursor(END)
        self.cellentry.bind('<Return>', callback)
        self.cellentry.bind('<KeyRelease>', callback)
        self.cellentry.focus_set()
        self.entrywin = self.create_window(x1 + self.inset, y1 + self.inset,
                                           width=w - self.inset * 2, height=h - self.inset * 2,
                                           window=self.cellentry, anchor='nw',
                                           tag='entry')
        return
