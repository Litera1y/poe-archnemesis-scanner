from typing import List
from PIL import ImageTk, Image
import cv2
import numpy as np

from DataClasses import RecipeItemNode


class ArchnemesisItemsMap:
    """
    Holds the information about all archnemesis items, recipes, images and map them together
    """
    def __init__(self, scale: float):
        # Put everything into the list so we could maintain the display order
        self._arch_items = [
            ('키타바', ['투코하마', '아버라스', '타락자', '시체 폭파자']),
            ('이노센스', ['루나리스', '솔라리스', '거울상', '마나 착취자']),
            ('샤카리', ['얽는 자', '영혼 포식자', '가뭄 인도자']),
            ('아버라스', ['화염 질주자', '격분', '회춘']),
            ('투코하마', ['뼈 분쇄자', '집행자', '마그마 장벽']),
            ('염수왕', ['얼음 감옥', '폭풍 질주자', '인도하는 소환수']),
            ('아라칼리', ['시체 폭파자', '얽는 자', '암살자']),
            ('솔라리스', ['무적', '마그마 장벽', '강화하는 소환수']),
            ('루나리스', ['무적', '서리 질주자', '강화하는 소환수']),
            ('제웅', ['사술사', '악담', '타락자']),
            ('원소 강화', ['환기술사', '강철 주입', '혼돈술사']),
            ('결정 가죽', ['만년설', '회춘', '광전사']),
            ('무적', ['파수꾼', '거수', '축성자']),
            ('타락자', ['사혈자', '혼돈술사']),
            ('마나 착취자', ['축성자', '정력가']),
            ('폭풍 질주자', ['폭풍술사', '가속된']),
            ('거울상', ['메아리꾼', '영혼 도관']),
            ('마그마 장벽', ['방화', '뼈 분쇄자']),
            ('환기술사', ['화염술사', '서리술사', '폭풍술사']),
            ('시체 폭파자', ['강령술사', '방화']),
            ('화염 질주자', ['화염술사', '가속된']),
            ('영혼 포식자', ['영혼 도관', '강령술사', '가르강튀아']),
            ('얼음 감옥', ['만년설', '파수꾼']),
            ('서리 질주자', ['서리술사', '가속된']),
            ('나무인간 떼', ['맹독성', '파수꾼', '강철 주입']),
            ('시간의 거품', ['거수', '사술자', '비전 강화']),
            ('얽는 자', ['맹독성', '사혈자']),
            ('가뭄 인도자', ['악담', '명사수']),
            ('사술자', ['혼돈술사', '메아리꾼']),
            ('집행자', ['격분', '광전사']),
            ('회춘', ['가르강튀아', '흡혈']),
            ('강령술사', ['포격수', '과충전']),
            ('협잡꾼', ['과충전', '암살자', '메아리꾼']),
            ('암살자', ['명사수', '흡혈']),
            ('강화하는 소환수', ['강령술사', '집행자', '가르강튀아']),
            ('인도하는 소환수', ['정력가', '비전 강화']),
            ('비전 강화', []),
            ('광전사', []),
            ('사혈자', []),
            ('포격수', []),
            ('뼈 분쇄자', []),
            ('혼돈술사', []),
            ('축성자', []),
            ('명사수', []),
            ('정력가', []),
            ('메아리꾼', []),
            ('화염술사', []),
            ('격분', []),
            ('서리술사', []),
            ('가르강튀아', []),
            ('가속된', []),
            ('방화', []),
            ('거수', []),
            ('악담', []),
            ('풍요', []),
            ('과충전', []),
            ('만년설', []),
            ('파수꾼', []),
            ('영혼 도관', []),
            ('강철 주입', []),
            ('폭풍술사', []),
            ('맹독성', []),
            ('흡혈', []),
            ('쓰레기', [])
        ]
        self._images = dict()
        self._small_image_size = 30
        self._update_images(scale)

    def _update_images(self, scale):
        self._scale = scale
        for item, _ in self._arch_items:
            self._images[item] = dict()
            image = self._load_image(item, scale)
            self._image_size = image.size
            self._images[item]['scan-image'] = self._create_scan_image(image)
            # Convert the image to Tk image because we're going to display it
            self._images[item]['display-image'] = ImageTk.PhotoImage(image=image)
            image = image.resize((self._small_image_size, self._small_image_size))
            self._images[item]['display-small-image'] = ImageTk.PhotoImage(image=image)

    def _load_image(self, item: str, scale: float):
        image = Image.open(f'pictures/{item}.png')
        # Scale the image according to the input parameter
        return image.resize((int(image.width * scale), int(image.height * scale)))

    def _create_scan_image(self, image):
        # Remove alpha channel and replace it with predefined background color
        background = Image.new('RGBA', image.size, (10, 10, 32))
        image_without_alpha = Image.alpha_composite(background, image)
        scan_template = cv2.cvtColor(np.array(image_without_alpha), cv2.COLOR_RGB2BGR)
        w, h, _ = scan_template.shape

        # Crop the image to help with scanning
        return scan_template[int(h * 0.16):int(h * 0.75), int(w * 0.16):int(w * 0.85)]


    def get_scan_image(self, item):
        return self._images[item]['scan-image']

    def get_display_image(self, item):
        return self._images[item]['display-image']

    def get_display_small_image(self, item):
        return self._images[item]['display-small-image']

    def items(self):
        for item, _ in self._arch_items:
            yield item

    def recipes(self):
        for item, recipe in self._arch_items:
            if recipe:
                yield (item, recipe)

    def get_subtree_for(self, item: str):
        tree = RecipeItemNode(item, [])
        nodes = [tree]
        while len(nodes) > 0:
            node = nodes.pop(0)
            children = self.get_components_for(node.item)
            if len(children) > 0:
                node.components = [RecipeItemNode(c, []) for c in children]
                nodes.extend(node.components)
        return tree

    def get_parent_recipes_for(self, item: str) -> List[str]:
        parents = list()
        for parent, components in self._arch_items:
            if item in components:
                parents.append(parent)
        return parents

    def get_components_for(self, item) -> List[str]:
        return next(l for x, l in self._arch_items if x == item)

    @property
    def image_size(self):
        return self._image_size

    @property
    def scale(self) -> float:
        return self._scale

    @scale.setter
    def scale(self, scale: float) -> None:
        self._update_images(scale)

    @property
    def small_image_size(self):
        return self._small_image_size
