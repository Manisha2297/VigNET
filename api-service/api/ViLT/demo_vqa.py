import torch
import copy
import requests
import io
import numpy as np
import json
import urllib.request
from PIL import Image

from api.ViLT.vilt.config import ex
from api.ViLT.vilt.modules import ViLTransformerSS

from api.ViLT.vilt.transforms import pixelbert_transform
from api.ViLT.vilt.datamodules.datamodule_base import get_pretrained_tokenizer


@ex.main
def main(_config):
    _config = copy.deepcopy(_config)

    loss_names = {
        "itm": 0,
        "mlm": 0,
        "mpp": 0,
        "vqa": 1,
        "imgcls": 0,
        "nlvr2": 0,
        "irtr": 0,
        "arc": 0,
    }
    tokenizer = get_pretrained_tokenizer(_config["tokenizer"])

    with urllib.request.urlopen(
        "https://github.com/dandelin/ViLT/releases/download/200k/vqa_dict.json"
    ) as url:
        id2ans = json.loads(url.read().decode())

    _config.update(
        {
            "loss_names": loss_names,
        }
    )

    model = ViLTransformerSS(_config)
    model.setup("test")
    model.eval()

    device = "cuda:0" if _config["num_gpus"] > 0 else "cpu"
    model.to(device)

    def infer(url, text):
        try:
            # res = requests.get(url)
            image = Image.open(url).convert("RGB")
            img = pixelbert_transform(size=384)(image)
            img = img.unsqueeze(0).to(device)
        except Exception as e:
            print(e)
            return False

        batch = {"text": [text], "image": [img]}

        with torch.no_grad():
            encoded = tokenizer(batch["text"])
            batch["text_ids"] = torch.tensor(encoded["input_ids"]).to(device)
            batch["text_labels"] = torch.tensor(encoded["input_ids"]).to(device)
            batch["text_masks"] = torch.tensor(encoded["attention_mask"]).to(device)
            infer = model.infer(batch)
            vqa_logits = model.vqa_classifier(infer["cls_feats"])

        answer = id2ans[str(vqa_logits.argmax().item())]

        return [np.array(image), answer]

    x = infer(_config['image_url'],_config['question'])
    print("Question :", _config['question'])
    print("Answer :", x[1])
    ex.info['answer'] = x[1]
    return x[1]


def get_predictions(image_path, question):
    ex.run(config_updates={'num_gpus': 0, 'load_path': './api/ViLT/weights/vilt_vqa.ckpt', 'test_only': True,
                           'image_url': image_path,
                           'question': question})
