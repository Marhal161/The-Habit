import random
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from datetime import datetime
from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.utils import platform
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList
from kivymd.uix.list import IconRightWidget
from kivymd.uix.card import MDCard
from kivymd.uix.fitimage import FitImage

if platform == "android":
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

from database import Database

# Initialize db instance
db = Database()

class DialogContent(MDBoxLayout):
    """OPENS A DIALOG BOX THAT GETS THE TASK FROM THE USER"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.date_text.text = str(datetime.now().strftime('%A %d %B %Y'))

    def show_date_picker(self):
        """Opens the date picker"""
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        """This function gets the date from the date picker and converts it to a
        more friendly form then changes the date label on the dialog to that"""
        date = value.strftime('%A %d %B %Y')
        self.ids.date_text.text = str(date)

class MenuDialogContent(MDBoxLayout):
    def __init__(self, tasks, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.orientation = "vertical"
        self.spacing = "10dp"
        self.size_hint_y = None
        self.height = "400dp"

        print("Tasks received in MenuDialogContent:", tasks)  # Debugging line

        self.scroll_view = MDScrollView(size_hint=(1, None), size=(self.width, self.height))
        self.list_view = MDList()
        self.scroll_view.add_widget(self.list_view)
        self.add_widget(self.scroll_view)

        self.update_tasks(tasks)

    def update_tasks(self, tasks):
        self.list_view.clear_widgets()
        for task in tasks:
            task_item = TwoLineAvatarIconListItem(
                text=task[1],
                secondary_text=task[2],
                on_release=lambda x, task=task: self.select_task(task)
            )
            task_item.add_widget(IconRightWidget(
                icon="trash-can-outline",
                on_release=lambda x, task_id=task[0]: self.delete_task(task_id)
            ))
            self.list_view.add_widget(task_item)

    def select_task(self, task):
        self.app.select_task(task)
        self.app.close_menu_dialog()

    def delete_task(self, task_id):
        db.delete_task(task_id)
        self.app.update_menu_dialog()  # Update the menu dialog

class ListItemWithCheckbox(TwoLineAvatarIconListItem):
    '''Custom list item'''
    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        # state a pk which we shall use link the list items with the database primary keys
        self.pk = pk

    def mark(self, check, the_list_item):
        '''mark the task as complete or incomplete'''
        if check.active == True:
            the_list_item.text = '[s]'+the_list_item.text+'[/s]'
            db.mark_task_as_complete(the_list_item.pk)# here
        else:
            the_list_item.text = str(db.mark_task_as_incomplete(the_list_item.pk))# Here

    def delete_item(self, the_list_item):
        '''Delete the task'''
        self.parent.remove_widget(the_list_item)
        db.delete_task(the_list_item.pk)# Here

class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    '''Custom left container'''

class MainApp(MDApp):
    task_list_dialog = None
    menu_dialog = None
    selected_task = None
    tracked_count = 0
    images = ["image.png", "image2.png", "image3.png", "image4.png", "image5.png"]  # Add your image paths here

    def build(self):
        # Setting theme to my favorite theme
        self.theme_cls.primary_palette = "DeepPurple"
        return self.root

    def show_task_dialog(self):
        if not self.task_list_dialog:
            self.task_list_dialog = MDDialog(
                title="Create habit",
                type="custom",
                content_cls=DialogContent(),
            )

        self.task_list_dialog.open()

    def show_menu(self):
        try:
            completed_tasks, uncomplete_tasks = db.get_tasks()
            all_tasks = completed_tasks + uncomplete_tasks

            print("Tasks retrieved from database:", all_tasks)  # Debugging line

            if not self.menu_dialog:
                self.menu_dialog = MDDialog(
                    title="My Habits",
                    type="custom",
                    content_cls=MenuDialogContent(tasks=all_tasks, app=self),
                    buttons=[
                        MDFlatButton(
                            text="CLOSE",
                            on_release=self.close_menu_dialog
                        ),
                    ]
                )
            else:
                self.menu_dialog.content_cls.update_tasks(all_tasks)
            self.menu_dialog.open()
        except Exception as e:
            print(e)
            pass

    def update_menu_dialog(self):
        if self.menu_dialog:
            completed_tasks, uncomplete_tasks = db.get_tasks()
            all_tasks = completed_tasks + uncomplete_tasks
            self.menu_dialog.content_cls.update_tasks(all_tasks)

    def close_menu_dialog(self, *args):
        if self.menu_dialog:
            self.menu_dialog.dismiss()

    def on_start(self):
        """Do not load tasks on the main screen"""
        pass

    def close_dialog(self, *args):
        self.task_list_dialog.dismiss()

    def add_task(self, task, task_date):
        '''Add task to the list of tasks'''
        # Add task to the db
        created_task = db.create_task(task.text, task_date)# Here
        task.text = ''
        self.close_dialog()
        self.update_menu_dialog()  # Update the menu dialog to show the new task

    def select_task(self, task):
        self.selected_task = task
        self.root.ids.selected_task_label.text = f"[b]{task[1]}[/b]\n{task[2]}"
        random_image = random.choice(self.images)  # Select a random image
        self.root.ids.selected_task_image.source = random_image  # Update the image source
        self.root.ids.track_button.disabled = False
        self.root.ids.track_button.opacity = 1  # Make the button visible
        self.root.ids.tracked_count_label.opacity = 1  # Make the label visible
        self.tracked_count = db.get_tracked_count(task[0])
        self.root.ids.tracked_count_label.text = f"Tracked: {self.tracked_count}"

    def track_task(self):
        if self.selected_task:
            db.track_task(self.selected_task[0])
            self.tracked_count = db.get_tracked_count(self.selected_task[0])
            self.root.ids.tracked_count_label.text = f"Tracked: {self.tracked_count}"

if __name__ == '__main__':
    app = MainApp()
    app.run()