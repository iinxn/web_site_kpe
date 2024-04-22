from flet import Container, AlertDialog, Text, TextButton

class Components(Container):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.alter_dialog_block = AlertDialog(
            modal=True,
            actions=[TextButton("OK", on_click=self.close_dlg_block)],
            on_dismiss=lambda e: print("Modal dialog dismissed!")
        )

    def show_block_dialog(self, content_text, title_text):
        self.alter_dialog_block.content = Text(content_text)
        self.alter_dialog_block.title = Text(title_text)
        self.alter_dialog_block.open = True
        self.page.dialog = self.alter_dialog_block
        self.page.update()

    def close_dlg_block(self, e):
        self.alter_dialog_block.open = False
        print("Вы закрыли модульное окно блокировки")
        self.page.update()
