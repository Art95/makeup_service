import torch
from makeup_service.face_makeup.model import BiSeNet
from PIL import Image
import torchvision.transforms as transforms


class SemanticSegmentation:
    def __init__(self, model_path):
        self.__net = BiSeNet(n_classes=19)
        self.__net.cuda()
        self.__net.load_state_dict(torch.load(model_path))
        self.__net.eval()

        mean = (0.485, 0.456, 0.406)
        std = (0.229, 0.224, 0.225)

        self.__to_tensor = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean, std),
        ])

    def get_segmentation(self, image):
        with torch.no_grad():
            resized_image = image.resize((512, 512), Image.BILINEAR)
            img = self.__to_tensor(resized_image)
            img = torch.unsqueeze(img, 0)
            img = img.cuda()
            out = self.__net(img)[0]
            segmentation = out.squeeze(0).cpu().numpy().argmax(0)

            return segmentation
