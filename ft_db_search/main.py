import flet
from flet import *
import asyncio
from getdata import request_data

class DropdownMenu(UserControl):
    def __init__(self):
        self.controls_list = {}
        super().__init__()

    def check_instance(self, e, height):
        obj = self.controls_list["data"]
        if height == 0:
            self.controls_list["search"].content.controls[2].value = f"{height} results found"
            self.controls_list["search"].content.update()
            self.leave(e)
        else:
            obj.height = 70 + (height * 20)
            obj.update()

    def leave(self, e):
        obj = self.controls_list["data"]
        obj.height = 50
        obj.update()

    async def filter_data_table(self, e):

        # Call to action when particular selction is made.
        def text_b_clicked(e):
            print(e.control.text)
            # Read the corresponding row of the selected design
            # We will use this data to display below.
            design_inventory = recorded_data[recorded_data["Design-No"] == e.control.text]
            print(design_inventory)
            # Collapse result window once required option is selected.
            self.leave(e)
            # Display text if clicked
            # Access the data container in your GUI and add the new Column
            self.controls_list["display"].content.controls[0].text = design_inventory.to_string(index=False)
            self.controls_list["display"].content.update()
            
        # Get data from CSV. It is a dataframe.
        recorded_data = request_data()
        
        # Access column 0: "All Designs" in our case. Column 0 is a dataframe,
        # It has to be converted to a list for our convenience.
        records = recorded_data["Design-No"]
        # print(records.tolist())

        name_list = Column(
            scroll="auto",
            spacing=20,
            expand=True,
            alignment=MainAxisAlignment.END,
        )
        obj = self.controls_list["data"]
        obj.content = Container(
            padding=padding.only(top=60, left=15, right=15, bottom=10),
            content=name_list,
        )

        if e.data.lower() == "":
            obj.content = None
            self.controls_list["search"].content.controls[2].value = f"0 results found"
            self.controls_list["search"].content.update()
            self.leave(e)
            # self.leave(e)
        else:
            count = 0
            for name in records.tolist():
                if e.data.lower() in name.lower():
                    name_list.controls.append(
                        Row(
                            visible=True,
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                TextButton(text=name, on_click=text_b_clicked)
                            ],
                        )
                    )
                    count += 1
                self.controls_list["search"].content.controls[2].value = f"{count} results found"
                self.controls_list["search"].content.update()
                self.check_instance(e, count)

    def drop_down_search(self):
        _object_ = Container(
            width=450,
            height=50,
            bgcolor="white10",
            border_radius=6,
            padding=8,
            content=Row(
                spacing=10,
                vertical_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Icon(
                        name=icons.SEARCH_ROUNDED,
                        size=17,
                        opacity=0.85,
                    ),
                    TextField(
                        border_color="transparent",
                        height=20,
                        text_size=14,
                        content_padding=0,
                        cursor_color="white",
                        cursor_width=1,
                        color="white",
                        hint_text="Search",
                        on_change=lambda e: asyncio.run(self.filter_data_table(e)),
                    ),
                    Text(size=9, italic=True, color="white54"),
                ],
            ),
        )
        self.controls_list["search"] = _object_
        return _object_

    def drop_down_data_box(self):
        _object_ = Container(
            width=450,
            height=50,
            bgcolor="white10",
            border_radius=6,
            alignment=alignment.bottom_center,
            animate=animation.Animation(300, "decelerate"),
            clip_behavior=ClipBehavior.HARD_EDGE,
        )
        self.controls_list["data"] = _object_
        return _object_
    
    def inventory_display(self):
        # Returns the inventory display UI element
        # It will be updated during call to action functions later.
        _object_ = Container(
            bgcolor="blue10",
            border_radius=6,
            alignment=alignment.bottom_center,
            content=[
                Text(size=10, color="green10"),
            ],
        )
        self.controls_list["display"] = _object_
        return _object_
    

    def build(self):
        return Column(
                    width=450,
                    height=500,
                    expand=True,
                    controls=[
                        self.drop_down_data_box(), 
                        self.drop_down_search(),
                        self.inventory_display(),
                     ],
                )


def main(page: Page):
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.add(
        DropdownMenu(),
    )
    page.update()


if __name__ == "__main__":
    flet.app(target=main)
