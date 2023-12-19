import time
import mayaa
import random
import asyncio


async def swap(array, s, i):
    (array[s], array[i]) = (array[i], array[s])


async def selection_sort(array):
    size = len(array)
    for s in range(size):
        min_idx = s

        for i in range(s + 1, size):
            # For sorting in descending order
            # for minimum element in each loop
            if array[i] < array[min_idx]:
                min_idx = i
        # Arranging min at the correct position
        time.sleep(0.1)
        await swap(array, s, min_idx)


def mergeSort(array):
    if len(array) > 1:
        #  r is the point where the array is divided into two subarrays
        r = len(array) // 2
        L = array[:r]
        M = array[r:]
        # Sort the two halves
        mergeSort(L)
        mergeSort(M)

        i = j = k = 0

        # Until we reach either end of either L or M, pick larger among
        # elements L and M and place them in the correct position at A[p..r]
        while i < len(L) and j < len(M):
            if L[i] < M[j]:
                array[k] = L[i]
                i += 1
            else:
                array[k] = M[j]
                j += 1
            k += 1
            return

        # When we run out of elements in either L or M,
        # pick up the remaining elements and put in A[p..r]
        while i < len(L):
            array[k] = L[i]
            i += 1
            k += 1
            return

        while j < len(M):
            array[k] = M[j]
            j += 1
            k += 1
            return


def bubble_sort(array):
    for i in range(len(array)):
        for j in range(0, len(array) - i - 1):
            if array[j] > array[j + 1]:
                temp = array[j]
                array[j] = array[j + 1]
                array[j + 1] = temp
                return


def make_data(num, endpoints):
    arr = []
    for i in range(num):
        arr.append(random.randint(*endpoints))
    return arr


class Box:
    def __init__(self, screen: mayaa.screen.Screen, data) -> None:
        self.screen = screen
        self.data = data
        self.item_num = len(self.data)
        self.width = 600
        self.height = 400
        self.item_width = self.width // self.item_num
        self.surface = self.screen.surface
        self.dim = self.screen.surface.get_size()
        self.xpos = self.dim[0] * 0.5 - self.width * 0.5
        self.ypos = self.dim[1] * 0.5 - self.height * 0.5

    def render(self):
        mayaa.draw.rect(
            self.surface,
            [50, 50, 50],
            [
                self.xpos,
                self.ypos,
                self.width,
                self.height,
            ],
            0,
        )

        for index, item in enumerate(self.data):
            mayaa.draw.rect(
                self.surface,
                [150, 150, 150],
                [
                    self.xpos + self.item_width * index,
                    self.ypos + self.height - item,
                    self.item_width,
                    item,
                ],
                0,
            )

        mayaa.draw.rect(
            self.surface,
            "white",
            [
                self.xpos,
                self.ypos,
                self.width,
                self.height,
            ],
            1,
        )


class Text:
    def __init__(self, screen: mayaa.screen.Screen, text, position) -> None:
        self.screen = screen
        self.text = text
        self.position = position
        self.font = self.screen.font_manager.main_font
        self.rendered_text = self.font.render(f"{self.text}", "True", [0, 200, 0])

    def update_text(self, text):
        if text != self.text:
            self.text = text
            self.rendered_text = self.font.render(f"{self.text}", "True", [50, 50, 50])

    def render(self):
        rectsize = [
            self.rendered_text.get_width() + 5 * 2,
            self.rendered_text.get_height() + 5 * 2,
        ]
        mayaa.draw.rect(
            self.screen.surface, [40, 40, 40], [*self.position, *rectsize], 0, 4
        )
        mayaa.draw.rect(
            self.screen.surface, [50, 50, 50], [*self.position, *rectsize], 2, 4
        )
        self.screen.surface.blit(
            self.rendered_text,
            mayaa.pygame_backend.Vector2(self.position)
            + mayaa.pygame_backend.Vector2(rectsize) * 0.5
            - mayaa.pygame_backend.Vector2(self.rendered_text.get_size()) * 0.5,
        )


class Main(mayaa.screen.Screen):
    def __init__(self, screen_id, screen_manager) -> None:
        super().__init__(screen_id, screen_manager)
        self.data = make_data(100, [1, 400])
        self.box = Box(self, self.data)
        self.time = time.time()
        self.occur = False
        self.fps = Text(self, "Mayaa Text Always Working :)", [10, 10])

    def update(self):
        elapsed = int((time.time() - self.time) * 100) * 10
        if elapsed % 20 == 0 and self.occur is False:
            bubble_sort(self.box.data)
            self.occur = True
        if elapsed % 20 != 0:
            self.occur = False
        return super().update()

    def render(self):
        self.surface.fill([30, 30, 30])
        self.fps.render()
        self.box.render()
        return super().render()


class SortApp(mayaa.core.Core):
    def __init__(self, win_size, win_name: str) -> None:
        super().__init__(win_size, win_name)
        self.main = Main("main", self.screen_manager)
        self.screen_manager.set_initial_screen("main")
        self.fps = 600


if __name__ == "__main__":
    app = SortApp([320 * 3, 180 * 3], "SortApp")
    app.run()
